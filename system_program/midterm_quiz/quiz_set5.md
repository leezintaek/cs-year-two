# 중간고사 대비 모의문제 — Set 5

> 범위: A Tour of Computer Systems(1주차) ~ Control Flow(7주차)
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (C / x86-64 AT&T 어셈블리)
> 환경 가정: x86-64 Linux, gcc `-Og`, `-fwrapv`, `-fcf-protection=none`, little endian, w = 32 (int)
> 인자 `%rdi, %rsi, %rdx, %rcx, %r8, %r9` / 반환값 `%rax`
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** 어셈블러가 만든 오브젝트 파일 `hello.o`는 텍스트 파일이다.

**2.** `int x, y;`일 때 `int64_t p = x * y;`는 곱셈을 64비트로 수행하므로 오버플로우가 생기지 않는다.

**3.** 비정규화(denormalized) 값에는 hidden bit 1이 없고 M = f 이다.

**4.** 일반 `movq $imm, %rax`의 immediate는 32비트이며 64비트로 sign-extend 된다.

**5.** `jb`, `ja`는 signed 비교 결과에 따라 점프하는 명령어이다.

---

## Part B. 객관식

**6.** SRAM과 DRAM에 대한 설명으로 옳은 것은?
① DRAM은 주기적인 refresh가 필요하고 SRAM보다 밀도가 높다.
② SRAM은 주로 메인 메모리로 사용된다.
③ SRAM은 전원이 꺼져도 데이터가 유지된다.
④ DRAM은 비트당 트랜지스터 6개를 사용한다.

**7.** 다음 코드 실행 후 `s`의 값은?
```c
short s = SHRT_MAX;
s = s + 1;
```
① 32768  ② −32768  ③ 0  ④ −1

**8.** single precision에서 S = 1, e = `11111111`, f = 0 인 비트 패턴이 나타내는 값은?
① −0  ② NaN  ③ −∞  ④ 가장 작은 음의 비정규화 값

**9.** ISA와 명령어 인코딩에 대한 설명으로 옳은 것은?
① x86-64 명령어는 모두 4바이트 고정 길이이다.
② ARM은 대표적인 CISC 구조이다.
③ x86-64는 1 ~ 15바이트의 가변 길이 명령어를 사용한다.
④ RISC는 보통 1,000개가 넘는 명령어를 가진다.

**10.** `%rax = 0x11223344ffffffff`일 때 `addl $1, %eax` 실행 후 `%rax`는?
① `0x1122334500000000`  ② `0x0000000000000000`  ③ `0x1122334400000000`  ④ `0x0000000100000000`

**11.** 다음 어셈블리에 해당하는 C 함수 `char f(long x)`의 본문은?
```
test  %rdi, %rdi
sete  %al
ret
```
① `return x != 0;`  ② `return x == 0;`  ③ `return x < 0;`  ④ `return x & 1;`

---

## Part C. 단답형

**12.** little endian 머신에서 다음 코드를 실행했다. 각 값을 hex로 쓰시오.
```c
long x = 0x0102030405060708;
unsigned char *p = (unsigned char *) &x;
```
(a) `p[2]`
(b) `*(unsigned short *)(p + 3)`
(c) `*(unsigned int *)(p + 4)`

**13.** single precision float 비트 패턴이 나타내는 값을 쓰시오.
(a) `0x3F400000`
(b) `0x80000000`
(c) `0x7F800000`

**14.** w = 32일 때 각 식의 결과(0 또는 1)를 쓰시오.
(a) `-1 > 0U`
(b) `2147483647 > (int) 2147483648U`
(c) `(unsigned) -1 > -2`
(d) `2147483647U > -2147483647 - 1`

**15.** 아래 어셈블리에 대해 답하시오.
```
f:                              # a in %rdi, i in %rsi
    movsbl (%rdi,%rsi,1), %eax
    lea    (%rax,%rax,2), %eax
    ret
```
(a) `a`의 원소 타입과 반환 타입을 추론하시오.
(b) 함수 본문을 C 한 줄로 쓰시오.

**16.** 아래 C 코드는 `gcc -O1`에서도 conditional move 대신 조건 분기로 번역된다. 그 이유를 한 문장으로 쓰시오.
```c
long f(long *p) { return p ? *p + 1 : 0; }
```

---

## Part D. 빈칸 채우기 손코딩

**17.** 빈칸을 채우시오.
```c
int uadd_ok(unsigned x, unsigned y) {   // 오버플로우가 없으면 1
    unsigned sum = x + y;
    return ____(a)____;
}

int x = 12345;
int m = ~x + x;    // m의 값: ____(b)____
```

**18.** 메모리 → 메모리 복사 함수의 어셈블리를 완성하시오.
```c
void copy(int buf[], int *p, long i) { buf[i] = *p; }
```
```
copy:                           # buf in %rdi, p in %rsi, i in %rdx
    mov   ____(a)____, %eax
    mov   %eax, ____(b)____
    ret
```

**19.** 아래 C 함수를 `gcc -Og`로 컴파일한 결과의 빈칸을 채우시오.
```c
long f(long n) {
    long s = 0;
    do {
        s += n;
        n -= 2;
    } while (n > 0);
    return s;
}
```
```
f:                              # n in %rdi
    mov   $0x0, %eax
.L2:
    add   %rdi, %rax
    ____(a)____ $0x2, %rdi
    ____(b)____                 # n과 0을 비교해 플래그 설정
    ____(c)____ .L2
    ret
```

**20.** 아래 함수를 `gcc -O1`로 컴파일한 결과의 빈칸을 채우시오.
```c
long max(long x, long y) { return x > y ? x : y; }
```
```
max:                            # x in %rdi, y in %rsi
    mov   %rsi, %rax
    cmp   ____(a)____
    ____(b)____ %rdi, %rax
    ret
```

---
---

## 정답 및 해설

**1. X** — `.i`, `.s`는 텍스트이지만 `.o`와 실행 파일은 **바이너리** 파일이다.

**2. X** — `x * y`가 int(32비트)로 먼저 계산되어 오버플로우된 뒤 64비트로 sign-extend 된다. `(int64_t) x * y`처럼 캐스팅을 먼저 해야 한다.

**3. O** — e = 0이면 M = f (0.f), E = 1 − bias.

**4. O** — 64비트 immediate가 필요할 때만 `movabsq`를 쓴다.

**5. X** — above/below(`a`, `b`)는 **unsigned** 비교(CF 사용). signed는 greater/less(`g`, `l`).

**6. ①** — ② SRAM은 캐시, ③ SRAM도 휘발성, ④ 비트당 6 트랜지스터는 SRAM.

**7. ②** — 32767 + 1 = 32768은 short 범위를 넘어 `0x8000` = −32768로 wrap-around 된다.

**8. ③** — e가 모두 1이고 f = 0이면 무한대. S = 1이므로 −∞.

**9. ③** — x86-64는 CISC(가변 길이 1 ~ 15바이트), ARM·RISC-V는 RISC(보통 4바이트 고정, 명령어 100개 미만).

**10. ②** — `%eax` = `0xffffffff` + 1 = `0x00000000` (carry는 버림). 32비트 연산이라 상위 32비트도 0이 된다.

**11. ②** — `test %rdi,%rdi`는 x & x = x로 플래그 설정. `sete`는 ZF = 1(x == 0)일 때 1.

**12.** 메모리: `p[0..7]` = `08 07 06 05 04 03 02 01`
(a) **`0x06`**
(b) **`0x0405`** — `p[3]`=`05`, `p[4]`=`04` → little endian으로 `0x0405`
(c) **`0x01020304`** — `p[4..7]` = `04 03 02 01`

**13.**
(a) **0.75** — `0 01111110 1000…0`: e = 126 → E = −1, M = 1.1(2) → 1.1(2) × 2⁻¹ = 0.11(2) = 0.75
(b) **−0** — S = 1, e = 0, f = 0
(c) **+∞** — S = 0, e = 모두 1, f = 0

**14.**
(a) **1** — `-1` → `0xFFFFFFFF`(UMAX) > 0
(b) **1** — `(int) 2147483648U` = `0x80000000` = INT_MIN, signed 비교 TMax > TMin
(c) **1** — `-2`도 unsigned로 바뀌어 `0xFFFFFFFF > 0xFFFFFFFE`
(d) **0** — TMin이 unsigned `0x80000000`으로 바뀌어 `0x7FFFFFFF > 0x80000000`은 거짓

**15.**
(a) 원소 타입 **`char`(signed char)** — 1바이트를 scale 1로 읽고 sign-extend(`movsbl`). 반환 타입 **`int`** — 결과를 `%eax`(32비트)에 둔다.
(b) `return a[i] * 3;` — `lea (%rax,%rax,2)` = 3 × a[i]

**16.** cmov는 양쪽 식을 모두 먼저 계산하므로 `p`가 NULL이어도 `*p`를 역참조하게 되어 segmentation fault가 날 수 있기 때문이다. (risky computation)

**17.** (a) `sum >= x` (또는 `!(sum < x)`)  (b) **−1**
unsigned 덧셈은 오버플로우가 나면 결과가 x보다 작아진다. `~x + x`는 모든 비트가 1 = −1 (x 값과 무관).

**18.** (a) `(%rsi)`  (b) `(%rdi,%rdx,4)`
메모리 → 메모리 이동은 불가능하므로 `%eax`를 거친다. int 배열이라 scale 4, 32비트 레지스터 사용.

**19.** (a) `sub`  (b) `test %rdi,%rdi` (또는 `cmp $0x0,%rdi`)  (c) `jg`
do-while은 body → test → 조건이 참이면 body로 돌아간다. 점프 전에 test가 오므로 맨 앞에 `jmp`가 없다.

**20.** (a) `%rsi,%rdi` (x − y 계산)  (b) `cmovg` (`cmovge`도 결과는 같다)
기본값으로 `rax = y`를 넣어 두고, x > y이면 `rax = x`로 바꾼다. x == y일 때는 어느 쪽을 골라도 값이 같으므로 실제 gcc는 `cmovge`를 내기도 한다.
