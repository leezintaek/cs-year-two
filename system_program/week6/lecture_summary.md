# Week 6: Machine-Level Representation — Arithmetic Operations (산술·논리 연산)

교재: Computer Systems 3rd Edition by Bryant, Chap 3 (3.4, 3.5 중심)

## 0. 중간고사 안내

- **일시**: 2026년 10월 20일 오후 8시
- **장소**: 하이테크센터 강당 (지하 1층)
- 시험에 제공되는 정보: `limits.h` 일부 (`SHRT_MIN/MAX`, `USHRT_MAX`, `INT_MIN/MAX`, `UINT_MAX`, `LONG_MIN/MAX` 등), x86-64 레지스터 정보 및 calling convention 일부
- **수업에서 다룬 환경 기준**으로 풀 것 (`-fcf-protection=none`, `-fwrapv` 등)

## 1. 오늘의 목표

산술·논리 연산이 어셈블리로 어떻게 표현되는지 이해한다.

```c
void func(long buf[], long x, long y) {
    buf[x] = 2*x - y;
}
```
```
lea  (%rsi,%rsi,1),%rax   # rax = x + x = 2x
sub  %rdx,%rax            # rax = 2x - y
mov  %rax,(%rdi,%rsi,8)   # buf[x] = rax
retq
```

같은 명령어라도 **operand 크기에 따라 여러 변형(variant)** 이 존재한다.

## 2. Data Sizes와 Suffix

| Intel 용어 | 크기 | Suffix | C 타입 예 |
|---|---|---|---|
| byte | 1 byte | `b` | `char` |
| word | 2 bytes | `w` | `short` |
| double word | 4 bytes | `l` | `int` |
| quad word | 8 bytes | `q` | `long`, 포인터 |

- Intel이 16비트 → 32비트로 확장된 역사 때문에 "word"가 **16비트**를 의미한다.
- Word size는 시스템의 근본적인 파라미터이다.

### 레지스터 이름 (8 / 4 / 2 / 1 byte)
| 64-bit | 32-bit | 16-bit | 8-bit |
|--------|--------|--------|-------|
| `%rax` | `%eax` | `%ax`  | `%al` |
| `%rdi` | `%edi` | `%di`  | `%dil`|
| `%rsi` | `%esi` | `%si`  | `%sil`|

## 3. mov 명령어 클래스

- `mov`: 데이터를 **변환 없이 복사**한다.
- 크기 지정 방법
  - suffix로 명시: `movb`, `movw`, `movl`, `movq`
  - suffix 생략 시 **레지스터 operand로부터 크기를 추론**
- 연습: 알맞은 suffix 고르기
  1. `movl %eax, (%rsp)` — `%eax`가 4바이트
  2. `movw (%rax), %dx` — `%dx`가 2바이트
  3. `movb $0xff, %bl` — `%bl`이 1바이트
  4. `mov_ (%rsp,%rdx,4), %dl` → `movb`
  5. `mov_ (%rdx), %rax` → `movq`
  6. `mov_ %dx, (%rax)` → `movw`
- 메모리 주소 계산에 쓰이는 레지스터(`%rsp`, `%rax` 등)는 항상 64비트지만, 이는 **데이터 크기와 무관**하다.

### mov는 해당 바이트만 갱신한다 — 단, movl은 예외!

`%rax = 0x0011223344556677`에서:

| 명령어 | 결과 `%rax` |
|---|---|
| `movb $-1, %al` | `0011 2233 4455 66ff` |
| `movw $-1, %ax` | `0011 2233 4455 ffff` |
| `movl $-1, %eax` | `0000 0000 ffff ffff` ← **상위 4바이트가 0이 됨** |
| `movq $-1, %rax` | `ffff ffff ffff ffff` |

- **목적지가 레지스터인 `movl`(32비트 연산)은 상위 32비트를 0으로 만든다.**

### 왜 movl은 상위 32비트를 0으로 만드는가?

1. **Make the Common Case Fast** (Patterson의 컴퓨터 구조 8대 아이디어 중 하나)
   - x86-64는 64비트를 지원하지만, 실제로는 **32비트 값/연산이 여전히 더 흔하다**.
   - 효율적인 연산: `movl`, `movzbl`, `movzwl`, `addl`, `orl`, `xorl` 등
   - 효율적인 인코딩: `movq`, `movabsq`, `cltq` 등
2. **Partial register dependency 제거 (pipelining)**
   - 파이프라인은 앞선 명령어가 끝나기 전에 다음 명령어를 겹쳐 실행한다. 명령어 간 의존성이 있으면 stall이 발생할 수 있다.
   - 레거시 x86 방식(`movw $0xFFFF, %ax` 후 `addq %rax, %rdi`): `%ax`만 바뀌므로 `%rax` 전체 값을 얻으려면 **이전 상위 비트 값까지 기다려야** 함 → partial register dependency.
   - x86-64 방식(`movl $0xFFFFFFFF, %eax`): 상위 32비트를 0으로 확정하므로 **이전 값에 대한 의존성이 사라지고**, 결과를 forwarding/out-of-order 실행에 활용할 수 있다.

## 4. movq와 movabsq

- `movq`는 레지스터/메모리 간 64비트 이동.
- 문제: immediate가 64비트라면 명령어가 너무 길어진다. 대부분의 상수는 32비트 안에 들어간다.
- 따라서 **일반 `movq`는 32비트 immediate만 지원하고, 이를 64비트로 sign-extend**한다.
  - 예: `movq $-1, %rax` → `ffff ffff ffff ffff` (7바이트 인코딩)
- **진짜 64비트 immediate가 필요할 때만 `movabsq`** 를 사용한다.
  - source: 64비트 immediate만 가능 / destination: 레지스터만 가능
  - 예: `movabsq $0x0011223344556677, %rax`

## 5. Truncation (축소)

- 작은 타입으로 줄이는 데는 **특별한 명령어가 필요 없다**. 목적지 크기에 맞는 레지스터 부분만 골라 쓰면 된다.
- 어셈블리는 **데이터 타입을 추적하지 않는다**.

```c
void f1(char  *x, long y) { *x = y; }   // mov %sil,(%rdi)
void f2(short *x, long y) { *x = y; }   // mov %si,(%rdi)
void f3(int   *x, long y) { *x = y; }   // mov %esi,(%rdi)
void f4(long  *x, long y) { *x = y; }   // mov %rsi,(%rdi)
```

### Practice #1: Data Movement (Little-Endian 주의)

초기: `%rax = ffff ffff 1234 5678`, 메모리 `0x200: 98 ba dc fe 10 32 54 76`

| 명령어 | 결과 `%rax` | 설명 |
|---|---|---|
| `movw 0x202, %ax` | `ffff ffff 1234 fedc` | 0x202~0x203 = `dc fe` → 0xfedc |
| `movb 0x207, %al` | `ffff ffff 1234 fe76` | 0x207 = 0x76 |
| `movl $0xfe1234, %eax` | `0000 0000 00fe 1234` | movl → 상위 32비트 0 |
| `movq 0x200, %rax` | `7654 3210 fedc ba98` | 8바이트, little-endian |
| `movabsq $0x0011223344556677, %rax` | `0011 2233 4455 6677` | |

- **Little-Endian**: 가장 낮은 자리(LS) 바이트가 시작 주소에 저장된다.

## 6. 확장: movs와 movz

작은 source를 큰 destination으로 복사할 때 사용. **목적지는 반드시 레지스터**여야 한다.

- 형식: `movs` / `movz` + (source 크기 suffix) + (destination 크기 suffix)
  - 예: `movsbq` = byte → quad, sign extend

### movs (Sign-extend)
- source의 **MSB를 복제**해 남은 상위 비트를 채운다 → **signed 타입** 변환에 사용.
- `movsbw`, `movsbl`, `movswl`, `movsbq`, `movswq`, `movslq`
- `cltq`: `%eax` → `%rax` sign-extend 전용 (= `movslq %eax, %rax`, 인코딩이 2바이트로 짧음)

```c
void f5(long *x, char  y) { *x = y; }  // movsbq %sil,%rsi ; mov %rsi,(%rdi)
void f6(long *x, short y) { *x = y; }  // movswq %si,%rsi  ; mov %rsi,(%rdi)
void f7(long *x, int   y) { *x = y; }  // movslq %esi,%rsi ; mov %rsi,(%rdi)
void f8(long *x, long  y) { *x = y; }  // mov %rsi,(%rdi)  (같은 타입 → 확장 불필요)
```

- C 문장 `=` 은 mov, **signed → movs**, char→long → `movsbq` 처럼 대응된다.
- 상수 타입 변환은 **컴파일 타임에** 수행된다: `*((long *)0x104) = -1;` → `mov $0xffffffffffffffff, %rax`

### movz (Zero-extend)
- 남은 상위 바이트를 **0으로 채운다** → **unsigned 타입** 변환에 사용.
- `movzbw`, `movzbl`, `movzwl`, `movzbq`, `movzwq`
- **`movzlq`는 존재하지 않는다!** → `movl`이 이미 상위 4바이트를 0으로 만들기 때문 (`movl` = 논리적으로 `movzlq`).
- 컴파일러는 `movzbq` 대신 `movzbl`을 자주 쓴다 (32비트 연산이 상위 32비트를 0으로 만들므로 결과가 같고 인코딩이 짧음).

```c
void f9 (unsigned long *x, unsigned char  y) { *x = y; }  // movzbl %sil,%esi ; mov %rsi,(%rdi)
void f10(unsigned long *x, unsigned short y) { *x = y; }  // movzwl %si,%esi  ; mov %rsi,(%rdi)
void f11(unsigned long *x, unsigned int   y) { *x = y; }  // mov %esi,%eax    ; mov %rax,(%rdi)
void f12(unsigned long *x, unsigned long  y) { *x = y; }  // mov %rsi,(%rdi)
```

### Practice #2, #3: movs / movz

초기: `%rax = 0`, 메모리 `0x200: 98 ba dc fe 10 32 54 76`

| 명령어 | 결과 `%rax` | 설명 |
|---|---|---|
| `movslq 0x200, %rax` | `ffff ffff fedc ba98` | 0xfedcba98의 MSB=1 → 상위 1로 채움 |
| `movsbw 0x201, %ax` | `ffff ffff fedc ffba` | 0xba → 16비트로 sign extend, 하위 2바이트만 갱신 |
| `movzwl 0x202, %eax` | `0000 0000 0000 fedc` | 32비트 이동이므로 상위 32비트도 0 (= 논리적 movzwq) |

## 7. 데이터 이동 → 산술 연산

- 지금까지: operand 준비 (레지스터↔메모리 이동, truncate, extend)
- 이제: 연산 (`lea`, 단항 연산, 이항 산술·논리 연산, shift)
- 대부분의 산술·논리 명령어는 **크기별 변형**이 있다: `addb`, `addw`, `addl`, `addq`
- 제어 흐름/스택 명령어는 **주소 크기(64비트)** 와 밀접: `callq`, `retq`, `pushq`, `popq`

## 8. lea (Load Effective Address)

`lea Src, Dst` — Src의 **유효 주소 자체**를 Dst에 복사한다. **메모리에서 아무것도 읽지 않는다.**

| operand | mov | lea |
|---|---|---|
| `6(%rax), %rdx` | 주소 (6+%rax)로 가서 **데이터**를 %rdx에 복사 | **(6+%rax) 값**을 %rdx에 복사 |
| `7(%rax,%rax,8), %rdx` | 주소 (7+%rax+8·%rax)의 데이터를 복사 | (7+%rax+8·%rax) 값을 복사 |

### 용도 1: 주소 계산 (`&x[i]` vs `x[i]`)
```c
long  g1(long buf[], long idx) { return buf[idx];  }  // mov (%rdi,%rsi,8),%rax
long *g2(long buf[], long idx) { return &buf[idx]; }  // lea (%rdi,%rsi,8),%rax
int  *g3(int  buf[], long idx) { return &buf[idx]; }  // lea (%rdi,%rsi,4),%rax  (원소 크기 4)
```

### 용도 2: 산술식 `x + k*y` 계산 (k = 1, 2, 4, 8)
- 일반 `add`/`imul`은 한 번에 연산 하나만 하지만, `lea`는 **덧셈+곱셈을 한 번에** 수행한다.
```c
long g4(long x) { return x*48; }
```
```
lea (%rdi,%rdi,2),%rax   # rax = 3x
shl $0x4,%rax            # rax = 3x * 16 = 48x
retq
```

## 9. Unary Operations (단항 연산)

operand 하나 (레지스터 또는 메모리)가 source이자 destination.

| 명령어 | 효과 | 설명 |
|---|---|---|
| `inc D` | D ← D + 1 | 증가 (C의 `++`) |
| `dec D` | D ← D − 1 | 감소 (C의 `--`) |
| `neg D` | D ← −D | 부호 반전 |
| `not D` | D ← ~D | 비트 반전 |

예 (교재 Problem 3.8, `%rax=0x100`, `%rcx=0x1`, `%rdx=0x3`, 메모리 `0x100:0xFF, 0x108:0xAB, 0x110:0x13, 0x118:0x11`):
- `decq %rcx` → `%rcx` = 0x0
- `incq 0x10(%rax)` → 주소 0x110 = 0x14

## 10. Binary Operations (이항 연산)

`op S, D` — **source가 먼저, destination이 나중**. D ← D op S

| 명령어 | 효과 |
|---|---|
| `add S, D` | D ← D + S |
| `sub S, D` | D ← D − S (**순서 주의**: D에서 S를 뺌) |
| `imul S, D` | D ← D × S |
| `xor S, D` | D ← D ^ S |
| `or S, D` | D ← D \| S |
| `and S, D` | D ← D & S |

- 두 번째 operand(D): 레지스터 또는 메모리
- 첫 번째 operand(S): 레지스터, 메모리, **immediate** 가능
- (mov와 마찬가지로 두 operand가 동시에 메모리일 수는 없다)

예 (위와 같은 초기값):
- `addq %rcx, (%rax)` → 0x100: 0xFF + 1 = **0x100**
- `subq %rdx, 8(%rax)` → 0x108: 0xAB − 3 = **0xA8**
- `imulq $16, (%rax,%rdx,8)` → 주소 0x100+3·8 = 0x118: 0x11 × 16 = **0x110**

## 11. Shift Operations

| 명령어 | 효과 | 설명 |
|---|---|---|
| `sal k, D` | D ← D << k | left shift |
| `shl k, D` | D ← D << k | left shift (`sal`과 동일) |
| `sar k, D` | D ← D >>ₐ k | **arithmetic** right shift: 왼쪽을 MSB로 채움 → **signed** |
| `shr k, D` | D ← D >>ₗ k | **logical** right shift: 왼쪽을 0으로 채움 → **unsigned** |

- C에서는 둘 다 `x >> k`로 쓰며, 타입(signed/unsigned)에 따라 컴파일러가 선택한다.

8비트 예:

| 연산 | x = `01100011` | x = `10010101` |
|---|---|---|
| `x << 4` | `00110000` | `01010000` |
| `x >> 4` (logical) | `00000110` | `00001001` |
| `x >> 4` (arithmetic) | `00000110` | `11111001` |

## 12. Practice: 산술 연산은 operand 크기에 맞춰 목적지를 갱신

초기: `%rax = 0x100`, `%rcx = 0x0f0f0000`, `%rbx = 0x10`, 메모리 `0x200: 98 ba dc fe 10 32 54 76`

| 명령어 | 결과 | 설명 |
|---|---|---|
| `leaq (%rax,%rcx), %rcx` | `%rcx = 0000 0000 0f0f 0100` | 0x100 + 0x0f0f0000 (메모리 접근 없음) |
| `addl (%rax,%rax), %ebx` | `%rbx = 0000 0000 fedc baa8` | 주소 0x200의 4바이트 0xfedcba98 + 0x10, 32비트 연산 → 상위 0 |
| `subw $4, %bx` | `%rbx = 0000 0000 fedc baa4` | 하위 2바이트만 갱신 |

## 13. C ↔ 어셈블리 변환 예제

```c
long arith(long x, long y, long z) {
    long t1 = x ^ y;
    long t2 = z * 48;
    long t3 = t1 & 0x0F0F0F0F;
    long t4 = t2 - t3;
    return t4;
}
```
```
arith:                         # x in %rdi, y in %rsi, z in %rdx
  xorq  %rsi, %rdi             # t1 = x ^ y
  leaq  (%rdx,%rdx,2), %rax    # 3*z
  salq  $4, %rax               # t2 = 16 * (3*z) = 48*z
  andl  $252645135, %edi       # t3 = t1 & 0x0F0F0F0F  (32비트 연산으로 충분)
  subq  %rdi, %rax             # return t2 - t3
  ret
```
- 레지스터 재사용: `%rdi` = x → t1 → t3, `%rax` = t2 → 반환값
- `andl`: 상수가 32비트 양수이므로 결과의 상위 32비트는 어차피 0 → 32비트 연산으로 충분 (Make the common case fast)

## 14. 강의 Quiz 풀이

> 반환값 `%rax`, 인자 `%rdi`, `%rsi`, `%rdx` 순. `objdump -t`의 크기는 마지막 명령어의 offset + 길이.

| 문제 | 답 |
|---|---|
| 3-1 `int i = s;` (short→int) | `movswl %di,%eax` (signed → movs, w→l) |
| 3-2 `unsigned int i = s;` (unsigned short→unsigned int) | `movzwl %di,%eax` (unsigned → movz) |
| 3-3 `lea (%rdi,%rdi,2)` + `shl $2` | `return x*12;`, 크기 `0x9` |
| 3-4 `sub`, `lea`, `sar $2`, `and` | `t1 = a - b + c;` `t2 = t1 >> 2;` (signed → `sar`), 크기 `0x12` |
| 3-5 `x[y] = 3y*4` | `x[y] = y*12;` (반환값 `%rax = y`), 크기 `0x10` |
| 3-6 `lea (%rsi,%rsi,1)`, `sub`, `mov ... (%rdi,%rsi,8)` | `buf[x] = 2*x - y;` `return y;`, 크기 `0xf` |

## 15. 핵심 정리

1. **Suffix** b/w/l/q = 1/2/4/8 바이트. 생략 시 레지스터로 크기 추론.
2. **mov는 해당 바이트만 갱신**하지만, **레지스터 목적지의 32비트 연산은 상위 32비트를 0으로** 만든다 (의존성 제거, common case fast).
3. 일반 `movq`의 immediate는 32비트 sign-extend, 64비트 상수는 **`movabsq`**.
4. **Truncation은 명령어 불필요**, 확장은 **signed → movs**, **unsigned → movz** (`movzlq`는 없음 → `movl` 사용).
5. **lea는 메모리 접근 없이 주소 계산** → 포인터 계산과 `x + k*y` 형태 산술에 활용.
6. 이항 연산은 **`op S, D` → D = D op S** (`sub`의 순서 주의).
7. Right shift: **unsigned → `shr`(0 채움)**, **signed → `sar`(MSB 채움)**.
