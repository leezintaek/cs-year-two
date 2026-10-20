# 중간고사 대비 모의문제 — Set 2

> 범위: A Tour of Computer Systems(1주차) ~ Control Flow(7주차)
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (C / x86-64 AT&T 어셈블리)
> 환경 가정: x86-64 Linux, gcc `-Og`, `-fwrapv`, `-fcf-protection=none`, little endian, w = 32 (int)
> 인자 `%rdi, %rsi, %rdx, %rcx, %r8, %r9` / 반환값 `%rax`
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** DRAM은 비트당 트랜지스터 6개를 사용하며 주기적인 refresh가 필요 없다.

**2.** `int x = INT_MIN;`일 때 (`-fwrapv`) `-x == x`는 참이다.

**3.** float 변수 a, b, c에 대해 `(a + b) + c == a + (b + c)`는 항상 성립한다.

**4.** AT&T 문법의 `mov %rax, %rbx`는 `%rbx`의 값을 `%rax`로 복사한다.

**5.** `gcc -Og`에서 `while` 루프는 먼저 test 부분으로 무조건 점프하는 "jump to middle" 방식으로 번역된다.

---

## Part B. 객관식

**6.** 접근 속도가 빠른 것부터 느린 것 순서로 옳게 나열한 것은?
① 레지스터 > 캐시(SRAM) > 메인 메모리(DRAM) > 디스크
② 캐시(SRAM) > 레지스터 > 메인 메모리(DRAM) > 디스크
③ 레지스터 > 메인 메모리(DRAM) > 캐시(SRAM) > 디스크
④ 캐시(SRAM) > 메인 메모리(DRAM) > 레지스터 > 디스크

**7.** 다음 코드의 출력은?
```c
unsigned char c = 200;
char d = c;
printf("%d\n", d);
```
① 200  ② −56  ③ 56  ④ −200

**8.** single precision의 bias와 정규화(normalized) 값의 E 범위로 옳은 것은?
① 127, −126 ~ 127  ② 127, −127 ~ 128  ③ 128, −127 ~ 127  ④ 1023, −1022 ~ 1023

**9.** `mov 0x8(%rdi), %rax`와 `lea 0x8(%rdi), %rax`에 대한 설명으로 옳은 것은?
① 둘 다 주소 `%rdi + 8`의 메모리를 읽는다.
② `lea`는 `%rdi + 8`이라는 값 자체를 `%rax`에 넣는다.
③ `lea`는 결과에 따라 condition code를 설정한다.
④ `mov`는 주소만 계산하고 메모리는 읽지 않는다.

**10.** `cmp %rsi, %rdi` 다음 `jg L`이 점프하는 조건은?
① `%rsi > %rdi` (signed)  ② `%rdi > %rsi` (signed)  ③ `%rdi > %rsi` (unsigned)  ④ `%rsi > %rdi` (unsigned)

**11.** 컴파일러가 conditional move(`cmov`)를 쓰기에 **부적절하지 않은** 경우는?
① then/else 양쪽 계산이 모두 매우 비싸다.
② 한쪽 계산이 NULL 포인터를 역참조할 수 있다.
③ 양쪽 계산이 모두 뺄셈 한 번이다.
④ 한쪽 계산이 전역 변수를 수정하는 부작용이 있다.

---

## Part C. 단답형

**12.** 8비트 값 `x = 0xB5`에 대해 결과를 8비트 hex로 쓰시오.
(a) `x >> 3` (logical)
(b) `x >> 3` (arithmetic)
(c) `x << 2`

**13.** −6.25를 single precision float로 표현했을 때의 비트 패턴을 hex로 쓰시오. (S, e, f 과정을 함께 쓸 것)

**14.** 다음 각 변수의 값을 10진수로 쓰시오.
```c
short s = -1;
unsigned short us = (unsigned short) s;   // (a)
int i = s;                                // (b)
unsigned int ui = s;                      // (c)
int x = 70000;
short t = (short) x;                      // (d)
```

**15.** 아래 어셈블리를 보고 원래 C 함수 `long f(long x, long y)`를 쓰시오.
```
f:                              # x in %rdi, y in %rsi
    cmp   %rsi, %rdi
    jge   .L2
    lea   (%rsi,%rsi,2), %rax
    ret
.L2:
    mov   %rdi, %rax
    sub   %rsi, %rax
    ret
```

**16.** 초기값: `%rax = 0x100`, `%rcx = 0x2`, 메모리 `0x100 = 0x10`, `0x108 = 0x20`, `0x110 = 0x30` (각 8바이트). 각 명령어는 **독립적으로** 실행된다. 바뀌는 레지스터 또는 메모리 주소와 그 값을 쓰시오.
(a) `addq %rcx, 8(%rax)`
(b) `subq (%rax), %rcx`
(c) `imulq $3, (%rax,%rcx,8)`
(d) `leaq 8(%rax,%rcx,4), %rdx`

---

## Part D. 빈칸 채우기 손코딩

**17.** 현재 머신이 little endian이면 1을 반환하는 함수를 완성하시오.
```c
int is_little_endian(void) {
    int x = 1;
    unsigned char *p = ____(a)____;
    return ____(b)____;
}
```

**18.** 1인 비트의 개수를 세는 함수를 `gcc -Og`로 컴파일한 결과의 빈칸을 채우시오.
```c
long count(unsigned long x) {
    long c = 0;
    while (x != 0) {
        c += x & 1;
        x >>= 1;
    }
    return c;
}
```
```
count:                          # x in %rdi
    mov   $0x0, %eax
    jmp   .L2
.L3:
    mov   %rdi, %rdx
    and   $0x1, %edx
    add   %rdx, %rax
    ____(a)____ %rdi            # x >>= 1
.L2:
    ____(b)____ %rdi, %rdi
    ____(c)____ .L3
    ret
```

**19.** 각 C 함수에 대응하는 확장 명령어를 쓰시오. (한 줄 + `ret`)
```c
long          f1(short x)         { return x; }   // ____(a)____ %di, %rax
unsigned long f2(unsigned char c) { return c; }   // ____(b)____ %dil, %eax
long          f3(int i)           { return i; }   // ____(c)____ %edi, %rax
```

**20.** `x * 40`을 곱셈 명령어 없이 계산하는 어셈블리를 완성하시오.
```c
long mul40(long x) { return x * 40; }
```
```
mul40:                          # x in %rdi
    lea   ____(a)____, %rax     # rax = 5x
    ____(b)____ $3, %rax        # rax = 40x
    ret
```

---
---

## 정답 및 해설

**1. X** — 비트당 6 트랜지스터, refresh 불필요는 **SRAM**의 특징이다. DRAM은 트랜지스터 1개 + 커패시터, 주기적 refresh가 필요하다.

**2. O** — 2의 보수 범위가 비대칭이라 TMin의 음수는 표현할 수 없어서 다시 TMin이 된다. (`~x + 1`도 TMin)

**3. X** — 부동소수점 연산은 결합법칙이 성립하지 않는다. 예: `(3.14f + 1e20) - 1e20 = 0`, `3.14f + (1e20 - 1e20) = 3.14`.

**4. X** — AT&T는 `mov src, dst`이다. `%rax`의 값을 `%rbx`로 복사한다.

**5. O** — while은 body를 한 번도 실행하지 않을 수 있으므로 먼저 test로 `jmp`한다. do-while 구조 맨 앞에 `jmp` 하나가 추가된 형태.

**6. ①** — 레지스터(CPU 내부) > SRAM 캐시(~2ns) > DRAM(~15ns) > 디스크(~7ms).

**7. ②** — 200 = `0xC8`. 비트는 그대로 두고 signed char로 재해석하면 200 − 256 = **−56**. printf로 넘길 때 int로 sign-extend 되어 −56이 출력된다.

**8. ①** — bias = 2^(8−1) − 1 = 127. e는 1 ~ 254 (0과 255는 예약)이므로 E = e − 127 은 −126 ~ 127.

**9. ②** — `lea`는 유효 주소를 계산만 하고 메모리를 읽지 않는다. 플래그도 바꾸지 않는다.

**10. ②** — `cmp %rsi,%rdi`는 `%rdi − %rsi`. `jg`는 signed greater이므로 `%rdi > %rsi`.

**11. ③** — 계산이 단순하고 안전하면 양쪽을 다 계산해도 손해가 없으니 cmov가 유리하다. ①은 비싼 계산, ②④는 위험한 계산(부작용, segfault)이라 cmov를 쓰면 안 된다.

**12.** `x = 1011 0101`
(a) `0x16` — `0001 0110` (왼쪽을 0으로 채움)
(b) `0xF6` — `1111 0110` (MSB 1을 복제)
(c) `0xD4` — `1101 0100` (밀려난 상위 비트는 버림)

**13. `0xC0C80000`**
6.25 = 110.01(2) = 1.1001(2) × 2²
S = 1, e = 2 + 127 = 129 = `10000001`, f = `1001000…0`
`1 10000001 10010000000000000000000` = `1100 0000 1100 1000 0000 …` = `0xC0C80000`

**14.**
(a) **65535** — 비트 `0xFFFF`를 unsigned로 재해석
(b) **−1** — sign extension은 값을 보존한다
(c) **4294967295** — 먼저 32비트로 sign-extend(`0xFFFFFFFF`)한 뒤 unsigned로 해석
(d) **4464** — 70000 = `0x00011170`, 하위 16비트 `0x1170` = 4464 (truncation)

**15.**
```c
long f(long x, long y) {
    if (x < y)
        return 3 * y;
    return x - y;
}
```
`jge .L2`는 조건이 거짓일 때(x ≥ y) body를 건너뛰는 점프이므로 원래 조건은 `x < y`. `lea (%rsi,%rsi,2)` = 3y.

**16.**
(a) 메모리 `0x108` = 0x20 + 2 = **0x22**
(b) `%rcx` = 2 − 0x10 = −14 = **`0xfffffffffffffff2`** (`sub S, D`는 D − S)
(c) 주소 0x100 + 2×8 = `0x110`: 0x30 × 3 = **0x90**
(d) `%rdx` = 0x100 + 2×4 + 8 = **0x110** (메모리 접근 없음)

**17.** (a) `(unsigned char *) &x`  (b) `p[0] == 1` (또는 `*p`)
little endian이면 가장 낮은 주소에 LSB(`0x01`)가 저장된다.

**18.** (a) `shr` — unsigned이므로 logical shift (`shr $1, %rdi`와 같음)  (b) `test`  (c) `jne`
`test %rdi,%rdi`로 x가 0인지 ZF에 반영하고, 0이 아니면 body로 돌아간다.

**19.** (a) `movswq` — signed short → long  (b) `movzbl` — unsigned char, 32비트 쓰기가 상위도 0으로 만들어 `movzbq`와 같다  (c) `movslq` (`cltq`도 가능하지만 `cltq`는 `%eax → %rax` 전용이라 여기서는 `movslq`)

**20.** (a) `(%rdi,%rdi,4)`  (b) `shl` (또는 `sal`)
5x × 8 = 40x. `lea`로 x + 4x를 한 번에 계산하고 왼쪽 시프트 3으로 ×8.
