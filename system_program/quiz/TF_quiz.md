# TF_quiz

- 범위: week1 ~ week7 (A Tour of Computer Systems ~ Control Flow)
- 환경 가정: x86-64 Linux, gcc, `-fwrapv`, `-fcf-protection=none`, `-Og` (별도 표기가 없으면)
- 정답: `TF_quiz_answer.md`

---

### Q1.
`%rax = 0x100`, `%rbx = 0x10`이고 메모리 `0x200 ~ 0x207`에 바이트 `98 ba dc fe 10 32 54 76`이 순서대로 저장되어 있다. `addl (%rax,%rax), %ebx` 실행 후 `%rbx`는 `0x00000000fedcbaa8`이다.

답: ☐ T ☐ F

### Q2.
w = 32일 때 C 식 `2147483647U < -2147483647-1`의 결과는 1(참)이다.

답: ☐ T ☐ F

### Q3.
`a = 0`, `b = 1`일 때 `cmp b, a`를 실행하면 CF와 SF가 모두 1로 설정된다.

답: ☐ T ☐ F

### Q4.
아래 코드에서 `f1`은 `0.00`으로 출력된다.

```c
float x = 16777216.0f;          // 2^24
float f1 = (1.0f + x) - x;
printf("f1 = %.2f\n", f1);
```

답: ☐ T ☐ F

### Q5.
링크 단계에서 다른 object file이나 library에 정의된 함수에 대한 외부 참조를 해결하는 과정을 relocation이라고 한다.

답: ☐ T ☐ F

### Q6.
`%rdx = 0xf000`, `%rcx = 0x100`일 때 operand `-0x8(%rdx,%rcx,4)`가 가리키는 메모리 주소는 `0xf408`이다.

답: ☐ T ☐ F

### Q7.
아래 코드를 실행하면 `i: ...` 줄은 한 번도 출력되지 않고 `done`만 출력된다.

```c
int n = -1;
for (unsigned int i = 3; i >= n; i--)
    printf("i: %d\n", i);
printf("done\n");
```

답: ☐ T ☐ F

### Q8.
아래 어셈블리로 컴파일되는 `long q6(long buf[], long x, long y)`의 반환값은 `2*x - y`이다.

```
mov  %rdx,%rax
lea  (%rsi,%rsi,1),%rdx
sub  %rax,%rdx
mov  %rdx,(%rdi,%rsi,8)
ret
```

답: ☐ T ☐ F

### Q9.
IEEE 754 형식을 따르는 8-bit 부동소수점(sign 1, exponent 4, fraction 3)에서 표현 가능한 가장 작은 양의 denormalized 값은 $2^{-10}$이다.

답: ☐ T ☐ F

### Q10.
`cmp b, a` 명령어는 `b - a`를 계산하여 그 결과로 condition code만 설정한다.

답: ☐ T ☐ F

### Q11.
`gcc -c test.c` 후 `objdump -t test.o`로 symbol table을 보면 `printf`는 `*UND*` 섹션으로 표시된다.

답: ☐ T ☐ F

### Q12.
`int x, y;`에 대해 `int64_t pll = x * y;`라고 쓰면 곱셈이 64비트로 수행되므로 overflow 없이 정확한 곱을 얻는다.

답: ☐ T ☐ F

### Q13.
`%rax = 0`이고 메모리 `0x200 ~ 0x207`에 바이트 `98 ba dc fe 10 32 54 76`이 저장되어 있다. `movsbw 0x201, %ax` 실행 후 `%rax`는 `0x000000000000ffba`이다.

답: ☐ T ☐ F

### Q14.
`float f = 2.75f;`의 비트 패턴을 16진수로 나타내면 `0x40300000`이다.

답: ☐ T ☐ F

### Q15.
`long f(long x){ return x*3; }`를 컴파일하면 lea 한 번으로 `lea (,%rdi,3),%rax`가 생성될 수 있다.

답: ☐ T ☐ F

### Q16.
`long result = x ? *x + 1 : 0;` (x는 `long *`)은 계산이 간단하므로 `gcc -O1`에서 conditional move(`cmov`)로 컴파일된다.

답: ☐ T ☐ F

### Q17.
Little Endian 머신에서 `int x = 0x01234567;`이고 `&x == 0x100`이면, 주소 `0x103`에는 `0x67`이 저장된다.

답: ☐ T ☐ F

### Q18.
아래 어셈블리로 컴파일되는 함수 `long q3(long x)`의 반환값은 `x*6`이다.

```
lea  (%rdi,%rdi,2),%rax
shl  $0x2,%rax
ret
```

답: ☐ T ☐ F

### Q19.
Single precision에서 가장 큰 denormalized 값은 정확히 $2^{-126} - 2^{-149}$이다.

답: ☐ T ☐ F

### Q20.
레지스터 없이 `F = (X+Y) - (X*Y)`를 계산하면 메모리 접근이 9번 필요하지만, 레지스터를 사용하면 3번으로 줄어든다.

답: ☐ T ☐ F

### Q21.
x86-64/Linux calling convention에서 함수의 5번째 정수 인자는 `%r8` 레지스터로 전달된다.

답: ☐ T ☐ F

### Q22.
w = 32일 때 C 식 `-1 < 0U`의 결과는 1(참)이다.

답: ☐ T ☐ F

### Q23.
8-bit 덧셈 `0x7F + 0x01`을 수행하면 OF = 1, CF = 0이 된다.

답: ☐ T ☐ F

### Q24.
`movzbq`, `movzwq`와 마찬가지로 32-bit를 64-bit로 zero-extend하는 `movzlq` 명령어가 존재한다.

답: ☐ T ☐ F

### Q25.
`10.10100`₂를 소수점 아래 2비트로 round-to-even 하면 `10.11`₂이 된다.

답: ☐ T ☐ F

### Q26.
아래 코드의 출력은 `Value: 255`이다.

```c
void print_value(char value) { printf("Value: %d\n", value); }
int main() {
    unsigned char c = 255;
    print_value(c);
}
```

답: ☐ T ☐ F

### Q27.
`void f(){ long ret = *((long *)0x104); }`를 `-Og`로 컴파일하면 메모리 load 없이 `retq` 한 줄만 남는다.

답: ☐ T ☐ F

### Q28.
전처리 단계(`gcc -E`)의 결과물인 `.i` 파일은 binary file이다.

답: ☐ T ☐ F

### Q29.
메모리 `0x200 ~ 0x207`에 바이트 `98 ba dc fe 10 32 54 76`이 저장되어 있을 때, `movq 0x200, %rax` 실행 후 `%rax`는 `0x98badcfe10325476`이다.

답: ☐ T ☐ F

### Q30.
`leaq` 명령어는 산술 연산을 수행하지만 condition code를 변경하지 않는다.

답: ☐ T ☐ F

### Q31.
`float f = -3.99f; int i = (int)f;`를 실행하면 `i`는 `-4`이다.

답: ☐ T ☐ F

### Q32.
`int x = -17;`의 32-bit 비트 패턴은 `0xffffffef`이다.

답: ☐ T ☐ F

### Q33.
`%rip`에는 현재 실행 중인 명령어의 주소가 저장된다.

답: ☐ T ☐ F

### Q34.
아래 어셈블리에서 `sar`이 사용된 이유는 `long`이 signed 타입이기 때문이며, `t2`는 `(a - b + c) >> 2`이다.

```
long q4(long a, long b, long c) { long t1 = ...; long t2 = ...; return t1 & t2; }

sub  %rsi,%rdi
lea  (%rdi,%rdx,1),%rax
mov  %rax,%rdx
sar  $0x2,%rdx
and  %rdx,%rax
ret
```

답: ☐ T ☐ F

### Q35.
`double d = 74.5;`의 11-bit exponent 필드 값을 16진수로 나타내면 `0x405`이다.

답: ☐ T ☐ F

### Q36.
2048×2048 배열을 복사할 때, `dst[i][j] = src[i][j]`를 바깥 루프 `i`, 안쪽 루프 `j`로 돌리는 `copyij`가 `copyji`보다 느리다.

답: ☐ T ☐ F

### Q37.
8-bit 덧셈 `0xFF + 0x01`을 수행하면 CF = 1, ZF = 1, OF = 1이 된다.

답: ☐ T ☐ F

### Q38.
`short sy = -15213; int y = (int) sy;`에서 `y`의 상위 2바이트는 `0x0000`이다.

답: ☐ T ☐ F

### Q39.
`%rax = 0x0011223344556677`일 때 `movl $-1, %eax`를 실행하면 `%rax`는 `0x00000000ffffffff`이 된다.

답: ☐ T ☐ F

### Q40.
Single precision에서 exponent 필드가 `e = 0`인 denormalized 값의 실제 지수 E는 $-127$이다.

답: ☐ T ☐ F

### Q41.
CISC ISA는 고정 길이 명령어 인코딩(보통 4바이트)을 사용하고, RISC ISA는 가변 길이 인코딩을 사용한다.

답: ☐ T ☐ F

### Q42.
`u * 24`는 `(u << 5) - (u << 3)`으로 계산할 수 있다.

답: ☐ T ☐ F

### Q43.
gcc가 `while` 루프를 jump-to-middle 방식으로 번역하면, 루프의 첫 명령어는 테스트 부분으로 가는 무조건 `jmp`이다.

답: ☐ T ☐ F

### Q44.
`void f11(unsigned long *x, unsigned int y){ *x = y; }`는 `movzlq` 대신 `mov %esi,%eax`와 `mov %rax,(%rdi)`로 컴파일된다.

답: ☐ T ☐ F

### Q45.
8-bit 부동소수점(sign 1, exponent 4, fraction 3, IEEE 754 방식)에서 비트 패턴 `01001001`의 값은 4.5이다.

답: ☐ T ☐ F

### Q46.
SRAM은 DRAM보다 빠르지만, 비트당 필요한 트랜지스터 수는 더 적다.

답: ☐ T ☐ F

### Q47.
`long y = 0x12345678; char v = (char) y; printf("%d\n", v);`의 출력은 `120`이다.

답: ☐ T ☐ F

### Q48.
같은 어셈블리 코드를 AT&T 문법으로 쓰든 Intel 문법으로 쓰든 assembler가 생성하는 기계어 바이너리는 동일하다.

답: ☐ T ☐ F

### Q49.
아래 코드의 출력은 `True ...`로 시작한다.

```c
float f1 = 0.1f, f2 = 0.6f, f3 = 0.7f;
if (f1 + f2 == f3) printf("True f1+f2=%.10f\n", f1 + f2);
else               printf("False f1+f2=%.10f\n", f1 + f2);
```

답: ☐ T ☐ F

### Q50.
ANSI/ISO C 표준에 따르면 `long`은 최소 64비트여야 한다.

답: ☐ T ☐ F
