# 코드 분석 — Tic-Tac-Toe with AI Bot (`12234169-이진택-code.py`)

C++ 문법을 기준으로, Python 문법 차이와 Minimax 알고리즘 구조를 정리한 문서.

## ① Python 문법 — C++와 다른 점들

**1. 타입을 안 쓴다 (동적 타이핑)**
```python
board = [' '] * 9
```
C++라면 `std::vector<char> board(9, ' ');` 인데, Python은 변수 선언에 타입이 없다. `[' '] * 9`는 리스트를 9번 반복해서 늘리는 문법 — C++의 `vector(9, ' ')` 생성자와 같은 효과다.

**2. 리스트 컴프리헨션** (`get_empty_positions`, 39번 줄)
```python
return [i for i in range(9) if board[i] == ' ']
```
C++로 풀어 쓰면:
```cpp
vector<int> result;
for (int i = 0; i < 9; i++)
    if (board[i] == ' ') result.push_back(i);
return result;
```
한 줄로 "for + if + 담을 값"을 표현하는 문법. `range(9)`는 C++의 `for(int i=0;i<9;i++)`와 같다.

**3. 튜플과 언패킹** (`WIN_LINES`, `minimax` 등)
```python
for a, b, c in WIN_LINES:
```
`WIN_LINES`는 `(0,1,2)` 같은 튜플(수정 불가능한 고정 크기 묶음, C++의 `std::tuple<int,int,int>`에 대응)의 리스트다. `for a, b, c in ...`는 각 튜플을 풀어서 세 변수에 한 번에 대입 — C++에는 없는 문법(구조체 분해와 비슷).

**4. 체이닝 비교**
```python
if board[a] != ' ' and board[a] == board[b] == board[c]:
```
Python은 `a == b == c`를 `a==b and b==c`로 해석해준다. C++는 이런 체이닝이 없어서 `a==b && b==c`로 풀어 써야 한다.

**5. `None`과 `float('inf')`**
- `None`은 C++의 `nullptr`/`std::nullopt`에 대응하는 "값 없음" 표시자.
- `float('-inf')`, `float('inf')`는 C++의 `-INFINITY`, `INFINITY` (또는 `INT_MIN`/`INT_MAX`)와 같은 역할 — minimax 초기 최댓값/최솟값을 세팅할 때 쓴다.

**6. 함수가 값처럼 전달됨** (`get_bot_position`)
```python
if strategy == 1:
    return bot_move_minimax(board)
```
C++의 함수 포인터나 `std::function` 없이도, if문으로 분기해서 원하는 함수를 그냥 호출하기만 하면 된다. Python 함수는 일급 객체라 이런 코드가 자연스럽다.

**7. 리스트는 참조로 넘어간다**
```python
board[pos] = BOT_MARK   # minimax 내부에서 board를 직접 수정
...
board[pos] = ' '        # 되돌림(백트래킹)
```
C++에서 `vector<char>&`로 레퍼런스를 넘기는 것과 동일한 효과가 기본이다. Python은 리스트/딕셔너리 같은 가변(mutable) 객체를 함수에 넘기면 **항상 참조**로 넘어간다 (C++처럼 값 복사를 원하면 명시적으로 `board.copy()` 해야 함). 이 코드는 복사 없이 같은 board를 계속 고쳤다가 되돌리는 식으로 동작한다.

**8. f-string**
```python
print(f" {board[0]} | {board[1]} | {board[2]} ")
```
C++의 `std::format` (C++20)이나 `printf`와 비슷한 문자열 삽입 문법. `f"...{표현식}..."` 형태로 변수를 문자열에 바로 끼워 넣는다.

**9. `if __name__ == "__main__":`**
C++의 `int main()`과 목적은 같다("이 파일이 직접 실행될 때만 실행"). Python은 파일 자체가 스크립트라서, 다른 파일에서 이 파일을 `import`했을 때는 `play_game()`이 자동으로 실행되지 않게 막아주는 관용구다.

**10. 입출력**
`input()` = `std::cin`, `print()` = `std::cout`. 단, `input()`은 항상 **문자열**을 반환하므로(`raw.isdigit()`으로 숫자인지 검사 후 `int(raw)`로 직접 변환) C++의 `cin >> n`처럼 자동 형변환은 없다.

## ② 알고리즘 — Minimax (완전 탐색)

**핵심 구조**: 재귀 + 백트래킹으로 게임 트리를 끝까지 완전 탐색한다.

```
minimax(board, turn):
    승자가 있으면 즉시 리턴 (+1 봇 승, -1 사용자 승, 0 무승부)   ← 종료 조건(base case)
    turn이 BOT이면:
        빈 칸마다: 그 자리에 놓아보고 → 재귀호출(상대 턴) → 원상복구
        가능한 결과 중 최댓값 선택   (봇 = 이익 극대화)
    turn이 PLAYER면:
        같은 방식이지만 최솟값 선택  (사용자 = 봇의 이익을 최소화한다고 가정)
```

이건 **게임 이론의 minimax 알고리즘** 그대로다. 틱택토는 상태 수가 매우 작아서(최대 9! = 362,880가지 수순, 실제로는 승패로 조기 종료돼서 훨씬 적음) 알파-베타 가지치기 같은 최적화 없이도 완전 탐색이 순식간에 끝난다. C++로 짜도 로직은 동일하고, 유일한 차이는 재귀 함수 시그니처에 `vector<char>&`를 명시해야 한다는 것뿐이다.

**백트래킹 패턴**이 여러 곳(`minimax` 내부 두 곳, `bot_move_minimax`)에서 반복된다:
```python
board[pos] = MARK      # 1. 수를 둔다
score = minimax(...)   # 2. 그 상태를 평가한다 (재귀)
board[pos] = ' '       # 3. 원상복구 (다음 후보를 시도하기 위해)
```
이 패턴은 "한 상태 배열을 계속 재사용하며 탐색"하는 전형적인 방식으로, 매 후보마다 board를 복사하지 않아 메모리 효율이 좋다(대신 원상복구를 반드시 해줘야 하는 게 함정).

**`bot_move_minimax`와 `minimax`의 관계**: `bot_move_minimax`는 "봇이 처음 둘 수(pos) 자체"를 찾는 함수이고, `minimax`는 "그 이후 상태의 점수"만 계산하는 재귀 함수다. 그래서 최상위에서 `bot_move_minimax`가 각 빈 칸에 대해 직접 수를 둬보고 `minimax`를 한 번씩 호출해 점수를 비교하는 구조 — 재귀 함수 자체가 "이 수를 둘지 말지"까지 결정하지 않고 점수만 리턴하도록 역할이 분리돼 있다.

**다른 두 전략**은 알고리즘이라 부를 것도 없이 단순하다 — Random은 `random.choice`, Left-up first는 `min()`으로 인덱스가 가장 작은 빈 칸을 고른다. Minimax와 비교하면 "탐색 없이 즉시 결정"이라는 점이 대조된다.

전반적으로 코드는 과제 명세(전략 3종, 예외 2종, Minimax 유틸리티 +1/-1/0)를 정확히 구현하고 있고, 알고리즘적으로도 깨끗한 정석 minimax다.
