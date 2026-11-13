"""QuizGame 클래스: 게임 전체(메뉴, 퀴즈 풀기/추가/목록/점수)를 관리한다."""
import json
import os
import random
from datetime import datetime
from pathlib import Path

from default_data import create_default_quizzes
from inputs import GoBack, QuitGame, ask_int, ask_text
from quiz import Quiz

LINE = "=" * 40
THIN = "-" * 40
# 프로젝트 루트의 state.json (어느 폴더에서 실행해도 같은 파일을 쓰도록 이 파일 위치 기준)
STATE_PATH = Path(__file__).resolve().parent / "state.json"


class QuizGame:
    MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "퀴즈 삭제", "점수 기록", "종료"]

    def __init__(self, quizzes: list = None, best_score=None, history: list = None):
        self.quizzes = quizzes if quizzes is not None else create_default_quizzes()
        self.best_score = best_score  # 아직 풀지 않았으면 None
        self.history = history if history is not None else []  # 보너스: 모든 게임 기록

    # ---------- 화면 ----------
    def print_menu(self) -> None:
        print(LINE)
        print("       🎯 나만의 퀴즈 게임 🎯")
        print(LINE)
        for number, title in enumerate(self.MENU_ITEMS, 1):
            print(f"{number}. {title}")
        print(LINE)
        print("※ 어느 화면에서든 b 를 입력하면 메인 메뉴로 돌아갑니다.")

    # ---------- 기능 ----------
    def play(self) -> None:
        """퀴즈 풀기: 모든 문제를 출제하고 결과/최고 점수를 보여준다.

        문제당 배점은 100/문제수. 힌트(h)를 보고 맞히면 그 문제는 배점의 절반만 받는다.
        """
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return
        available = len(self.quizzes)
        # 보너스: 문제 수 선택 + 랜덤 출제 (random.sample은 중복 없이 무작위로 고른다)
        count = available if available == 1 else ask_int(f"풀 문제 수를 선택하세요 (1-{available}, 뒤로: b): ", 1, available)
        selected = random.sample(self.quizzes, count)
        total = count
        per_question = 100 / total
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")
        correct = 0
        hints_used = 0
        earned = 0.0
        for number, quiz in enumerate(selected, 1):
            print(THIN)
            quiz.show(number)
            used_hint = False
            while True:
                if quiz.hint and not used_hint:
                    user_answer = ask_int("정답 입력 (힌트: h, 뒤로: b): ", 1, Quiz.CHOICE_COUNT, allow=("h",))
                else:
                    user_answer = ask_int("정답 입력 (뒤로: b): ", 1, Quiz.CHOICE_COUNT)
                if user_answer == "h":
                    print(f"💡 힌트: {quiz.hint}\n   (힌트를 쓰면 이 문제 배점이 절반이 됩니다)")
                    used_hint = True
                    hints_used += 1
                    continue
                break
            if quiz.is_correct(user_answer):
                correct += 1
                earned += per_question * (0.5 if used_hint else 1)
                print("✅ 정답입니다!\n")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({quiz.choices[quiz.answer - 1]}) 입니다.\n")
        score = round(earned)
        print(THIN)
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if hints_used:
            print(f"💡 힌트 {hints_used}회 사용 (감점 반영됨)")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        print(LINE)
        self.history.append({"played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             "total": total, "correct": correct, "score": score})
        self.save()  # 풀 때마다 바로 저장

    def add_quiz(self) -> None:
        """퀴즈 추가: 문제, 선택지 4개, 정답 번호를 입력받아 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다. (중간에 b 를 입력하면 저장하지 않고 메뉴로 돌아갑니다)\n")
        question = ask_text("문제를 입력하세요: ")
        choices = [ask_text(f"선택지 {i}: ") for i in range(1, Quiz.CHOICE_COUNT + 1)]
        answer = ask_int(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save()  # 추가한 직후 바로 파일에 저장 (종료할 때까지 기다리지 않는다)
        print("✅ 퀴즈가 추가되었습니다!")

    def show_list(self) -> None:
        """퀴즈 목록: 등록된 문제를 번호와 함께 보여준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(THIN)
        for number, quiz in enumerate(self.quizzes, 1):
            print(f"[{number}] {quiz.question}")
        print(THIN)

    def show_score(self) -> None:
        """점수 확인: 저장된 최고 점수를 보여준다."""
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요.")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점")

    def delete_quiz(self) -> None:
        """퀴즈 삭제(보너스): 번호로 골라 지우고 바로 파일에 반영한다."""
        if not self.quizzes:
            print("⚠️ 삭제할 퀴즈가 없습니다.")
            return
        self.show_list()
        number = ask_int("삭제할 퀴즈 번호 (취소: 0, 뒤로: b): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.")
            return
        removed = self.quizzes.pop(number - 1)
        self.save()  # 삭제 후 파일에 즉시 반영
        print(f"🗑️ 삭제했습니다: {removed.question}")

    def show_history(self) -> None:
        """점수 기록(보너스): 날짜/시간, 푼 문제 수, 정답 수, 점수를 보여준다."""
        if not self.history:
            print("⚠️ 아직 게임 기록이 없습니다.")
            return
        print(f"\n📜 게임 기록 (총 {len(self.history)}회)\n")
        print(THIN)
        for number, item in enumerate(self.history, 1):
            print(f"[{number}] {item['played_at']} | {item['total']}문제 중 {item['correct']}정답 | {item['score']}점")
        print(THIN)

    # ---------- 파일 저장/불러오기 (state.json, UTF-8) ----------
    def to_state(self) -> dict:
        return {"quizzes": [q.to_dict() for q in self.quizzes], "best_score": self.best_score, "history": self.history}

    def save(self, path: Path = None) -> None:
        """현재 상태를 JSON으로 저장한다. 임시 파일에 쓴 뒤 교체해 저장 도중 끊겨도 원본이 깨지지 않게 한다."""
        path = path or STATE_PATH
        tmp = path.with_suffix(".json.tmp")
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.to_state(), f, ensure_ascii=False, indent=2)
            os.replace(tmp, path)
        except OSError as error:
            print(f"⚠️ 저장에 실패했습니다: {error}")

    @classmethod
    def load(cls, path: Path = None) -> "QuizGame":
        """state.json을 읽어 게임을 만든다. 파일이 없거나 손상돼도 항상 실행 가능해야 한다."""
        path = path or STATE_PATH
        if not path.exists():
            print("ℹ️ 저장된 파일이 없어 기본 퀴즈 데이터를 사용합니다.")
            return cls()
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best = data["best_score"]
            if best is not None and (isinstance(best, bool) or not isinstance(best, int) or not 0 <= best <= 100):
                raise ValueError("best_score 값이 올바르지 않습니다.")
            history = data.get("history", [])  # 예전 파일(history 없음)과도 호환
            if not isinstance(history, list) or not all(
                    isinstance(h, dict) and {"played_at", "total", "correct", "score"} <= h.keys() for h in history):
                raise ValueError("history 형식이 올바르지 않습니다.")
        except (OSError, ValueError, KeyError, TypeError) as error:  # JSONDecodeError는 ValueError의 하위 클래스
            print(f"⚠️ 데이터 파일이 손상되어 기본 퀴즈 데이터로 복구합니다. ({type(error).__name__})")
            try:
                os.replace(path, path.with_suffix(".json.corrupt"))  # 원인 분석용 백업
            except OSError:
                pass
            game = cls()
            game.save(path)
            return game
        score_text = "없음" if best is None else f"{best}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {score_text})")
        return cls(quizzes, best, history)

    # ---------- 실행 루프 ----------
    def run(self) -> None:
        exit_number = len(self.MENU_ITEMS)
        handlers = {1: self.play, 2: self.add_quiz, 3: self.show_list, 4: self.show_score, 5: self.delete_quiz, 6: self.show_history}
        try:
            while True:
                self.print_menu()
                try:
                    choice = ask_int("선택: ", 1, exit_number)
                    if choice == exit_number:
                        print("👋 게임을 종료합니다.")
                        break
                    handlers[choice]()
                except GoBack:  # 메뉴/풀기/추가/삭제 어디서든 b → 진행 중이던 작업은 반영하지 않고 메뉴로
                    print("↩️ 메인 메뉴로 돌아갑니다. (진행 중이던 내용은 반영되지 않습니다)")
        except QuitGame:
            pass
        finally:
            self.save()  # 정상 종료/Ctrl+C/EOF 어느 경우든 가능한 범위에서 저장
