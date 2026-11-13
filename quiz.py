"""Quiz 클래스: 퀴즈 1개를 표현하는 '문제 카드 한 장'.

카드 한 장에 들어 있는 것
  question : 문제 (글자)
  choices  : 선택지 4개 (리스트)
  answer   : 정답 번호 1~4  ← 0부터가 아니라 1부터! (화면에 보이는 번호와 같게)
  hint     : 힌트 (없으면 빈 글자)

카드가 할 줄 아는 것
  show()        : 화면에 문제와 선택지를 보여준다
  is_correct()  : 고른 번호가 정답인지 알려준다
  to_dict() / from_dict() : 파일 저장용 딕셔너리로 바꾸기 / 딕셔너리에서 다시 카드 만들기
"""
from ui import paint


class Quiz:
    CHOICE_COUNT = 4  # 선택지는 항상 4개

    def __init__(self, question: str, choices: list, answer: int, hint: str = ""):
        """카드를 만든다. 규칙에 안 맞는 값이면 만들지 않고 ValueError 를 낸다.

        예) Quiz("2+2는?", ["1", "2", "3", "4"], 4)
        """
        # 앞뒤 공백 정리
        question = str(question).strip()
        choices = [str(c).strip() for c in choices]

        # 규칙 검사: 잘못된 카드가 아예 만들어지지 않게 막는다
        if not question:
            raise ValueError("문제가 비어 있습니다.")
        if len(choices) != self.CHOICE_COUNT or not all(choices):
            raise ValueError(f"선택지는 비어 있지 않은 {self.CHOICE_COUNT}개여야 합니다.")
        # True/False 도 파이썬에서는 숫자(1/0)로 취급되므로 bool 은 따로 막는다
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(f"정답은 1~{self.CHOICE_COUNT} 사이의 번호여야 합니다.")

        # self.○○ = 값 : "이 카드의 ○○ 칸에 값을 넣는다". 카드마다 칸이 따로라 섞이지 않는다.
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = str(hint or "").strip()

    def show(self) -> None:
        """문제와 선택지 4개를 화면에 보여준다."""
        print(paint("Q. " + self.question, "bold"))
        print()
        for index, choice in enumerate(self.choices, 1):  # enumerate(…, 1): 번호를 1부터 붙인다
            print(f"   {paint(index, 'yellow', 'bold')}) {choice}")
        print()

    def is_correct(self, user_answer: int) -> bool:
        """고른 번호가 정답이면 True, 아니면 False."""
        return user_answer == self.answer

    def to_dict(self) -> dict:
        """저장용 딕셔너리로 바꾼다. (JSON 파일에는 객체를 바로 저장할 수 없기 때문)"""
        data = {"question": self.question, "choices": list(self.choices), "answer": self.answer}
        if self.hint:  # 힌트가 있을 때만 넣는다 → 힌트 없는 퀴즈는 과제 기본 형식 그대로
            data["hint"] = self.hint
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """저장된 딕셔너리로 카드를 다시 만든다. (to_dict 의 반대)"""
        return cls(data["question"], data["choices"], data["answer"], data.get("hint", ""))
