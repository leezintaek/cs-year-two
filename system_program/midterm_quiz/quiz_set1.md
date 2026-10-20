# 중간고사 대비 모의문제 — Set 1

> 범위: A Tour of Computer Systems(1주차) ~ Control Flow(7주차)
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (C / x86-64 AT&T 어셈블리)
> 환경 가정: x86-64 Linux, gcc `-Og`, `-fwrapv`, `-fcf-protection=none`, little endian, w = 32 (int)
> 인자 `%rdi, %rsi, %rdx, %rcx, %r8, %r9` / 반환값 `%rax`
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** 어셈블러(`as`)가 만든 `hello.o`는 기계어로 되어 있으므로 그 자체로 실행할 수 있다.

**2.** w = 32일 때 C 식 `-1 < 0U`의 결과는 1(참)이다.

**3.** IEEE 754에서 지수 필드 e가 모두 0이면 E = 1 − bias, M = f 로 해석한다.

**4.** `leaq` 명령어는 계산 결과에 따라 ZF, SF 등의 condition code를 갱신한다.

**5.** `movl $-1, %eax`를 실행하면 `%rax`의 상위 32비트는 이전 값을 그대로 유지한다.

---

## Part B. 객관식

**6.** `#include <stdio.h>`를 처리하는 컴파일 단계와 그 단계의 결과 파일로 옳은 것은?
① 컴파일러, `hello.s`  ② 전처리기, `hello.i`  ③ 어셈블러, `hello.o`  ④ 링커, `hello`

**7.** 8비트 2의 보수에서 −20의 비트 패턴은?
① `0x94`  ② `0xEB`  ③ `0xEC`  ④ `0x14`

**8.** 다음 중 single precision float로 **정확하게 표현할 수 없는** 값은?
① 0.5  ② 0.75  ③ 0.1  ④ 3.25

**9.** `%rdx = 0xf000`, `%rcx = 0x100`일 때 `leaq 0x10(%rdx,%rcx,8), %rax` 실행 후 `%rax`는?
① `0xf110`  ② `0xf810`  ③ `0xf808`  ④ 주소 `0xf810`에 저장된 값

**10.** `cmp %rsi, %rdi` 다음에 **unsigned** 비교로 `%rdi < %rsi`일 때 점프하려면 어떤 명령어를 써야 하는가?
① `jl`  ② `jb`  ③ `jg`  ④ `ja`

**11.** 다음 중 x86-64에 **존재하지 않는** 명령어는?
① `movzbq`  ② `movslq`  ③ `movzlq`  ④ `movsbw`

---

## Part C. 단답형

**12.** `int x = 0x12345678;`이 주소 `0x200`에 저장되어 있다.
(a) little endian 머신에서 `0x200 ~ 0x203`의 바이트를 순서대로 쓰시오.
(b) big endian 머신에서 `0x200 ~ 0x203`의 바이트를 순서대로 쓰시오.

**13.** single precision float의 비트 패턴이 `0xC1680000`이다. 이 값을 10진수로 쓰시오. (S, e, E, M을 함께 쓸 것)

**14.** 메모리 `0x300 ~ 0x307`에 바이트 `f0 81 22 33 44 55 66 77`이 저장되어 있고, `%rax = 0x0123456789abcdef`이다. 각 명령어는 **독립적으로** 실행된다. 실행 후 `%rax`를 16자리 hex로 쓰시오.
(a) `movzbl 0x301, %eax`
(b) `movsbw 0x301, %ax`
(c) `movw 0x300, %ax`
(d) `movslq 0x300, %rax`

**15.** 아래는 `long f(long x, long y)`를 컴파일한 결과이다.
```
f:                              # x in %rdi, y in %rsi
    lea   (%rdi,%rdi,4), %rax
    lea   (%rsi,%rax,2), %rax
    sar   $3, %rax
    ret
```
(a) 함수 본문을 C 한 줄(`return ...;`)로 쓰시오.
(b) `f(-3, 5)`의 반환값은?

**16.** 8비트 연산 후 CF, ZF, SF, OF 값을 각각 쓰시오.
(a) `%al = 0x90`, `%bl = 0xA0` 에서 `addb %bl, %al`
(b) `%al = 0x00` 에서 `cmpb $0x01, %al`

---

## Part D. 빈칸 채우기 손코딩

**17.** 두 int의 덧셈이 오버플로우 없이 가능한지 검사하는 함수를 완성하시오. (모든 경우에 정확하도록)
```c
int tadd_ok(int x, int y) {
    int sum = x + y;
    int neg_over = x < 0 && y < 0 && ____(a)____;
    int pos_over = x > 0 && y > 0 && ____(b)____;
    return !neg_over && !pos_over;
}
```

**18.** 아래 C 함수를 `gcc -Og`로 컴파일한 결과의 빈칸을 채우시오.
```c
long sum_arr(int arr[], long n) {
    long s = 0;
    for (long i = 0; i < n; i++)
        s += arr[i];
    return s;
}
```
```
sum_arr:                        # arr in %rdi, n in %rsi
    mov   $0x0, %eax            # s = 0
    mov   $0x0, %edx            # i = 0
    jmp   .L2
.L3:
    movslq ____(a)____, %rcx    # arr[i]
    add   %rcx, %rax
    add   $0x1, %rdx
.L2:
    cmp   ____(b)____           # i - n
    ____(c)____ .L3
    ret
```

**19.** 아래 C 함수의 어셈블리 빈칸을 채우시오.
```c
int lt(unsigned long a, unsigned long b) { return a < b; }
```
```
lt:                             # a in %rdi, b in %rsi
    cmp   ____(a)____
    ____(b)____ %al
    ____(c)____ %al, %eax
    ret
```

**20.** 두 int의 곱셈이 오버플로우 없이 가능한지 검사하는 함수를 완성하시오.
```c
#include <stdint.h>
int tmult_ok(int x, int y) {
    int64_t pll = ____(a)____;
    return pll == ____(b)____;
}
```

---
---

## 정답 및 해설

**1. X** — 오브젝트 파일은 다른 파일·라이브러리의 함수(예: `printf`) 참조를 포함하므로 완전한 프로그램이 아니다. 링커가 심볼 해결과 재배치를 해야 실행 파일(ELF)이 된다.

**2. X** — signed와 unsigned가 섞이면 signed가 unsigned로 바뀐다. `-1` → `4294967295U`이므로 `4294967295 < 0`은 거짓(0).

**3. O** — 비정규화(denormalized) 형태: hidden bit가 없어서 M = f, 지수는 0 − bias가 아니라 1 − bias.

**4. X** — `lea`는 주소 계산 전용이라 플래그를 건드리지 않는다.

**5. X** — 목적지가 레지스터인 32비트 연산은 상위 32비트를 0으로 만든다. 결과: `0x00000000ffffffff`.

**6. ②** — 전처리기(`cpp`)가 `#` 지시문을 처리해 `hello.i`(텍스트)를 만든다.

**7. ③** — 20 = `00010100` → 비트 반전 `11101011` → +1 → `11101100` = `0xEC`.
① `0x94`는 sign-magnitude 표현, ② `0xEB`는 1의 보수(+1 빠뜨림).

**8. ③** — 0.1 = 0.0001100110011…(2)로 무한히 반복된다. x/2ᵏ 꼴만 정확하게 표현된다. (0.5 = 1/2, 0.75 = 3/4, 3.25 = 13/4)

**9. ②** — 0xf000 + 0x100×8 + 0x10 = 0xf000 + 0x800 + 0x10 = `0xf810`. `lea`는 메모리를 읽지 않으므로 ④는 틀렸다(④는 `mov`의 동작).

**10. ②** — `cmp %rsi,%rdi`는 `%rdi − %rsi`를 계산한다. unsigned "below"는 `jb`(CF). `jl`은 signed.

**11. ③** — `movl`이 이미 상위 32비트를 0으로 만들기 때문에 `movzlq`는 필요 없어서 존재하지 않는다.

**12.** (a) `78 56 34 12` (LSB가 낮은 주소)  (b) `12 34 56 78` (MSB가 낮은 주소)

**13. −14.5**
`0xC1680000` = `1 10000010 11010000000000000000000`
S = 1, e = 130 → E = 130 − 127 = 3, M = 1.1101(2)
값 = −1.1101(2) × 2³ = −1110.1(2) = **−14.5**

**14.**
(a) `0x0000000000000081` — `0x81`을 zero-extend. 32비트 목적지라 상위 32비트도 0.
(b) `0x0123456789abff81` — `0x81`(MSB = 1)을 16비트로 sign-extend → `0xff81`. 하위 2바이트만 바뀐다.
(c) `0x0123456789ab81f0` — `0x300`=`f0`, `0x301`=`81` → little endian으로 `0x81f0`.
(d) `0x00000000332281f0` — 4바이트 `f0 81 22 33` → `0x332281f0`. MSB(0x33의 최상위 비트)가 0이라 상위는 0으로 채워진다.

**15.** (a) `return (10*x + y) >> 3;`
- 첫 `lea`: rax = x + 4x = 5x
- 둘째 `lea`: rax = y + 2·(5x) = 10x + y
- `sar`: 산술 시프트이므로 signed `>>`

(b) **−4** — 10·(−3) + 5 = −25. −25 >> 3 은 산술 시프트라 내림(floor)이 되어 ⌊−3.125⌋ = −4. (0 방향 나눗셈 −3이 아니다.)

**16.**
(a) 0x90 + 0xA0 = 0x130 → 결과 `0x30`
CF = **1** (MSB에서 carry 발생), ZF = **0**, SF = **0**, OF = **1** (음수 + 음수 = 양수, −112 + −96 = −208은 8비트 범위 밖)
(b) 0x00 − 0x01 = `0xFF`
CF = **1** (borrow 발생, unsigned 0 < 1), ZF = **0**, SF = **1**, OF = **0** (0 − 1 = −1은 정상 범위)

**17.** (a) `sum >= 0`  (b) `sum < 0`
강의 코드는 `sum > 0`으로 되어 있지만 TMin + TMin = 0 이 되는 경우가 있어서 `>= 0`이어야 모든 음의 오버플로우를 잡는다. 양의 오버플로우 결과는 0이 될 수 없다(최대 합 2·TMax = −2 로 wrap).

**18.** (a) `(%rdi,%rdx,4)` — int 원소라 scale 4  (b) `%rsi,%rdx` — `i − n` 계산  (c) `jl` — signed long 비교 `i < n`
int를 long `s`에 더하므로 `movslq`로 sign-extend 한다.

**19.** (a) `%rsi,%rdi` (a − b 계산)  (b) `setb` (unsigned below, CF)  (c) `movzbl`
`setX`는 1바이트만 쓰므로 int로 반환하려면 zero-extend가 필요하다.

**20.** (a) `(int64_t) x * y`  (b) `(int) pll`
`(int64_t)(x * y)`나 그냥 `x * y`로 쓰면 곱셈이 32비트에서 먼저 일어나 오버플로우된 뒤 확장되므로 검사가 안 된다. 캐스팅 위치가 핵심.
