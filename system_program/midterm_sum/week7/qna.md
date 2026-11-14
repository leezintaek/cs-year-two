# Week 7 — Q&A

## Q1. `test b, a`에서 SF가 `a & b < 0`일 때 set되는 게 왜 그런지 이해가 안 돼

핵심은 **SF(Sign Flag)는 "연산 결과의 MSB(최상위 비트)를 그대로 복사한 것"** 이라는 점이다. SF는 어떤 연산이었는지(빼기인지 AND인지) 신경 쓰지 않는다. 결과값의 맨 왼쪽 비트가 1이면 SF=1, 0이면 SF=0이다.

**1단계: MSB = 1 ⇔ signed로 음수**

two's complement에서 MSB는 sign bit이다. 그래서 "결과의 MSB가 1이다"는 "결과를 signed로 보면 음수다"와 같은 말이다.

- `cmp b, a` → 결과 `a - b`의 MSB가 SF → "SF = `(a - b) < 0`"
- `test b, a` → 결과 `a & b`의 MSB가 SF → "SF = `(a & b) < 0`"

즉 두 경우 모두 같은 규칙(결과의 MSB → SF)이고, 결과식만 다를 뿐이다.

**2단계: `a & b`의 MSB는 언제 1이 되나?**

AND는 비트별로 계산하므로, 결과의 MSB = (a의 MSB) & (b의 MSB). 그래서 **a와 b의 MSB가 둘 다 1일 때만** 결과 MSB가 1이 된다.

→ `a & b < 0` ⇔ **a < 0 이고 b < 0** (둘 다 음수)

**예시 (4-bit)**

```
a = 1010 (-6)          a = 1010 (-6)
b = 1100 (-4)          b = 0111 ( 7)
-----------            -----------
a&b = 1000 (-8)        a&b = 0010 ( 2)
MSB=1 → SF=1           MSB=0 → SF=0
```

**3단계: 그래서 `test %rdi, %rdi`가 유용하다**

같은 값을 두 번 넣으면 `a & a = a` 이므로 결과는 a 자신이다.
- SF = a의 MSB → **`a < 0`인지** 바로 알 수 있음
- ZF = `a == 0`인지

값을 바꾸지 않고 "음수인가? 0인가?"만 플래그로 확인하는, `cmp $0, %rdi`보다 짧은 인코딩의 관용구다.

**정리**: SF는 "결과의 sign bit"일 뿐이고, `test`의 결과가 `a & b`이니까 SF = `(a & b) < 0`라고 쓴 것이다. AND 특성상 이는 "a, b가 둘 다 음수"와 같다.

## Q2. 결국 MSB가 1일 때만 SF에 영향을 주는 거잖아. 그럼 이게 필요한 이유가 뭐야?

**먼저 오해 하나 정리**: SF는 "MSB가 1일 때만 영향받는" 게 아니라, flag를 설정하는 명령어가 실행될 때마다 **항상 0 또는 1로 덮어써진다.** 결과 MSB가 1이면 SF=1, 0이면 SF=0. 즉 SF는 매번 "방금 나온 결과가 음수인가?"에 대한 답을 담고 있다.

**왜 필요한가: CPU의 조건 분기는 flag만 보고 결정한다**

`jl`, `js`, `setl` 같은 조건부 명령어는 레지스터 값을 직접 보지 않고 **오직 condition code(flags)만 읽는다.** 그래서 "음수인가?"라는 정보가 flag에 들어 있어야 C의 `if (a < 0)` 같은 조건을 어셈블리로 만들 수 있다. SF가 그 정보를 담는 유일한 flag다.

**쓰이는 곳 1: `test`로 부호 검사**

```c
if (a < 0) { ... }
```
```
test %rdi, %rdi     # a & a = a → SF = a의 MSB
js   .L_negative    # SF=1이면 점프 (jump if sign)
```
값을 바꾸지 않고, 비교 대상(0)을 따로 쓰지 않고, 명령어 하나로 부호를 확인할 수 있다.

**쓰이는 곳 2 (더 중요): signed 비교**

`cmp b, a` 후 `a < b`(signed)인지 판단하는 `jl`은 **`SF ^ OF`** 를 본다. `a - b`가 음수인지(SF)와 overflow가 났는지(OF)를 같이 봐야 정확한 signed 대소 비교가 된다. SF가 없으면 `jl`, `jge`, `jle`, `jg` 같은 **signed 비교 점프를 만들 수 없다.**
(참고: unsigned 비교는 SF 대신 CF를 쓴다 → `jb`, `ja` 등)

**정리**
- SF = "직전 결과가 signed로 음수인가"를 매번 기록하는 flag
- 분기 명령어는 flag만 보기 때문에, 부호 검사(`js`)와 signed 비교(`jl` 등 = `SF^OF`)에 반드시 필요하다
- `test`에서 서로 다른 a, b로 SF를 보는 경우는 드물고, 실제로는 `test %rdi,%rdi`처럼 **같은 값의 부호를 확인할 때** 주로 쓴다

## Q3. `test` instruction을 썼을 때 SF가 주요한 역할을 하는 상황이 있어?

있다. 거의 전부 **같은 레지스터를 두 번 넣는 `test %reg, %reg`** 형태이고, 목적은 **값과 0의 signed 대소 비교**다.

**전제: `test`는 OF와 CF를 항상 0으로 만든다**

AND는 overflow/carry가 생길 수 없으므로 `test` 후에는 OF=0, CF=0이다. 그래서 signed 비교 조건 `SF ^ OF`가 그냥 **`SF`** 가 된다. 즉 `test %rdi, %rdi`는 사실상 `cmp $0, %rdi`(a - 0 계산)와 같은 flag를 만들되, 인코딩이 더 짧다.

**SF가 핵심인 경우**

| C 조건 | 어셈블리 | 보는 flag |
|---|---|---|
| `a < 0` | `test %rdi,%rdi` + `js` 또는 `jl` | SF |
| `a >= 0` | `test %rdi,%rdi` + `jns` 또는 `jge` | ~SF |
| `a <= 0` | `test %rdi,%rdi` + `jle` | SF \| ZF |
| `a > 0` | `test %rdi,%rdi` + `jg` | ~SF & ~ZF |
| `a == 0` | `test %rdi,%rdi` + `je` | ZF (SF 무관) |

`a <= 0`, `a > 0`처럼 **SF와 ZF를 함께** 쓰는 경우도 많다. "0인가"는 ZF, "음수인가"는 SF가 맡는다.

```c
long abs_val(long a) {
    if (a < 0) return -a;
    return a;
}
```
```
test %rdi, %rdi     # SF = a의 MSB, OF = 0
js   .L_neg         # a < 0 이면 점프
```

**SF가 거의 쓰이지 않는 경우**

- 서로 다른 값 `test %rsi, %rdi`: 이건 주로 **bit mask 검사**용이다. `(a & mask) == 0`처럼 특정 비트가 켜졌는지 보는 것이므로 **ZF**를 쓴다. 이때 SF(= a와 b가 둘 다 음수)는 실용적인 의미가 거의 없다.

**정리**: `test`에서 SF가 주인공이 되는 건 **`test %reg,%reg`로 값의 부호(0과의 signed 비교)를 확인할 때**이고, mask 검사에는 ZF를 쓴다.

## Q4. [TF_quiz Q3] `a = 0`, `b = 1`일 때 `cmp b, a`를 실행하면 CF와 SF가 모두 1이 되는 이유는?

**정답: T**

`cmp b, a`는 `t = a - b`를 계산하고 결과는 저장하지 않은 채 condition code만 설정한다. → `t = 0 - 1`

**비트 결과**
```
  0000 ... 0000   (a = 0)
- 0000 ... 0001   (b = 1)
---------------
  1111 ... 1111   (borrow 발생)
```

| Flag | 값 | 이유                                |
|------|----|-------------------------------------|
| CF   | 1  | unsigned로 0 < 1 → MSB에서 borrow   |
| ZF   | 0  | 결과가 0이 아님                     |
| SF   | 1  | 결과 MSB가 1 (signed로 -1 < 0)      |
| OF   | 0  | 0 - 1 = -1은 signed 범위 안         |

- 뺄셈에서 CF는 **unsigned 기준으로 a < b일 때(borrow)** 1이 된다.
- SF는 결과의 MSB를 그대로 복사한다.

**연결되는 내용**
- 이 상태에서 `jb`(CF) → 점프 (unsigned로 0 < 1)
- `jl`(SF^OF = 1^0 = 1) → 점프 (signed로 0 < 1)
- 두 해석 모두 "a < b"로 일치하는 경우이다.

## Q5. [TF_quiz Q10] "`cmp b, a`는 `b - a`를 계산한다"가 틀린 이유는?

**정답: F** (`a - b`를 계산한다)

- `cmp b, a`는 `sub b, a`와 같은 계산(`a - b`)을 하되, 결과를 `a`에 저장하지 않고 **condition code만 설정**한다.
- AT&T 문법은 `op src, dst` 순서이고, `sub src, dst`는 `dst = dst - src`이다. `cmp`도 같은 순서를 따르므로 **두 번째 operand에서 첫 번째 operand를 뺀다.**

**예시**
```
cmp $0x64,%rdi     # t = x - 100
jle .L_out         # x - 100 <= 0, 즉 x <= 100이면 점프
```
- `jle`는 "두 번째 operand ≤ 첫 번째 operand"일 때 점프한다 → `x <= 100`
- 순서를 반대로(`100 - x`) 생각하면 조건을 거꾸로 해석하게 되므로 주의한다.

## Q6. [TF_quiz Q16] `long result = x ? *x + 1 : 0;`이 `gcc -O1`에서 cmov로 컴파일되지 않는 이유는?

**정답: F** (조건 분기 `je`로 컴파일된다)

**cmov의 동작 방식**
- conditional move는 **then 값과 else 값을 둘 다 먼저 계산**해 놓고, 조건에 따라 어느 값을 쓸지만 고른다.

**이 코드를 cmov로 만들면**
```
mov  (%rdi),%rax     # *x를 무조건 먼저 읽음  ← x가 NULL이면 여기서 segfault
add  $1,%rax
test %rdi,%rdi
cmovz $0,%rax        # (참고: 실제 x86에는 즉시값 cmov가 없음, 개념 설명용)
ret
```
- 조건(`x != NULL`)을 확인하기 **전에** `*x`를 읽어버린다.
- `x`가 NULL이면 C 코드에서는 안전하게 0을 반환해야 하는데, cmov 버전은 프로그램이 죽는다.

**실제 gcc -O1 결과**
```
mov  $0x0,%eax
test %rdi,%rdi
je   .done           # x == NULL이면 *x를 읽지 않고 건너뜀
mov  (%rdi),%rax
add  $0x1,%rax
.done:
ret
```

**cmov를 쓰면 안 되는 경우 (Bad Cases)**

| 경우                | 이유                                  |
|---------------------|---------------------------------------|
| Expensive 계산      | 안 쓸 쪽까지 계산해 오히려 손해       |
| Risky 계산          | 안 쓸 쪽 계산이 오류를 일으킬 수 있음 |

- 계산이 "간단한지"만 보는 게 아니라, **양쪽을 미리 계산해도 안전한지**도 컴파일러가 판단한다.

## Q7. [TF_quiz Q23] 8-bit 덧셈 `0x7F + 0x01`에서 OF = 1, CF = 0이 되는 이유는?

**정답: T**

```
  0111 1111   (0x7F)
+ 0000 0001   (0x01)
-----------
  1000 0000   (0x80)   MSB 밖으로 나가는 carry 없음
```

**같은 비트 결과를 두 가지로 해석**

| 해석     | 계산            | 결과       | Flag   |
|----------|-----------------|------------|--------|
| unsigned | 127 + 1 = 128   | 범위 안    | CF = 0 |
| signed   | 127 + 1 = -128  | overflow   | OF = 1 |

- **CF**: unsigned overflow 검사 → MSB에서 밖으로 carry가 나갔는가? 8비트 unsigned 범위는 0~255이므로 128은 정상 → CF = 0
- **OF**: signed overflow 검사 → 양수 + 양수인데 결과가 음수(MSB = 1) → OF = 1
  - 조건: `(a>0 && b>0 && t<0) || (a<0 && b<0 && t>0)`
- 나머지: SF = 1 (결과 MSB가 1), ZF = 0 (결과가 0이 아님)

**비교: `0xFF + 0x01`**
- 결과 `0x00`, MSB에서 carry 발생 → CF = 1, ZF = 1
- signed로는 -1 + 1 = 0으로 정상 → OF = 0
- 즉 CF와 OF는 **서로 독립적**이다. CPU는 같은 덧셈을 하고 두 해석의 overflow를 각각 기록한다.

## Q8. [TF_quiz Q30] `leaq`가 산술 연산을 하면서도 condition code를 변경하지 않는 이유는?

**정답: T**

- condition code는 **산술·논리 연산 명령어**(`add`, `sub`, `and`, `xor`, `shl` 등)가 실행될 때 자동으로(implicitly) 설정된다.
- 그러나 `lea`는 원래 **주소 계산(address computation)** 용도의 명령어이다. 덧셈·곱셈처럼 쓰일 뿐 ALU의 산술 연산 명령어로 취급되지 않으므로 flag를 건드리지 않는다.
  - 강의: "Implicitly set by arithmetic and logical operations (**not by leaq**)"

**flag를 바꾸지 않는 명령어 정리**

| 명령어 | flag 변경 | 이유                     |
|--------|-----------|--------------------------|
| `mov`  | X         | 데이터 이동만 함         |
| `lea`  | X         | 주소 계산 명령어         |
| `add`  | O         | 산술 연산                |
| `cmp`  | O         | flag 설정이 목적         |
| `test` | O         | flag 설정이 목적         |

**왜 유용한가**
- `cmp`로 flag를 설정한 뒤 `jcc`로 점프하기 전에 다른 계산을 끼워 넣어야 할 때, `lea`를 쓰면 flag가 깨지지 않는다.
- 예: 강의 `f2`에서 `lea (%rsi,%rsi,2),%rax`로 `3*result`를 계산 — 덧셈+곱셈을 한 번에, flag 영향 없이 수행한다.

## Q9. [TF_quiz Q37] 8-bit 덧셈 `0xFF + 0x01`에서 OF = 1이 아닌 이유는?

**정답: F** (CF = 1, ZF = 1은 맞지만 **OF = 0**)

```
  1111 1111   (0xFF)
+ 0000 0001   (0x01)
-----------
1 0000 0000   → 8비트 결과 0x00, MSB 밖으로 carry 1
```

| Flag | 값 | 이유                                      |
|------|----|-------------------------------------------|
| CF   | 1  | unsigned: 255 + 1 = 256 → 범위 초과       |
| ZF   | 1  | 8비트 결과가 0x00                         |
| SF   | 0  | 결과 MSB가 0                              |
| OF   | 0  | signed: -1 + 1 = 0 → 정상                 |

- **OF 판단은 signed로 해석해서** 한다. `0xFF`는 signed로 **-1**이다.
- OF 조건: (양수 + 양수 → 음수) 또는 (음수 + 음수 → 양수)
- 여기서는 **음수 + 양수**이므로 부호가 다른 두 수의 덧셈 → **절대 overflow가 날 수 없다.**

**Q23(`0x7F + 0x01`)과 비교**

| 연산           | CF | OF | 해석                                 |
|----------------|----|----|--------------------------------------|
| `0x7F + 0x01`  | 0  | 1  | unsigned 정상 / signed overflow      |
| `0xFF + 0x01`  | 1  | 0  | unsigned overflow / signed 정상      |

- CF와 OF는 **독립적**이다. "carry가 나면 overflow도 났다"고 연결 짓지 않는다.

## Q10. [TF_quiz Q43] `while` 루프를 jump-to-middle 방식으로 번역하면 첫 명령어가 테스트로 가는 무조건 `jmp`인 이유는?

**정답: T**

**while vs do-while의 차이**
- `do-while`: 본문을 **먼저 한 번 실행**한 후 조건 검사
- `while`: **조건을 먼저 검사** → 조건이 처음부터 거짓이면 본문이 한 번도 실행되지 않아야 한다.

**jump-to-middle 구조**
```
        goto test;          ← 먼저 테스트로 무조건 점프
loop:
        body-statement
test:
        t = test-expr;
        if (t) goto loop;   ← 조건이 참이면 본문으로
```

**강의 예시 `f4`**
```c
long f4(long cnt) {
    while (cnt > 100) cnt--;
    return 3*cnt;
}
```
```
0:  jmp  6 <f4+6>      # jump to middle (테스트로)
2:  sub  $0x1,%rdi     # body
6:  cmp  $0x64,%rdi    # test: cnt - 100
a:  jg   2 <f4+2>      # cnt > 100이면 body로
c:  lea  (%rdi,%rdi,2),%rax
10: retq
```

**do-while(`f3`)과 비교**
```
0:  sub  $0x1,%rdi     # body가 바로 시작 (초기 jmp 없음)
4:  cmp  $0x64,%rdi
8:  jg   0 <f3>
```
- do-while은 본문을 무조건 한 번 실행하므로 초기 `jmp`가 필요 없다.
- while은 do-while 구조에 **"처음에 테스트로 점프"만 추가**한 형태이다. 이렇게 하면 테스트 코드를 한 벌만 두고도 while의 의미를 지킬 수 있다.
- `for` 루프도 init 후 같은 방식(jump to testing)으로 번역된다 (`f5`).
