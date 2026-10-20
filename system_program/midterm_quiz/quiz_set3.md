# 중간고사 대비 모의문제 — Set 3

> 범위: A Tour of Computer Systems(1주차) ~ Control Flow(7주차)
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (C / x86-64 AT&T 어셈블리)
> 환경 가정: x86-64 Linux, gcc `-Og`, `-fwrapv`, `-fcf-protection=none`, little endian, w = 32 (int)
> 인자 `%rdi, %rsi, %rdx, %rcx, %r8, %r9` / 반환값 `%rax`
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** 링커의 두 가지 주요 작업은 심볼 해결(symbol resolution)과 재배치(relocation)이다.

**2.** C에서 signed와 unsigned가 한 비교식에 섞이면 unsigned 값이 signed로 변환된 뒤 비교된다.

**3.** IEEE 754에서 지수 필드가 모두 1이고 fraction이 0이 아니면 NaN이다.

**4.** x86-64의 scaled indexed addressing `Imm(rb, ri, s)`에서 s는 1, 2, 4, 8, 16 중 하나일 수 있다.

**5.** `test %rsi, %rdi`는 `%rdi & %rsi`를 계산해 그 결과를 `%rdi`에 저장한다.

---

## Part B. 객관식

**6.** 2048×2048 배열을 복사할 때 `for(i) for(j)` 순서가 `for(j) for(i)` 순서보다 약 19배 빨랐다. 가장 큰 원인은?
① C 배열은 행 우선으로 저장되어 연속 접근이 캐시를 잘 활용한다.
② `for(i)` 순서가 분기 예측을 더 잘 맞춘다.
③ `for(j)` 순서는 매번 디스크에 접근한다.
④ `for(i)` 순서가 레지스터를 더 많이 사용한다.

**7.** w = 32일 때 결과가 1(참)인 식은?
① `-1 < 0U`
② `2147483647 > -2147483647-1`
③ `2147483647U > -2147483647-1`
④ `(unsigned)-1 < -2`

**8.** 이진수 `10.01100`을 round-to-even으로 소수점 아래 2자리까지 반올림한 결과는?
① `10.01`  ② `10.10`  ③ `10.11`  ④ `11.00`

**9.** 다음 중 **잘못된(인코딩할 수 없는)** 명령어는?
① `movq $0x10, (%rax)`  ② `movq (%rax), (%rbx)`  ③ `movb %al, (%rsp)`  ④ `movl %eax, %ebx`

**10.** `movabsq`에 대한 설명으로 옳은 것은?
① 목적지로 메모리를 쓸 수 있다.
② 64비트 immediate를 레지스터에 넣을 때 사용한다.
③ 32비트 immediate를 64비트로 sign-extend 한다.
④ source로 메모리 주소를 쓸 수 있다.

**11.** 같은 조건의 `do-while`과 `while` 루프를 `gcc -Og`로 번역했을 때의 차이로 옳은 것은?
① `while`은 맨 앞에 test로 가는 무조건 `jmp`가 하나 더 있다.
② `do-while`은 test가 body보다 먼저 나온다.
③ `while`은 조건 점프 대신 `cmov`를 사용한다.
④ 둘은 항상 완전히 같은 어셈블리가 된다.

---

## Part C. 단답형

**12.** 8비트 2의 보수 덧셈 결과를 hex와 10진수로 쓰고, 오버플로우 종류(양의 / 음의 / 없음)를 쓰시오.
(a) `0x70 + 0x30`
(b) `0x90 + 0x88`

**13.** single precision float에 대해 답하시오.
(a) 15.75의 비트 패턴을 hex로 쓰시오.
(b) 가장 작은 양의 비정규화(denormalized) 값을 2의 거듭제곱으로 쓰시오.

**14.** 메모리 `0x200 ~ 0x207`에 바이트 `98 ba dc fe 10 32 54 76`이 있고, `%rax = 0x0123456789abcdef`이다. 각 명령어는 **독립적으로** 실행된다. 실행 후 `%rax`를 16자리 hex로 쓰시오.
(a) `movb 0x203, %al`
(b) `movswq 0x206, %rax`
(c) `movzbw 0x200, %ax`
(d) `movl 0x204, %eax`

**15.** 아래는 `long f(long n)`의 어셈블리이다.
```
f:                              # n in %rdi
    mov   $0x1, %eax
    jmp   .L2
.L3:
    imul  %rdi, %rax
    sub   $0x1, %rdi
.L2:
    cmp   $0x1, %rdi
    jg    .L3
    ret
```
(a) 원래 C 함수를 `while`을 써서 쓰시오.
(b) `f(5)`의 반환값은?

**16.** 초기값: `%rax = 0x100`, `%rbx = 0x1111111111110010`, 메모리 `0x200 ~ 0x207`은 14번과 같다. 각 명령어는 **독립적으로** 실행된다. 실행 후 `%rbx`를 16자리 hex로 쓰시오.
(a) `addw 0x204, %bx`
(b) `addl 0x204, %ebx`
(c) `xorq %rbx, %rbx`
(d) `leaq (%rbx,%rax,4), %rbx`

---

## Part D. 빈칸 채우기 손코딩

**17.** 실행 결과가 주석과 같도록 빈칸을 채우시오. (비트 연산만 사용)
```c
int x = -5;
printf("%____(a)____\n", x);    // 출력: 0xfffffffb
int y = ____(b)____ + 1;        // y == 5
```

**18.** 아래 C 함수를 `gcc -Og`로 컴파일한 결과의 빈칸을 채우시오.
```c
long absdiff(long x, long y) {
    long r;
    if (x < y) r = y - x;
    else       r = x - y;
    return r;
}
```
```
absdiff:                        # x in %rdi, y in %rsi
    cmp   %rsi, %rdi
    ____(a)____ .L2
    mov   %rsi, %rax
    sub   %rdi, %rax
    ret
.L2:
    mov   %rdi, %rax
    ____(b)____ %rsi, %rax
    ret
```

**19.** 18번 함수를 `gcc -O1`로 컴파일하면 분기 없이 conditional move를 쓴다. 빈칸을 채우시오.
```
absdiff:                        # x in %rdi, y in %rsi
    mov   %rsi, %rax
    sub   %rdi, %rax            # rax = y - x
    mov   %rdi, %rdx
    sub   %rsi, %rdx            # rdx = x - y
    cmp   %rsi, %rdi
    ____(a)____ %rdx, %rax
    ret
```

**20.** 각 C 함수의 어셈블리 빈칸을 채우시오. (`a` in `%rdi`, `i` in `%rsi`)
```c
int  *p(int a[], long i) { return &a[i]; }   // ____(a)____ (%rdi,%rsi,4), %rax
long  g(int a[], long i) { return a[i]; }    // ____(b)____ ____(c)____, %rax
```

---
---

## 정답 및 해설

**1. O** — 심볼 해결: 외부 참조(예: `printf`)를 실제 정의와 연결. 재배치: 주소를 조정해 하나로 결합.

**2. X** — 반대다. signed가 **unsigned로** 암묵적 변환된다.

**3. O** — e = 모두 1일 때 f = 0이면 ±∞, f ≠ 0이면 NaN.

**4. X** — s는 1, 2, 4, 8만 가능하다 (char, short, int, long/포인터 크기).

**5. X** — `test`는 AND 결과로 플래그(ZF, SF)만 설정하고 결과는 저장하지 않는다. 저장하는 것은 `and`.

**6. ①** — 행 우선 순회는 메모리를 연속으로 접근해 캐시 locality가 좋다. 열 우선은 매번 2048×원소크기만큼 떨어진 곳을 접근해 캐시 미스가 많다.

**7. ②**
① `-1` → UMAX, `UMAX < 0` 거짓
② 둘 다 signed: TMax > TMin 참
③ unsigned 비교: `0x7FFFFFFF > 0x80000000` 거짓
④ 둘 다 unsigned: `0xFFFFFFFF < 0xFFFFFFFE` 거짓

**8. ②** — 남길 부분 `10.01`, 버릴 부분 `100` = 정확히 절반(halfway). 최하위 비트가 1(홀수)이므로 올려서 짝수로 → `10.10`.

**9. ②** — 메모리 → 메모리 이동은 한 명령어로 불가능하다. 레지스터를 거쳐야 한다.

**10. ②** — `movabsq`는 64비트 immediate를 source로, 레지스터만 목적지로 쓴다. ③은 일반 `movq`의 동작.

**11. ①** — while = jump to middle. do-while 구조 앞에 `jmp test`만 추가된다.

**12.**
(a) `0xA0` = **−96**, **양의 오버플로우** (112 + 48 = 160 > 127 → 160 − 256 = −96)
(b) `0x18` = **24**, **음의 오버플로우** (−112 + −120 = −232 < −128 → −232 + 256 = 24)

**13.**
(a) **`0x417C0000`** — 15.75 = 1111.11(2) = 1.11111(2) × 2³
S = 0, e = 3 + 127 = 130 = `10000010`, f = `1111100…0`
`0 10000010 11111000000000000000000` = `0100 0001 0111 1100 0000 …`
(b) **2⁻¹⁴⁹** — 비정규화 값 = f × 2^(1−127) = f × 2⁻¹²⁶. f의 최소값은 2⁻²³ (마지막 비트만 1) → 2⁻²³ × 2⁻¹²⁶ = 2⁻¹⁴⁹.

**14.**
(a) `0x0123456789abcdfe` — `0x203` = `fe`, 하위 1바이트만 바뀐다.
(b) `0x0000000000007654` — `0x206`=`54`, `0x207`=`76` → `0x7654`, MSB 0이므로 상위 0.
(c) `0x0123456789ab0098` — `0x98`을 16비트로 zero-extend → `0x0098`, 하위 2바이트만 바뀐다.
(d) `0x0000000076543210` — 4바이트 `10 32 54 76` → `0x76543210`, movl이라 상위 32비트 0.

**15.**
(a)
```c
long f(long n) {
    long result = 1;
    while (n > 1) {
        result *= n;
        n--;
    }
    return result;
}
```
(b) **120** — 1×5×4×3×2 (n! 계산)

**16.**
(a) `0x1111111111113220` — 메모리 word `0x3210` + `0x0010` = `0x3220`, 하위 2바이트만 바뀐다.
(b) `0x0000000087653220` — `0x76543210` + `0x11110010` = `0x87653220`. 32비트 연산이라 상위 32비트 0.
(c) `0x0000000000000000` — 자기 자신과 XOR하면 0.
(d) `0x1111111111110410` — `%rbx` + 4 × 0x100 = + 0x400 (메모리 접근 없음).

**17.** (a) `#x`  (b) `~x`
`%#x`는 `0x` 접두사가 붙은 소문자 hex. `~x + 1 == -x`이므로 `~(-5) + 1 = 5`.

**18.** (a) `jge`  (b) `sub`
조건 `x < y`가 거짓(x ≥ y)일 때 else로 점프하므로 `jge`. else 부분은 `rax = x − y`.

**19.** (a) `cmovge`
기본값 `rax = y − x`(then 쪽)를 넣어 두고, x ≥ y이면 `rdx = x − y`로 바꾼다. `cmp %rsi,%rdi`는 x − y를 계산하므로 signed greater-or-equal인 `cmovge`.

**20.** (a) `lea`  (b) `movslq`  (c) `(%rdi,%rsi,4)`
주소 자체를 반환하면 `lea`, 값을 읽으면서 int → long으로 확장하면 `movslq`.
