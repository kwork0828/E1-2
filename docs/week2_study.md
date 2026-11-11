# 2주차 시험 공부 자료

> 직접 정리한 2주차(Python / 예외 / 클래스 / JSON / Git / 1주차 복습) 공부 자료입니다.
> 예상문제용 자료이며 실제 출제 문제가 아닙니다. 기본 퀴즈(`default_data.py`)의 문제는 아래 개념 카드마다 한 문제씩 만들었습니다.

# A. 개념 정리본

## PART 1. Python 기초

### 파이썬 실행과 버전 확인

- 쉬운 설명: 파이썬 파일은 '레시피 종이', python 명령은 '요리사'예요. 요리사에게 종이를 건네면 요리(실행)가 시작돼요.
- 기술 설명: 터미널에서 python 파일명 으로 실행합니다. 버전은 python -V (대문자 V). 미션은 Python 3.10 이상, 외부 라이브러리 없이 표준 라이브러리만 쓰게 합니다.

```
python main.py
python -V
```

시험에 나올 명령어:

```
python main.py  /  python -V
```

시험 답안:

```
python main.py
python -V  (또는 python --version)
```

**한 줄 암기: 실행은 python 파일명, 버전은 대문자 -V.**

### input 과 print

- 쉬운 설명: print 는 '말하기', input 은 '질문하고 대답 듣기'예요.
- 기술 설명: input(안내문) 은 사용자가 친 글자를 항상 문자열(str)로 돌려줍니다. print(값) 은 화면에 출력합니다.

```
name = input("이름: ")
print("안녕", name)
```

시험에 나올 명령어:

```
name = input("이름: ")
```

시험 답안:

```
input  (결과는 항상 str)
```

**한 줄 암기: input 의 결과는 무조건 문자열.**

### 자료형 변환 int / str / float

- 쉬운 설명: 글자 '5'는 사과 그림, 숫자 5는 진짜 사과예요. 계산하려면 그림을 진짜로 바꿔야 해요.
- 기술 설명: int("5")=5, float("3.5")=3.5, str(20)="20". 문자열과 숫자는 바로 더할 수 없습니다. int(3.9)=3 (버림).

```
n = int(input("숫자: "))
print(n + 1)
print("나이: " + str(20))
```

시험에 나올 명령어:

```
int(...)  float(...)  str(...)
```

시험 답안:

```
int / float / str
```

**한 줄 암기: input 받은 숫자는 int() 로 바꿔서 계산.**

### type() 으로 자료형 확인

- 쉬운 설명: type 은 물건의 '라벨'을 읽어 주는 돋보기예요.
- 기술 설명: type(값) 의 출력은 <class 'int'>, <class 'str'>, <class 'float'>, <class 'list'> 형태입니다.

```
print(type(3))      # <class 'int'>
print(type(3 / 1))  # <class 'float'>
```

시험에 나올 명령어:

```
print(type(3))
```

시험 답안:

```
<class 'int'>
```

**한 줄 암기: type() 출력은 <class '이름'>.**

### 연산자 / // % **

- 쉬운 설명: 피자 7조각을 2명이 나누면: 3.5(/), 한 사람당 3조각(//), 남는 1조각(%).
- 기술 설명: / 나누기(항상 float), // 몫, % 나머지, ** 거듭제곱.

```
print(7 / 2)   # 3.5
print(7 // 2)  # 3
print(7 % 2)   # 1
print(2 ** 10) # 1024
```

시험에 나올 명령어:

```
print(7 // 2)
```

시험 답안:

```
3
```

**한 줄 암기: / 나누기, // 몫, % 나머지, ** 제곱.**

### f-string

- 쉬운 설명: 빈칸 있는 편지지에 이름을 쏙 끼워 넣는 기능이에요.
- 기술 설명: 따옴표 앞에 f 를 붙이고 {변수} 를 쓰면 값이 들어갑니다.

```
name = "Kim"
print(f"Hi {name}!")  # Hi Kim!
```

시험에 나올 명령어:

```
print(f"Hi {name}!")
```

시험 답안:

```
Hi Kim!
```

**한 줄 암기: f"...{변수}..."**

### 문자열 메서드 strip / split / lower / isdigit

- 쉬운 설명: strip=가장자리 먼지 털기, split=가위로 자르기, lower=소문자로, isdigit=숫자만 있나 검사.
- 기술 설명: strip() 앞뒤 공백 제거, split(",") 구분자로 잘라 리스트, lower() 소문자, isdigit() 숫자 문자열이면 True.

```
print(" hi ".strip())
print("a,b".split(","))
print("ABC".lower())
print("42".isdigit())
```

시험에 나올 명령어:

```
" hi ".strip()   "a,b".split(",")
```

시험 답안:

```
hi / ['a', 'b'] / abc / True
```

**한 줄 암기: 입력 검사 = strip() 후 isdigit().**

## PART 2. 리스트·딕셔너리

### 리스트 인덱스와 슬라이싱

- 쉬운 설명: 리스트는 '번호표 달린 사물함'. 번호는 0번부터! 음수는 뒤에서부터 세요.
- 기술 설명: x[0] 첫째, x[-1] 마지막. x[1:3] 은 1번부터 3번 '앞'까지 (끝 번호 미포함).

```
x = [10, 20, 30, 40]
print(x[0], x[-1])  # 10 40
print(x[1:3])       # [20, 30]
print(x[-2:])       # [30, 40]
```

시험에 나올 명령어:

```
x[-1]   x[1:3]
```

시험 답안:

```
40 / [20, 30]
```

**한 줄 암기: 인덱스는 0부터, 슬라이스는 끝 번호 제외.**

### 리스트 메서드 append pop sort len

- 쉬운 설명: append=줄 맨 끝에 서기, pop=맨 끝 사람 데려가기, sort=키 순서로 세우기, len=몇 명인지 세기.
- 기술 설명: append(값) 추가, pop() 맨 뒤 꺼냄(값 반환), sort() 오름차순 정렬(원본 변경), len(리스트) 개수.

```
a = [3, 1, 2]
a.append(0)
a.sort()
print(a)       # [0, 1, 2, 3]
print(a.pop()) # 3
print(len(a))  # 3
```

시험에 나올 명령어:

```
a.append(3)   a.pop()   a.sort()   len(a)
```

시험 답안:

```
append / pop / sort / len
```

**한 줄 암기: sort() 는 원본을 바꾸고 None 을 돌려준다.**

### 딕셔너리 기본

- 쉬운 설명: 딕셔너리는 '사전'. 단어(키)를 찾으면 뜻(값)이 나와요.
- 기술 설명: {키: 값}. d[키] 로 읽고 쓰기. keys() 키들, values() 값들, items() (키, 값) 쌍.

```
d = {"a": 1, "b": 2}
print(list(d.keys()))   # ['a', 'b']
print(list(d.values())) # [1, 2]
for k, v in d.items():
    print(k, v)
```

시험에 나올 명령어:

```
d.keys()  d.values()  d.items()
```

시험 답안:

```
keys / values / items
```

**한 줄 암기: keys 키, values 값, items 둘 다.**

### get 과 KeyError

- 쉬운 설명: 사전에 없는 단어를 '억지로' 찾으면 화내고(에러), 'get'으로 정중히 물으면 없다고만 해요.
- 기술 설명: d["없는키"] → KeyError. d.get("없는키") → None, d.get("없는키", 0) → 0.

```
d = {"a": 1}
print(d.get("b"))     # None
print(d.get("b", 0))  # 0
```

시험에 나올 명령어:

```
d.get("b", 0)
```

시험 답안:

```
0
```

**한 줄 암기: 없는 키: [] 는 KeyError, get 은 None.**

## PART 3. 제어문·함수

### if / elif / else

- 쉬운 설명: 갈림길 표지판: 첫 길 아니면 둘째 길, 그것도 아니면 마지막 길.
- 기술 설명: 위에서부터 검사해 처음 참인 블록 하나만 실행. 'else if' 가 아니라 elif. 끝에 콜론(:)과 들여쓰기 필수.

```
x = 5
if x > 10:
    print("A")
elif x > 3:
    print("B")
else:
    print("C")
```

시험에 나올 명령어:

```
elif x > 3:
```

시험 답안:

```
B
```

**한 줄 암기: if → elif → else, 콜론과 들여쓰기.**

### for 와 range

- 쉬운 설명: for 는 '줄 서 있는 사람 한 명씩 불러오기', range 는 번호표 뭉치예요.
- 기술 설명: range(3)=0,1,2 / range(1,4)=1,2,3 / range(1,10,3)=1,4,7. 끝 숫자는 포함하지 않습니다.

```
for i in range(3):
    print(i, end=" ")  # 0 1 2
```

시험에 나올 명령어:

```
for i in range(3):
```

시험 답안:

```
0 1 2
```

**한 줄 암기: range(끝) 은 0부터 끝-1 까지.**

### while

- 쉬운 설명: '배부를 때까지 먹기' — 조건이 참인 동안 계속 반복해요.
- 기술 설명: 조건이 거짓이 되면 종료. 조건을 바꾸는 코드(n += 1)를 안 넣으면 무한 반복.

```
n = 0
while n < 3:
    n += 1
print(n)  # 3
```

시험에 나올 명령어:

```
while n < 3:
```

시험 답안:

```
3
```

**한 줄 암기: while 안에는 조건을 바꾸는 줄이 있어야 한다.**

### break 와 continue

- 쉬운 설명: continue=이번 한 번만 패스, break=게임 끝내고 나가기.
- 기술 설명: continue 는 남은 코드를 건너뛰고 다음 반복. break 는 반복문 전체 종료.

```
for i in range(5):
    if i == 2:
        continue
    print(i, end="")  # 0134
```

시험에 나올 명령어:

```
continue   break
```

시험 답안:

```
0134
```

**한 줄 암기: continue 건너뛰기, break 탈출.**

### 함수 def / return / None

- 쉬운 설명: 함수는 '자동판매기': 돈(매개변수)을 넣으면 음료(return)가 나와요. return 이 없으면 빈손(None).
- 기술 설명: def 이름(매개변수): 로 정의, return 으로 값을 돌려줌. return 이 없으면 None.

```
def add(a, b):
    return a + b
print(add(2, 3))  # 5

def f():
    pass
print(f())        # None
```

시험에 나올 명령어:

```
def add(a, b):   return a + b
```

시험 답안:

```
5 / None
```

**한 줄 암기: return 없으면 None.**

### random.shuffle (보너스: 랜덤 출제)

- 쉬운 설명: 카드 덱을 섞는 것과 같아요.
- 기술 설명: import random 후 random.shuffle(리스트) 는 원본 순서를 무작위로 섞습니다. 표준 라이브러리라 설치가 필요 없습니다.

```
import random
items = [1, 2, 3]
random.shuffle(items)
```

시험에 나올 명령어:

```
import random   random.shuffle(items)
```

시험 답안:

```
shuffle
```

**한 줄 암기: 섞기 = random.shuffle.**

## PART 4. 예외 처리

### try / except

- 쉬운 설명: 그네를 타다(try) 넘어지면 안전매트(except)가 받아 줘요. 프로그램이 안 죽어요.
- 기술 설명: try: 에서 에러가 나면 except 예외이름: 블록이 실행됩니다.

```
try:
    int("a")
except ValueError:
    print("숫자 아님")
```

시험에 나올 명령어:

```
except ValueError:
```

시험 답안:

```
숫자 아님
```

**한 줄 암기: try 시도, except 처리.**

### 예외 이름 6종

- 쉬운 설명: 에러에도 이름표가 있어요. 이름표를 보면 어디가 아픈지 알 수 있어요.
- 기술 설명: ValueError(변환 불가), IndexError(리스트 번호 범위 밖), KeyError(없는 키), FileNotFoundError(없는 파일), ZeroDivisionError(0으로 나눔), json.JSONDecodeError(JSON 형식 깨짐).

```
int("abc")        # ValueError
[1, 2][5]         # IndexError
{"a": 1}["b"]    # KeyError
open("no.txt")    # FileNotFoundError
10 / 0            # ZeroDivisionError
```

시험에 나올 명령어:

```
except (ValueError, KeyError):
```

시험 답안:

```
ValueError / IndexError / KeyError / FileNotFoundError / ZeroDivisionError / json.JSONDecodeError
```

**한 줄 암기: 변환=Value, 번호=Index, 키=Key, 파일=FileNotFound, 0=ZeroDivision.**

### 입력 검증과 KeyboardInterrupt / EOFError (미션 요구)

- 쉬운 설명: 손님이 이상한 주문을 해도 가게는 문을 닫지 않고 '다시 말씀해 주세요' 라고 해요.
- 기술 설명: 미션의 최소 입력 처리: 앞뒤 공백 제거(strip), 숫자 변환 실패(ValueError), 허용 범위 밖 숫자, 빈 입력은 안내 후 재입력. Ctrl+C 는 KeyboardInterrupt, 입력이 끝난 input() 은 EOFError — 둘 다 잡아서 안내하고 가능하면 저장 후 안전 종료.

```
while True:
    text = input("선택: ").strip()
    if text == "":
        print("입력해 주세요")
        continue
    try:
        n = int(text)
    except ValueError:
        print("숫자만 입력")
        continue
    if 1 <= n <= 5:
        break
    print("1-5 사이")
```

시험에 나올 명령어:

```
except ValueError:   except (KeyboardInterrupt, EOFError):
```

시험 답안:

```
ValueError / KeyboardInterrupt / EOFError
```

**한 줄 암기: Ctrl+C = KeyboardInterrupt, 입력 끝 = EOFError.**

## PART 5. 클래스

### class, __init__, self

- 쉬운 설명: 클래스는 '붕어빵 틀'. 틀로 찍어 낸 붕어빵이 객체. (1주차의 Image=틀, Container=찍어 낸 것과 같은 느낌!)
- 기술 설명: class 이름: 으로 정의. __init__ 은 객체가 만들어질 때 자동 실행되는 생성자. self 는 '나 자신'.

```
class Cat:
    def __init__(self, name):
        self.name = name
c = Cat("Nabi")
print(c.name)  # Nabi
```

시험에 나올 명령어:

```
class Cat:   def __init__(self, name):
```

시험 답안:

```
class / __init__ / self
```

**한 줄 암기: 틀=class, 생성자=__init__, 나=self.**

### 객체(인스턴스)와 메서드

- 쉬운 설명: 붕어빵 하나하나가 인스턴스. 붕어빵이 할 수 있는 행동(짖기)이 메서드.
- 기술 설명: 객체 = 클래스(...) 호출로 생성. 메서드는 클래스 안의 함수이며 첫 매개변수가 self. 객체.메서드() 로 호출.

```
class Dog:
    def __init__(self, name):
        self.name = name
    def bark(self):
        return self.name + "!"
print(Dog("Rex").bark())  # Rex!
```

시험에 나올 명령어:

```
Dog("Rex").bark()
```

시험 답안:

```
Rex!
```

**한 줄 암기: 객체.메서드() — 메서드의 첫 매개변수는 self.**

### Quiz / QuizGame 책임 분리

- 쉬운 설명: Quiz 는 '문제지 한 장', QuizGame 은 '시험 감독관'. 각자 맡은 일만 해요.
- 기술 설명: Quiz: 질문·보기·정답 데이터와 정답 확인. QuizGame: 퀴즈 목록 관리, 메뉴, 점수, 파일 저장/불러오기.

```
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer
```

시험에 나올 명령어:

```
class QuizGame:
```

시험 답안:

```
Quiz = 문제 데이터 / QuizGame = 진행·저장
```

**한 줄 암기: Quiz=데이터, QuizGame=진행.**

### if __name__ == "__main__":

- 쉬운 설명: '이 파일을 직접 눌렀을 때만 문을 열어요'라는 열쇠예요.
- 기술 설명: 파일을 직접 실행하면 __name__ 이 "__main__" 이 되어 아래 코드가 실행. 다른 파일에서 import 하면 실행되지 않음.

```
if __name__ == "__main__":
    game = QuizGame()
    game.run()
```

시험에 나올 명령어:

```
if __name__ == "__main__":
```

시험 답안:

```
__main__
```

**한 줄 암기: 직접 실행할 때만 돌게 하는 시작점.**

## PART 6. JSON 저장

### JSON 이란? (Volume 과 연결)

- 쉬운 설명: JSON 은 '공책 파일'. 프로그램을 꺼도 공책은 남아요. 1주차 Docker Volume(컨테이너가 지워져도 남는 보관함)과 같은 역할이에요.
- 기술 설명: 데이터를 글자로 저장하는 형식. 파이썬 딕셔너리/리스트와 거의 같은 모양. 미션 state.json 은 {"quizzes":[{"question","choices","answer"}],"best_score":3} 구조.

```
{
  "quizzes": [
    {"question": "1+1?", "choices": ["1", "2"], "answer": 2}
  ],
  "best_score": 3
}
```

시험에 나올 명령어:

```
import json
```

시험 답안:

```
import json
```

**한 줄 암기: JSON = 프로그램이 꺼져도 남는 공책(Volume 느낌).**

### dump / load  vs  dumps / loads

- 쉬운 설명: s 가 없으면 '파일(서류함)', s 가 있으면 '문자열(메모지)'.
- 기술 설명: json.dump(data, f) 파일에 쓰기 / json.load(f) 파일에서 읽기 / json.dumps(data) 문자열로 / json.loads(문자열) 문자열에서.

```
import json
s = json.dumps({"a": 1})  # '{"a": 1}'
d = json.loads(s)         # {'a': 1}
```

시험에 나올 명령어:

```
json.dump(data, f)   json.load(f)
```

시험 답안:

```
파일: dump / load   문자열: dumps / loads
```

**한 줄 암기: s = string(문자열).**

### with open 과 모드

- 쉬운 설명: with open 은 '문 열고 일하다 나가면 자동으로 문 닫아 주는 도우미'예요.
- 기술 설명: "w" 쓰기(덮어씀), "r" 읽기, "a" 이어쓰기. with 블록이 끝나면 파일이 자동으로 닫힙니다.

```
with open("state.json", "w", encoding="utf-8") as f:
    json.dump(data, f)
```

시험에 나올 명령어:

```
with open("state.json", "r", encoding="utf-8") as f:
```

시험 답안:

```
w / r / a
```

**한 줄 암기: w 쓰기, r 읽기, a 이어쓰기.**

### encoding, ensure_ascii, indent

- 쉬운 설명: 한글이 깨지지 않게 '한글 번역기(utf-8)'를 켜고, 보기 좋게 '줄 바꿈(indent)'을 해요.
- 기술 설명: open(..., encoding="utf-8"). json.dump(data, f, ensure_ascii=False, indent=2) — 한글 그대로, 들여쓰기 2칸.

```
json.dump(data, f, ensure_ascii=False, indent=2)
```

시험에 나올 명령어:

```
ensure_ascii=False   indent=2   encoding="utf-8"
```

시험 답안:

```
ensure_ascii=False
```

**한 줄 암기: 한글 저장 = utf-8 + ensure_ascii=False.**

### os.path.exists 와 파일 없을 때 처리

- 쉬운 설명: 공책을 펴기 전에 '공책이 있나?' 먼저 확인해요.
- 기술 설명: import os 후 os.path.exists("state.json") 가 True/False. 없으면 기본 데이터로 시작. 파일이 깨졌으면 json.JSONDecodeError 처리.

```
import os
if os.path.exists("state.json"):
    print("파일 있음")
```

시험에 나올 명령어:

```
os.path.exists("state.json")
```

시험 답안:

```
os.path.exists
```

**한 줄 암기: 읽기 전에 exists 로 확인.**

### 파일이 없거나 손상됐을 때 (미션 요구)

- 쉬운 설명: 공책이 없으면 새 공책(기본 퀴즈)으로 시작하고, 찢어졌으면 알려 주고 새 공책으로 바꿔요.
- 기술 설명: state.json 이 없으면(첫 실행) 기본 퀴즈 데이터를 사용. 손상(json.JSONDecodeError)이나 읽기·쓰기 오류는 try/except 로 잡아 안내 메시지를 출력하고 기본 데이터로 복구(초기화). 프로그램은 계속 실행 가능해야 합니다.

```
try:
    with open("state.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = default_data()
except json.JSONDecodeError:
    print("파일이 손상되어 초기화합니다")
    data = default_data()
```

시험에 나올 명령어:

```
except FileNotFoundError:   except json.JSONDecodeError:
```

시험 답안:

```
FileNotFoundError / json.JSONDecodeError
```

**한 줄 암기: 없으면 기본 데이터, 깨졌으면 안내 후 복구.**

## PART 7. Git

### 필수 7종 명령어

- 쉬운 설명: add = 준비, commit = 저장. 사진관 비유: init(스튜디오 열기), add(찍을 사람 세우기), commit(찰칵), push(인화본 보내기), pull(받아오기), checkout(다른 방 이동), clone(통째 복사).
- 기술 설명: git init / git add . / git commit -m "메시지" / git push / git pull / git checkout 브랜치 / git clone 주소.

```
git init
git add .
git commit -m "Feat: 시작"
git push
```

시험에 나올 명령어:

```
git init   git add .   git commit -m "..."   git push   git pull   git checkout   git clone
```

시험 답안:

```
init, add, commit, push, pull, checkout, clone
```

**한 줄 암기: init → add → commit → push.**

### status / diff / log

- 쉬운 설명: status=지금 상태 점검, diff=뭐가 바뀌었나 비교, log=지난 일기장.
- 기술 설명: git status 상태, git diff 변경 내용(add 전), git log --oneline --graph 한 줄 + 가지 그래프.

```
git status
git diff
git log --oneline --graph
```

시험에 나올 명령어:

```
git log --oneline --graph
```

시험 답안:

```
git log --oneline --graph
```

**한 줄 암기: log 는 --oneline --graph 로 예쁘게.**

### branch / switch / checkout -b

- 쉬운 설명: 브랜치는 '평행우주'. 원래 이야기(main)를 건드리지 않고 새 이야기를 써 볼 수 있어요.
- 기술 설명: git branch 목록 / git branch 이름 생성 / git checkout -b 이름 또는 git switch -c 이름 = 만들면서 이동.

```
git branch
git checkout -b feature
git switch -c feature2
```

시험에 나올 명령어:

```
git checkout -b feature   git switch -c feature
```

시험 답안:

```
git checkout -b feature  /  git switch -c feature
```

**한 줄 암기: checkout -b = switch -c.**

### merge (main 에서 실행)

- 쉬운 설명: 평행우주의 이야기를 '본편(main)'에 합치는 일이에요. 본편 자리에 서서 불러와요.
- 기술 설명: git checkout main (또는 git switch main) 후 git merge feature. 합친 브랜치는 git branch -d feature (합치지 않은 건 -D 강제).

```
git switch main
git merge feature
git branch -d feature
```

시험에 나올 명령어:

```
git merge feature   git branch -d feature   git branch -D feature
```

시험 답안:

```
git merge feature
```

**한 줄 암기: merge 는 받는 쪽(main)에서. -d 안전, -D 강제.**

### merge conflict 와 해결

- 쉬운 설명: 두 사람이 같은 칸에 서로 다른 글을 썼어요. 사람이 직접 보고 하나를 골라야 해요.
- 기술 설명: 충돌 파일에 <<<<<<< HEAD (내 쪽) / ======= (구분선) / >>>>>>> 브랜치 (가져온 쪽) 표시. 표시 줄을 지우고 원하는 내용만 남긴 뒤 git add . → git commit. 포기하려면 git merge --abort.

```
<<<<<<< HEAD
내 내용
=======
상대 내용
>>>>>>> feature
```

시험에 나올 명령어:

```
git merge --abort
```

시험 답안:

```
git merge --abort
```

**한 줄 암기: 충돌 해결: 표시 지우기 → add → commit. 포기: --abort.**

### remote 와 push -u

- 쉬운 설명: remote 는 'GitHub 집 주소 저장', origin 은 그 주소의 별명이에요.
- 기술 설명: git remote add origin 주소 / git remote -v 확인 / git push -u origin main (첫 push 때 추적 설정, 이후엔 git push).

```
git remote add origin https://github.com/user/repo.git
git remote -v
git push -u origin main
```

시험에 나올 명령어:

```
git remote add origin 주소   git remote -v   git push -u origin main
```

시험 답안:

```
git push -u origin main
```

**한 줄 암기: 첫 push 는 -u origin main.**

### .gitignore 와 git rm --cached

- 쉬운 설명: .gitignore 는 '이건 사진 찍지 마세요' 명단. 이미 찍힌 건 --cached 로 사진첩에서만 빼요.
- 기술 설명: .gitignore 에 __pycache__/ , .env 같은 줄을 적습니다. 이미 추적 중인 파일은 git rm --cached .env (파일은 남김).

```
__pycache__/
.env
```

시험에 나올 명령어:

```
git rm --cached .env
```

시험 답안:

```
git rm --cached .env
```

**한 줄 암기: 비밀(.env)과 캐시(__pycache__/)는 ignore.**

### 커밋 메시지 타입

- 쉬운 설명: 편지 앞머리에 '용건 딱지'를 붙이는 거예요.
- 기술 설명: Feat 새 기능 / Fix 버그 수정 / Docs 문서 / Refactor 구조 개선. 예: git commit -m "Feat: 퀴즈 추가".

```
git commit -m "Fix: 점수 계산 오류"
```

시험에 나올 명령어:

```
git commit -m "Feat: ..."
```

시험 답안:

```
Feat / Fix / Docs / Refactor
```

**한 줄 암기: Feat 기능, Fix 수정, Docs 문서, Refactor 정리.**

### 미션 Git 제출 기준

- 쉬운 설명: 숙제 인증 조건: 커밋 10번 이상, 가지(브랜치) 만들고 합친 기록, 복제(clone)와 당겨오기(pull) 기록.
- 기술 설명: 기능 단위로 최소 10개 이상 의미 있는 커밋, 브랜치 생성과 병합(checkout, merge) 1회 이상, clone 과 pull 각 1회 이상. 제출물에는 git log --oneline --graph 결과 화면이 포함됩니다. 필수 7종: init, add, commit, push, pull, checkout, clone.

```
git checkout -b quiz-play
git commit -m "Feat: 퀴즈 출제 기능 구현"
git checkout main
git merge quiz-play
git log --oneline --graph
```

시험에 나올 명령어:

```
git log --oneline --graph   git clone 주소   git pull
```

시험 답안:

```
git log --oneline --graph
```

**한 줄 암기: 커밋 10+, 브랜치 병합 1+, clone·pull 1+.**

## PART 8. 1주차 복습

### ls -la 와 chmod

- 쉬운 설명: ls -la 는 '집 안 서랍 전부 + 열쇠 정보까지 보기', chmod 는 열쇠 바꾸기.
- 기술 설명: ls -la 숨김 포함 자세히. chmod 755 는 rwxr-xr-x 로 표시되는 실행 파일용, chmod 644 는 rw-r--r-- 로 표시되는 일반 파일용. r=4 w=2 x=1.

```
ls -la
chmod 755 run.sh
chmod 644 note.txt
```

시험에 나올 명령어:

```
ls -la   chmod 755 run.sh   chmod 644 note.txt
```

시험 답안:

```
ls -la / chmod 755 / chmod 644
```

**한 줄 암기: 755 실행파일, 644 일반파일.**

### docker run 옵션

- 쉬운 설명: 이미지는 설계도(레고 설명서), 컨테이너는 실행본(조립된 레고). run 은 조립 시작!
- 기술 설명: -d 백그라운드, -p 내포트:컨테이너포트, --name 이름, -v 볼륨:경로, --rm 종료 시 자동 삭제.

```
docker run -d -p 8080:80 --name web nginx
```

시험에 나올 명령어:

```
docker run -d -p 8080:80 --name web nginx
```

시험 답안:

```
docker run -d -p 8080:80 --name web nginx
```

**한 줄 암기: -d 뒤에서 / -p 포트 / --name 이름.**

### docker build / ps / logs / exec

- 쉬운 설명: build=조립 설명서 만들기, ps=지금 뭐 돌아가나, logs=일기 보기, exec=안에 들어가 보기.
- 기술 설명: docker build -t 이름:태그 . / docker ps -a (멈춘 것 포함) / docker logs -f 이름 / docker exec -it 이름 bash (exec=새 명령 실행, attach=기존 화면에 붙기).

```
docker build -t myapp:1.0 .
docker ps -a
docker logs -f web
docker exec -it web bash
```

시험에 나올 명령어:

```
docker build -t myapp:1.0 .   docker ps -a   docker logs -f web   docker exec -it web bash
```

시험 답안:

```
위 4개 명령어 그대로
```

**한 줄 암기: build 끝의 점(.) 잊지 말기.**

### docker rm  vs  rmi

- 쉬운 설명: rm 은 '조립된 레고 치우기', rmi 는 '설명서(이미지) 버리기'. i = image.
- 기술 설명: docker rm 컨테이너이름 / docker rmi 이미지이름. 실행 중인 컨테이너는 docker stop 후 rm (또는 rm -f). 컨테이너를 쓰는 이미지는 먼저 컨테이너를 지워야 합니다.

```
docker rm web
docker rmi nginx
```

시험에 나올 명령어:

```
docker rm web   docker rmi nginx
```

시험 답안:

```
rm = 컨테이너 / rmi = 이미지
```

**한 줄 암기: rmi 의 i 는 image.**

### Dockerfile 키워드

- 쉬운 설명: Dockerfile 은 요리 레시피: 재료 고르기(FROM), 주방 정하기(WORKDIR), 재료 넣기(COPY), 조리(RUN), 완성 후 내놓기(CMD).
- 기술 설명: FROM 베이스 이미지 / WORKDIR 작업 폴더 / COPY 파일 복사 / RUN 빌드 중 실행 / ENV 환경변수 / EXPOSE 포트 안내(실제로 열지는 않음, 연결은 -p) / CMD 컨테이너 시작 시 실행. RUN 은 빌드 때, CMD 는 시작 때.

```
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENV MODE=prod
EXPOSE 8000
CMD ["python", "main.py"]
```

시험에 나올 명령어:

```
FROM  WORKDIR  COPY  RUN  ENV  EXPOSE  CMD
```

시험 답안:

```
RUN = 빌드할 때 / CMD = 컨테이너 시작할 때
```

**한 줄 암기: RUN 은 만들 때, CMD 는 켤 때.**

### Linux 기본 명령 pwd cp mv rm -rf

- 쉬운 설명: pwd = 내 위치, cp = 복사, mv = 이동·이름 바꾸기, rm -rf = 휴지통 없이 삭제.
- 기술 설명: pwd 현재 작업 디렉터리(상대경로의 기준). 절대경로는 / 부터 전체 경로. cp 원본 복사본, mv 원본 새이름, rm -rf 폴더 강제 삭제(복구 어려움).

```
pwd
cp file.txt backup.txt
mv file.txt newfile.txt
rm -rf test/
```

시험에 나올 명령어:

```
pwd   cp file.txt backup.txt   mv file.txt newfile.txt   rm -rf test/
```

시험 답안:

```
위 4개 명령어 그대로
```

**한 줄 암기: rm -rf 는 조심: 복구가 어렵다.**

### 포트 매핑과 localhost:8080

- 쉬운 설명: 포트 매핑은 '내 컴퓨터 8080번 문'과 '컨테이너 80번 문'을 이어 주는 것이에요.
- 기술 설명: -p 호스트포트:컨테이너포트. -p 8080:80 이면 브라우저에서 localhost:8080 으로 접속해 컨테이너 안 80번 웹 서버에 닿습니다.

```
docker run -d -p 8080:80 nginx
# 브라우저: localhost:8080
```

시험에 나올 명령어:

```
docker run -d -p 8080:80 nginx
```

시험 답안:

```
localhost:8080
```

**한 줄 암기: -p 호스트:컨테이너 (앞이 내 컴퓨터).**

### Bind Mount 와 Volume

- 쉬운 설명: Bind Mount = 내 폴더를 컨테이너에 직접 연결(바로 반영), Volume = 컨테이너 밖 창고(삭제돼도 남음).
- 기술 설명: Bind Mount: -v ./app:/app 처럼 호스트 경로를 직접 지정, 코드 수정이 즉시 반영되어 개발용. Volume: Docker 가 관리하는 저장소, 컨테이너가 지워져도 데이터가 유지되어 운영·DB 용.

```
docker run -v ./app:/app nginx
docker run -v mydata:/data nginx
```

시험에 나올 명령어:

```
-v ./app:/app   -v mydata:/data
```

시험 답안:

```
개발 단계는 Bind Mount, 운영 단계는 Volume
```

**한 줄 암기: 개발은 Bind Mount, 운영은 Volume.**

### docker images / stats / attach vs exec

- 쉬운 설명: images = 이미지 창고 보기, stats = 컨테이너 건강검진, attach = 하던 일 같이 보기, exec = 새 일 시키기.
- 기술 설명: docker images 로컬 이미지 목록, docker stats CPU·메모리·네트워크 사용량, docker attach 기존 프로세스에 연결, docker exec 새 프로세스 실행(실무 표준).

```
docker images
docker stats
docker attach web
docker exec -it web bash
```

시험에 나올 명령어:

```
docker images   docker stats   docker attach web
```

시험 답안:

```
images / stats / attach / exec
```

**한 줄 암기: 실무에서는 대부분 exec.**

### 재현 가능한 환경, Git 과 GitHub

- 쉬운 설명: 같은 설명서와 같은 부엌이면 누가 만들어도 같은 요리가 나와요. 내 일기장은 Git, 인터넷 공유 일기장은 GitHub.
- 기술 설명: 재현 가능한 환경(Reproducible Environment) = 누가 어디서 실행해도 같은 결과. Docker 가 실행 환경을, Git 이 코드 버전을 맞춥니다. Git = 로컬 버전 관리 도구, GitHub 는 인터넷에 있는 원격 저장소 겸 협업 플랫폼. 환경까지 같이 포장하면 어디서든 똑같이 실행됨.

```
Dockerfile  -> docker build -> Image -> docker run -> Container
git add -> git commit -> git push
```

시험에 나올 명령어:

```
docker build -t myapp:1.0 .   git push
```

시험 답안:

```
재현 가능한 환경 (Reproducible Environment)
```

**한 줄 암기: 환경까지 같이 포장하면 어디서든 똑같이 실행됨.**

---

# D. 시험 직전 암기카드

## Python 한 장 요약

- 실행 python main.py / 버전 python -V
- input 은 항상 str → 계산하려면 int()
- / 나누기 · // 몫 · % 나머지 · ** 제곱
- x[-1] 마지막 · x[1:3] 끝 번호 제외
- append 추가 · pop 꺼내기 · sort 정렬 · len 개수
- d.get(키) → 없으면 None · d[키] → KeyError
- if → elif → else · for i in range(3) → 0,1,2
- break 탈출 · continue 건너뛰기 · return 없으면 None

## 예외 6종

- int("abc") → ValueError
- 리스트 범위 밖 → IndexError
- 없는 키 → KeyError
- 없는 파일 → FileNotFoundError
- 0으로 나눔 → ZeroDivisionError
- JSON 깨짐 → json.JSONDecodeError

## 클래스 · JSON

- class 이름: · 생성자 __init__ · 자기자신 self
- if __name__ == "__main__":
- dump/load = 파일 · dumps/loads = 문자열
- with open("state.json", "w", encoding="utf-8") as f:
- json.dump(data, f, ensure_ascii=False, indent=2)
- os.path.exists("state.json")

## Git 흐름

- init → add . → commit -m "msg" → push
- clone · pull · checkout(=switch)
- status · diff · log --oneline --graph
- branch · checkout -b 이름 · switch -c 이름
- main 에서 git merge 브랜치 → branch -d(안전) / -D(강제)
- 충돌: <<<<<<< HEAD / ======= / >>>>>>> → 정리 후 add, commit · 포기 merge --abort
- remote add origin 주소 · remote -v · push -u origin main
- git rm --cached 파일 · .gitignore(__pycache__/ , .env)
- Feat · Fix · Docs · Refactor

## 미션 요구사항 (2주차)

- 데이터 파일: 프로젝트 루트 state.json (UTF-8)
- 클래스 2개 이상 (예: Quiz, QuizGame) / Python 3.10 이상, 표준 라이브러리만
- 입력 처리: strip → 숫자 변환(ValueError) → 범위 검사 → 빈 입력, 안내 후 재입력
- Ctrl+C = KeyboardInterrupt, 입력 끝 = EOFError → 안전 종료
- 파일 없음 → 기본 퀴즈 / 손상 → 안내 후 복구
- Git: 커밋 10개 이상, 브랜치 병합 1회 이상, clone·pull 1회 이상
- README: 개요, 주제 선정 이유, 실행 방법, 기능 목록, 파일 구조, 데이터 파일 설명

## 1주차 복습

- ls -la · chmod 755(실행) / 644(일반)
- docker run -d -p 8080:80 --name web nginx
- docker build -t 이름:태그 .
- docker ps -a · docker logs -f · docker exec -it 이름 bash
- docker rm = 컨테이너 · docker rmi = 이미지
- Dockerfile: FROM WORKDIR COPY RUN ENV EXPOSE CMD (RUN 빌드때 / CMD 시작때)
- pwd 위치 · cp 복사 · mv 이동/이름변경 · rm -rf 강제삭제(위험)
- docker images 이미지 목록 · stats 자원 사용량 · exec 새 프로세스 · attach 기존 프로세스
- Image 는 설계도, Container 는 그걸 실제로 띄운 실행본 · 개발 때는 Bind Mount, 운영 때는 Volume
- Git = 로컬 · GitHub = 원격 · add = 준비 · commit = 저장 · 재현성: 환경까지 같이 포장하면 어디서든 똑같이 실행됨

## 출제 확률 TOP 10 (예상)

근거 있는 추정일 뿐 실제 출제와 다를 수 있습니다.

1. git merge 와 브랜치 명령 (checkout -b / switch -c / merge / branch -d) (명령어 위주 시험에서 가장 자주 묻기 좋은 묶음)
2. git push -u origin main, remote add origin, remote -v (원격 연결은 미션 필수 흐름)
3. git log --oneline --graph, status, diff (확인 명령은 단답으로 내기 쉬움)
4. 필수 7종 (init add commit push pull checkout clone) (미션 필수 명령)
5. json.dump / load vs dumps / loads (헷갈리기 쉬워 구분 문제로 적합)
6. with open(... "w"/"r", encoding="utf-8") 와 ensure_ascii=False (저장·불러오기 코드 빈칸)
7. 예외 이름 (ValueError, IndexError, KeyError, FileNotFoundError, ZeroDivisionError) (상황 → 이름 연결)
8. / // % ** 연산 결과와 슬라이싱 출력값 (출력값 문제의 단골)
9. class, __init__, self, if __name__ == "__main__" (클래스 용어 빈칸)
10. docker run -d -p --name / build -t / ps -a / rm vs rmi (1주차 복습 핵심)
