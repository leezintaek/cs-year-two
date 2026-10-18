# SP 연습 문제 (Quiz 1 ~ 4 변형)

- 참고: `SP Quiz 1, Quiz 2 Integer and FP.pdf`, `SP 3-4.pdf`
- 형식: PDF 퀴즈와 같은 **빈칸 채우기 / 출력 예측 / 어셈블리 작성**
- 환경 가정: x86-64 Linux, gcc, `-Og`, `-fwrapv`, little endian (별도 표기가 없으면)
- 함수 인자 순서: `%rdi`, `%rsi`, `%rdx`, `%rcx`, `%r8`, `%r9` / 반환값: `%rax`
- 정답: `SP_practice_quiz_answer.md`

---

## Part 1. Bits, Bytes, and Integers (Quiz 1)

### P1. Casting Surprise
출력을 쓰시오.

```c
void print_value(char value) {
    printf("Value: %d\n", value);
}
int main() {
    unsigned char c = 200;
    print_value(c);
    return 0;
}
```

출력: `Value: ________`

### P2. Mixed Signed/Unsigned Expression
아래 두 프로그램의 출력(또는 동작)을 쓰시오.

```c
// (a)
int n = -1;
for (unsigned int i = 2; i >= n; i--)
    printf("i: %d\n", i);
printf("done\n");

// (b)
int n = 0;
for (unsigned int i = 2; i >= n; i--)
    printf("i: %d\n", i);
printf("done\n");
```

(a) ______________________

(b) ______________________

### P3. Expanding Numbers
`show_bytes`는 PDF Quiz 1과 같다 (`printf("%#.2x\n", start[i]);`). 빈칸을 채우시오.

```c
int main() {
    char cx = -2;
    int x = (int) cx;
    printf("cx=%d\n", cx);
    show_bytes((pointer) &cx, sizeof(char));
    printf("x=%d\n", x);
    show_bytes((pointer) &x, sizeof(int));
    return 0;
}
```

```
cx=______
______

x=______
______
______
______
______
```

### P4. Expanding Numbers (unsigned)
```c
unsigned char uc = 0x80;
int x = uc;
printf("x=%d\n", x);
show_bytes((pointer) &x, sizeof(int));
```

```
x=______
______
______
______
______
```

이때 일어난 확장은 zero extension / sign extension 중 무엇인가? ______________

### P5. Truncating Numbers
```c
int x = 300;
char cx = (char) x;
printf("x=%d\n", x);
show_bytes((pointer) &x, sizeof(int));
printf("cx=%d\n", cx);
show_bytes((pointer) &cx, sizeof(char));
```

```
x=300
______
______
______
______

cx=______
______
```

### P6. Special Case of Negation
"Hello"는 각각 몇 번 출력되는가?

```c
// (a)
int cnt = -3;
while (-cnt >= 0) { printf("Hello\n"); cnt++; }

// (b)
int cnt = INT_MIN;
while (-cnt >= 0) { printf("Hello\n"); cnt++; }
```

(a) ______번  (b) ______번

### P7. Integer Overflow of Addition
```c
int main() {
    int x = INT_MIN + INT_MIN;
    if (x >= 0) printf("positive x %d\n", x);
    else        printf("negative x %d\n", x);
    return 0;
}
```

출력: ______________________

### P8. Multiply with Shift
```c
int main() {
    int x = INT_MAX / 2 + 1;
    if (2 * x >= 0) printf("positive x %d\n", 2 * x);
    else            printf("negative x %d\n", 2 * x);
    return 0;
}
```

(1) `x`의 값을 16진수로: ______________

(2) 출력: ______________________

### P9. Cost of Arithmetic Operations
강의의 상대 비용 표를 기준으로, 아래 연산을 **비싼 것부터** 나열하시오.

`integer multiply`, `pointer dereference`, `floating point`, `integer divide`, `shift`, `function call`

______ > ______ > ______ > ______ > ______ > ______

---

## Part 2. Floating Point (Quiz 2)

### P10. IEEE 754 Single Precision
빈칸을 채우시오 (`x /wt`는 32비트를 2진수로 출력).

```c
int main() {
    float f1 = -6.5f;
    float f2 = ______f;
    float f3 = 10.0f;
    return 0;
}
```

```
(gdb) x /wt &f1
________________________________
(gdb) x /wt &f2
00111111010000000000000000000000
(gdb) x /wt &f3
________________________________
```

### P11. Special Values in C
각 변수의 출력을 쓰시오 (NaN은 부호 무관하게 `nan`으로 써도 된다).

```c
double d1 = -1.0 / 0.0;
double d2 = INFINITY * 0.0;
double d3 = 1.0 / INFINITY;
double d4 = INFINITY + 1.0;
```

d1: ______  d2: ______  d3: ______  d4: ______

`double`에서 NaN의 exponent 필드와 fraction 필드는 각각 어떤 조건을 만족하는가?

exponent: ______________  fraction: ______________

### P12. 8-bit Floating Point (1)
IEEE 754 규칙을 따르는 8-bit 형식: **sign 1비트, exponent 4비트, fraction 3비트**

(1) bias = ______

(2) 1.0의 비트 표현: ______________

(3) 정규화(normalized) 형식으로 표현 가능한 가장 큰 수(10진수): ______________

(4) 비트 패턴 `01001001`의 10진수 값: ______________

### P13. 8-bit Floating Point (2)
이번에는 **sign 1비트, exponent 3비트, fraction 4비트** 형식이다.

(1) bias = ______

(2) 1.0의 비트 표현: ______________

(3) 정규화 형식으로 표현 가능한 가장 큰 수: ______________

(4) 가장 작은 양의 denormalized 수: ______________

(5) 비트 패턴 `01011010`의 10진수 값: ______________

### P14. Rounding (round-to-nearest-even)
아래 2진수를 **소수점 아래 2비트**(1/4 단위)로 반올림하시오.

| 원래 값      | 반올림 결과 |
|--------------|-------------|
| `10.00011₂`  |             |
| `10.00110₂`  |             |
| `10.11100₂`  |             |
| `10.10100₂`  |             |

### P15. Rounding in C
```c
float f1 = 0.1f, f2 = 0.2f, f3 = 0.3f;
if (f1 + f2 == f3) printf("True\n");
else               printf("False\n");
```

출력: ______

(참고: PDF Quiz 2의 `0.1f + 0.6f == 0.7f`는 `False`였다. 결과가 같은지 비교해 보자.)

### P16. int to float/double Casting
```c
int i1 = 16777217;    // 2^24 + 1
int i2 = 33554435;    // 2^25 + 3
int i3 = INT_MAX;
float  f1 = (float) i1;
float  f2 = (float) i2;
float  f3 = (float) i3;
double d3 = (double) i3;
printf("%f\n%f\n%f\n%lf\n", f1, f2, f3, d3);
```

```
______________
______________
______________
______________
```

`f3`의 비트 패턴(16진수): ______________

### P17. float/double to int Casting
```c
float  a = 1.0e10f;
float  b = -3.0e9f;
float  c = 3.7f, d = -3.7f, e = -0.5f;
printf("%d %d\n", (int) a, (int) b);
printf("%d %d %d\n", (int) c, (int) d, (int) e);
```

```
______________ ______________
______ ______ ______
```

### P18. Violation of Associativity
```c
float x = 16777216.0f;          // 2^24
float f1 = (3.0f + x) - x;
float f2 = (2.0f + x) - x;
float f3 = 3.0f + (x - x);

float y = 1e20f;
float g1 = (y + -y) + 3.14f;
float g2 = y + (-y + 3.14f);
printf("f1=%.2f f2=%.2f f3=%.2f\n", f1, f2, f3);
printf("g1=%.2f g2=%.2f\n", g1, g2);
```

```
f1=______ f2=______ f3=______
g1=______ g2=______
```

---

## Part 3. Data Movement (Quiz 3)

### P19. Operand Forms
레지스터와 메모리 상태가 아래와 같다.

| 주소  | 값   |   | 레지스터 | 값    |
|-------|------|---|----------|-------|
| 0x100 | 0xFF |   | `%rdi`   | 0x100 |
| 0x108 | 0xAB |   | `%rsi`   | 0x3   |
| 0x110 | 0x13 |   |          |       |
| 0x118 | 0x11 |   |          |       |

각 operand의 **값**을 쓰시오.

| Operand            | 값 |
|--------------------|----|
| `%rdi`             |    |
| `$0x108`           |    |
| `0x108`            |    |
| `(%rdi)`           |    |
| `8(%rdi)`          |    |
| `(%rdi,%rsi,8)`    |    |
| `-8(%rdi,%rsi,8)`  |    |
| `0x104(,%rsi,4)`   |    |

### P20. mov instruction (absolute / indirect / indexed)
빈칸을 채우시오.

```c
// (a)
void func() { *((long *)0x200) = 5; }
```
```
mov ______, ______
retq
```

```c
// (b)
long func() { long ret = *((long *)0x200); return ret; }
```
```
mov ______, ______
retq
```

```c
// (c)
void func(int buf[], long idx) { buf[idx] = -1; }
```
```
movl ______, ______________
retq
```

```c
// (d)
void func(short buf[], long idx) { buf[idx] = -1; }
```
```
movw ______, ______________
retq
```

### P21. mov instruction (memory to memory)
```c
void func(int buf[], int *xp, long idx) {
    buf[idx] = *xp;
}
```
```
mov ______________, ______
mov ______, ______________
retq
```

### P22. Invalid mov
아래 명령어 중 **잘못된** 것을 모두 고르고 이유를 쓰시오.

1. `movl %eax, %rdx`
2. `movq (%rax), (%rsp)`
3. `movw %ax, (%rsp)`
4. `movb %si, 8(%rbp)`
5. `movq %rax, $0x123`
6. `movq $0x0011223344556677, %rax`
7. `movl $0x1, %eax`

### P23. Register Names
| 64-bit | 32-bit | 16-bit | 8-bit |
|--------|--------|--------|-------|
| `%rax` |        |        |       |
| `%rdx` |        |        |       |
| `%rsi` |        |        |       |
| `%r8`  |        |        |       |

---

## Part 4. Instruction Size & Extension (Quiz 4)

### P24. Larger source → smaller destination
```c
void f2(short *x, long y) { *x = y; }   // mov ______, (%rdi)
void f3(int   *x, long y) { *x = y; }   // mov ______, (%rdi)
void f4(long  *x, long y) { *x = y; }   // mov ______, (%rdi)
```

### P25. Smaller source → larger destination
빈칸을 채우시오. (확장 방식은 **source 타입**으로 결정된다.)

```c
void f6 (long *x, short y)           { *x = y; }
void f7 (long *x, int y)             { *x = y; }
void f10(unsigned long *x, unsigned short y) { *x = y; }
void f11(unsigned long *x, unsigned int y)   { *x = y; }
void g1 (unsigned long *x, char y)   { *x = y; }
void g2 (long *x, unsigned char y)   { *x = y; }
```

```
f6 : ________ ______, %rsi      / mov %rsi,(%rdi)
f7 : ________ ______, %rsi      / mov %rsi,(%rdi)
f10: ________ ______, %esi      / mov %rsi,(%rdi)
f11: ________ ______, %eax      / mov %rax,(%rdi)
g1 : ________ ______, %rsi      / mov %rsi,(%rdi)
g2 : ________ ______, %esi      / mov %rsi,(%rdi)
```

### P26. Upper bits after mov
각 명령어는 **독립적으로** `%rax = 0x0011223344556677` 상태에서 실행된다. 실행 후 `%rax`를 쓰시오.

| 명령어            | 실행 후 `%rax`       |
|-------------------|----------------------|
| `movb $-1, %al`   |                      |
| `movw $-1, %ax`   |                      |
| `movl $-1, %eax`  |                      |
| `movq $-1, %rax`  |                      |

### P27. movz / movs with %dl
`%dl = 0xAA`, `%rax = 0x0011223344556677`일 때 (각각 독립 실행)

| 명령어              | 실행 후 `%rax`       |
|---------------------|----------------------|
| `movb %dl, %al`     |                      |
| `movsbq %dl, %rax`  |                      |
| `movzbq %dl, %rax`  |                      |

### P28. movabsq
아래 대입 중 `movabsq`가 **반드시** 필요한 것은?

```c
void a(long *xp) { *xp = -1; }
void b(long *xp) { *xp = 0x7fffffff; }
void c(long *xp) { *xp = 0x0011223344556677; }
```

답: ______  이유: ______________________________

---

## Part 5. Arithmetic Operations (Quiz 5)

### P29. lea (Load Effective Address)
```c
// (a)
int *func(int buf[], long idx) { return &buf[idx]; }
// lea ______________, %rax

// (b)
long *func(long buf[], long idx) { return &buf[idx + 2]; }
// lea ______________, %rax

// (c)
char *func(char buf[], long idx) { return &buf[idx]; }
// lea ______________, %rax
```

### P30. mov vs lea
P19의 레지스터/메모리 상태에서 (`%rdi = 0x100`, `%rsi = 0x3`)

- `lea -8(%rdi,%rsi,8), %rax` 실행 후 `%rax` = ______
- `mov -8(%rdi,%rsi,8), %rax` 실행 후 `%rax` = ______

### P31. lea로 곱셈 계산하기
빈칸을 채우시오.

```c
long m9 (long x) { return x * 9;  }   // lea ______________, %rax

long m12(long x) { return x * 12; }   // lea ______________, %rax
                                      // shl $____, %rax

long m40(long x) { return x * 40; }   // lea ______________, %rax
                                      // shl $____, %rax
```

### P32. Swap function (int 버전)
```c
void swap(int *xp, int *yp) {
    int t1 = *xp;
    int t2 = *yp;
    *xp = t2;
    *yp = t1;
}
```
```
mov ______, %eax
mov ______, %edx
mov %edx, ______
mov %eax, ______
retq
```

### P33. Fill in the missing parts of assembly code
```c
long arith2(long x, long y, long z) {
    long t1 = x + y;
    long t2 = z * 24;
    long t3 = t1 & 0x0F0F;
    long t4 = t2 - t3;
    return t4;
}
```
```
addq %rsi, %rdi                  # t1 = x + y
______ (%rdx,%rdx,2), %rax       # 3*z
salq $____, %rax                 # t2 = 24*z
andl $______, %edi               # t3 = t1 & 0x0F0F (10진수로)
______ ______, ______            # return t2 - t3
ret
```

### P34. Fill in the missing parts of the C code (1)
```
lea (%rdi,%rsi,4), %rax
lea (%rdx,%rdx,2), %rdx
lea (%rax,%rdx,4), %rax
retq
```
```c
long scale(long x, long y, long z) {
    return ______________________;
}
```

### P35. Fill in the missing parts of the C code (2)
```
lea (%rsi,%rsi,2), %rax
sub %rdx, %rax
mov %rax, (%rdi,%rsi,8)
retq
```
```c
void quiz2(long buf[], long x, long y) {
    ______________________;
}
```
