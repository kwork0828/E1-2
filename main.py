"""나만의 퀴즈 게임 - 진입점 (메뉴 뼈대 단계)."""
from inputs import QuitGame, ask_int

LINE = "=" * 40
MENU_ITEMS = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료"]


def print_menu() -> None:
    print(LINE)
    print("       🎯 나만의 퀴즈 게임 🎯")
    print(LINE)
    for number, title in enumerate(MENU_ITEMS, 1):
        print(f"{number}. {title}")
    print(LINE)


def main() -> None:
    try:
        while True:
            print_menu()
            choice = ask_int("선택: ", 1, len(MENU_ITEMS))
            if choice == len(MENU_ITEMS):
                print("👋 게임을 종료합니다.")
                break
            print(f"({MENU_ITEMS[choice - 1]}) 기능은 준비 중입니다.")
    except QuitGame:
        pass


if __name__ == "__main__":
    main()
