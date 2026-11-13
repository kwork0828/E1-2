"""사용자 입력 처리 (이상한 입력을 걸러내는 '문지기').

이 파일이 하는 일
  - 프로그램의 모든 입력은 여기 있는 함수(ask, ask_text, ask_int)를 거친다.
  - 그래서 공백 / 글자 / 범위 밖 숫자 / 빈 입력 / 뒤로가기 / Ctrl+C 를
    프로그램 전체에서 똑같은 규칙으로 처리할 수 있다.

입력 흐름 (한 줄 입력이 들어오면)
  ESC 키 또는 b    →  GoBack 예외   →  한 단계 뒤로 (퀴즈 추가: 이전 칸 / 그 외: 메인 메뉴)
  Ctrl+C / 입력 끝 →  QuitGame 예외 →  저장 후 안전 종료
  그 밖의 글자     →  앞뒤 공백을 지우고 돌려준다
"""
import codecs
import os
import sys

from ui import INTERACTIVE, warn, width

BACK_WORDS = ("b", "뒤로")  # 이 글자를 입력하고 Enter 를 눌러도 ESC 와 똑같이 뒤로간다
ESC = "\x1b"                # ESC 키를 누르면 컴퓨터에 들어오는 글자


# =====================================================================
# 1. 우리가 직접 만든 예외 두 가지
#    예외는 '오류'뿐 아니라 "여기서 하던 일을 멈추고 위로 돌아가라"는 신호로도 쓸 수 있다.
# =====================================================================
class GoBack(Exception):
    """뒤로가기 신호. ESC 키나 b 를 입력하면 발생한다.

    받는 곳
      - QuizGame.add_quiz : 이전 입력 칸으로 한 칸 돌아간다.
      - QuizGame.run      : 그 밖의 화면에서는 메인 메뉴로 돌아간다.
    """


class QuitGame(Exception):
    """종료 신호. Ctrl+C 를 누르거나 입력이 끝났을 때(EOF) 발생한다.

    빨간 에러 화면(트레이스백) 대신 QuizGame.run 이 받아서, 저장한 뒤 조용히 끝낸다.
    """


# =====================================================================
# 2. 키를 한 글자씩 읽기 (ESC 를 Enter 없이 바로 알아채기 위해)
#    보통의 input() 은 Enter 를 눌러야 글자를 넘겨줘서 ESC 를 바로 잡을 수 없다.
#    그래서 사람이 터미널에서 직접 실행할 때만 키를 한 글자씩 읽는다.
#    (Windows 는 msvcrt, macOS/Linux 는 termios — 둘 다 표준 라이브러리)
# =====================================================================
def _echo(text: str) -> None:
    """화면에 글자를 바로 보여준다 (줄바꿈 없이)."""
    sys.stdout.write(text)
    sys.stdout.flush()


def _erase(char: str) -> None:
    """Backspace: 화면에서 글자 하나를 지운다. 한글은 2칸이라 2칸을 지운다."""
    cells = width(char) or 1
    _echo("\b" * cells + " " * cells + "\b" * cells)


def _read_line_windows(prompt: str) -> str:
    import msvcrt
    _echo(prompt)
    chars = []
    while True:
        key = msvcrt.getwch()            # 키 하나를 기다렸다가 받는다 (화면에는 안 찍힘)
        if key in ("\x00", "\xe0"):      # 방향키·F키 같은 특수키는 두 글자로 들어온다 → 무시
            msvcrt.getwch()
        elif key == ESC:
            _echo("\n")
            raise GoBack
        elif key == "\x03":              # Ctrl+C
            raise KeyboardInterrupt
        elif key == "\x1a":              # Ctrl+Z (Windows 의 입력 끝)
            raise EOFError
        elif key in ("\r", "\n"):        # Enter
            _echo("\n")
            return "".join(chars)
        elif key == "\x08":              # Backspace
            if chars:
                _erase(chars.pop())
        elif key.isprintable():          # 일반 글자(한글 포함)
            chars.append(key)
            _echo(key)


def _read_line_unix(prompt: str) -> str:
    import select
    import termios
    import tty
    fd = sys.stdin.fileno()
    saved = termios.tcgetattr(fd)        # 터미널 설정을 기억해 두었다가 끝나면 꼭 되돌린다
    decoder = codecs.getincrementaldecoder("utf-8")()  # 한글은 여러 바이트로 들어오므로 모아서 글자로 바꾼다
    _echo(prompt)
    chars = []
    try:
        # Enter 없이 한 글자씩 받기 (Ctrl+C 는 그대로 동작). TCSANOW: 미리 입력된 글자를 버리지 않는다
        tty.setcbreak(fd, termios.TCSANOW)
        while True:
            byte = os.read(fd, 1)
            if not byte or byte == b"\x04":                 # 입력 끝 / Ctrl+D
                if not chars:
                    raise EOFError
                continue
            if byte == b"\x1b":
                # 방향키는 'ESC + 글자들'로 들어온다. 뒤따르는 글자가 바로 있으면 방향키 → 무시
                if select.select([fd], [], [], 0.05)[0]:
                    os.read(fd, 16)
                    continue
                _echo("\n")
                raise GoBack
            if byte in (b"\r", b"\n"):
                _echo("\n")
                return "".join(chars)
            if byte in (b"\x7f", b"\x08"):                  # Backspace
                if chars:
                    _erase(chars.pop())
                continue
            char = decoder.decode(byte)
            if char and char.isprintable():
                chars.append(char)
                _echo(char)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, saved)


def _read_line(prompt: str) -> str:
    """한 줄 입력. 직접 실행 중이면 키를 한 글자씩 읽고(ESC 지원), 아니면 보통의 input() 을 쓴다."""
    if not INTERACTIVE:                  # 자동 입력(파이프)·캡처 도구로 실행할 때
        return input(prompt)
    if os.name == "nt":
        return _read_line_windows(prompt)
    return _read_line_unix(prompt)


# =====================================================================
# 3. 다른 파일에서 쓰는 입력 함수 3개
# =====================================================================
def ask(prompt: str) -> str:
    """한 줄을 입력받아 앞뒤 공백을 지우고 돌려준다. 모든 입력의 출발점.

    예) "  3  " → "3"
    ESC 또는 b → GoBack,  Ctrl+C → QuitGame
    """
    try:
        text = _read_line(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되었습니다. 안전하게 종료합니다.")
        raise QuitGame
    if ESC in text or text.lower() in BACK_WORDS:
        raise GoBack
    return text


def ask_text(prompt: str) -> str:
    """빈 칸이 아닌 글자를 받을 때까지 다시 묻는다. (문제·선택지 입력용)"""
    while True:
        text = ask(prompt)
        if text:
            return text
        warn("⚠️ 빈 입력입니다. 내용을 입력하세요.")


def ask_int(prompt: str, low: int, high: int, allow: tuple = ()):
    """low~high 사이의 정수를 받을 때까지 다시 묻는다. (메뉴·정답·문제 수 입력용)

    allow : 숫자가 아니어도 통과시킬 글자. 예) allow=("h",) 이면 힌트용 "h" 를 그대로 돌려준다.

    통과 순서: 빈 입력? → 허용 글자? → 숫자로 바뀌나? → 범위 안인가? → 통과
    하나라도 걸리면 안내를 보여주고 continue 로 처음부터 다시 묻는다.
    """
    while True:
        raw = ask(prompt)
        if raw == "":
            warn(f"⚠️ 빈 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if raw.lower() in allow:
            return raw.lower()
        try:
            number = int(raw)            # "abc" 처럼 숫자가 아니면 여기서 ValueError
        except ValueError:
            warn(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if not low <= number <= high:
            warn(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number                    # 모든 검사를 통과했을 때만 여기까지 온다
