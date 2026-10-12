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
