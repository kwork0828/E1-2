"""Quiz 클래스: 퀴즈 1개(문제, 선택지 4개, 정답 번호)를 표현한다."""


class Quiz:
    CHOICE_COUNT = 4  # 선택지는 4개 고정

    def __init__(self, question: str, choices: list, answer: int, hint: str = ""):
        question = str(question).strip()
        choices = [str(c).strip() for c in choices]
        if not question:
            raise ValueError("문제가 비어 있습니다.")
        if len(choices) != self.CHOICE_COUNT or not all(choices):
            raise ValueError(f"선택지는 비어 있지 않은 {self.CHOICE_COUNT}개여야 합니다.")
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(f"정답은 1~{self.CHOICE_COUNT} 사이의 번호여야 합니다.")
        self.question = question
        self.choices = choices
        self.answer = answer  # 1~4 번호로 일관되게 관리 (0부터 아님)
        self.hint = str(hint or "").strip()  # 보너스: 힌트(없으면 빈 문자열)

    def show(self, number: int = None) -> None:
        """문제와 선택지를 출력한다."""
        title = f"[문제 {number}]" if number is not None else "[문제]"
        print(title)
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, 1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer: int) -> bool:
        """사용자가 고른 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def to_dict(self) -> dict:
        data = {"question": self.question, "choices": list(self.choices), "answer": self.answer}
        if self.hint:  # 힌트가 있을 때만 저장 → 기본 스키마(question/choices/answer)와 호환
            data["hint"] = self.hint
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        return cls(data["question"], data["choices"], data["answer"], data.get("hint", ""))
