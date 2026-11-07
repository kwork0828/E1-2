"""사용자 입력 처리 모듈.

모든 숫자 입력은 이 모듈을 통해 받는다. 한 곳에서 검증하면
공백/문자/범위 밖/빈 입력/Ctrl+C/EOF 처리가 프로그램 전체에서 같은 규칙으로 동작한다.
"""


class QuitGame(Exception):
    """Ctrl+C(KeyboardInterrupt) 또는 입력 스트림 종료(EOFError)를 알리는 예외.

    비정상 종료(트레이스백) 대신 main에서 받아 저장 후 안전하게 종료하기 위해 사용한다.
    """


def ask(prompt: str) -> str:
    """한 줄을 입력받아 앞뒤 공백을 제거해 돌려준다."""
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되었습니다. 안전하게 종료합니다.")
        raise QuitGame


def ask_text(prompt: str) -> str:
    """빈 입력이 아닌 문자열을 받을 때까지 반복한다."""
    while True:
        text = ask(prompt)
        if text:
            return text
        print("⚠️ 빈 입력입니다. 내용을 입력하세요.")


def ask_int(prompt: str, low: int, high: int, allow: tuple = ()):
    """low~high 사이의 정수를 받을 때까지 반복한다.

    allow에 든 문자열(예: "h")은 정수가 아니어도 그대로(소문자) 돌려준다.
    """
    while True:
        raw = ask(prompt)
        if raw == "":
            print(f"⚠️ 빈 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if raw.lower() in allow:
            return raw.lower()
        try:
            number = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if not low <= number <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number
