"""QuizGame 클래스: 게임 전체를 진행하는 '사회자'.

이 파일이 하는 일
  - 메뉴를 보여주고, 번호에 맞는 기능(풀기/추가/목록/점수/삭제/기록)을 실행한다.
  - 퀴즈·최고 점수·기록을 state.json 에 저장하고 불러온다.

전체 흐름
  main.py → QuizGame.load()  : state.json 을 읽어 게임 객체를 만든다
          → game.run()       : [메뉴 보여주기 → 번호 입력 → 기능 실행] 을 종료할 때까지 반복
          → 끝날 때 save()   : 정상 종료든 Ctrl+C 든 마지막에 저장

파일 안의 순서
  1. 메뉴 화면   2. 기능 6개   3. 저장/불러오기   4. 실행 반복(run)
"""
import json
import os
import random
from datetime import datetime
from pathlib import Path

from default_data import DEFAULT_VERSION, OLD_DEFAULT_QUESTIONS, create_default_quizzes
from inputs import GoBack, QuitGame, ask, ask_int, ask_text
from quiz import Quiz
from ui import (INTERACTIVE, box_bottom, box_line, box_mid, box_top, clear, error, note, pad, paint,
                progress, section, success, warn)

# 저장 파일 위치: 이 파일(quiz_game.py)과 같은 폴더의 state.json
# → 어느 폴더에서 실행해도 항상 같은 파일을 쓴다.
STATE_PATH = Path(__file__).resolve().parent / "state.json"


class QuizGame:
    MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "퀴즈 삭제", "점수 기록", "종료"]

    def __init__(self, quizzes: list = None, best_score=None, history: list = None):
        """게임 상태 3가지를 들고 있는다. 값을 안 주면 처음 상태(기본 49문제, 점수 없음)로 시작."""
        self.quizzes = quizzes if quizzes is not None else create_default_quizzes()  # Quiz 객체 리스트
        self.best_score = best_score  # 최고 점수 (0~100). 아직 안 풀었으면 None
        self.history = history if history is not None else []  # 게임 기록 리스트 (보너스)

    # =================================================================
    # 1. 메뉴 화면
    # =================================================================
    def print_menu(self) -> None:
        """메뉴를 테두리 상자 안에 두 칸으로 보여준다. 맨 위에는 현재 상태를 한 줄로 표시."""
        best = "-" if self.best_score is None else f"{self.best_score}점"
        print()
        box_top()
        box_line(paint("🎯 나만의 퀴즈 게임", "bold"))
        box_line(paint(f"퀴즈 {len(self.quizzes)}개 · 최고 점수 {best} · 플레이 {len(self.history)}회", "gray"))
        box_mid()
        # 메뉴 7개를 왼쪽 4개 [1~4], 오른쪽 3개 [5~7] 로 나눠 한 줄에 두 개씩 출력
        half = (len(self.MENU_ITEMS) + 1) // 2
        for row in range(half):
            cells = []
            for number in (row + 1, row + 1 + half):
                if number <= len(self.MENU_ITEMS):
                    title = self.MENU_ITEMS[number - 1]
                    # pad(): 한글 폭까지 계산해 칸을 맞춘다 (ui.py 참고)
                    cells.append(paint(f"[{number}]", "yellow", "bold") + " " + pad(title, 16))
            box_line(" " + "   ".join(cells))
        box_bottom()
        note("  ESC 또는 b: 뒤로가기 · Ctrl+C: 저장 후 종료")

    # =================================================================
    # 2. 기능 6개 (메뉴 1~6번)
    # =================================================================
    def play(self) -> None:
        """[1] 퀴즈 풀기: 고른 수만큼 무작위로 출제하고 점수를 매긴다.

        점수 규칙
          - 문제당 배점 = 100 ÷ 문제 수   (예: 3문제면 문제당 33.3점)
          - 힌트(h)를 보고 맞히면 그 문제는 배점의 절반
          - 합계를 반올림 → 100점 만점 점수
        도중에 ESC/b 를 누르면 GoBack 이 run() 까지 올라가 메뉴로 돌아간다. (이 게임은 기록하지 않음)
        """
        if not self.quizzes:
            warn("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        # (1) 문제 수 고르기 → 그만큼 무작위로 뽑기
        available = len(self.quizzes)
        if available == 1:
            count = 1
        else:
            count = ask_int(f"풀 문제 수를 선택하세요 (1-{available}, 뒤로: ESC): ", 1, available)
        selected = random.sample(self.quizzes, count)  # 중복 없이 count 개를 무작위로 뽑는다
        total = count
        per_question = 100 / total

        # (2) 한 문제씩 출제
        section(f"📝 퀴즈 시작 · 총 {total}문제")
        correct = 0      # 맞힌 문제 수
        hints_used = 0   # 힌트를 본 횟수
        earned = 0.0     # 지금까지 얻은 점수 (소수)
        for number, quiz in enumerate(selected, 1):
            print()
            print(paint(f"문제 {number}/{total}", "cyan", "bold") + "  " + progress(number - 1, total)
                  + paint(f"  정답 {correct}", "gray"))
            quiz.show()

            # 정답 번호를 받을 때까지 반복. h 를 넣으면 힌트를 보여주고 같은 문제를 다시 묻는다.
            used_hint = False
            while True:
                if quiz.hint and not used_hint:   # 힌트는 문제당 한 번만
                    user_answer = ask_int("정답 입력 (힌트: h, 뒤로: ESC): ", 1, Quiz.CHOICE_COUNT, allow=("h",))
                else:
                    user_answer = ask_int("정답 입력 (뒤로: ESC): ", 1, Quiz.CHOICE_COUNT)
                if user_answer == "h":
                    print(paint(f"💡 힌트: {quiz.hint}", "yellow"))
                    note("   (힌트를 쓰면 이 문제 배점이 절반이 됩니다)")
                    used_hint = True
                    hints_used += 1
                    continue
                break

            # 채점
            if quiz.is_correct(user_answer):
                correct += 1
                earned += per_question * (0.5 if used_hint else 1)  # 힌트를 썼으면 절반
                success("✅ 정답입니다!")
            else:
                # answer 는 1~4 번호, 리스트는 0부터 세므로 꺼낼 때만 -1
                error(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({quiz.choices[quiz.answer - 1]}) 입니다.")

        # (3) 결과 보여주기 + 최고 점수 갱신
        score = round(earned)
        print()
        box_top()
        box_line(paint("🏆 결과", "bold"))
        box_line(f"정답 {paint(correct, 'green', 'bold')} / {total}문제   점수 {paint(f'{score}점', 'yellow', 'bold')}")
        box_line(progress(score, 100))
        if hints_used:
            box_line(paint(f"💡 힌트 {hints_used}회 사용 (감점 반영됨)", "gray"))
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            box_line(paint("🎉 새로운 최고 점수입니다!", "green", "bold"))
        box_bottom()

        # (4) 기록에 남기고 바로 저장
        self.history.append({"played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             "total": total, "correct": correct, "score": score})
        self.save()

    def add_quiz(self) -> None:
        """[2] 퀴즈 추가: 문제 → 선택지 4개 → 정답 번호, 6칸을 차례로 입력받는다.

        ESC/b 를 누르면 '이전 칸'으로 한 칸 돌아간다. 첫 칸(문제)에서 누르면 메뉴로 돌아간다.
        """
        section("📌 퀴즈 추가")
        note("ESC 또는 b: 이전 칸으로 (첫 칸에서는 메뉴로)")
        print()
        labels = ["문제를 입력하세요: "] + [f"선택지 {i}: " for i in range(1, Quiz.CHOICE_COUNT + 1)]
        labels.append(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ")
        values = [None] * len(labels)  # 칸마다 입력한 값을 담아 둔다
        step = 0                       # 지금 입력 중인 칸 번호 (0 = 문제)
        while step < len(labels):
            try:
                if step == len(labels) - 1:        # 마지막 칸은 숫자(정답 번호)
                    values[step] = ask_int(labels[step], 1, Quiz.CHOICE_COUNT)
                else:
                    values[step] = ask_text(labels[step])
                step += 1                          # 다음 칸으로
            except GoBack:
                if step == 0:
                    raise                          # 첫 칸에서 뒤로 → run() 이 받아 메뉴로
                step -= 1                          # 이전 칸으로
                note(f"↩️ 이전 칸으로 돌아갑니다. (전에 입력한 값: {values[step]})")

        question, choices, answer = values[0], values[1:-1], values[-1]
        self.quizzes.append(Quiz(question, choices, answer))
        self.save()  # 종료를 기다리지 않고 바로 저장 → 갑자기 꺼져도 남는다
        success(f"✅ 퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}개)")

    def show_list(self) -> None:
        """[3] 퀴즈 목록: 등록된 문제를 번호와 함께 보여준다."""
        if not self.quizzes:
            warn("⚠️ 등록된 퀴즈가 없습니다.")
            return
        section(f"📋 퀴즈 목록 · 총 {len(self.quizzes)}개")
        digits = len(str(len(self.quizzes)))  # 번호 자리수 (50개면 2자리) → 번호를 오른쪽 정렬
        for number, quiz in enumerate(self.quizzes, 1):
            print(paint(f"{number:>{digits}}", "yellow") + "  " + quiz.question)

    def show_score(self) -> None:
        """[4] 점수 확인: 저장된 최고 점수를 보여준다."""
        if self.best_score is None:
            warn("⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요.")
            return
        section("🏆 점수 확인")
        print(f"최고 점수 {paint(f'{self.best_score}점', 'yellow', 'bold')}  " + progress(self.best_score, 100))

    def delete_quiz(self) -> None:
        """[5] 퀴즈 삭제 (보너스): 번호로 골라 지우고 바로 저장한다. 0 은 취소."""
        if not self.quizzes:
            warn("⚠️ 삭제할 퀴즈가 없습니다.")
            return
        self.show_list()
        number = ask_int("삭제할 퀴즈 번호 (취소: 0, 뒤로: ESC): ", 0, len(self.quizzes))
        if number == 0:
            note("삭제를 취소했습니다.")
            return
        removed = self.quizzes.pop(number - 1)  # 화면 번호는 1부터, 리스트는 0부터
        self.save()
        success(f"🗑️ 삭제했습니다: {removed.question} (남은 퀴즈 {len(self.quizzes)}개)")

    def show_history(self) -> None:
        """[6] 점수 기록 (보너스): 게임마다 날짜/시간, 푼 문제 수, 정답 수, 점수를 보여준다."""
        if not self.history:
            warn("⚠️ 아직 게임 기록이 없습니다.")
            return
        section(f"📜 게임 기록 · 총 {len(self.history)}회")
        for number, item in enumerate(self.history, 1):
            print(paint(f"{number:>2}", "yellow") + paint(f"  {item['played_at']}", "gray")
                  + f"  {item['total']}문제 중 {item['correct']}정답  " + paint(f"{item['score']:>3}점", "bold"))

    # =================================================================
    # 3. 저장 / 불러오기 (state.json, UTF-8)
    # =================================================================
    def to_state(self) -> dict:
        """저장할 내용을 딕셔너리로 만든다. Quiz 객체는 그대로 저장할 수 없어 딕셔너리로 바꾼다."""
        return {"default_version": DEFAULT_VERSION,
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score,
                "history": self.history}

    def save(self, path: Path = None) -> None:
        """state.json 에 저장한다.

        안전 저장: 임시 파일(.tmp)에 다 쓴 다음 한 번에 바꿔치기(os.replace) 한다.
        → 쓰는 도중 꺼져도 원래 파일이 반쯤 쓰인 채 깨지지 않는다.
        """
        path = path or STATE_PATH
        tmp = path.with_suffix(".json.tmp")
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                # ensure_ascii=False: 한글을 \uXXXX 가 아닌 한글 그대로 저장 / indent=2: 사람이 읽기 좋게 줄바꿈
                json.dump(self.to_state(), f, ensure_ascii=False, indent=2)
            os.replace(tmp, path)
        except OSError as exc:
            warn(f"⚠️ 저장에 실패했습니다: {exc}")

    @staticmethod
    def upgrade_defaults(quizzes: list) -> list:
        """예전 기본 문제는 새 기본 문제로 바꾸고, 사용자가 직접 추가한 문제는 뒤에 그대로 붙인다."""
        defaults = create_default_quizzes()
        default_questions = {q.question for q in defaults}
        user_added = [q for q in quizzes
                      if q.question not in OLD_DEFAULT_QUESTIONS and q.question not in default_questions]
        return defaults + user_added

    @classmethod
    def load(cls, path: Path = None) -> "QuizGame":
        """state.json 을 읽어 게임 객체를 만든다. 어떤 경우에도 게임은 시작되어야 한다.

        경우 4가지
          ① 파일 없음 (첫 실행)       → 기본 49문제로 시작
          ② 파일이 깨짐               → .corrupt 로 백업해 두고 기본 데이터로 복구
          ③ 예전 기본 문제 버전 파일   → 기본 문제만 새 것으로 교체 (직접 추가한 문제·점수·기록은 유지)
          ④ 정상                      → 그대로 이어서
        """
        path = path or STATE_PATH

        # ① 파일 없음
        if not path.exists():
            print("ℹ️ 저장된 파일이 없어 기본 퀴즈 데이터를 사용합니다.")
            return cls()

        # 파일 읽기 + 내용 검사. 형식이 하나라도 이상하면 except 로 간다.
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]  # 잘못된 퀴즈면 Quiz 가 ValueError
            best = data["best_score"]
            if best is not None and (isinstance(best, bool) or not isinstance(best, int) or not 0 <= best <= 100):
                raise ValueError("best_score 값이 올바르지 않습니다.")
            history = data.get("history", [])  # history 가 없는 예전 파일도 읽을 수 있게
            if not isinstance(history, list) or not all(
                    isinstance(h, dict) and {"played_at", "total", "correct", "score"} <= h.keys() for h in history):
                raise ValueError("history 형식이 올바르지 않습니다.")

        # ② 파일이 깨짐 (JSON 문법 오류도 ValueError 의 한 종류라 여기서 같이 잡힌다)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            warn(f"⚠️ 데이터 파일이 손상되어 기본 퀴즈 데이터로 복구합니다. ({type(exc).__name__})")
            try:
                os.replace(path, path.with_suffix(".json.corrupt"))  # 원인 확인용으로 남겨 둔다
            except OSError:
                pass
            game = cls()
            game.save(path)
            return game

        # ③ 예전 기본 문제 버전 (default_version 이 없거나 낮음)
        version = data.get("default_version", 1)
        if not isinstance(version, int) or version < DEFAULT_VERSION:
            quizzes = cls.upgrade_defaults(quizzes)
            game = cls(quizzes, best, history)
            game.save(path)  # 바로 저장 → 다음 실행부터는 다시 바꾸지 않는다
            note(f"🔄 기본 퀴즈가 새 버전으로 바뀌어 자동으로 교체했습니다. (퀴즈 {len(quizzes)}개, 점수·기록은 그대로)")
            return game

        # ④ 정상
        score_text = "없음" if best is None else f"{best}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {score_text})")
        return cls(quizzes, best, history)

    # =================================================================
    # 4. 실행 반복 (메뉴 → 입력 → 기능 → 다시 메뉴)
    # =================================================================
    @staticmethod
    def pause(message: str) -> None:
        """직접 실행 중일 때만 Enter 를 기다린다. 여기서 ESC 를 눌러도 그냥 넘어간다."""
        if not INTERACTIVE:
            return
        try:
            ask(paint(message, "gray"))
        except GoBack:
            pass

    def run(self) -> None:
        exit_number = len(self.MENU_ITEMS)  # 7 = 종료
        # 메뉴 번호 → 실행할 메서드. if/elif 를 6번 쓰는 대신 딕셔너리로 바로 찾는다.
        handlers = {1: self.play, 2: self.add_quiz, 3: self.show_list,
                    4: self.show_score, 5: self.delete_quiz, 6: self.show_history}
        try:
            while True:
                clear()  # 직접 실행 중일 때만 화면을 지우고 메뉴를 새로 그린다
                self.print_menu()

                # 메뉴 번호 받기 (메뉴에서 ESC 는 더 돌아갈 곳이 없으므로 안내만 한다)
                try:
                    choice = ask_int(paint("선택 ▶ ", "bold"), 1, exit_number)
                except GoBack:
                    note(f"ℹ️ 이미 메인 메뉴입니다. 끝내려면 {exit_number}번을 고르세요.")
                    self.pause("↵ Enter ")
                    continue
                if choice == exit_number:
                    print("👋 게임을 종료합니다.")
                    break

                # 기능 실행. 도중에 ESC/b 가 들어오면 GoBack 이 여기까지 올라온다.
                try:
                    handlers[choice]()   # 마지막 () 가 "그 메서드를 실행하라"는 뜻
                    self.pause("\n↵ Enter 를 누르면 메뉴로 돌아갑니다 ")  # 결과를 읽을 시간을 준다
                except GoBack:
                    note("↩️ 메인 메뉴로 돌아갑니다. (진행 중이던 내용은 반영되지 않습니다)")

        except QuitGame:   # Ctrl+C / 입력 끝 → 조용히 종료 (아래 finally 에서 저장)
            pass
        finally:
            self.save()    # 정상 종료든 Ctrl+C 든 마지막에 반드시 저장
