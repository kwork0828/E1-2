"""터미널 화면 꾸미기: 색상, 테두리, 진행 막대, 화면 지우기.

표준 라이브러리만 사용한다 (os, sys, unicodedata).
- 색상은 ANSI 이스케이프 코드("\\033[32m" 같은 글자)로 칠한다. 터미널이 이 글자를 색으로 바꿔 보여준다.
- 파일이나 파이프로 출력할 때는 색 코드가 그대로 찍혀 지저분해지므로 자동으로 색을 끈다.
  NO_COLOR 환경변수가 있으면 끄고, FORCE_COLOR 가 있으면 켠다(실행 화면 캡처 도구용).
"""
import os
import sys
import unicodedata


def _color_enabled() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return sys.stdout.isatty()


USE_COLOR = _color_enabled()
# 사람이 직접 터미널에서 실행 중일 때만 화면 지우기/Enter 대기를 한다 (자동 입력·캡처 때는 하지 않음)
INTERACTIVE = sys.stdin.isatty() and sys.stdout.isatty()
if USE_COLOR and os.name == "nt":
    os.system("")  # Windows 콘솔에서 ANSI 색상 코드를 켜는 관용 코드

CODES = {"bold": "1", "dim": "2", "red": "31", "green": "32", "yellow": "33",
         "blue": "34", "magenta": "35", "cyan": "36", "gray": "90"}
LINE_WIDTH = 46


def paint(text, *styles) -> str:
    """text 에 색/굵기를 입힌다. 예) paint("정답", "green", "bold")"""
    if not USE_COLOR or not styles:
        return str(text)
    seq = ";".join(CODES[s] for s in styles)
    return f"\033[{seq}m{text}\033[0m"


def width(text: str) -> int:
    """화면에서 차지하는 칸 수. 한글·이모지는 2칸, 영문·숫자는 1칸."""
    total = 0
    for ch in text:
        if unicodedata.combining(ch) or ch in "️‍":
            continue
        total += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return total


def pad(text: str, size: int) -> str:
    """한글 폭까지 계산해서 size 칸이 되도록 오른쪽을 공백으로 채운다 (두 칸 메뉴 정렬용)."""
    return text + " " * max(0, size - width(text))


# ---------- 왼쪽 테두리만 있는 상자 (오른쪽 테두리는 터미널마다 한글 폭이 달라 어긋나기 쉬워 쓰지 않음) ----------
def box_top() -> None:
    print(paint("┏" + "━" * LINE_WIDTH, "cyan"))


def box_mid() -> None:
    print(paint("┣" + "━" * LINE_WIDTH, "cyan"))


def box_bottom() -> None:
    print(paint("┗" + "━" * LINE_WIDTH, "cyan"))


def box_line(text: str = "") -> None:
    print(paint("┃ ", "cyan") + text)


def section(title: str) -> None:
    """기능 화면의 제목 줄. 예) ── 📋 퀴즈 목록 ─────"""
    print()
    print(paint("── ", "cyan") + paint(title, "bold") + paint(" " + "─" * max(4, LINE_WIDTH - width(title) - 4), "cyan"))


def progress(done: int, total: int, size: int = 20) -> str:
    """진행 막대 문자열. 예) ■■■■□□□□"""
    filled = round(size * done / total) if total else 0
    return paint("■" * filled, "cyan") + paint("□" * (size - filled), "gray")


def success(message: str) -> None:
    print(paint(message, "green", "bold"))


def error(message: str) -> None:
    print(paint(message, "red", "bold"))


def warn(message: str) -> None:
    print(paint(message, "yellow"))


def note(message: str) -> None:
    print(paint(message, "gray"))


def clear() -> None:
    """화면을 지운다. 직접 실행 중일 때만 동작."""
    if INTERACTIVE:
        os.system("cls" if os.name == "nt" else "clear")
