"""실제 프로그램을 입력 스크립트로 실행하고, 그 '실제 출력'을 터미널 모양 PNG로 렌더링한다.

- 출력 텍스트는 docs/demo/*.txt 로 함께 저장한다. (이미지가 조작이 아님을 확인할 수 있도록)
- 임시 폴더에 프로젝트를 복사해 실행하므로 개발 중인 state.json을 건드리지 않는다.
- 랜덤 출제는 시드를 고정해 재실행해도 같은 화면이 나오게 한다.
"""
import html, random, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ["main.py", "quiz.py", "quiz_game.py", "inputs.py", "default_data.py"]
SEED = 7
sys.path.insert(0, str(ROOT))
from default_data import create_default_quizzes  # noqa: E402
from quiz import Quiz  # noqa: E402


def run(workdir: Path, lines: list) -> str:
    """seed를 고정한 채 실제 main()을 실행한다.

    파이프로 넣은 입력은 화면에 보이지 않으므로, input()을 '입력값을 그대로 다시 출력'하는 얇은 래퍼로 감싼다.
    (진짜 터미널에서 사용자가 타이핑한 값이 보이는 것과 같은 모양. 프로그램 로직은 그대로)
    """
    code = (
        "import builtins, random; random.seed(%d)\n"
        "_real = builtins.input\n"
        "def _echo(prompt=''):\n"
        "    value = _real(prompt)\n"
        "    print(value)\n"
        "    return value\n"
        "builtins.input = _echo\n"
        "import main; main.main()\n" % SEED
    )
    feed = "\n".join(lines) + "\n"
    out = subprocess.run([sys.executable, "-c", code], cwd=workdir, input=feed, capture_output=True,
                         text=True, encoding="utf-8").stdout
    return out.strip("\n")


def render(text: str, name: str, title: str, page) -> None:
    (ROOT / "docs/demo" / f"{name}.txt").write_text(text + "\n", encoding="utf-8")
    page_html = f"""<html><body style="margin:0;background:#1e1e1e">
<div style="display:inline-block;min-width:640px;font-family:'Noto Sans Mono CJK KR','Noto Sans CJK HK',monospace,'Noto Color Emoji';">
<div style="background:#333;color:#ddd;padding:6px 12px;font-size:13px;font-family:sans-serif">{html.escape(title)}</div>
<pre style="margin:0;padding:14px 18px;color:#e6e6e6;font-size:15px;line-height:1.45">{html.escape(text)}</pre></div></body></html>"""
    page.set_content(page_html)
    page.locator("div").first.screenshot(path=str(ROOT / "docs/screenshots" / f"{name}.png"))


def main() -> None:
    from playwright.sync_api import sync_playwright
    quizzes = create_default_quizzes()
    # 'add_quiz' 시나리오에서 7번째 퀴즈가 추가된 뒤 play를 실행하므로 같은 상태로 맞춰 정답을 계산한다.
    quizzes.append(Quiz("영화 '기생충'의 감독은?", ["박찬욱", "봉준호", "김기덕", "이창동"], 2))
    random.seed(SEED)
    picked = random.sample(quizzes, 3)  # 실행 시 프로그램이 고를 문제와 동일(같은 시드, 같은 호출 순서)
    answers = []
    for i, q in enumerate(picked):
        if i == 0:
            answers += ["h", str(q.answer)]            # 힌트 사용 후 정답
        elif i == 1:
            answers += [str(q.answer)]                  # 정답
        else:
            answers += [str(q.answer % 4 + 1)]          # 일부러 오답
    tmp = Path(tempfile.mkdtemp())
    for f in SRC:
        shutil.copy(ROOT / f, tmp / f)
    shots = {}
    shots["menu"] = ("메뉴 화면 (python main.py)", run(tmp, ["7"]))
    shots["invalid_input"] = ("잘못된 입력 처리 (문자 / 범위 밖 / 빈 입력 / 앞뒤 공백)", run(tmp, ["abc", "9", "", "  7  "]))
    shots["add_quiz"] = ("퀴즈 추가 (빈 입력·범위 밖 정답 처리 포함)", run(tmp, [
        "2", "", "영화 '기생충'의 감독은?", "박찬욱", "봉준호", "김기덕", "이창동", "0", "2", "7"]))
    shots["list"] = ("퀴즈 목록", run(tmp, ["3", "7"]))
    shots["play"] = ("퀴즈 풀기 (3문제 선택, 힌트 사용, 오답 포함) + 점수 확인", run(tmp, ["1", "3"] + answers + ["4", "7"]))
    shots["score"] = ("점수 확인 / 점수 기록", run(tmp, ["4", "6", "7"]))
    shots["restart"] = ("프로그램 재시작 후 데이터 유지 (저장된 데이터 불러오기)", run(tmp, ["3", "7"]))
    shots["delete"] = ("퀴즈 삭제 (취소 / 범위 밖 / 삭제)", run(tmp, ["5", "0", "5", "9", "7", "6", "7"]))
    if "--git-log" in sys.argv:  # 최종 커밋 직전의 실제 git 그래프
        log = subprocess.run(["git", "--no-pager", "log", "--oneline", "--graph", "--all"], cwd=ROOT,
                             capture_output=True, text=True, encoding="utf-8").stdout.strip()
        shots["git_log"] = ("$ git --no-pager log --oneline --graph --all", log)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=2, viewport={"width": 1000, "height": 800})
        for name, (title, text) in shots.items():
            render(text, name, title, page)
        browser.close()
    shutil.rmtree(tmp, ignore_errors=True)
    print("screenshots:", ", ".join(shots))


if __name__ == "__main__":
    main()
