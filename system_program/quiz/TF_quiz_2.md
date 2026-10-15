# TF_quiz 2

- 범위: week1 ~ week7 (A Tour of Computer Systems ~ Control Flow)
- 환경 가정: x86-64 Linux, gcc, `-fwrapv`, `-fcf-protection=none`, `-Og` (별도 표기가 없으면)
- 번호는 `TF_quiz.md`(Q1~Q50)에 이어서 Q51~Q100
- 정답: `TF_quiz_2_answer.md`

---

### Q51.
`float f = 0.7f;`의 비트 패턴을 16진수로 나타내면 `0x3F333333`이다.

답: ☐ T ☐ F :F 0x30066666...

### Q52.
아래 어셈블리로 컴파일되는 `long q5(long x[], long y)`는 `x[y] = 12*y`를 수행하고 `y`를 반환한다.

```
mov  %rsi,%rax
lea  (%rsi,%rsi,2),%rdx
shl  $0x2,%rdx
mov  %rdx,(%rdi,%rsi,8)
ret
```

답: ☐ T

### Q53.
`-fwrapv`로 컴파일한 아래 코드는 `surprise 2147483647`을 출력한다.

```c
int x = INT_MIN;
if (x < 1 && x - 1 >= 0)
    printf("surprise %d \n", x - 1);
```

답: ☐ T

### Q54.
64-bit에서 `a = -1`, `b = 1`일 때 `cmp b, a`를 실행하면 CF = 1이 된다.

답: ☐ F

### Q55.
`gcc -o hello test.c`로 링크한 뒤 `objdump -t hello`로 보면, `main`의 주소는 `test.o`에서와 같이 `0x0000000000000000`으로 유지된다.

답: ☐ T ☐ F :F test.o에서는 상대주소 링크하면 절대 주소

### Q56.
주소 `0x40`에 값 5가 저장되어 있을 때, `mov $0x40,%rax`를 실행하면 `%rax`는 5가 된다.

답: ☐ F

### Q57.
w = 32일 때 C 식 `2147483647 < 2147483648U`의 결과는 0(거짓)이다.

답: ☐ T

### Q58.
3-bit fraction을 가정하고 $1.010_2 \times 2^{-1}$과 $-1.110_2 \times 2^{-2}$를 곱하면, 정규화와 반올림을 마친 최종 결과의 지수는 $-3$이다.

답: ☐ T ☐ F

### Q59.
`%rax = 0xffffffffffffffff`이고 메모리 `0x200 ~ 0x207`에 바이트 `98 ba dc fe 10 32 54 76`이 저장되어 있다. `movzwl 0x202, %eax` 실행 후 `%rax`는 `0xffffffff0000fedc`이다.

답: ☐ T ☐ F

### Q60.
`if (x <= 1)`을 `cmp $0x1,%edi`로 비교할 때, `x - 1`에서 overflow가 날 수 있으므로 SF만으로는 판단할 수 없고 `SF ^ OF`를 사용해야 한다.

답: ☐ T ☐ F

### Q61.
아래 코드에서 `x`의 바이트를 낮은 주소부터 출력하면 `0x80 0xff 0xff 0xff`이다.

```c
char cx = -128;
int x = (int) cx;
show_bytes((pointer) &x, sizeof(int));
```

답: ☐ T ☐ F

### Q62.
SRAM은 DRAM과 달리 refresh가 필요 없으므로 nonvolatile 메모리이다.

답: ☐ T ☐ F

### Q63.
`float f = 15213.0f;`의 비트 패턴을 16진수로 나타내면 `0x466DB400`이다.

답: ☐ T ☐ F

### Q64.
`void f7(int buf[], long idx){ buf[idx] = -1; }`를 컴파일하면 `movl $0xffffffff,(%rdi,%rsi,8)`이 생성된다.

답: ☐ T ☐ F

### Q65.
`movabsq $0x0011223344556677, (%rdi)`처럼 `movabsq`의 목적지로 메모리를 사용할 수 있다.

답: ☐ T ☐ F

### Q66.
`-fwrapv`로 컴파일하면 `int foo(int x){ return x + 1 > x; }`는 모든 `x`에 대해 1을 반환한다.

답: ☐ T ☐ F

### Q67.
`long f1(long x){ if (x > 100) return 1; return 0; }`를 `gcc -O1`로 컴파일하면 `setg %al` 뒤에 `movzbl %al,%eax`가 오는데, 이는 `setg`가 `%rax`의 하위 1바이트만 바꾸기 때문이다.

답: ☐ T ☐ F

### Q68.
소수점 아래 둘째 자리까지 round-to-even 하면 `7.8850000`은 `7.89`가 된다.

답: ☐ T ☐ F

### Q69.
강의의 정규화 기준(CPU 1 cycle 0.5ns를 1초로 환산)에서 DRAM 접근은 약 30초, 디스크 접근은 약 162일에 해당한다.

답: ☐ T ☐ F

### Q70.
`%rax = 0x100`, `%rcx = 0x0f0f0000`일 때 `leaq (%rax,%rcx), %rcx`를 실행하면 `%rcx`는 `0x0f0f0100`이 된다.

답: ☐ T ☐ F

### Q71.
강의의 `tadd_ok`에 `x = INT_MIN`, `y = -1`을 넣으면 1(overflow 없음)을 반환한다.

```c
int tadd_ok(int x, int y) {
    int sum = x + y;
    int neg_over = x < 0 && y < 0 && sum > 0;
    int pos_over = x > 0 && y > 0 && sum < 0;
    return !neg_over && !pos_over;
}
```

답: ☐ T ☐ F

### Q72.
`-fcf-protection=none` 옵션 없이 컴파일하면 함수 시작 부분에 `endbr64` 명령어가 나타날 수 있다.

답: ☐ T ☐ F

### Q73.
Single precision에서 가장 큰 normalized 값의 exponent 필드는 `1111 1111`이다.

답: ☐ T ☐ F

### Q74.
`test %rsi,%rdi`는 `%rdi & %rsi`를 계산해 그 결과를 `%rdi`에 저장하고 condition code를 설정한다.

답: ☐ T ☐ F

### Q75.
4-bit unsigned 곱셈 `1011 × 1101`의 결과를 4비트로 자르면 15이다.

답: ☐ T ☐ F

### Q76.
`int q1(short s){ int i = s; return i; }`의 기계어 `0f bf c7`은 `movzwl %di,%eax`이다.

답: ☐ T ☐ F

### Q77.
C 컴파일러와 Fortran 컴파일러는 같은 assembly language로 된 출력 파일을 생성할 수 있다.

답: ☐ T ☐ F

### Q78.
`float f1 = 0.1f;`는 저장 과정의 반올림 때문에 실제 0.1보다 약간 큰 값으로 저장된다.

답: ☐ T ☐ F

### Q79.
`int x = INT_MAX; char cx = (char) x;`를 실행하면 `cx`는 127이다.

답: ☐ T ☐ F

### Q80.
x86-64 ISA를 처음 지원한 Intel 프로세서는 Core 2(2006)이다.

답: ☐ T ☐ F

### Q81.
8-bit 값 `0x80`을 오른쪽으로 2비트 SHR 하면 `0xE0`이 된다.

답: ☐ T ☐ F

### Q82.
`jae`(jump if above or equal)의 조건은 `~CF & ~ZF`이다.

답: ☐ T ☐ F

### Q83.
`x = INT_MIN`일 때 `2*x >= 0` 조건은 참이다.

답: ☐ T ☐ F

### Q84.
IEEE 754에서 exponent 필드가 모두 1이고 fraction 필드가 0이면 NaN이다.

답: ☐ T ☐ F

### Q85.
shell은 명령줄의 첫 단어가 built-in command이면 해당 프로그램을 디스크에서 메모리로 load한 뒤 실행한다.

답: ☐ T ☐ F

### Q86.
`%rax = 0xffffffff1234fedc`이고 메모리 `0x200 ~ 0x207`에 바이트 `98 ba dc fe 10 32 54 76`이 저장되어 있다. `movb 0x207, %al` 실행 후 `%rax`는 `0xffffffff1234fe76`이다.

답: ☐ T ☐ F

### Q87.
4-bit two's complement의 표현 범위는 −8 ~ 7이고, 4-bit sign-magnitude의 표현 범위는 −7 ~ 7이다.

답: ☐ T ☐ F

### Q88.
`%rbx`에 8이 저장되어 있을 때 `mov %rbx,0x50`을 실행하면 주소 `0x50`의 메모리에 8이 저장된다.

답: ☐ T ☐ F

### Q89.
float 비트 패턴 `01000000010100000000000000000000`의 값은 3.5이다.

답: ☐ T ☐ F

### Q90.
`ja`는 signed 비교 결과에 따라 점프하는 명령어이다.

답: ☐ T ☐ F

### Q91.
아래 코드에서 `u_money`의 출력값은 1이다.

```c
unsigned short u_money = USHRT_MAX;   // 65535
u_money = u_money + 2;
printf("u_money = %d", u_money);
```

답: ☐ T ☐ F

### Q92.
`int * g3(int buf[], long idx){ return &buf[idx]; }`를 컴파일하면 `lea (%rdi,%rsi,8),%rax`가 생성된다.

답: ☐ T ☐ F

### Q93.
Double precision에서 가장 작은 양의 normalized 값은 $2^{-1022}$이다.

답: ☐ T ☐ F

### Q94.
`readelf -h hello`로 ELF header를 보면 `Data` 항목에 `2's complement, little endian`이 표시된다.

답: ☐ T ☐ F

### Q95.
ISA가 같은 프로세서들은 microarchitecture도 같아야 한다.

답: ☐ T ☐ F

### Q96.
`int y`의 값과 관계없이 `y + ~y`는 0이다.

답: ☐ T ☐ F

### Q97.
일반 `movq` 명령어의 immediate operand는 32비트 값이며, 64비트로 sign-extend되어 사용된다.

답: ☐ T ☐ F

### Q98.
아래 `f2`의 어셈블리에는 조건부 jump 1개와 무조건 jump 1개가 있다.

```c
long f2(long x, long y) {
    long result;
    if (x > y) result = x - y;
    else       result = y - x;
    result = 3 * result;
    return result;
}
```

답: ☐ T ☐ F

### Q99.
1/10은 2진 fixed point로 `0.0001100110011[0011]…`처럼 반복되므로 float로 정확히 표현할 수 없다.

답: ☐ T ☐ F

### Q100.
`void f2(){ *((long *)0x104) = -1; }`와 `void f3(){ long *xp = (long *)0x104; *xp = -1; }`는 같은 명령어 `movq $0xffffffffffffffff,0x104`로 컴파일된다.

답: ☐ T ☐ F
