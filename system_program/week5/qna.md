# Week 5 — Q&A

## Q1. Microarchitecture가 하드웨어 구성과 성능이 달라도, ISA가 같으면 같은 instruction과 동작을 가진다는 거야?

맞다. 다만 **"동작이 같다"는 건 프로그래머가 관찰할 수 있는 결과(ISA 수준의 동작)가 같다**는 뜻이고, 내부에서 그 결과를 만드는 방식까지 같다는 뜻은 아니다.

**ISA = 약속(인터페이스), Microarchitecture = 그 약속을 지키는 구현**

ISA가 정하는 것 (같은 ISA면 모든 CPU에서 동일):
- 어떤 instruction이 있고, 어떤 바이트로 인코딩되는지 (예: `mov`, `add`의 machine code)
- 각 instruction이 **상태(레지스터 + 메모리)를 어떻게 바꾸는지**
- 레지스터의 종류와 개수 (x86-64면 `%rax`~`%r15`의 16개 범용 레지스터)

Microarchitecture가 정하는 것 (CPU마다 다를 수 있음):
- pipeline 단계 수, cache 크기와 구조, branch prediction 방식
- out-of-order execution 여부, 실행 유닛 개수, 클럭 속도
- 내부적으로 instruction을 더 작은 micro-op으로 쪼개는지 여부

**결과적으로**
- 같은 x86-64 바이너리를 Intel i7이든 AMD Ryzen이든 **다시 컴파일하지 않고 그대로 실행**할 수 있다.
- 예를 들어 `addq %rsi, %rax`를 실행한 뒤 `%rax`에 들어 있는 값은 어느 CPU에서나 같다.
- 하지만 **얼마나 빨리** 실행되는지(사이클 수, 처리량), 전력 소모 등은 다르다.

**비유**: ISA는 "자동차는 핸들·액셀·브레이크로 조작한다"는 규칙이고, microarchitecture는 엔진 설계다. 운전자(프로그래머)는 어떤 차든 같은 방식으로 조작하고 같은 방향으로 움직이지만, 가속 성능이나 연비는 차마다 다르다.

**참고(예외적인 부분)**
- 같은 ISA 계열이라도 **확장 명령어**(예: AVX-512)는 일부 CPU에만 있을 수 있다. 이 경우 "기본 ISA는 같고, 추가 확장 지원 여부가 다르다"고 본다.
- 실행 시간 차이처럼 ISA가 정의하지 않는 부분은 관찰될 수 있다 (Spectre 같은 side-channel 공격이 이 차이를 이용한다). 그래도 instruction의 **결과값** 자체는 같다.

## Q2. CISC와 RISC의 차이를 더 자세히 설명해줘

### 1. 핵심 철학의 차이
- **CISC (Complex Instruction Set Computer)**: "명령어 하나가 많은 일을 하게 하자." 고수준 언어의 한 줄에 가까운 일을 instruction 하나로 처리하려 한다.
- **RISC (Reduced Instruction Set Computer)**: "명령어는 단순하게, 대신 빠르게 많이 실행하자." 각 instruction은 아주 작은 일만 하고, 하드웨어를 단순하게 만들어 빠르게 돌린다.

### 2. 항목별 비교

| 항목 | CISC (x86-64) | RISC (ARM, MIPS, RISC-V) |
|---|---|---|
| 명령어 수 | 매우 많음 (Intel 매뉴얼 1,200페이지 이상) | 적음 (보통 100개 미만) |
| 명령어 길이 | **가변 길이** (1~15바이트) | **고정 길이** (보통 4바이트) |
| 메모리 접근 | 산술 명령어가 메모리 operand를 직접 사용 가능 (`addq (%rdi), %rax`) | **Load/Store 구조**: 메모리 접근은 load/store만 가능, 연산은 레지스터끼리만 |
| Addressing mode | 다양함 (`Imm(rb, ri, s)` 등) | 단순함 (주로 base + offset) |
| 레지스터 수 | 상대적으로 적음 (x86-64 범용 16개) | 많음 (ARM64 31개, RISC-V 32개) |
| 코드 크기 | 작음 (명령어 하나가 많은 일을 하고, 짧은 명령어는 1바이트) | 큼 (같은 일에 명령어가 더 많이 필요) |
| 하드웨어(decoder) | 복잡함 | 단순함 → 적은 트랜지스터, 낮은 전력 |
| Pipeline | 명령어마다 길이·실행 시간이 달라 구현이 어려움 | 길이와 형식이 일정해 pipeline에 유리 |
| 대표 사용처 | PC, 서버 | 스마트폰, 임베디드, Apple Silicon |

### 3. 예시: 메모리 값에 레지스터 값을 더하기
C 코드: `*p += x;` (p는 `%rdi`, x는 `%rsi`)

**CISC (x86-64)**: 한 줄
```asm
addq %rsi, (%rdi)      # M[rdi] = M[rdi] + rsi
```

**RISC (RISC-V)**: 세 줄
```asm
ld   t0, 0(a0)         # load: t0 = M[a0]
add  t0, t0, a1        # 레지스터끼리 연산
sd   t0, 0(a0)         # store: M[a0] = t0
```
CISC는 load → add → store를 명령어 하나에 묶었고, RISC는 각 단계를 별개의 명령어로 표현한다.

### 4. 가변 길이 vs 고정 길이가 왜 중요한가
- **고정 길이(RISC)**: 다음 명령어 위치가 항상 `PC + 4`다. 여러 명령어를 동시에 fetch·decode하기 쉽고, opcode나 레지스터 필드가 항상 같은 비트 위치에 있어 decoder가 단순하다.
- **가변 길이(CISC)**: 현재 명령어를 어느 정도 decode해야 길이를 알 수 있고, 그래야 다음 명령어의 시작 위치를 안다. 대신 자주 쓰는 명령어를 짧게 만들 수 있어 코드 밀도가 높다.

### 5. 역사적 배경
- 1970년대에는 메모리가 비싸고 컴파일러가 약했다. 그래서 코드 크기를 줄이고 어셈블리를 직접 짜기 편한 CISC가 유리했다.
- 1980년대에 컴파일러가 발전하면서, 복잡한 명령어는 실제로 잘 쓰이지 않는다는 연구 결과가 나왔다. 그래서 단순한 명령어를 빠르게 실행하는 RISC가 등장했다 (Berkeley RISC, Stanford MIPS).

### 6. 현재: 경계가 흐려짐
- 현대 x86 CPU는 **겉(ISA)은 CISC지만 속(microarchitecture)은 RISC처럼** 동작한다. decoder가 복잡한 x86 instruction을 단순한 **micro-op(μop)** 여러 개로 쪼개고, 내부 core는 이 μop을 RISC 방식으로 pipeline에 넣어 실행한다. Q1에서 본 "ISA와 microarchitecture는 별개"라는 개념의 좋은 예다.
- 반대로 ARM 같은 RISC도 성능을 위해 명령어가 점점 늘어났다 (SIMD 등).
- 그래서 오늘날 둘의 차이는 성능보다는 **명령어 인코딩, decoder 복잡도, 전력 효율, 호환성(x86 레거시)**에서 더 크게 드러난다.

## Q3. Opcode는 강의에 나온 3가지 분류(데이터 이동, 산술 연산, 분기)밖에 없어?

아니다. 강의의 3가지는 **가장 기본적이고 대표적인 분류**를 예로 든 것이다. 실제 ISA에는 훨씬 다양한 opcode가 있다. 다만 크게 보면 대부분 다음 셋 중 하나로 묶을 수 있어서 이 3가지를 기본 틀로 소개한 것이다.
- **Data movement**: 데이터를 옮긴다.
- **Computation**: 데이터로 계산한다.
- **Control flow**: 다음에 실행할 instruction을 바꾼다.

### x86-64의 opcode 분류 (더 자세히)

| 분류 | 예시 명령어 | 설명 |
|---|---|---|
| 데이터 이동 | `mov`, `movzx`/`movsx`, `lea`, `xchg` | 레지스터·메모리 간 복사, zero/sign extension, 주소 계산 |
| 스택 조작 | `push`, `pop` | 스택에 값을 넣고 빼기 (`%rsp` 자동 변경) |
| 산술 연산 | `add`, `sub`, `imul`, `idiv`, `inc`, `dec`, `neg` | 정수 사칙연산 |
| 논리(비트) 연산 | `and`, `or`, `xor`, `not` | 비트 단위 연산 |
| 시프트/회전 | `shl`, `sar`, `shr`, `rol`, `ror` | 비트 이동 (week2의 `<<`, `>>`) |
| 비교/검사 | `cmp`, `test` | 결과값은 버리고 **condition code(flags)만 설정** |
| 조건부 동작 | `setcc`(`sete`, `setl` …), `cmovcc` | flags에 따라 값을 설정하거나 이동 |
| 분기 | `jmp`, `jcc`(`je`, `jne`, `jl` …) | 무조건/조건 분기 |
| 프로시저 호출 | `call`, `ret` | 함수 호출과 복귀 (스택에 return address 저장) |
| 시스템 | `syscall`, `int`, `hlt` | OS 커널 호출, 인터럽트, CPU 정지 |
| 부동소수점/SIMD | `addss`, `mulsd`, `vaddps`(AVX) 등 | 실수 연산, 여러 데이터를 한 번에 처리 (week3 floating point와 연결) |
| 형변환 | `cvtsi2sd`, `cvttsd2si`, `cqto` | 정수 ↔ 실수 변환, 부호 확장 |
| 동기화/원자적 연산 | `lock` prefix, `cmpxchg`, `xadd` | 멀티코어에서의 atomic 연산 |
| 기타 | `nop`, `cpuid`, `rdtsc` | 아무것도 안 함, CPU 정보 조회, 사이클 카운터 읽기 |

### 3가지 분류에 딱 맞지 않는 예
- **`cmp`, `test`**: 산술 연산(`sub`, `and`)과 같은 계산을 하지만 결과를 저장하지 않고 flags만 바꾼다. 다음에 올 조건 분기를 위한 준비 단계다.
- **`lea`**: 형식은 데이터 이동이지만, 실제로는 메모리에 접근하지 않고 **주소 계산식**만 수행한다. 그래서 산술 연산 용도로도 자주 쓰인다 (예: `lea (%rdi,%rdi,2), %rax` → `rax = rdi * 3`).
- **`syscall`**: 데이터를 옮기거나 계산하지 않는다. OS 커널로 제어를 넘기는 특수한 명령어다 (강의의 "operand 없는 instruction" 예시).
- **`push`/`call`**: 여러 동작을 한 번에 한다. 예를 들어 `call`은 "return address push + jump"를 합친 것이고, 이것이 Q2에서 본 CISC의 특징이다.

### 정리
강의의 3가지는 instruction이 하는 일을 **개념적으로 나눈 기본 틀**이고, 실제 x86-64에는 수천 개의 opcode 변형이 있다. CS:APP 교재 순서를 따른다면 이후 강의에서 `lea`, 산술/논리 연산, condition code와 `cmp`/`jcc`, `call`/`ret`을 차례로 다룰 가능성이 높다.

## Q4. 강의노트의 "[Instruction size]" 그림에서 고정 길이, 가변 길이는 뭐야?

슬라이드 그림:
```
Variable : [Opcode / # of operands][Operand 1][Operand 2] … [Operand n]
Fixed    : [Opcode][Operand 1][Operand 2][Operand 3]
```
이 그림은 **instruction 하나가 machine code(바이트)로 어떻게 인코딩되는지**를 보여준다. 바로 앞의 CISC/RISC 비교표에 있던 "Variable-size (1~15 bytes)" vs "Fixed-length (4 bytes)"를 그림으로 나타낸 것이다.

### 가변 길이 (Variable, CISC / x86-64)
- 맨 앞의 **opcode가 "무슨 연산인지"와 함께 "operand가 몇 개이고 어떤 형태인지"까지** 알려준다. 그래서 그림에 `Opcode / # of operands`라고 적혀 있다.
- operand 개수가 0개일 수도 n개일 수도 있고, 각 operand의 크기(레지스터 번호, 1/4/8바이트 상수, 메모리 주소 계산 정보 등)도 다르다. 그래서 **instruction마다 전체 길이가 달라진다**.
- 실제 x86-64 예시:

| 어셈블리 | machine code (16진수) | 길이 |
|---|---|---|
| `ret` | `c3` | 1바이트 |
| `push %rbp` | `55` | 1바이트 |
| `mov %rsp, %rbp` | `48 89 e5` | 3바이트 |
| `add $1, %rax` | `48 83 c0 01` | 4바이트 |
| `movabs $0x1122334455667788, %rax` | `48 b8 88 77 66 55 44 33 22 11` | 10바이트 |

  operand가 없는 `ret`은 1바이트이고, 8바이트 상수를 담는 `movabs`는 10바이트다. 마지막 예시에서 상수가 `88 77 … 11` 순서로 저장된 것은 week2에서 배운 little endian 때문이다.

### 고정 길이 (Fixed, RISC)
- **모든 instruction이 같은 크기**(보통 4바이트 = 32비트)이고, opcode와 operand 필드의 **위치와 개수가 형식으로 정해져 있다**. 그림에서 operand 칸이 3개로 고정된 이유다.
- 예: RISC-V의 `add x5, x6, x7` (R-type 형식, 32비트)
```
| funct7 (7) | rs2 (5) | rs1 (5) | funct3 (3) | rd (5) | opcode (7) |
|  0000000   |  00111  |  00110  |    000     | 00101  |  0110011   |
              x7=src2   x6=src1                 x5=dst   add 계열
```
  레지스터 번호는 항상 같은 비트 위치에 있다. operand가 필요 없는 명령어도 4바이트를 다 쓰고, 큰 상수는 한 instruction에 다 들어가지 않아서 여러 instruction으로 나눠 만든다.
  (실제 RISC-V는 opcode가 맨 오른쪽 하위 비트에 있다. 강의 그림은 위치보다 "칸 수가 정해져 있다"는 개념을 보여주는 것이다.)

### 왜 중요한가 (Q2와 연결)

| | 가변 길이 | 고정 길이 |
|---|---|---|
| 장점 | 자주 쓰는 명령어를 짧게 만들 수 있다 → **코드 크기가 작다** | 다음 명령어 위치가 항상 `PC + 4`다 → **fetch·decode가 단순하고 빠르며 pipeline에 유리하다** |
| 단점 | 앞 명령어를 decode해야 다음 명령어의 시작 위치를 알 수 있다 → **decoder가 복잡하다** | 짧게 표현할 수 있는 명령어도 4바이트를 다 쓴다 → **코드가 커진다**, 큰 상수를 한 번에 못 넣는다 |
