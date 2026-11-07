"""나만의 퀴즈 게임 - 진입점 (메뉴 뼈대 단계)."""
from default_data import create_default_quizzes
from inputs import QuitGame, ask_int, ask_text
from quiz import Quiz
from play import play_round

LINE = "=" * 40
MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료"]


def print_menu() -> None:
    print(LINE)
    print("       🎯 나만의 퀴즈 게임 🎯")
    print(LINE)
    for number, title in enumerate(MENU_ITEMS, 1):
        print(f"{number}. {title}")
    print(LINE)


def solve(quizzes: list, state: dict) -> None:
    """퀴즈 풀기: 결과를 보여주고 최고 점수를 갱신한다."""
    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
        return
    correct, total, score = play_round(quizzes)
    print(LINE)
    print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
    if state["best_score"] is None or score > state["best_score"]:
        state["best_score"] = score
        print("🎉 새로운 최고 점수입니다!")
    print(LINE)


def add_quiz(quizzes: list) -> None:
    """퀴즈 추가: 문제, 선택지 4개, 정답 번호를 입력받아 등록한다."""
    print("\n📌 새로운 퀴즈를 추가합니다.\n")
    question = ask_text("문제를 입력하세요: ")
    choices = [ask_text(f"선택지 {i}: ") for i in range(1, Quiz.CHOICE_COUNT + 1)]
    answer = ask_int(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
    quizzes.append(Quiz(question, choices, answer))
    print("✅ 퀴즈가 추가되었습니다!")


def show_list(quizzes: list) -> None:
    """퀴즈 목록: 등록된 문제를 번호와 함께 보여준다."""
    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다.")
        return
    print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)\n")
    print("-" * 40)
    for number, quiz in enumerate(quizzes, 1):
        print(f"[{number}] {quiz.question}")
    print("-" * 40)


def show_score(state: dict) -> None:
    """점수 확인: 저장된 최고 점수를 보여준다."""
    if state["best_score"] is None:
        print("⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요.")
        return
    print(f"\n🏆 최고 점수: {state['best_score']}점")


def main() -> None:
    quizzes = create_default_quizzes()
    state = {"best_score": None}
    try:
        while True:
            print_menu()
            choice = ask_int("선택: ", 1, len(MENU_ITEMS))
            if choice == len(MENU_ITEMS):
                print("👋 게임을 종료합니다.")
                break
            if choice == 1:
                solve(quizzes, state)
            elif choice == 2:
                add_quiz(quizzes)
            elif choice == 3:
                show_list(quizzes)
            elif choice == 4:
                show_score(state)
            else:
                print(f"({MENU_ITEMS[choice - 1]}) 기능은 준비 중입니다.")
    except QuitGame:
        pass


if __name__ == "__main__":
    main()
