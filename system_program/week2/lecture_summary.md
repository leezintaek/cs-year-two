# Week 2 — Bits, Bytes, and Integers

**과목**: CSE3209 System Programming (2026 가을)
**교재**: Computer Systems, 3rd Edition (Bryant), Chapter 2 (pp.31-pp.105)

## 1. 오늘의 목표 (Today's Goal)

- 정수(Integer)의 표현(representation)/해석(interpretation)/캐스팅(casting)을 이해하는 것이 목표.
- 정수 연산은 예상치 못한(surprising) 결과를 낳을 수 있고, 버그의 원인이 될 수 있다.
- 예시: `INT_MIN`을 가진 `x`에 대해 `x < 1 && x-1 >= 0`, `x < 0 && -x <= 0` 같은 조건이 **참**이 되는 경우가 있음 → 정수 오버플로우 때문.

## 2. 비트와 바이트 (Bits and Bytes)

- **비트(bit)**: 0 또는 1. 컴퓨터는 "on/off" 두 상태 개념 위에 만들어짐. 트랜지스터가 이를 하드웨어로 구현.
  - 비트를 **표현**하는 것(두 개의 구분 가능한 물리적 상태)과 **저장**하는 것(플립플롭·래치 같은 양안정(bistable) 회로)은 다른 문제.
- **8비트 = 1바이트**, 4비트(반 바이트)는 **니블(nibble)**.
- 비트 패턴에 의미(해석)를 부여함으로써 숫자, 문자, 집합, 문자열 등을 표현할 수 있음.
- 컴퓨터 메모리는 거대한 바이트 배열이며 **바이트 단위로만 주소를 매길 수 있다(byte-addressable)** — 비트 단위 주소 지정은 불가능.

## 3. 16진수 표기법 (Hexadecimal Notation)

- 32/64비트처럼 큰 수를 다룰 때, 사람이 읽기 좋은 base-16(16진수)로 표기.
- 예: 165(10진수) = `0b10100101`(2진수) = `0xa5`(16진수).
- 16진수는 2진수로 변환이 쉬우면서도(4비트=1자리) 훨씬 짧아 "휴대성(portable)" 있는 표기.

## 4. 정수의 표현 방식 (Representations of Numbers)

- **Unsigned Integers**: 0 이상의 수만 표현.
- **Signed Integers**: 양수/음수/0을 모두 표현.
- **Floating-point**: 실수 표현(다음 강의에서 다룸).

### Unsigned 표현/해석 (B2U)
- w비트 벡터 `[x_{w-1}, ..., x_0]`를 이진 가중 위치 표기법으로 해석.
- `B2U_w(x) = Σ x_i · 2^i` (i = 0 ~ w-1)
- 매핑 범위: `{0,1}^w → {0, 2^w - 1}`

## 5. 음수와 양수를 함께 표현하는 방법

### Sign-Magnitude(부호-크기) 표현
- 최상위 비트(MSB)를 부호 비트로 사용, 나머지로 크기를 표현.
- **단점**: 0이 두 가지(`+0`, `-0`)로 표현됨, 덧셈 하드웨어가 복잡해짐(부호를 먼저 판별해야 함).

### Two's-Complement(2의 보수) 표현 — 대부분의 최신 머신이 사용
- 핵심 아이디어: 보수(complement)를 이용하면 부호와 무관하게 이진 덧셈이 그대로 동작.
  - 10진수 예: A − B = A + (10^w − B), 캐리(carry)는 버림.
  - 2진수: A − B = A + (2^w − B), 캐리는 버림.
- 음수의 2의 보수 만들기: `C = 2^w - x = (2^w - 1 - x) + 1 = ~x + 1`
  - 규칙: 양수에서 시작 → **모든 비트를 뒤집고(flip)** → **1을 더한다**.
  - 예(8비트, -5): `00000101`(+5) → flip → `11111010` → +1 → `11111011` = `0xfb`
- 또 다른 트릭(오른쪽에서 왼쪽으로): 오른쪽부터 읽다가 처음 나오는 1까지는 그대로 **복사(copy)**하고, 그 이후 비트는 **반전(flip)**한다.
  - 예: -4 → `00000100` → (복사: 100, 반전: 11111) → `11111100` = `0xfc`
- gdb의 `x` 커맨드로 실제 비트 패턴 확인 가능 (`x /1bx`, `/1hx`, `/1wx`, `/1gx` 등, b=byte, h=halfword, w=word, g=giant word; t/x/d/o/u/f/a/c/s/i 형식 지정자).

### Two's-Complement 해석 (B2T)
- MSB에 **음의 가중치** `-2^{w-1}`을 부여(→ 부호 비트).
- `B2T_w(x) = -x_{w-1}·2^{w-1} + Σ x_i·2^i` (i = 0 ~ w-2)

## 6. C의 정수 타입과 크기

- ANSI/ISO C 표준: `char`, `short`, `int`, `long` 각각 signed/unsigned 존재.
- `int`/`short`는 최소 16비트, `long`은 `int` 이상이며 최소 32비트여야 함.
- x86-64에서 `long`과 포인터는 64비트(**LP64** 데이터 모델). (ILP64는 int/long/pointer 모두 64비트)
- 정확한 크기는 **머신과 컴파일러에 따라 다름**.
- x86-64 typical 크기: `char`=1, `short`=2, `int`=4, `long`=8, `float`=4, `double`=8, `Pointer`=8 바이트.
- `<limits.h>`: `UCHAR_MAX`, `USHRT_MAX`, `UINT_MAX`, `ULONG_MAX`(unsigned 최댓값), `CHAR_MIN/MAX`, `SHRT_MIN/MAX`, `INT_MIN/MAX`, `LONG_MIN/MAX` 정의. 이 값들도 **컴파일러 구현에 따라 다름**.
- `<stdint.h>`(C99): `intN_t`/`uintN_t` 형태의 **정확한 너비(explicitly-sized)**, 플랫폼 독립적 정수 타입 제공 → 이식성 있는 코드 작성 가능.

### 중요한 수치 (Word size별)
| Value | 8bit | 16bit | 32bit | 64bit |
|---|---|---|---|---|
| UMax | 0xFF (255) | 0xFFFF (65535) | 0xFFFFFFFF (4,294,967,295) | 0xFFFFFFFFFFFFFFFF |
| TMin | 0x80 (-128) | 0x8000 (-32768) | 0x80000000 (-2,147,483,648) | 0x8000000000000000 |
| TMax | 0x7F (127) | 0x7FFF (32767) | 0x7FFFFFFF (2,147,483,647) | 0x7FFFFFFFFFFFFFFF |

## 7. printf와 정수

- 32비트 정수용 주요 포맷 지정자: `%d`(signed), `%u`(unsigned), `%x`(hex).
- **포맷 지정자는 "어떻게 출력할지"만 결정** — 실제 비트는 동일.
- `%x`(소문자 hex) vs `%X`(대문자), `%#x`(0x 접두사), `%#08X`(0X 접두사 + 너비 8 + 0 패딩).
- 예: `int x=3, y=-3;` → `x+y`는 비트상 `0x00000000`.

## 8. 오버플로우 (Overflow)

- 표현 가능한 최댓값을 초과하면 **최솟값으로 wrap-around**: `0b1111 + 0b1 = 0b0000`.
- 최솟값 아래로 내려가면 **최댓값으로 wrap-around**: `0b0000 - 0b1 = 0b1111`.
- C는 오버플로우를 에러로 알리지 않는다.
- 실제 사례: YouTube "강남스타일" 조회수가 32비트 정수(최대 2,147,483,647) 범위를 초과해 64비트로 전환해야 했음.
- 예: `short s_money = SHRT_MAX; s_money = s_money + 1;` → 오버플로우되어 음수가 됨.

## 9. 캐스팅 (Casting)

- 명시적 캐스팅: `(int)`, `(unsigned int)` 등 — U2T/T2U와 동일한 규칙.
- 암묵적 캐스팅: 대입문, 함수 호출 인자 전달 시에도 발생.
- **바이트(비트 패턴)는 캐스팅해도 그대로 유지되며, 타입에 따라 다르게 "재해석"될 뿐**.
  - 예: `int v = -1;` → `unsigned int uv = (unsigned int) v;` → `v = -1`, `uv = 4294967295`, 둘 다 비트 패턴은 `0xffffffff`.

### Signed ↔ Unsigned 관계
- 2의 보수 → unsigned 변환 시 **순서 역전(ordering inversion)**: 큰 음수가 큰 양수로 매핑됨.
- signed와 unsigned 범위 사이를 오갈 때 값이 `2^w`만큼 커지거나 작아지는 효과.

### 캐스팅 서프라이즈 (Casting Surprises)
- **상수(constant)**: 기본은 signed. `U` 접미사를 붙이면 unsigned (`0U`, `4294967259U`).
- **표현식 평가**: signed와 unsigned가 한 식에 섞이면 **signed가 unsigned로 암묵적 캐스팅**됨. 비교 연산자(`<`, `>`, `==`, `<=`, `>=`)도 포함.
  - 예: `int x = -1; if (x > 0U)` → 참(!) — `x`가 unsigned로 캐스팅되어 매우 큰 값이 되기 때문.
  - `W=32` 기준 예시표: `-1 > 0U`(unsigned 비교), `2147483647U < -2147483648`(unsigned 비교) 등 다수의 "함정" 사례 존재.

## 10. 바이트 순서 (Byte Ordering / Endianness)

- 멀티바이트 워드를 메모리에 저장할 때 바이트 순서를 정하는 두 방식.
- **Big Endian**(Sun, PPC Mac, 인터넷 표준): 최하위 바이트(LSB)가 **가장 높은 주소**에 위치.
- **Little Endian**(x86, ARM 기반 Android/iOS/Windows): 최하위 바이트가 **가장 낮은 주소**에 위치.
- 예: `x = 0x01234567`, `&x = 0x100`일 때
  - Big Endian: `0x100~0x103` = `01 23 45 67`
  - Little Endian: `0x100~0x103` = `67 45 23 01`
- 네트워크 프로그래밍에서는 `htons()` 등으로 호스트 바이트 순서 ↔ 네트워크 바이트 순서(빅 엔디안) 변환 필요.
- `show_bytes()` 같은 함수로 `unsigned char *`를 이용해 실제 메모리의 바이트를 하나씩 출력해 확인 가능.

## 11. 비트 표현의 확장(Expanding)과 축소(Truncating)

### 확장 (더 작은 타입 → 더 큰 타입)
- C는 자동으로 **부호 확장(sign extension)**을 수행.
- 규칙: MSB(부호 비트)를 k번 복사하여 앞에 붙인다. `X' = [x_{w-1}, ..., x_{w-1}, x_{w-1}, x_{w-2}, ..., x_0]`
- **Unsigned 확장**: 상위 비트에 0을 채움.
- **Signed 확장**: 상위 비트에 부호 비트를 채움(음수면 1, 양수면 0). → 두 경우 모두 원래 값과 같은 값을 유지.

### 축소 (더 큰 타입 → 더 작은 타입, Truncating)
- 상위 `w-k`비트를 그냥 버리고 하위 k비트만 남김: `[x_{k-1}, ..., x_0]`.
- signed/unsigned 모두 동일한 규칙으로 잘림.
- 예: `int x = 15213; char u = (char) x;` → `u = 109` (하위 8비트만 남음, `109` = `0x6d`)
- **예상치 못한 결과**를 낳을 수 있음(값이 완전히 달라짐).

## 12. 2의 보수 음수화 (Two's-Complement Negation)

- 일반적으로 `TComp(u) = -u`.
- **TMin은 특수 케이스**: `TComp(TMin) = TMin` (자기 자신의 음수가 자기 자신!) — 표현 가능한 범위가 대칭이 아니기 때문.
- 관찰: `~x + x == 111...11₂ == -1`, 즉 `~x + 1 == -x`.
- 예: `int x = INT_MIN;` → `~x + 1`을 계산해도 여전히 `INT_MIN`(오버플로우).
- `-fwrapv` 컴파일 옵션: signed 산술 연산(음수화/덧셈/뺄셈/곱셈)의 오버플로우가 2의 보수 방식으로 **wrap-around**된다고 컴파일러가 가정하도록 지시(기본적으로 signed overflow는 undefined behavior).

## 13. 덧셈 (Addition)

### Unsigned 덧셈 (UADD)
- `x, y`가 `[0, 2^w - 1]` 범위일 때, 참 합(true sum)은 최대 `w+1`비트 필요.
- 상위 캐리 비트를 버림 = `2^w`를 빼는 것과 동일 = **모듈로 `2^w` 연산**.
- **오버플로우 판정**: `sum < x` (또는 `sum < y`)이면 오버플로우 발생.

### Two's-Complement 덧셈 (TADD)
- `x, y`가 `[-2^{w-1}, 2^{w-1}-1]` 범위일 때, 참 합은 최대 `w+1`비트 필요 → 상위 비트를 버리고 남은 `w`비트를 2의 보수로 해석.
- **양의 오버플로우(Positive overflow)**: `x+y ≥ 2^{w-1}`일 때 합이 `2^w`만큼 줄어들며 음수처럼 보임.
- **음의 오버플로우(Negative overflow)**: `x+y < -2^{w-1}`일 때 합이 `2^w`만큼 늘어나며 양수처럼 보임.
- 대부분의 컴퓨터는 **동일한 덧셈 하드웨어 명령어**로 unsigned/signed 덧셈을 모두 처리.
- 오버플로우 없는 덧셈 검사 함수:
  ```c
  int tadd_ok(int x, int y) {
    int sum = x+y;
    int neg_over = x < 0 && y < 0 && sum > 0;
    int pos_over = x > 0 && y > 0 && sum < 0;
    return !neg_over && !pos_over;
  }
  ```
- 예: `x=1; y=INT_MAX;` → `x+y < 0` → 오버플로우로 `INT_MIN`이 됨.

## 14. 뺄셈 (Subtraction, 참고)

- `a - b = a + (-b)` → b의 2의 보수를 구해 a에 더하면 됨.
- 즉, **덧셈 회로와 보수(complement) 회로만 있으면 뺄셈도 구현 가능**(별도의 뺄셈 회로 불필요).

## 15. 곱셈 (Multiplication)

- w비트 수 두 개를 곱하면 결과는 **최대 2w비트**가 필요할 수 있음.
  - 2의 보수 최댓값: `(TMin_w)^2 = 2^{2w-2}` → `2w-1`비트로는 표현 불가능해 2w비트 필요.
  - Unsigned 최댓값: `(2^w-1)^2 = 2^{2w} - 2^{w+1} + 1` → 역시 2w비트 필요.
- 원리: 각 자릿수(비트)에 대한 부분곱(partial product)을 구하고, 시프트한 뒤 모두 더함. 곱하는 비트가 1이면 피승수를 복사, 0이면 0으로 시프트만.
- 결과의 상위 w비트는 버려짐(`UMult_w(u,v) = u·v mod 2^w`).
- 음수 곱셈: (1) 그냥 곱한 뒤 부호가 다르면 결과를 음수화, 또는 (2) Booth's algorithm 사용.
- 오버플로우 없는 곱셈 검사(64비트로 확장 후 다시 축소해 비교):
  ```c
  int tmult_ok(int x, int y) {
    int64_t pll = (int64_t) x * y;
    return pll == (int) pll;
  }
  ```
  - 주의: `int64_t pll = x*y;`처럼 쓰면 곱셈이 **32비트로 먼저 계산되어(오버플로우 가능) 이후 64비트로 부호 확장**되므로 잘못된 결과가 나올 수 있음. 캐스팅 위치가 중요.
- 오버플로우 예시: `int x=50000; x*x` → 음수로 오버플로우. `x=INT_MIN; 2*x` → `0`이 됨(오버플로우로 wrap).

## 16. 2의 거듭제곱 곱셈과 시프트 (Power-of-2 Multiply with Shift)

- `u << k`는 `u * 2^k`와 같음 (signed/unsigned 모두 성립).
- 예: `u * 8 == u << 3`, `u * 24 == (u << 5) - (u << 3)`.
- 대부분의 머신에서 시프트+덧셈이 곱셈보다 빠르므로, **컴파일러가 자동으로 이런 최적화 코드를 생성**함 (예: `x*8`을 `shl $0x3, %eax`로 컴파일).

## [참고] 나눗셈 (Division)

- 곱셈보다 복잡하며, unsigned 나눗셈은 **시프트(shift)와 뺄셈(subtract)** 반복으로 구현 가능(곱셈용 하드웨어를 재사용).
- 이 알고리즘은 음수까지 확장 가능.

## [참고] 연산별 상대 비용 (Relative Cost)

| 연산 | 상대 비용 |
|---|---|
| printf / scanf | 1000 |
| malloc / free | 800 |
| 삼각함수 (sin, cos...) | 500 |
| 부동소수점 연산(모든 연산) | 100 |
| 정수 나눗셈 | 30 |
| 정수 곱셈 | 20 |
| 함수 호출 | 10 |
| 배열 인덱싱 | 6 |
| 시프트 | 5 |
| 덧셈/뺄셈 | 5 |
| 포인터 역참조 | 2 |
| 비트 and/or/not | 1 |
| 논리 and/or/not | 1 |

→ 시프트/덧셈은 매우 저렴한 반면, 곱셈/나눗셈/부동소수점/printf는 상대적으로 매우 비쌈. 이 때문에 컴파일러가 곱셈을 시프트+덧셈으로 대체하는 최적화를 자주 수행.
