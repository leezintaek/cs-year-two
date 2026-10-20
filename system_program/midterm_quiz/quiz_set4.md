# 중간고사 대비 모의문제 — Set 4

> 범위: A Tour of Computer Systems(1주차) ~ Control Flow(7주차)
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (C / x86-64 AT&T 어셈블리)
> 환경 가정: x86-64 Linux, gcc `-Og`, `-fwrapv`, `-fcf-protection=none`, little endian, w = 32 (int)
> 인자 `%rdi, %rsi, %rdx, %rcx, %r8, %r9` / 반환값 `%rax`
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** 오브젝트 파일의 심볼 테이블은 링킹 단계에서 링커가 처음 만든다.

**2.** unsigned 덧셈 `s = x + y`에서 `s < x`이면 오버플로우가 발생한 것이다.

**3.** double precision의 bias는 1023이다.

**4.** 컴파일러가 `movzbq` 대신 `movzbl`을 자주 쓰는 이유는 두 명령어의 결과가 서로 다르기 때문이다.

**5.** `setX` 명령어는 목적지 레지스터 8바이트 전체를 0 또는 1로 설정한다.

---

## Part B. 객관식

**6.** 셸에서 `./hello`를 입력했을 때 일어나는 일로 옳은 것은?
① `hello`는 셸의 내장(built-in) 명령으로 처리된다.
② 실행 파일이 디스크에서 메인 메모리로 적재된 뒤 CPU가 `main`의 기계어를 실행한다.
③ CPU가 디스크에 있는 기계어를 직접 읽어 실행한다.
④ 셸이 `hello.c`를 컴파일한 뒤 실행한다.

**7.** `int x = INT_MIN;` (`-fwrapv`)에 대한 설명으로 **옳지 않은** 것은?
① `x - 1 > 0`은 참이다.
② `-x < 0`은 참이다.
③ `x * 2 == 0`은 참이다.
④ `~x + 1 == INT_MAX`는 참이다.

**8.** `(int)(-2.7) + (int)(2.7)`의 값은?
① −1  ② 0  ③ 1  ④ 정의되지 않음

**9.** `%rdx = 0x1000`, `%rcx = 0x3`일 때 `movq 0x8(%rdx,%rcx,8), %rax`가 읽는 메모리 주소는?
① `0x1020`  ② `0x1018`  ③ `0x100b`  ④ `0x1023`

**10.** `unsigned int u;`에 대해 `u >> 2`를 계산할 때 컴파일러가 사용하는 명령어는?
① `sar`  ② `shr`  ③ `sal`  ④ `shl`

**11.** `cmp b, a` 실행 후 signed 비교 `a < b`를 판단하는 플래그 조합은?
① `SF`  ② `SF ^ OF`  ③ `CF`  ④ `CF | ZF`

---

## Part C. 단답형

**12.**
(a) `0xA7`을 2진수, unsigned 10진수, 8비트 signed 10진수로 각각 쓰시오.
(b) (a)의 signed 값을 16비트 2의 보수로 나타낸 hex는?

**13.** fraction이 3비트인 부동소수점에서 다음 덧셈을 수행하시오. (round-to-even)
(1.011)₂ × 2⁰ + (1.011)₂ × 2⁻²
(a) 지수를 맞춘 뒤 가수 덧셈 결과(반올림 전)를 쓰시오.
(b) 반올림한 최종 결과를 2진 과학적 표기와 10진수로 쓰시오.

**14.** `char c = 0xF0;`일 때 각 변수 값을 hex와 10진수로 쓰시오.
```c
int i = c;                          // (a)
unsigned int u = c;                 // (b)
unsigned int v = (unsigned char) c; // (c)
```

**15.** 아래 어셈블리에 대해 답하시오.
```
f:                              # x in %rdi (unsigned long)
    mov   $0x0, %eax
.L2:
    add   %rdi, %rax
    shr   %rdi
    test  %rdi, %rdi
    jne   .L2
    ret
```
(a) 원래 C 함수를 `do-while`을 써서 쓰시오.
(b) `f(13)`의 반환값은?

**16.** `cmpq %rsi, %rdi` 실행 후 CF, ZF, SF, OF를 쓰고, `jl`, `jg`, `jb`, `ja` 중 점프하는 것을 모두 고르시오.
(a) `%rdi = 1`, `%rsi = 2`
(b) `%rdi = -1`, `%rsi = 1`

---

## Part D. 빈칸 채우기 손코딩

**17.** float의 비트에서 S, e, f 필드를 꺼내는 코드를 완성하시오.
```c
float f = -14.5f;
unsigned u = *(unsigned *) &f;
unsigned s    = u >> ____(a)____;
unsigned e    = (u >> 23) & ____(b)____;
unsigned frac = u & ____(c)____;
```

**18.** 아래 함수를 `gcc -O1`로 컴파일한 결과의 빈칸을 채우시오.
```c
long gt100(long x) { return x > 100; }
```
```
gt100:                          # x in %rdi
    cmp   ____(a)____, %rdi
    ____(b)____ %al
    ____(c)____ %al, %eax
    ret
```

**19.** 음수 원소의 개수를 세는 함수를 `gcc -Og`로 컴파일한 결과의 빈칸을 채우시오.
```c
long cnt_neg(long a[], long n) {
    long c = 0;
    for (long i = 0; i < n; i++)
        if (a[i] < 0) c++;
    return c;
}
```
```
cnt_neg:                        # a in %rdi, n in %rsi
    mov   $0x0, %eax            # c
    mov   $0x0, %edx            # i
    jmp   .L2
.L4:
    cmpq  $0x0, ____(a)____     # a[i] - 0
    ____(b)____ .L3
    add   $0x1, %rax
.L3:
    add   $0x1, %rdx
.L2:
    cmp   %rsi, %rdx
    ____(c)____ .L4
    ret
```

**20.** 아래 C 함수의 어셈블리 빈칸을 채우시오.
```c
long arith2(long x, long y, long z) {
    long t1 = x + y;
    long t2 = z * 24;
    long t3 = t1 >> 4;
    return t2 - t3;
}
```
```
arith2:                         # x in %rdi, y in %rsi, z in %rdx
    add   %rsi, %rdi            # t1 = x + y
    lea   ____(a)____, %rax     # 3z
    ____(b)____ $3, %rax        # t2 = 24z
    ____(c)____ $4, %rdi        # t3 = t1 >> 4
    sub   %rdi, %rax
    ret
```

---
---

## 정답 및 해설

**1. X** — 심볼 테이블은 **어셈블러**가 `.o`를 만들 때 생성하고, 링커는 이를 사용한다.

**2. O** — 오버플로우가 나면 true sum에서 2^w가 빠지므로 결과가 피연산자보다 작아진다.

**3. O** — 지수 11비트 → bias = 2¹⁰ − 1 = 1023.

**4. X** — 32비트 쓰기가 상위 32비트를 0으로 만들기 때문에 결과는 **같다**. `movzbl`이 인코딩이 더 짧아서 쓴다.

**5. X** — `setX`는 목적지 **1바이트**만 설정한다. 그래서 더 큰 타입으로 반환하려면 `movzbl`이 필요하다.

**6. ②** — `hello`는 built-in이 아니므로 외부 명령으로 보고 디스크에서 메모리로 적재한다. CPU는 메모리에 있는 명령어를 실행한다.

**7. ④**
① `INT_MIN - 1` = `INT_MAX` > 0 → 참
② `-INT_MIN` = `INT_MIN` < 0 → 참
③ `2 * INT_MIN` = 2³² mod 2³² = 0 → 참
④ `~x + 1` = `-x` = `INT_MIN` ≠ `INT_MAX` → 거짓

**8. ②** — float → int는 0 방향으로 버림: −2.7 → −2, 2.7 → 2. 합은 0.

**9. ①** — 0x1000 + 3×8 + 0x8 = 0x1000 + 0x18 + 0x8 = `0x1020`.

**10. ②** — unsigned 오른쪽 시프트는 logical(`shr`, 0 채움). signed는 `sar`.

**11. ②** — 오버플로우가 없으면 SF로 충분하지만, 오버플로우가 나면 부호가 뒤집히므로 `SF ^ OF`로 판단한다.

**12.**
(a) `1010 0111`, unsigned **167**, signed **−89** (167 − 256)
(b) **`0xFFA7`** — sign extension으로 상위 바이트를 1로 채운다.

**13.**
(a) (1.011)₂ × 2⁻² = (0.01011)₂ × 2⁰ 으로 맞춘 뒤
1.01100 + 0.01011 = **(1.10111)₂ × 2⁰**
(b) 3비트 남기기: `1.101 | 11` → 버리는 부분 `11`이 절반(`10`)보다 크므로 올림 → **(1.110)₂ × 2⁰ = 1.75**
(확인: 1.375 + 0.34375 = 1.71875 → 1.75로 반올림)

**14.**
(a) `0xFFFFFFF0` = **−16** — signed char는 sign extension
(b) `0xFFFFFFF0` = **4294967280** — 먼저 sign extension 후 unsigned로 해석
(c) `0x000000F0` = **240** — unsigned char로 먼저 바꾸면 zero extension

**15.**
(a)
```c
long f(unsigned long x) {
    long r = 0;
    do {
        r += x;
        x >>= 1;
    } while (x != 0);
    return r;
}
```
(b) **23** — 13 → 6 → 3 → 1 → 0 이므로 13 + 6 + 3 + 1 = 23

**16.** `cmpq %rsi,%rdi`는 `%rdi − %rsi`를 계산한다.
(a) 1 − 2 = −1 → CF = **1** (unsigned 1 < 2, borrow), ZF = **0**, SF = **1**, OF = **0**
점프: **`jl`, `jb`** (signed로도 unsigned로도 1 < 2)
(b) −1 − 1 = −2 → CF = **0** (unsigned로 `0xFFFF…FF` > 1 이라 borrow 없음), ZF = **0**, SF = **1**, OF = **0**
점프: **`jl`, `ja`** (signed로는 −1 < 1, unsigned로는 UMAX > 1)

**17.** (a) `31`  (b) `0xFF`  (c) `0x7FFFFF`
부호 1비트(31번), 지수 8비트(30~23번), fraction 23비트(22~0번). −14.5f → s = 1, e = 130, frac = `0x680000`.

**18.** (a) `$0x64`  (b) `setg`  (c) `movzbl`
`-O1`에서는 분기 대신 `setg`로 0/1을 만들고, 1바이트 결과를 long으로 반환하기 위해 zero-extend 한다.

**19.** (a) `(%rdi,%rdx,8)`  (b) `jge`  (c) `jl`
`a[i] < 0`이 거짓(a[i] ≥ 0)이면 `c++`를 건너뛰므로 `jge`. 루프 조건 `i < n`은 `jl`.

**20.** (a) `(%rdx,%rdx,2)`  (b) `shl` (또는 `sal`)  (c) `sar`
3z × 8 = 24z. `t1`은 signed long이므로 오른쪽 시프트는 산술 시프트 `sar`.
