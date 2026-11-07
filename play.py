"""퀴즈 풀기 로직 (feat/play 브랜치에서 작성)."""
from inputs import ask_int
from quiz import Quiz

LINE = "=" * 40
THIN = "-" * 40


def calc_score(correct: int, total: int) -> int:
    """100점 만점으로 환산한다. (문제 수가 달라도 점수를 비교할 수 있게)"""
    return round(correct / total * 100) if total else 0


def play_round(quizzes: list) -> tuple:
    """저장된 퀴즈를 모두 출제하고 (정답 수, 문제 수, 점수)를 돌려준다."""
    total = len(quizzes)
    print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")
    correct = 0
    for number, quiz in enumerate(quizzes, 1):
        print(THIN)
        quiz.show(number)
        user_answer = ask_int("정답 입력: ", 1, Quiz.CHOICE_COUNT)
        if quiz.is_correct(user_answer):
            correct += 1
            print("✅ 정답입니다!\n")
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({quiz.choices[quiz.answer - 1]}) 입니다.\n")
    print(THIN)
    return correct, total, calc_score(correct, total)
