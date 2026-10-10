# Week 7: Machine-Level Representation — Control Flow (제어 흐름)

교재: Computer Systems 3rd Edition by Bryant, Chap 3 (3.6 중심)

## 0. 오늘의 목표

C의 `if`, `while`, `for`, 삼항 연산자 같은 **제어 흐름이 어셈블리로 어떻게 표현되는지** 이해한다.
핵심 흐름은 다음과 같다.

1. 연산 결과가 **condition code(플래그)** 에 기록된다 (암묵적 또는 `cmp`/`test`로 명시적).
2. 이 플래그를 읽는 명령어(`jX`, `cmovX`, `setX`)가 다음 동작을 결정한다.

## 1. Status Register (Flag Register)

- CPU의 현재 상태를 담는 레지스터 (x86-64에서는 `%rflags`)
  - condition code, interrupt mask, privilege level 등
- **Condition code**: 단일 비트 플래그들의 집합
  - **가장 최근의** 산술/논리 연산 결과로 자동 갱신된다.
  - 이를 이용해 다음에 무엇을 할지 결정한다.
- 플래그 비트의 크기와 의미는 아키텍처마다 다르다.

| 플래그 | 이름 | 용도 |
|---|---|---|
| `CF` | Carry Flag | **unsigned** overflow |
| `ZF` | Zero Flag | 결과가 0 |
| `SF` | Sign Flag | 결과가 음수 (**signed**) |
| `OF` | Overflow Flag | two's complement (**signed**) overflow |

## 2. Condition Codes — 암묵적 설정 (Implicit Setting)

예: `add b, a` → `t = a + b`

- **CF**: MSB에서 carry out 발생 시 (unsigned overflow)
  ```
    1111 1111 (0xFF, UMAX)
  + 0000 0001 (0x01)
  -----------
  1 0000 0000 (0x00) → carry 발생, CF=1
  ```
- **ZF**: `t == 0`
- **SF**: `t < 0` (signed로 해석)
- **OF**: signed overflow — `(a>0 && b>0 && t<0) || (a<0 && b<0 && t>0)`
  ```
    0111 1111 (0x7F, TMAX)
  + 0000 0001 (0x01)
  -----------
    1000 0000 (0x80) → carry 없음(CF=0), 하지만 OF=1
  ```

> **주의**: 산술·논리 연산은 플래그를 암묵적으로 설정하지만, **`leaq`는 플래그를 설정하지 않는다** (주소 계산 전용).

## 3. Condition Codes — 명시적 설정 (Explicit Setting)

### 3.1 `cmp b, a` — `a - b`를 계산하되 결과는 저장하지 않음

- `sub`와 같지만 **destination에 저장하지 않고 플래그만 설정**한다.
- **비교 순서 주의!** `cmp b, a`는 `a - b`이다 (AT&T 문법에서 operand 순서가 뒤집혀 보임).

| 플래그 | 설정 조건 (`t = a - b`) |
|---|---|
| CF | MSB에서 borrow 발생 → unsigned로 `a < b` |
| ZF | `a == b` |
| SF | `(a - b) < 0` (signed) |
| OF | `(a>0 && b<0 && (a-b)<0) \|\| (a<0 && b>0 && (a-b)>0)` |

Borrow 예시 (CF=1):
```
  0000 0000 (UMIN)
- 0000 0001 (1)
-----------
  1111 1111 (UMAX) → borrow 발생
```

#### Overflow 조건 정리

| 연산 | signed overflow | unsigned overflow |
|---|---|---|
| `a + b` | `a>0 && b>0 && a+b<0` 또는 `a<0 && b<0 && a+b>0` | `a+b < a \|\| a+b < b` |
| `a - b` | `a>0 && b<0 && a-b<0` 또는 `a<0 && b>0 && a-b>0` | `a < b` |

#### 플래그 조합으로 signed 비교하기

- **Equal?** → `ZF`
- **Less?** → `SF ^ OF` (= `(SF & ~OF) | (~SF & OF)`)
  - overflow가 없으면: `a - b < 0` 이면 `a < b` → SF=1, OF=0
  - overflow가 있으면: `a - b > 0` 으로 보여도 실제로는 `a < b` → SF=0, OF=1
  - 즉 **overflow까지 고려해야** 하므로 SF와 OF를 XOR한다.
- **Less or equal?** → `(SF ^ OF) | ZF`
- **Greater?** → `~((SF ^ OF) | ZF)`

예: `if (x <= 1)` → `cmp $0x1, %edi` (`x - 1` 계산)

### 3.2 `test b, a` — `a & b`를 계산하되 결과는 저장하지 않음

- `a & b` 결과로 플래그를 설정한다.
  - **ZF**: `a & b == 0`
  - **SF**: `a & b < 0`
- **같은 값을 두 operand에 넣으면** (`test %rdi, %rdi`) 그 값의 부호/0 여부를 SF, ZF로 바로 알 수 있다.

```c
long test_zero(long a) {
    if (a < 0) { ... }        // test %rdi, %rdi  → SF 확인
}
long test_flag(unsigned long a, unsigned long b) {
    if ((a & b) == 0) { ... } // test %rsi, %rdi  → ZF 확인
}
```
> 참고: 슬라이드의 `a & b == 0`은 C 연산자 우선순위상 `a & (b == 0)`으로 해석되므로, 의도대로 쓰려면 괄호 `(a & b) == 0`가 필요하다.

## 4. Condition Code를 사용하는 명령어

| 종류 | 동작 |
|---|---|
| `jX` | 조건에 따라 다른 명령어로 **점프** (control transfer) |
| `cmovX` | 조건에 따라 **데이터를 이동** (data transfer) |
| `setX` | 조건에 따라 **1바이트를 0 또는 1로 설정** |

`X`에 붙는 조건 접미사(e, ne, g, l, a, b ...)는 세 종류 모두 공통이다.

## 5. Jump 명령어

`cmp s1, s2` → `t = s2 - s1` 기준 (Figure 3.15)

| 명령어 | 조건 | 설명 |
|---|---|---|
| `jmp addr` | 1 | 무조건 점프 |
| `je` | `ZF` | equal |
| `jne` | `~ZF` | not equal |
| `jg` | `~(SF^OF) & ~ZF` | greater (**signed**) |
| `jge` | `~(SF^OF)` | greater or equal (signed) |
| `jl` | `SF^OF` | less (signed) |
| `jle` | `(SF^OF) \| ZF` | less or equal (signed) |
| `ja` | `~CF & ~ZF` | above (**unsigned**) |
| `jae` | `~CF` | above or equal (unsigned) |
| `jb` | `CF` | below (unsigned) |
| `jbe` | `CF \| ZF` | below or equal (unsigned) |

- **signed** 비교: greater / less (`g`, `l`) → SF, OF 사용
- **unsigned** 비교: above / below (`a`, `b`) → CF 사용

### Label

- 심볼 뒤에 콜론(`:`)을 붙인 것 (예: `.L1:`)
- 어셈블리에서 점프 목적지는 보통 symbolic label로 표시한다.
- object 파일을 만들 때 **assembler가 label이 붙은 명령어의 실제 주소를 결정해 인코딩**한다.

## 6. Conditional Branch: `if`

### 6.1 `if` 문

```c
long f1(long x) {
    if (x > 100)
        return 1;
    return 0;
}
```
```
<+0>:  cmp  $0x64,%rdi     # t = x - 100
<+4>:  jle  0xc <f1+12>    # 조건이 거짓(x <= 100)이면 body를 건너뜀
<+6>:  mov  $0x1,%eax      # if-body
<+11>: retq
<+12>: mov  $0x0,%eax      # out of body
<+17>: retq
```
- 컴파일 옵션: `gcc -Og -c f1.c -fcf-protection=none`
- 패턴: **비교 → 조건이 거짓이면 body 밖으로 점프** (C의 `>`가 어셈블리에서 반대 조건 `jle`로 나타남)

### 6.2 `if-then-else`

```c
long f2(long x, long y) {
    long result;
    if (x > y) result = x - y;
    else       result = y - x;
    result = 3 * result;
    return result;
}
```
```
<+0>:  cmp  %rsi,%rdi          # t = x - y
<+3>:  jle  0xd <f2+13>        # x <= y 이면 else로
<+5>:  sub  %rsi,%rdi          # then: x - y
<+8>:  mov  %rdi,%rsi
<+11>: jmp  0x10 <f2+16>       # 무조건 점프로 else 건너뜀
<+13>: sub  %rdi,%rsi          # else: y - x
<+16>: lea  (%rsi,%rsi,2),%rax # 3 * result
<+20>: retq
```
- then 블록 끝에 **무조건 점프(`jmp`)** 가 있어야 else 블록을 건너뛴다.

## 7. Loops

### 7.1 `do-while`

```
loop:
    body-statement
    t = test-expr;
    if (t) goto loop;
```

```c
long f3(long cnt) {
    do { cnt--; } while (cnt > 100);
    return 3 * cnt;
}
```
```
<+0>:  sub  $0x1,%rdi         # body
<+4>:  cmp  $0x64,%rdi        # test
<+8>:  jg   0x0 <f3>          # true면 body로
<+10>: lea  (%rdi,%rdi,2),%rax
<+14>: retq
```

### 7.2 `while` — "jump to middle" 방식

`while`은 body를 **한 번도 실행하지 않고 끝날 수 있으므로**, 먼저 test로 무조건 점프한다.

```
    goto test;          # jump to middle
loop:
    body-statement
test:
    t = test-expr;
    if (t) goto loop;
```

```c
long f4(long cnt) {
    while (cnt > 100) { cnt--; }
    return 3 * cnt;
}
```
```
<+0>:  jmp  0x6 <f4+6>        # jump to middle (test로)
<+2>:  sub  $0x1,%rdi         # body
<+6>:  cmp  $0x64,%rdi        # test
<+10>: jg   0x2 <f4+2>        # true면 body로
<+12>: lea  (%rdi,%rdi,2),%rax
<+16>: retq
```
- `do-while`과 비교하면 **맨 앞의 `jmp` 하나만 추가**된 구조이다.

### 7.3 `for`

`for`는 `while`로 변환한 뒤 같은 방식(jump to middle)으로 번역된다.

```c
for (init-expr; test-expr; update-expr)
    body-statement
```
```
    init-expr;
    goto test;
loop:
    body-statement
    update-expr;
test:
    t = test-expr;
    if (t) goto loop;
```

```c
long f5(long arr[], long n) {
    long sum = 0;
    for (long i = 0; i < n; i++)
        sum += arr[i];
    return sum + 1;
}
```
| 레지스터 | 용도 |
|---|---|
| `%rdi` | arr |
| `%rsi` | n |
| `%rdx` | i |
| `%rax` | sum, 반환값 |

```
<+0>:  mov  $0x0,%edx           # init: i = 0
<+5>:  mov  $0x0,%eax           # sum = 0
<+10>: jmp  0x14 <f5+20>        # jump to test
<+12>: add  (%rdi,%rdx,8),%rax  # body: sum += arr[i]
<+16>: add  $0x1,%rdx           # update: i++
<+20>: cmp  %rsi,%rdx           # test: i - n
<+23>: jl   0xc <f5+12>         # i < n 이면 body로
<+25>: add  $0x1,%rax           # sum + 1
<+29>: retq
```
- `mov $0x0,%edx`: 32비트 레지스터에 쓰면 상위 32비트가 0으로 채워지므로 `%rdx` 전체가 0이 된다.

## 8. Conditional Move (`cmovX`)

`val = Test ? Then_Expr : Else_Expr;` 를 번역하는 두 가지 방법:

| Conditional jump (control transfer) | Conditional move (data transfer) |
|---|---|
| `if (!Test) goto Else;`<br>`val = Then_Expr;`<br>`goto Done;`<br>`Else: val = Else_Expr;`<br>`Done: ...` | `val = Then_Expr;`<br>`eval = Else_Expr;`<br>`if (!Test) val = eval;` |

### 왜 cmov를 쓰는가? — Pipelining

- 현대 프로세서는 **pipeline**(예: fetch → decode → execute)으로 여러 명령어를 겹쳐 실행한다.
- 조건 분기가 있으면 **예측한 경로의 명령어로 pipeline을 미리 채워야** 하는데, 예측이 틀리면 pipeline을 비우고 다시 채워야 하므로 성능이 떨어진다.
- cmov는 **양쪽 값을 모두 계산한 뒤 조건에 맞는 값만 선택**하므로 분기가 없어 pipeline이 끊기지 않는다.

```c
long f6(long x, long y) {
    long result;
    if (x > y) result = x - y;
    else       result = y - x;
    return result;
}
```

| `gcc -Og` (분기 사용) | `gcc -O1` (cmov 사용) |
|---|---|
| `cmp %rsi,%rdi`<br>`jle c`<br>`mov %rdi,%rax`<br>`sub %rsi,%rax`<br>`ret`<br>`c: mov %rsi,%rax`<br>`sub %rdi,%rax`<br>`ret` | `mov %rdi,%rdx`<br>`sub %rsi,%rdx` &nbsp;# rdx = x-y<br>`mov %rsi,%rax`<br>`sub %rdi,%rax` &nbsp;# rax = y-x<br>`cmp %rsi,%rdi`<br>`cmovg %rdx,%rax` # x>y면 rax=x-y<br>`ret` |

- `cmovg`: greater 조건(`~(SF^OF) & ~ZF`)이면 move
- 컴파일러는 **계산 복잡도와 양쪽을 모두 계산할 때의 위험성**을 고려해 cmov 사용 여부를 결정한다.

### cmov가 부적절한 경우

1. **Expensive computations** — 양쪽을 모두 계산하므로, 계산이 매우 단순할 때만 이득
   - `val = Test(x) ? Hard1(x) : Hard2(x);` → 비효율
2. **Risky computations** — 계산 자체가 부작용/오류를 일으킬 수 있음
   ```c
   long f7(long *x) {
       long result = x ? *x + 1 : 0;
       return result;
   }
   ```
   - cmov로 만들면 `x`가 NULL이어도 `*x`를 **먼저 역참조** → segmentation fault 위험
   - 그래서 실제 `gcc -O1` 결과는 분기를 사용한다:
   ```
   mov  $0x0,%eax
   test %rdi,%rdi
   je   11 <f7+0x11>     # x == NULL이면 바로 리턴
   mov  (%rdi),%rax
   add  $0x1,%rax
   ret
   ```

## 9. Conditional Set (`setX`)

- 조건이 참이면 목적지 **바이트**를 1로, 거짓이면 0으로 설정한다.
- 0/1 결과를 만들어야 하는 모든 상황에서 분기·cmov보다 **매우 효율적**이다.

```c
char f8(long x) { return x == 0; }
```
```
test %rdi,%rdi
sete %al          # ZF=1이면 al = 1
ret
```

```c
char f9(long x, long y) { return x > y; }
void f10(char *buf, long x) { *buf = (x > 0); }
```
```
# f9                     # f10
cmp  %rsi,%rdi           test %rsi,%rsi
setg %al                 setg (%rdi)      # 메모리 바이트에도 직접 set 가능
ret                      ret
```

### f1을 `-O1`로 컴파일하면

`f1`은 사실상 `return x > 100;` 이므로 `set`으로 최적화된다.

| `gcc -Og` | `gcc -O1` |
|---|---|
| `cmp $0x64,%rdi`<br>`jle 0xc`<br>`mov $0x1,%eax`<br>`retq`<br>`mov $0x0,%eax`<br>`retq` | `cmp $0x64,%rdi`<br>`setg %al`<br>`movzbl %al,%eax`<br>`ret` |

- `setg`는 1바이트(`%al`)만 쓰므로, `long` 반환을 위해 `movzbl`로 **zero-extend** 한다 (32비트 쓰기 → 상위 32비트도 0).

## 10. 핵심 정리

- **Condition codes**: CF(unsigned), ZF, SF, OF(signed) — 산술/논리 연산이 암묵적으로 설정 (`lea` 제외)
- **명시적 설정**: `cmp b,a` → `a-b`, `test b,a` → `a&b` (둘 다 결과 저장 X, 플래그만)
- **signed 비교는 `SF^OF`**, unsigned 비교는 `CF` 사용
- **플래그 사용 명령어**: `jX`(점프), `cmovX`(조건부 이동), `setX`(0/1 바이트 설정)
- **if**: 반대 조건으로 body를 건너뜀 / **if-else**: then 끝에 무조건 `jmp`
- **do-while**: body → test → 조건 점프
- **while / for**: 먼저 test로 점프하는 **jump to middle**
- **cmov**: 분기 없이 pipeline 효율↑, 단 계산이 비싸거나 위험하면(NULL 역참조 등) 사용 불가
- **set**: 비교 결과를 0/1로 만들 때 가장 효율적, 반환 시 `movzbl`로 확장
