# TF_quiz 3

- 범위: week1 ~ week7 (A Tour of Computer Systems ~ Control Flow)
- 환경 가정: x86-64 Linux, gcc, `-fwrapv`, `-fcf-protection=none`, `-Og` (별도 표기가 없으면)
- 번호는 `TF_quiz_2.md`(Q51~Q100)에 이어서 Q101~Q150
- 정답: `TF_quiz_3_answer.md`

---

### Q101.
`%rax = 0xffffffffffffffff`이고 메모리 `0x200 ~ 0x207`에 바이트 `98 ba dc fe 10 32 54 76`이 저장되어 있다. `movsbl 0x200, %eax` 실행 후 `%rax`는 `0x00000000ffffff98`이다.

답: ☐ T ☐ F

### Q102.
w = 32일 때 C 식 `-2147483647-1 == 2147483648U`의 결과는 1(참)이다.

답: ☐ T ☐ F

### Q103.
아래 `f4`에 `cnt = 50`을 넣으면 반환값은 147이다.

```c
long f4(long cnt) {
    while (cnt > 100) { cnt--; }
    return 3 * cnt;
}
```

답: ☐ T ☐ F

### Q104.
`float f = 0.75f;`의 비트 패턴을 16진수로 나타내면 `0x3F600000`이다.

답: ☐ T ☐ F

### Q105.
어셈블러가 만든 object file(`hello.o`)은 다른 파일에 정의된 함수에 대한 참조를 포함할 수 있으므로, 그 자체로는 실행할 수 없다.

답: ☐ T ☐ F

### Q106.
`%rdx = 0x1000`, `%rcx = 0x20`일 때 operand `(,%rcx,4)`가 가리키는 메모리 주소는 `0x1080`이다.

답: ☐ T ☐ F

### Q107.
`unsigned char c = 0xF0; int i = c;`를 실행하면 `i`의 비트 패턴은 `0xFFFFFFF0`이다.

답: ☐ T ☐ F

### Q108.
8-bit에서 `a = 0x80`, `b = 0x01`일 때 `cmp b, a`를 실행하면 SF = 0, OF = 1이 되므로 `jl`은 점프한다.

답: ☐ T ☐ F

### Q109.
`double d = 2.5; int i = (int) d;`를 실행하면, 기본 반올림 모드가 round-to-even이므로 `i`는 2가 아니라 3이다.

답: ☐ T ☐ F

### Q110.
`long f(long x){ return x*20; }`는 `lea (%rdi,%rdi,4),%rax`와 `shl $0x2,%rax`로 컴파일될 수 있다.

답: ☐ T ☐ F

### Q111.
Flash memory는 SRAM, DRAM과 마찬가지로 volatile 메모리이다.

답: ☐ T ☐ F

### Q112.
x86-64/Linux calling convention에서 함수의 4번째 정수 인자는 `%rdx` 레지스터로 전달된다.

답: ☐ T ☐ F

### Q113.
"오른쪽부터 처음 나오는 1까지는 복사하고 나머지는 반전" 규칙으로 −12의 8-bit 2의 보수를 구하면 `11110100`(`0xF4`)이다.

답: ☐ T ☐ F

### Q114.
`not %rax`는 `%rax`의 값을 2의 보수 방식으로 부호 반전(`-%rax`)한다.

답: ☐ T ☐ F

### Q115.
gcc가 `do-while` 루프를 번역하면, `while` 루프처럼 맨 앞에 테스트 부분으로 가는 무조건 `jmp`가 생긴다.

답: ☐ T ☐ F

### Q116.
`int x = 16777217;`(= 2²⁴ + 1)일 때 `(int)(float)x == x`는 참이다.

답: ☐ T ☐ F

### Q117.
x86-64/Linux calling convention에서 7번째 이후의 정수 인자는 스택으로 전달된다.

답: ☐ T ☐ F

### Q118.
아래 코드의 출력은 `s_money = -32768`이다.

```c
short s_money = SHRT_MAX;   // 32767
s_money = s_money + 1;
printf("s_money = %d", s_money);
```

답: ☐ T ☐ F

### Q119.
8-bit 값 `0xB4`(`10110100`)에 `sar $3`을 적용하면 `0x16`이 된다.

답: ☐ T ☐ F

### Q120.
`cmov`는 then 값과 else 값 중 조건에 맞는 쪽만 계산하므로, 분기 없이도 불필요한 계산을 하지 않는다.

답: ☐ T ☐ F

### Q121.
C에서 `1.0/0.0`의 결과는 +∞이고, `∞ − ∞`의 결과는 NaN이다.

답: ☐ T ☐ F

### Q122.
Intel Core i7의 캐시 계층에서 L3 unified cache는 코어마다 하나씩 따로 있는 private cache이다.

답: ☐ T ☐ F

### Q123.
`mov %rax, $0x10`은 `%rax`의 값을 상수 `0x10`에 저장하는 유효한 명령어이다.

답: ☐ T ☐ F

### Q124.
`int x, y;`에 대해 `int64_t pll = (int64_t)(x * y);`로 쓰면 곱셈 결과를 64비트로 캐스팅하므로 overflow 없이 정확한 곱을 얻는다.

답: ☐ T ☐ F

### Q125.
`void f(unsigned long *x, unsigned char y){ *x = y; }`는 `movzbq` 대신 `movzbl %sil,%esi`와 `mov %rsi,(%rdi)`로 컴파일되며, 결과는 같다.

답: ☐ T ☐ F

### Q126.
`setX` 명령어는 레지스터뿐 아니라 `setg (%rdi)`처럼 메모리 바이트를 목적지로 사용할 수 있다.

답: ☐ T ☐ F

### Q127.
부동소수점 덧셈에서 두 수의 지수가 다르면, 지수가 큰 쪽의 가수를 왼쪽으로 shift하여 지수를 맞춘다.

답: ☐ T ☐ F

### Q128.
`long f1(long x){ x = -1; return x; }`는 `%rdi`를 거치지 않고 `mov $0xffffffffffffffff,%rax` 한 줄과 `retq`로 컴파일된다.

답: ☐ T ☐ F

### Q129.
Big Endian 머신에서 `int x = 0x01234567;`이고 `&x == 0x100`이면, 주소 `0x100`에는 `0x01`이 저장된다.

답: ☐ T ☐ F

### Q130.
`void f(char *x, long y){ *x = y; }`처럼 큰 타입을 작은 타입으로 줄이는 truncation에는 별도의 변환 명령어 없이 `mov %sil,(%rdi)`만 사용된다.

답: ☐ T ☐ F

### Q131.
강의의 `f5`(`for (long i = 0; i < n; i++) sum += arr[i];`)에서 `i < n` 비교 후 body로 돌아가는 점프는 `jb`이다.

답: ☐ T ☐ F

### Q132.
5.625를 2진 fixed point로 나타내면 `101.101`₂이다.

답: ☐ T ☐ F

### Q133.
DRAM은 비트당 트랜지스터 1개와 커패시터를 사용하므로 SRAM보다 밀도가 높고, 주기적인 refresh가 필요하다.

답: ☐ T ☐ F

### Q134.
unsigned 덧셈 `s = x + y`에서 overflow 발생 여부는 `s < x`인지로 판단할 수 있다.

답: ☐ T ☐ F

### Q135.
`%rdx = 0x1000`, `%rcx = 0x20`일 때 operand `0x10(%rdx,%rcx,8)`가 가리키는 메모리 주소는 `0x1110`이다.

답: ☐ T ☐ F

### Q136.
`cltq`는 `movslq %eax,%rax`와 같은 동작을 하지만 인코딩이 더 짧다.

답: ☐ T ☐ F

### Q137.
`%rdi = 0`일 때 `test %rdi,%rdi`를 실행하면 ZF = 1, SF = 0이 된다.

답: ☐ T ☐ F

### Q138.
`1.11100`₂를 소수점 아래 2비트로 round-to-even 하면 `10.00`₂이 된다.

답: ☐ T ☐ F

### Q139.
x86-64의 LP64 데이터 모델에서 `int`, `long`, 포인터는 모두 64비트이다.

답: ☐ T ☐ F

### Q140.
ALU와 cache는 ISA 수준에서 프로그래머에게 보이는 machine state에 포함된다.

답: ☐ T ☐ F

### Q141.
`%rax = 0`이고 메모리 `0x200 ~ 0x207`에 바이트 `98 ba dc fe 10 32 54 76`이 저장되어 있다. `movsbq 0x207, %rax` 실행 후 `%rax`는 `0xffffffffffffff76`이다.

답: ☐ T ☐ F

### Q142.
어셈블리의 symbolic label(예: `.L1:`)이 가리키는 실제 주소는 object file을 만들 때 assembler가 결정해 인코딩한다.

답: ☐ T ☐ F

### Q143.
부동소수점 곱셈에서는 두 수의 지수를 더하고, 가수를 곱하며, 결과의 부호는 두 부호의 XOR로 정한다.

답: ☐ T ☐ F

### Q144.
`x * 14`는 `(x << 4) - (x << 2)`로 계산할 수 있다.

답: ☐ T ☐ F

### Q145.
최초의 32비트 Intel x86 프로세서는 8086이다.

답: ☐ T ☐ F

### Q146.
`lea 6(%rax), %rdx`는 주소 `6 + %rax`의 메모리에서 데이터를 읽어 `%rdx`에 저장한다.

답: ☐ T ☐ F

### Q147.
`jbe`(jump if below or equal)의 조건은 `CF | ZF`이다.

답: ☐ T ☐ F

### Q148.
IEEE 754 방식에서 exponent 필드가 5비트이면 bias는 15이다.

답: ☐ T ☐ F

### Q149.
강의의 연산별 상대 비용 표에서 포인터 역참조는 덧셈/뺄셈보다 비싸다.

답: ☐ T ☐ F

### Q150.
디스크 I/O 접근(약 7ms)은 프로세서 사이클(0.5ns)보다 약 1,000만 배 이상 느리다.

답: ☐ T ☐ F
