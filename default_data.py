"""기본 퀴즈 데이터. 주제: 개발 입문 상식 (Python / Git / Docker).

주제 선정 이유: 이번 입학 연수에서 직접 배운 내용이라 퀴즈를 만들며 복습이 되고,
정답이 명확해서 객관식으로 만들기 좋기 때문이다.
"""
from quiz import Quiz

DEFAULT_QUIZ_DATA = [
    {"question": "Python의 창시자는?",
     "choices": ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"], "answer": 1, "hint": "네덜란드 출신 프로그래머입니다. 이름이 G로 시작해요."},
    {"question": "Python 리스트의 맨 뒤에 요소를 추가하는 메서드는?",
     "choices": ["add", "append", "push", "insert_last"], "answer": 2, "hint": "'덧붙이다'라는 뜻의 영단어예요."},
    {"question": "원격 저장소를 내 컴퓨터로 통째로 복제하는 Git 명령은?",
     "choices": ["git pull", "git push", "git clone", "git init"], "answer": 3, "hint": "영어로 '복제하다'라는 뜻이에요."},
    {"question": "Docker 이미지로부터 만들어진 '실행 중인 인스턴스'를 부르는 말은?",
     "choices": ["컨테이너", "볼륨", "레지스트리", "Dockerfile"], "answer": 1, "hint": "배에 싣는 화물 상자(container)에서 따온 이름이에요."},
    {"question": "Python에서 '키-값 쌍'으로 데이터를 저장하는 자료형은?",
     "choices": ["list", "tuple", "dict", "set"], "answer": 3, "hint": "사전(dictionary)의 줄임말이에요."},
    {"question": "컨테이너의 80번 포트를 호스트의 8080번 포트로 연결하는 docker run 옵션은?",
     "choices": ["-v 8080:80", "-p 8080:80", "-e 8080:80", "--port 80"], "answer": 2, "hint": "p는 port(포트)의 첫 글자예요. 호스트:컨테이너 순서!"},
]


def create_default_quizzes() -> list:
    """기본 데이터를 Quiz 인스턴스 리스트로 만든다."""
    return [Quiz.from_dict(item) for item in DEFAULT_QUIZ_DATA]
