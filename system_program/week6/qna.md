# Week 6 — Q&A

## Q1. [TF_quiz Q1] `%rax = 0x100`, `%rbx = 0x10`, 메모리 `0x200~0x207 = 98 ba dc fe 10 32 54 76`일 때 `addl (%rax,%rax), %ebx` 실행 후 `%rbx`가 `0x00000000fedcbaa8`인 이유는?

**정답: T**

**1단계: 주소 계산**
- `(%rax,%rax)`는 indexed addressing mode `(rb, ri)` → `M[R[rb] + R[ri]]`
- 주소 = `0x100 + 0x100 = 0x200`

**2단계: 메모리에서 4바이트 읽기**
- 접미사 `l`(double word)이므로 4바이트를 읽는다 → `98 ba dc fe`
- Little Endian이므로 낮은 주소의 바이트가 LSB → 값은 `0xfedcba98`

**3단계: 덧셈**
```
  0xfedcba98
+ 0x00000010   (%ebx)
------------
  0xfedcbaa8
```

**4단계: 상위 32비트**
- 목적지가 32비트 레지스터(`%ebx`)이므로, `movl`과 마찬가지로 **32비트 연산 결과를 레지스터에 쓸 때는 상위 32비트가 0이 된다.**
- 따라서 `%rbx = 0x00000000fedcbaa8`

**함정 포인트**
- 바이트를 `0x98badcfe`처럼 순서대로 읽으면 틀린다 (Little Endian).
- 상위 32비트가 원래 값을 유지한다고 착각하기 쉽다. 8/16비트(`addb`, `addw`) 연산은 나머지 비트를 유지하지만, **32비트 연산만 예외적으로 상위 32비트를 0으로 만든다.**

## Q2. [TF_quiz Q8] 아래 `q6`의 반환값이 `2*x - y`가 아닌 이유는?

```
mov  %rdx,%rax
lea  (%rsi,%rsi,1),%rdx
sub  %rax,%rdx
mov  %rdx,(%rdi,%rsi,8)
ret
```

**정답: F** (반환값은 `y`)

인자: `%rdi = buf`, `%rsi = x`, `%rdx = y` / 반환값: `%rax`

| 명령어                    | 동작                | 레지스터 상태     |
|---------------------------|---------------------|-------------------|
| `mov %rdx,%rax`           | rax ← y             | rax = y           |
| `lea (%rsi,%rsi,1),%rdx`  | rdx ← x + x         | rdx = 2x          |
| `sub %rax,%rdx`           | rdx ← rdx - rax     | rdx = 2x - y      |
| `mov %rdx,(%rdi,%rsi,8)`  | M[buf + 8x] ← rdx   | buf[x] = 2x - y   |

- `ret` 시점의 `%rax`는 첫 줄에서 넣은 `y` 그대로이다.
- 따라서 C 코드는:

```c
long q6(long buf[], long x, long y) {
    buf[x] = 2*x - y;
    return y;
}
```

**함정 포인트**
- `2x - y`는 **메모리(`buf[x]`)에 저장된 값**이고, 반환값이 아니다.
- 반환값은 항상 "`ret` 직전 `%rax`에 무엇이 있느냐"로 판단한다.
- 첫 줄에서 `y`를 `%rax`로 옮긴 이유: `%rdx`를 계산용으로 덮어써야 하는데, `y`는 반환값으로도 필요하므로 미리 `%rax`에 보관한 것이다.
- `sub %rax,%rdx`는 AT&T 문법이므로 `rdx - rax`이다 (`rax - rdx` 아님).

## Q3. [TF_quiz Q13] `%rax = 0`, 메모리 `0x200~0x207 = 98 ba dc fe 10 32 54 76`일 때 `movsbw 0x201, %ax` 실행 후 `%rax`가 `0x000000000000ffba`인 이유는?

**정답: T**

**1단계: 명령어 이름 해석**
- `movs` + `b` + `w` → **sign-extend**, source **byte** → destination **word(2바이트)**

**2단계: source 읽기**
- 주소 `0x201`의 1바이트 → `0xba` = `1011 1010` (MSB = 1)

**3단계: sign extension**
- MSB(1)를 복사해 2바이트로 확장 → `1111 1111 1011 1010` = `0xffba`

**4단계: 레지스터에 쓰기**
- 목적지가 `%ax`(16비트)이므로 **하위 2바이트만 바뀌고 나머지 6바이트는 그대로**이다.
- 원래 `%rax = 0`이었으므로 → `0x000000000000ffba`

**비교: 같은 바이트(`0xba`)를 다른 명령어로 옮기면**

| 명령어                | 결과 `%rax`            |
|-----------------------|------------------------|
| `movsbw 0x201,%ax`    | `0x000000000000ffba`   |
| `movzbw 0x201,%ax`    | `0x00000000000000ba`   |
| `movsbl 0x201,%eax`   | `0x00000000ffffffba`   |
| `movsbq 0x201,%rax`   | `0xffffffffffffffba`   |

- `movsbl`은 목적지가 32비트이므로 상위 32비트가 **0**이 된다 (32비트 쓰기 예외 규칙).
- 상위 비트가 1로 채워지는 범위는 **목적지 크기까지**이다.

## Q4. [TF_quiz Q18] 아래 `q3`의 반환값이 `x*6`이 아닌 이유는?

```
lea  (%rdi,%rdi,2),%rax
shl  $0x2,%rax
ret
```

**정답: F** (반환값은 `x*12`)

| 명령어                     | 동작                   | `%rax`   |
|----------------------------|------------------------|----------|
| `lea (%rdi,%rdi,2),%rax`   | rax ← x + x×2          | 3x       |
| `shl $0x2,%rax`            | rax ← rax << 2 (×4)    | 12x      |

- `shl $k`는 2^k를 곱한다. `$0x2`는 2비트 shift이므로 **×4**이다 (×2가 아님).
- 따라서 3x × 4 = **12x**

**함정 포인트**
- shift 양 `k`를 곱하는 수로 착각하면 3x × 2 = 6x라고 계산하게 된다.
- 비교: 강의의 `x*48` = `lea (%rdi,%rdi,2)` + `shl $4` → 3x × 16 = 48x

## Q5. [TF_quiz Q24] `movzbq`, `movzwq`처럼 `movzlq` 명령어가 존재하지 않는 이유는?

**정답: F** (`movzlq`는 존재하지 않는다)

- x86-64에는 **32비트 레지스터에 값을 쓰면 상위 32비트가 자동으로 0이 되는** 규칙이 있다.
- 그래서 일반 `movl`만으로 32비트 → 64비트 zero-extension이 이미 이루어진다. 별도의 `movzlq`가 필요 없다.

```c
void f11(unsigned long *x, unsigned int y) { *x = y; }
```
```
mov  %esi,%eax       # 32비트 이동 → %rax의 상위 32비트 = 0 (== 논리적으로 movzlq)
mov  %rax,(%rdi)
ret
```

**zero-extend / sign-extend 명령어 정리**

| source → dest | zero-extend        | sign-extend |
|---------------|--------------------|-------------|
| 1 → 2         | `movzbw`           | `movsbw`    |
| 1 → 4         | `movzbl`           | `movsbl`    |
| 1 → 8         | `movzbq`           | `movsbq`    |
| 2 → 4         | `movzwl`           | `movswl`    |
| 2 → 8         | `movzwq`           | `movswq`    |
| 4 → 8         | 없음 (`movl` 사용) | `movslq`    |

- sign-extend는 상위 비트를 **1로 채워야 할 수도** 있으므로 `movslq`가 따로 존재한다.
- 실제로 gcc는 `movzbq` 대신 `movzbl`을 자주 쓴다 (`f9` 예시: `movzbl %sil,%esi`). 32비트 쓰기 규칙으로 결과가 같고 인코딩이 더 짧기 때문이다.

## Q6. [TF_quiz Q29] 메모리 `0x200~0x207 = 98 ba dc fe 10 32 54 76`일 때 `movq 0x200, %rax` 결과가 `0x98badcfe10325476`이 아닌 이유는?

**정답: F** (결과는 `0x76543210fedcba98`)

- x86-64는 **Little Endian**이다 → 가장 낮은 주소(`0x200`)의 바이트가 **LSB**이다.
- 8바이트를 읽어 **주소가 높은 쪽부터 왼쪽(MSB)에** 쓰면 된다.

```
주소:   0x207 0x206 0x205 0x204 0x203 0x202 0x201 0x200
바이트:  76    54    32    10    fe    dc    ba    98
         MSB ←──────────────────────────────────→ LSB

%rax = 0x 76 54 32 10 fe dc ba 98
```

**함정 포인트**
- 메모리 그림을 왼쪽에서 오른쪽으로 그대로 읽으면 `0x98badcfe10325476`이 나온다. 이건 Big Endian 해석이다.
- 바이트 순서만 뒤집고, 바이트 안의 두 16진수 자리(`98`)는 뒤집지 않는다 (`89` 아님).

**같은 메모리에서 크기별로 읽으면 (강의 Practice #1)**

| 명령어            | 읽는 바이트      | 결과                   |
|-------------------|------------------|------------------------|
| `movb 0x207,%al`  | `76`             | `0x76`                 |
| `movw 0x202,%ax`  | `dc fe`          | `0xfedc`               |
| `movl 0x200,%eax` | `98 ba dc fe`    | `0xfedcba98`           |
| `movq 0x200,%rax` | `98 ~ 76` (8개)  | `0x76543210fedcba98`   |

## Q7. [TF_quiz Q34] Problem 3-4의 어셈블리에서 `sar`이 쓰인 이유와 `t2 = (a - b + c) >> 2`인 이유는?

**정답: T**

인자: `%rdi = a`, `%rsi = b`, `%rdx = c`

| 명령어                    | 동작              | 의미              |
|---------------------------|-------------------|-------------------|
| `sub %rsi,%rdi`           | rdi ← rdi - rsi   | rdi = a - b       |
| `lea (%rdi,%rdx,1),%rax`  | rax ← rdi + rdx   | t1 = a - b + c    |
| `mov %rax,%rdx`           | rdx ← rax         | rdx = t1          |
| `sar $0x2,%rdx`           | rdx ← rdx >> 2    | t2 = t1 >> 2      |
| `and %rdx,%rax`           | rax ← rax & rdx   | return t1 & t2    |

```c
long q4(long a, long b, long c) {
    long t1 = a - b + c;
    long t2 = t1 >> 2;
    return t1 & t2;
}
```

**`sar` vs `shr`**
- C의 `>>`는 하나지만, 어셈블리는 두 가지이다.
  - `sar` (arithmetic): 왼쪽을 **MSB(부호 비트)로 채움** → signed용
  - `shr` (logical): 왼쪽을 **0으로 채움** → unsigned용
- `long`은 signed이므로 `sar`이 생성된다. `unsigned long`이었다면 `shr`이 나온다.
- 이처럼 어셈블리의 명령어 선택을 보면 C 변수의 signed/unsigned 타입을 추측할 수 있다.

**참고**
- `sub`가 먼저 `%rdi`(a)를 덮어쓰므로, `a - b`가 계산된 뒤에는 원래 `a` 값은 사라진다.
- `mov %rax,%rdx`로 t1을 복사하는 이유: `t1 & t2`를 계산하려면 t1이 shift 후에도 남아 있어야 하기 때문이다.

## Q8. [TF_quiz Q39] `%rax = 0x0011223344556677`에서 `movl $-1, %eax` 후 `%rax`가 `0x00000000ffffffff`이 되는 이유는?

**정답: T**

- 하위 4바이트에는 `-1`(`0xffffffff`)이 들어간다.
- 그리고 x86-64에는 **32비트 레지스터를 목적지로 쓰면 상위 32비트를 0으로 만든다**는 예외 규칙이 있다.

| 명령어               | 결과 `%rax`              | 상위 비트       |
|----------------------|--------------------------|-----------------|
| `movb $-1, %al`      | `0x00112233445566ff`     | 유지            |
| `movw $-1, %ax`      | `0x001122334455ffff`     | 유지            |
| `movl $-1, %eax`     | `0x00000000ffffffff`     | **0으로 초기화**|
| `movq $-1, %rax`     | `0xffffffffffffffff`     | 전부 덮어씀     |

**왜 32비트만 예외인가 (강의 설명)**
- 8/16비트 쓰기처럼 상위 비트를 "유지"하면, 다음 명령어가 64비트 `%rax` 전체를 쓸 때 **이전 값과 새 값을 합쳐야** 한다. → 이전 명령어에 대한 의존성(partial register dependency)이 생겨 **pipeline이 멈출(stall) 수 있다.**
- 32비트 쓰기가 상위를 0으로 만들면 결과가 **새 값만으로 완전히 결정**된다. → 의존성이 사라져 pipeline이 효율적이다.
- 32비트 연산이 여전히 가장 흔하므로(Make the Common Case Fast) 이 경우를 빠르게 만든 것이다.

**함정 포인트**
- `-1`이니까 sign extension되어 `0xffffffffffffffff`이 된다고 생각하면 틀린다. **movl은 zero**로 채운다.

## Q9. [TF_quiz Q44] `void f11(unsigned long *x, unsigned int y){ *x = y; }`가 `mov %esi,%eax`, `mov %rax,(%rdi)`로 컴파일되는 이유는?

**정답: T**

**필요한 동작**
- `unsigned int`(4바이트) → `unsigned long`(8바이트): unsigned이므로 **zero extension** 필요

**`movzlq`가 없는 이유**
- 32비트 레지스터에 쓰면 상위 32비트가 자동으로 0이 된다. → 일반 `mov`(movl)만으로 zero extension이 끝난다. (Q5 참고)

**명령어별 동작**

| 명령어             | 동작                                         |
|--------------------|----------------------------------------------|
| `mov %esi,%eax`    | y(32비트)를 `%eax`로, `%rax` 상위 32비트 = 0 |
| `mov %rax,(%rdi)`  | 8바이트 전체를 `*x`에 저장                   |

- 첫 줄이 **"논리적으로 movzlq"** 역할을 한다.

**다른 크기와 비교 (강의 f9~f12)**

| 함수  | y 타입           | 확장 명령어          |
|-------|------------------|----------------------|
| `f9`  | `unsigned char`  | `movzbl %sil,%esi`   |
| `f10` | `unsigned short` | `movzwl %si,%esi`    |
| `f11` | `unsigned int`   | `mov %esi,%eax`      |
| `f12` | `unsigned long`  | 확장 없음            |

- `f9`, `f10`도 목적지가 32비트(`%esi`)라서 상위 32비트가 0이 되므로, 바로 `mov %rsi,(%rdi)`로 8바이트를 저장할 수 있다.

**signed였다면**
- `long *x, int y` → `movslq %esi,%rsi` (`f7`) — sign extension은 상위를 1로 채울 수도 있으므로 전용 명령어가 필요하다.

## Q10. [SP 3-4 No.5 Q6] `xorq %rsi, %rdi`를 하면 결과는 `%rdi`에 저장되는데, 주석은 왜 `t1 = x ^ y`인가?

**결론: 결과는 `%rdi`에 저장되는 게 맞다. 컴파일러가 `t1`을 `%rdi`에 배치한 것이다.**

**`t1`은 메모리 공간이 아니다**
- `t1`은 C 코드의 변수 **이름**일 뿐이고, 어셈블리에는 변수가 없다.
- 컴파일러가 각 변수를 어떤 레지스터에 둘지 정한다 (**register allocation**).
- 주석 `# t1 = x ^ y`는 "이 시점부터 `%rdi`가 `t1`을 담고 있다"는 뜻이다.

**왜 `%rdi`를 재사용하나**
- `x`는 `t1`을 계산하는 데만 쓰이고 이후 다시 쓰이지 않는다.
- 그래서 `x`가 있던 `%rdi`를 덮어써 `t1`을 저장해도 된다 → 레지스터 절약

**레지스터별 의미 변화**

| 명령어                 | `%rdi` | `%rax` |
|------------------------|--------|--------|
| 시작                   | x      | ?      |
| `xorq %rsi,%rdi`       | t1     | ?      |
| `leaq (%rdx,%rdx,2)`   | t1     | 3z     |
| `salq $4,%rax`         | t1     | t2     |
| `andl $252645135,%edi` | t3     | t2     |
| `subq %rdi,%rax`       | t3     | t4     |

- `andl`도 같은 방식으로 `%rdi`(`t1`) 자리에 `t3`를 덮어쓴다.
- `t2`와 `t4`는 `%rax`를 함께 쓴다. 마지막 결과 `t4`가 `%rax`에 남으므로 그대로 반환값이 된다.
- AT&T 문법의 2-operand 연산 `op S, D`는 **D = D op S**이므로 결과는 항상 두 번째 operand에 저장된다.

## Q11. [SP 연습 문제 P25] 확장할 때 `l`(32비트 dest) 버전 대신 `q`(64비트 dest) 버전을 써도 되나?

**결론: zero extension은 둘 다 되지만, sign extension은 반드시 `q` 버전이어야 한다.**

**zero extension (`movz`) — 둘 다 OK**
- `movzwl %si,%esi`: 32비트 레지스터에 쓰면 상위 32비트가 자동으로 0 → `%rsi` 전체가 zero extension된 값
- `movzwq %si,%rsi`: 처음부터 64비트로 0을 채움 → **결과가 같다**
- 컴파일러가 `l`을 고르는 이유: 64비트 operand에 필요한 REX.W prefix가 없어 **인코딩이 1바이트 짧다**.
- 같은 이유로 `movzbl`(g2, f9) 대신 `movzbq`를 써도 결과는 같다.

**sign extension (`movs`) — `l` 버전을 쓰면 틀림**
- `y = -1` (`%si = 0xFFFF`)일 때 `long *x`에 저장하는 경우 (f6)
  - `movswq %si,%rsi` → `%rsi = 0xFFFFFFFFFFFFFFFF` = -1 (정답)
  - `movswl %si,%esi` → `%esi = 0xFFFFFFFF`이지만, 32비트 쓰기 규칙 때문에 상위 32비트는 **0** → `%rsi = 0x00000000FFFFFFFF` = 4294967295 (오답)
- 32비트 쓰기가 상위를 0으로 채우는 규칙은 zero extension과만 맞아떨어진다. 그래서 sign extension에는 64비트 dest 전용 명령어(`movswq`, `movsbq`, `movslq`)가 필요하다.
- 단, dest 자체가 `int *`(4바이트)라면 `movswl`이 정답이다 (상위 32비트는 저장되지 않으므로).

**관련:** Q5(`movzlq`가 없는 이유), Q9(f11)
