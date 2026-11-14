# Week 5: Machine Level Representation Basics (기계 수준 표현 기초)

교재: Computer Systems 3rd Edition by Bryant, Chap 3 (p157–361).

## 0. 오늘의 목표

- C 코드가 기계어(어셈블리)로 어떻게 표현되는지 이해한다.
- 예: `swap()` 함수의 C 코드 ↔ 디스어셈블 결과

```c
void swap(long *xp, long *yp) {
    long t1 = *xp;
    *xp = *yp;
    *yp = t1;
}
```
```
mov  (%rdi),%rax
mov  (%rsi),%rdx
mov  %rdx,(%rdi)
mov  %rax,(%rsi)
retq
```

## 1. Intel CPU 역사

| CPU | 연도 | 특징 |
|---|---|---|
| 8080 | 1974 | 8비트, 64KB 메모리 지원 |
| 8086 | 1978 | 16비트, 5–10 MHz, 29K 트랜지스터 |
| 80386 | 1985 | **최초의 32비트** (i386, x86, IA32 ISA), 3단계 파이프라인 |
| 80486 | 1989 | 성능 향상, FPU(부동소수점 장치) 내장 |
| Pentium | 1993 | 5단계 파이프라인 |
| Pentium 4E | 2004 | **최초의 64비트 Intel x86** (x86-64 ISA) |
| Core 2 | 2006 | 최초의 멀티코어 Intel 프로세서 |
| Core i7 | 2008 | 4코어 |
| Core i9 | 2017 | 최대 24코어 |

- 발전 방향: 더 넓은 비트 폭, 더 많은 트랜지스터, 더 깊은 파이프라인, 더 넓은 superscalar, 더 높은 클럭, 더 많은 코어.
- **Word size는 시스템의 근본적인 파라미터이다.**

## 2. ISA (Instruction Set Architecture)

### ISA란?
- 명령어 집합을 정의하는 **추상 모델**. 명령어는 상태(**레지스터 + 메모리**)를 변경하며, 하드웨어 구현의 내부 세부사항은 숨긴다.
- 컴퓨터가 "무엇을" 하는지에 대한 논리적 관점 (물리적 관점이 아님).
- **SW와 HW의 경계** 역할을 한다.
- ISA는 일종의 **ADT(Abstract Data Type)** 로 볼 수 있다.
  - ADT: 연산과 상태를 정의하고 구현 세부사항을 추상화. 예: stack (push, pop, create_stack, is_empty)
  - ISA: 명령어(연산)와 레지스터+메모리(상태)를 정의.
- 예시 ISA: IA32(x86), x86-64, IA64, ARM

### Microarchitecture
- ISA의 **구현체**.
- 서로 다른 microarchitecture라도 같은 ISA를 공유할 수 있다.
  - 프로그래머 입장에서는 Pentium과 AMD Athlon이 같은 ISA를 지원하므로 명령어에 대해 같은 동작을 보인다.
- 예:
  - x86: Pentium, Pentium Pro, AMD Athlon
  - x86-64: Intel i3, i5, i7, i9
  - IA64: Itanium 시리즈
  - ARM: ARM7, ARM11, ARM Cortex-A53 (거의 모든 휴대폰에 사용)

### ISA 분류: CISC vs RISC

| CISC (Complex Instruction Set Computer) | RISC (Reduced Instruction Set Computer) |
|---|---|
| 명령어 수가 매우 많음 (Intel 명령어 문서 1,200페이지 이상) | 명령어 수가 적음 (보통 100개 미만) |
| 복잡한 명령어 덕분에 코드 크기가 작음 | 단순한 명령어 → 훨씬 적은 하드웨어로 구현 가능 |
| **가변 길이** 명령어 인코딩 (1~15바이트) | **고정 길이** 명령어 인코딩 (보통 4바이트) |
| x86, x86-64 (Intel, AMD) | ARM, MIPS, RISC-V |

### Instruction(명령어)의 구성
- **Opcode**: 수행할 연산을 지정
  - 메모리 ↔ 레지스터 간 데이터 이동 (예: `mov`)
  - 레지스터/메모리 데이터에 대한 산술 연산 (예: `add`, `sub`)
  - 프로그램의 다른 위치로 분기 (예: `jmp`)
- **Operands**: 연산의 파라미터
  - Immediate(상수), Register, Memory address
  - 예: `add $1, %rax`, `jmp 0x1000`, `syscall`(operand 없음)
- 가변 길이: Opcode + 가변 개수의 operand / 고정 길이: Opcode + 정해진 개수의 operand

## 3. Machine State (프로그래머 관점의 기계 상태)

- 일반적으로 **Register + Memory** 상태.
- CPU 내부:
  - 범용 레지스터 16개, `%rip`(Instruction pointer), `%rflags`(상태 및 condition codes)
  - ALU, Cache 등은 **ISA 수준에서 보이지 않음(transparent)**.
- Memory: Code(Instructions), Data, Stack 영역.
- **아키텍처의 레지스터와 메모리 addressing mode를 이해하는 것이 핵심이다.**

## 4. x86-64 레지스터

### 범용 레지스터 (General-Purpose Registers)
- 16개: `%rax, %rbx, %rcx, %rdx, %rsi, %rdi, %rbp, %rsp, %r8 ~ %r15`
- 하위 호환성(legacy compatibility)을 위해 각 레지스터는 여러 크기로 접근 가능:

| 크기 | 이름 | 예 (rax 계열) | 예 (r8 계열) |
|---|---|---|---|
| 64-bit | quad word | `%rax` | `%r8` |
| 32-bit | double word | `%eax` | `%r8d` |
| 16-bit | word | `%ax` | `%r8w` |
| 8-bit | byte | `%al` | `%r8b` |

- 역사: 원래 8086은 16비트 레지스터(8비트 접근도 지원) → IA32에서 32비트로 확장(`%e..`) → 현재 x86-64(`%r..`).
- 부동소수점 코드는 완전히 다른 명령어/레지스터 집합을 사용한다. **이 강의에서는 정수에 집중한다.**
- `%rsp`는 스택 포인터로 특수 용도로 예약되어 있다.

### 기타 레지스터
- `%rip`: **Instruction Pointer** — 다음에 실행할 명령어의 주소를 저장.
- `%rflags` (`%eflags`): **Flags Register** — 프로세서 상태를 관리하는 플래그 저장.
  - Condition codes: **CF, ZF, SF, OF**

## 5. x86-64/Linux 기본 Calling Convention (System V AMD64 ABI)

- **인자 전달**: 처음 6개의 인자는 왼쪽부터 순서대로 레지스터에 전달

| 레지스터 | 용도 |
|---|---|
| `%rdi` | 1번째 인자 |
| `%rsi` | 2번째 인자 |
| `%rdx` | 3번째 인자 |
| `%rcx` | 4번째 인자 |
| `%r8` | 5번째 인자 |
| `%r9` | 6번째 인자 |
| `%rax` | **반환값** |

- 7번째 이후 인자는 **스택**으로 전달.
- 예:
```c
long func(long *xp, long x) {   // xp: %rdi, x: %rsi
    *xp = x;
    return x;                   // 반환값: %rax
}
```
```
mov  %rsi,(%rdi)
mov  %rsi,%rax
retq
```

## 6. C를 어셈블리로 컴파일하기

### 방법 1: 컴파일러로 어셈블리 파일 생성
```
$ gcc -S ex.c -Og -fcf-protection=none
```
- `.s` 파일 생성. `.loc`, `.cfi_startproc` 같은 지시어(directive)와 함께 `movq %rsi,(%rdi)` 등이 출력됨.
- 어셈블리는 사람이 읽기 쉬운 중간 수준 코드이며, 하드웨어는 이진 표현만 "이해"한다.

### 방법 2: GNU gdb 사용
```
$ gcc -c -Og ex.c -fcf-protection=none
$ gdb ex.o
(gdb) disas func
```

- 옵션 참고: Intel x86-64에는 보호 메커니즘이 많으므로, 학습 시 `-fno-stack-protector`, `-fcf-protection=none`, `-mno-red-zone` 등으로 비활성화할 수 있다.
- `-Og`: 디버깅에 적합한 수준의 최적화.

### Disassembler (objdump)
```
$ objdump -d ex.o
0000000000000000 <swap>:
   0:  48 8b 07   mov  (%rdi),%rax
   3:  48 8b 16   mov  (%rsi),%rdx
   6:  48 89 17   mov  %rdx,(%rdi)
   9:  48 89 06   mov  %rax,(%rsi)
   c:  c3         retq
```
- Object code를 분석하는 유용한 도구. 명령어들의 비트 패턴을 분석한다.
- `a.out`(실행 파일)이나 `.o` 파일 모두에 사용 가능.
- 왼쪽 숫자는 오프셋, 가운데는 기계어 바이트(가변 길이: 3바이트, 1바이트 등), 오른쪽은 어셈블리.

## 7. 어셈블리 문법: AT&T vs Intel

| 항목 | AT&T | Intel |
|---|---|---|
| 사용 환경 | Unix 계열 (Linux, macOS) | Windows, Intel 공식 문서 |
| Operand 순서 | `mov src, dst` | `mov dst, src` |
| 레지스터 접두사 | `%rax` | `rax` (`%` 생략) |
| 메모리 접근 표기 | `(%rdi)` | `QWORD PTR [rdi]` (대괄호) |

- 예: AT&T `mov (%rdi),%rax` ↔ Intel `mov rax,QWORD PTR [rdi]`
- **어떤 문법을 쓰든 어셈블러가 생성하는 이진 값은 동일하다.**
- 전환 방법:
  1. `objdump -M intel -d ex.o`
  2. gdb에서 `set disassembly-flavor intel` (또는 `att`)

## 8. mov 명령어: 데이터 이동

```
mov src, dst
```

### Operand 유형
- **Immediate**: 상수 정수 데이터
  - 예: `$0x400`, `$-533` — C 상수와 비슷하지만 `$` 접두사를 붙임
  - **src로만 사용 가능**
- **Register**: 16개 정수 레지스터 중 하나
  - 예: `%rax`, `%r13`
  - 일부는 특정 명령어에서 특수 용도, 특히 `%rsp`는 특수 용도로 예약
- **Memory**: 레지스터 등으로 주어진 메모리 위치/주소
  - 가장 간단한 예: `(%rax)`, `0x400`
  - 다양한 "addressing mode"가 있음
  - **src, dst 중 최대 하나만 메모리** 가능 (src가 메모리면 dst는 레지스터여야 함)

### movq Operand 조합

| Source | Dest | 예시 | C 대응 |
|---|---|---|---|
| Imm | Reg | `movq $0x4,%rax` | `temp = 0x4;` |
| Imm | Mem | `movq $-147,(%rax)` | `*p = -147;` |
| Reg | Reg | `movq %rax,%rdx` | `temp2 = temp1;` |
| Reg | Mem | `movq %rax,(%rdx)` | `*p = temp;` |
| Mem | Reg | `movq (%rax),%rdx` | `temp = *p;` |

- **메모리 → 메모리 이동은 단일 명령어로 불가능하다.**

## 9. Operand Forms (기본)

| Form | Operand Value | 설명 |
|---|---|---|
| `$imm` | imm | Immediate (상수 값 자체) |
| `%ra` | R[ra] | 레지스터 ra의 값 |
| `imm` | M[imm] | Absolute(절대) 메모리 주소 imm에 있는 값 |

- `mov 0x104, ____` : 주소 0x104의 값을 읽어옴 (**load**)
- `mov ____, 0x104` : 주소 0x104의 메모리에 저장 (**store**)
- 주의: `$0x104`(상수) vs `0x104`(메모리 주소)를 구분해야 한다.

### Practice #1
가정: 각 명령어는 독립적으로 실행, 주소 0x40에 값 5가 저장됨, `%rbx`에 8이 저장됨.

| 명령어 | 결과 |
|---|---|
| `mov $0x40,%rax` | `%rax` = 0x40 (상수) |
| `mov 0x40,%rax` | `%rax` = 5 (주소 0x40의 값) |
| `mov %rbx,0x50` | 주소 0x50의 메모리 = 8 |

## 10. C → 기계어 변환 예제 (1)~(3): Immediate / Absolute 주소

### (1) 레지스터에 값 복사 — 반환값은 `%rax`
```c
long f1(long x) { x = -1; return x; }
```
```
mov  $0xffffffffffffffff,%rax
retq
```
- 반환값이 `%rax`에 들어가므로, 컴파일러는 `x`(`%rdi`)를 거치지 않고 바로 `%rax`에 -1을 넣는다.

### (2) 메모리 주소 0x104에 값 저장
```c
void f2() { *((long *)0x104) = -1; }
void f3() { long *xp = (long *)0x104; *xp = -1; }
```
```
movq  $0xffffffffffffffff,0x104
retq
```
- f2와 f3는 같은 기계어로 컴파일된다.
- 단항 `*` 연산자는 C/C++에서 dereference(역참조, indirection) 연산자로, 포인터 주소에 있는 값을 반환한다.

### (3) 주소 0x104의 값을 읽어오기
```c
long f4()      { long ret = *((long *)0x104); return ret; }
void f4dummy() { long ret = *((long *)0x104); }
```
```
f4:       mov  0x104,%rax     # 반환값이므로 %rax에 load
          retq
f4dummy:  retq                # 결과를 사용하지 않으므로 최적화로 제거
```

### Quiz: 인자 x를 주소 0x104에 저장
```c
void f5(long x) { *((long *)0x104) = x; }
```
```
mov  %rdi,0x104
retq
```

## 11. Addressing Mode

### Indirect Addressing Mode
| Form | Operand Value |
|---|---|
| `(ra)` | M[R[ra]] |
| `imm(rb)` | M[imm + R[rb]] |

- 레지스터 R이 메모리 주소를 지정.
- `mov (%rbx), ____` : `%rbx`에 저장된 주소의 값을 읽음
- `mov ____, (%rbx)` : `%rbx`에 저장된 주소의 메모리에 저장
- **Displacement** 사용 가능: 상수 D는 offset, 레지스터 R은 메모리 영역의 base
  - `mov 0x10(%rax), ____` : (0x10 + `%rax`) 주소의 값을 읽음

### Indexed Addressing Mode
| Form | Operand Value |
|---|---|
| `(rb, ri)` | M[R[rb] + R[ri]] |
| `imm(rb, ri)` | M[imm + R[rb] + R[ri]] |

- Base 레지스터와 Index 레지스터를 더한 값이 주소.
- Displacement(양수/음수 상수), rb, ri 중 생략된 것은 0으로 취급.

### Scaled Indexed Addressing Mode
| Form | Operand Value |
|---|---|
| `imm(rb, ri, s)` | M[imm + R[rb] + R[ri] × s] |

- Index 레지스터에 **scaling factor s**를 곱한다.
- **s는 반드시 1, 2, 4, 8 중 하나** (하드코딩).
- 이유: C의 포인터 연산은 가리키는 데이터 타입 크기만큼 스케일링되기 때문 (char=1, short=2, int=4, long/포인터=8).
- 예:
  - `mov 0x4(%rax,%rdx,2), ____` : 주소 = 0x4 + `%rax` + 2×`%rdx`
  - `mov ____, 0x4(,%rdx,4)` : 주소 = 4×`%rdx` + 0x4 (base 생략 → 0)

### 전체 일반형
```
Imm(rb, ri, s)  →  M[Imm + R[rb] + R[ri] × s]
```

### Practice #2
`%rdx` = 0xf000, `%rcx` = 0x0100

| Expression | Address Computation | Address |
|---|---|---|
| `0x8(%rdx)` | 0xf000 + 0x8 | 0xf008 |
| `(%rdx,%rcx)` | 0xf000 + 0x100 | 0xf100 |
| `(%rdx,%rcx,4)` | 0xf000 + 4×0x100 | 0xf400 |
| `0x80(,%rdx,2)` | 2×0xf000 + 0x80 | 0x1e080 |

## 12. C → 기계어 변환 예제 (4)~(6): Addressing Mode 활용

### (4) Indirect addressing: `*xp = x`
```c
void f6(long *xp, long x) { *xp = x; }   // xp: %rdi, x: %rsi
```
```
mov  %rsi,(%rdi)
retq
```

### (5) Scaled indexed addressing: 배열 접근
```c
void f7(long buf[], long idx) { buf[idx] = -1; }   // buf: %rdi, idx: %rsi
```
```
movq  $0xffffffffffffffff,(%rdi,%rsi,8)
retq
```
- `buf[idx]`의 주소 = buf + idx × sizeof(long) = `%rdi` + `%rsi`×8

### (6) 메모리 → 메모리 복사
```c
void f8(long buf[], long *xp, long idx) { buf[idx] = *xp; }
// buf: %rdi, xp: %rsi, idx: %rdx
```
```
mov  (%rsi),%rax          # 먼저 임시 레지스터로 load
mov  %rax,(%rdi,%rdx,8)   # 그 다음 메모리로 store
retq
```
- x86에는 두 개의 메모리 주소를 가지는 mov 인코딩이 없으므로, **임시 레지스터를 거쳐서** 복사한다.

## 13. 종합 예제: swap()

```c
void swap(long *xp, long *yp) {
    long t0 = *xp;
    long t1 = *yp;
    *xp = t1;
    *yp = t0;
}
```

| Register | Value |
|---|---|
| `%rdi` | xp |
| `%rsi` | yp |
| `%rax` | t0 |
| `%rdx` | t1 |

```
swap:
   movq  (%rdi), %rax   # t0 = *xp
   movq  (%rsi), %rdx   # t1 = *yp
   movq  %rdx, (%rdi)   # *xp = t1
   movq  %rax, (%rsi)   # *yp = t0
   ret
```
- 메모리→메모리 직접 이동이 불가하므로 두 값을 각각 레지스터에 load한 뒤 서로 바꿔 store한다.

## 핵심 정리

1. **ISA**는 SW/HW의 경계이며, 명령어와 상태(레지스터+메모리)를 정의하는 추상 모델이다. Microarchitecture는 그 구현이다.
2. x86-64는 **CISC**(가변 길이 명령어), ARM/RISC-V는 **RISC**(고정 길이 명령어).
3. x86-64는 범용 레지스터 16개를 가지며, 64/32/16/8비트 단위로 접근 가능하다.
4. Calling convention: 인자는 `%rdi, %rsi, %rdx, %rcx, %r8, %r9` 순, 반환값은 `%rax`.
5. AT&T 문법은 `mov src, dst`, `%` 레지스터, `()` 메모리 표기. Intel은 반대 순서, `[]` 표기.
6. `mov`의 operand: `$`Immediate, `%`Register, Memory. **메모리→메모리 이동은 불가**.
7. Addressing mode 일반형: `Imm(rb, ri, s)` → `M[Imm + R[rb] + R[ri]×s]`, s ∈ {1, 2, 4, 8}.
