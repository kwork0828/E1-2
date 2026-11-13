"""나만의 퀴즈 게임 — 시작 파일.

실행 방법:  python main.py

파일 지도 (어디에 무엇이 있나)
  main.py          시작점 (지금 이 파일)
  quiz_game.py     게임 진행: 메뉴, 기능 6개, 저장/불러오기
  quiz.py          퀴즈 1개 (문제 카드)
  inputs.py        입력 검사, 뒤로가기(ESC/b), Ctrl+C 처리
  ui.py            화면 꾸미기: 색, 테두리, 진행 막대
  default_data.py  기본 퀴즈 49문제
"""
from quiz_game import QuizGame


def main() -> None:
    # load(): state.json 을 읽어 게임을 만든다 → run(): 메뉴를 반복해서 보여준다
    QuizGame.load().run()


# 이 파일을 직접 실행했을 때만 main() 을 부른다. (다른 파일이 import 할 때는 실행되지 않음)
if __name__ == "__main__":
    main()
