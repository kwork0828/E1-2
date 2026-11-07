"""QuizGame 클래스: 게임 전체(메뉴, 퀴즈 풀기/추가/목록/점수)를 관리한다."""
from default_data import create_default_quizzes
from inputs import QuitGame, ask_int, ask_text
from quiz import Quiz

LINE = "=" * 40
THIN = "-" * 40


class QuizGame:
    MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료"]

    def __init__(self, quizzes: list = None, best_score=None):
        self.quizzes = quizzes if quizzes is not None else create_default_quizzes()
        self.best_score = best_score  # 아직 풀지 않았으면 None

    # ---------- 화면 ----------
    def print_menu(self) -> None:
        print(LINE)
        print("       🎯 나만의 퀴즈 게임 🎯")
        print(LINE)
        for number, title in enumerate(self.MENU_ITEMS, 1):
            print(f"{number}. {title}")
        print(LINE)

    # ---------- 기능 ----------
    @staticmethod
    def calc_score(correct: int, total: int) -> int:
        """100점 만점으로 환산한다. (문제 수가 달라도 점수를 비교할 수 있게)"""
        return round(correct / total * 100) if total else 0

    def play(self) -> None:
        """퀴즈 풀기: 모든 문제를 출제하고 결과/최고 점수를 보여준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return
        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")
        correct = 0
        for number, quiz in enumerate(self.quizzes, 1):
            print(THIN)
            quiz.show(number)
            user_answer = ask_int("정답 입력: ", 1, Quiz.CHOICE_COUNT)
            if quiz.is_correct(user_answer):
                correct += 1
                print("✅ 정답입니다!\n")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({quiz.choices[quiz.answer - 1]}) 입니다.\n")
        score = self.calc_score(correct, total)
        print(THIN)
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        print(LINE)

    def add_quiz(self) -> None:
        """퀴즈 추가: 문제, 선택지 4개, 정답 번호를 입력받아 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = ask_text("문제를 입력하세요: ")
        choices = [ask_text(f"선택지 {i}: ") for i in range(1, Quiz.CHOICE_COUNT + 1)]
        answer = ask_int(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        self.quizzes.append(Quiz(question, choices, answer))
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

    # ---------- 실행 루프 ----------
    def run(self) -> None:
        exit_number = len(self.MENU_ITEMS)
        handlers = {1: self.play, 2: self.add_quiz, 3: self.show_list, 4: self.show_score}
        try:
            while True:
                self.print_menu()
                choice = ask_int("선택: ", 1, exit_number)
                if choice == exit_number:
                    print("👋 게임을 종료합니다.")
                    break
                handlers[choice]()
        except QuitGame:
            pass
