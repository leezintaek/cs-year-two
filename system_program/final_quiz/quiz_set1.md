# 기말고사 대비 모의문제 — Set 1

> 범위: 8. Procedure Call and Stack
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (C / x86-64 AT&T 어셈블리)
> 환경 가정: x86-64 Linux, gcc `-Og`, `-fno-stack-protector`, `-mpreferred-stack-boundary=3`(8바이트 정렬), `-fcf-protection=none`, little endian
> 인자 `%rdi, %rsi, %rdx, %rcx, %r8, %r9` / 반환값 `%rax`
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** `pushq %rax`는 먼저 `%rax` 값을 `(%rsp)`에 저장한 다음 `%rsp`를 8 감소시킨다.

**2.** `popq %rdx`를 실행하면 pop된 자리의 메모리 값은 0으로 지워진다.

**3.** 7번째 이후 인자를 스택으로 넘긴 경우, callee가 `ret` 직전에 그 인자들을 pop해서 스택을 정리한다.

**4.** call 명령어가 없는 leaf procedure는 `volatile` 지역 변수가 있어도 `%rsp`를 조정하지 않고 `%rsp` 아래 공간에 바로 저장할 수 있다.

**5.** x86-64에서 스택 프레임은 런타임에 할당되므로, 프레임에 필요한 크기도 런타임에 결정된다.

---

## Part B. 객관식

**6.** 다음 코드에서 `call`이 스택에 push하는 return address는?
```
40061a: call  400630 <f>
40061f: mov   %rax,%rbx
```
① `0x40061a`  ② `0x40061f`  ③ `0x400630`  ④ `0x400622`

**7.** `-Og`로 컴파일할 때, 지역 변수가 레지스터가 아니라 **스택에 저장되는 이유가 아닌** 것은?
① 지역 변수에 `&` 연산자를 쓴다  ② 지역 변수가 배열이다  ③ 지역 변수가 `volatile`이다  ④ 지역 변수를 리턴 값으로 돌려준다

**8.** 다음 중 preserved(callee-saved) 레지스터가 **아닌** 것은?
① `%rbx`  ② `%rbp`  ③ `%r12`  ④ `%r10`

**9.** caller가 `call f`를 실행하기 직전 `%rsp = 0x7ff0`이다. `f`는 진입하자마자 아래 세 명령어를 실행한다. 세 명령어 실행 후 `%rsp`는?
```
push  %rbx
push  %rbp
sub   $0x10,%rsp
```
① `0x7fd0`  ② `0x7fc8`  ③ `0x7fe0`  ④ `0x7fb8`

**10.** ABI에 대한 설명으로 옳은 것은?
① ABI는 하드웨어가 무엇을 제공하는지(레지스터, 명령어 집합)를 정의한다.
② ISA가 같으면 ABI도 반드시 같다.
③ System V AMD64 ABI는 프로세서 독립적인 gABI와 프로세서 종속적인 psABI로 나뉘며, calling convention은 psABI에 속한다.
④ ABI는 컴파일러만 지키면 되고, 링커와 로더는 상관없다.

**11.** gdb에서 매 스텝마다 스택 top의 8바이트 값을 16진수로 자동 출력하는 명령어는?
① `display /x *(long *)($rsp)`  ② `display /x *(long *)(%rsp)`  ③ `display /x $rsp`  ④ `p /x %rsp`

---

## Part C. 단답형

**12.** 초기 상태가 `%rsp = 0x200`, `%rax = 0xAA`, `%rbx = 0xBB`, `%rcx = 0`이다. 아래 명령어를 순서대로 실행한 뒤 물음에 답하시오.
```
pushq %rax
pushq %rbx
popq  %rcx
pushq $0x5
popq  %rax
```
(a) 최종 `%rsp`
(b) 최종 `%rax`, `%rcx`
(c) 주소 `0x1f0`, `0x1f8`에 저장된 8바이트 값

**13.** 아래 코드에서 `caller`의 `call`을 실행하기 직전 `%rip = 0x40112d`, `%rsp = 0x7fffe010`이다.
```
0000000000401120 <sq>:
  401120: mov   %rdi,%rax
  401123: imul  %rdi,%rax
  401127: ret
0000000000401128 <caller>:
  401128: mov   $0x7,%edi
  40112d: call  401120 <sq>
  401132: add   $0x1,%rax
  401136: ret
```
(a) `call` 실행 직후 `%rip`, `%rsp`, `*(long *)%rsp`
(b) `sq`의 `ret` 실행 직후 `%rip`, `%rsp`, `%rax`

**14.** `incr2`와 `call_incr2`는 따로 컴파일되었다.
```c
long incr2(long *p, long val) { long x = *p; *p = x * val; return x + 1; }
long call_incr2() { long v1 = 6; long v2 = incr2(&v1, 3); return v1 - v2; }
```
(a) `call_incr2()`의 리턴 값은?
(b) `call_incr2`에서 `v1`과 `v2` 중 스택에 저장되는 것은 무엇이고, 그 이유는?

**15.** 아래 함수를 `-Og`로 컴파일한다.
```c
long Q(long);
long P(long x) { long v = Q(x); long u = Q(v); return x + u + v; }
```
(a) 첫 번째 `call Q`를 넘어 보존해야 하는 값은?
(b) 두 번째 `call Q`를 넘어 보존해야 하는 값은?
(c) 필요한 preserved register는 최소 몇 개이고, 그때 `P`의 시작과 끝에 나오는 `push`/`pop`은 각각 몇 개인가?

**16.** 아래 `call8`에서 `sum8`에 진입한 직후 `%rsp = 0x7fffd0c0`이다.
```c
long sum8(long, long, long, long, long, long, long, long);
long call8(void) { return sum8(10, 20, 30, 40, 50, 60, 70, 80); }
```
(a) 주소 `0x7fffd0c0`, `0x7fffd0c8`, `0x7fffd0d0`에 저장된 값은 각각 무엇인가? (값을 모르면 무엇인지 설명)
(b) `call8`에 진입한 직후(인자를 준비하기 전) `%rsp`는?

---

## Part D. 빈칸 채우기 손코딩

**17.** 아래 C 함수의 어셈블리 빈칸을 채우시오.
```c
long g(long, long);
void addstore(long x, long y, long *dest) { long t = g(x, y); *dest = t + y; }
```
```
addstore:                       # x in %rdi, y in %rsi, dest in %rdx
    push  %rbp
    ____(a)____
    mov   %rdx,%rbx             # save dest
    mov   %rsi,%rbp             # save y
    call  g
    add   ____(b)____           # t + y
    mov   %rax,____(c)____      # *dest = t + y
    ____(d)____
    ____(e)____
    ret
```

**18.** 아래 C 함수의 어셈블리 빈칸을 채우시오.
```c
long gx(long *);
long f(long x) { return gx(&x) + 1; }
```
```
f:                              # x in %rdi
    ____(a)____                 # set up
    mov   %rdi,____(b)____
    mov   ____(c)____,%rdi
    call  gx
    add   $0x1,%rax
    ____(d)____                 # finish
    ret
```

**19.** 문제 16의 `call8`을 컴파일한 결과의 빈칸을 채우시오.
```
call8:
    pushq ____(a)____
    pushq ____(b)____
    mov   $0x3c,____(c)____
    mov   $0x32,%r8d
    mov   $0x28,%ecx
    mov   $0x1e,%edx
    mov   $0x14,%esi
    mov   $0xa,%edi
    call  sum8
    ____(d)____
    ret
```

**20.** 아래 C 함수의 어셈블리 빈칸을 채우고 물음에 답하시오.
```c
long h(long a, long b) { volatile long t = a; t = t + b; return t; }
```
```
h:                              # a in %rdi, b in %rsi
    mov   %rdi,____(a)____      # t = a
    mov   -0x8(%rsp),%rax
    add   %rsi,%rax
    mov   %rax,-0x8(%rsp)       # t = t + b
    mov   ____(b)____,%rax      # return t
    ret
```
(c) `t`를 스택에 두는데도 `sub $0x8,%rsp` / `add $0x8,%rsp`가 없는 이유를 쓰시오.
(d) `return t;` 직전에 `%rax`에 이미 `t + b`가 있는데도 `-0x8(%rsp)`에서 다시 읽는 이유를 쓰시오.

---
---

## 정답 및 해설

**1. X** — 순서가 반대다. `subq $8,%rsp`로 먼저 공간을 할당한 뒤 `movq %rax,(%rsp)`로 저장한다.

**2. X** — pop은 `movq (%rsp),%rdx` 후 `addq $8,%rsp`일 뿐, 메모리를 지우지 않는다. 그래서 초기화하지 않은 지역 변수에 쓰레기 값이 보인다.

**3. X** — callee 진입 시 스택 top에는 return address가 있어서 callee는 인자를 pop할 수 없다. callee는 `0x8(%rsp)`처럼 오프셋으로 읽기만 하고, 정리는 **caller**가 `add $0x10,%rsp`처럼 한다.

**4. O** — leaf procedure는 다른 함수를 부르지 않으므로 `%rsp` 아래 공간이 덮어써질 일이 없다. System V ABI에서는 이 영역을 red zone(`%rsp` 아래 128바이트)이라 부른다.

**5. X** — 할당은 런타임에 일어나지만, **필요한 크기는 컴파일 타임에 결정된다**(`sub $0x8,%rsp`의 0x8은 컴파일러가 정한 상수).

**6. ②** — return address는 call **바로 다음 명령어의 주소**다.
③ `0x400630`은 점프할 callee 주소(`%rip`의 새 값), ④는 call 주소에 8(복귀 주소 크기)을 더한 값으로 의미가 없다.

**7. ④** — 리턴 값은 `%rax`로 넘기면 되므로 스택이 필요 없다. ①②③은 모두 **주소가 필요하거나 매번 메모리에 접근해야** 하는 경우다.

**8. ④** — preserved 레지스터는 `%rbx, %rbp, %r12, %r13, %r14, %r15` 6개다. `%r10`은 caller-saved.

**9. ②** — `call` 자체가 return address를 push한다는 점을 빠뜨리면 안 된다.
- `call`: 0x7ff0 − 8 = 0x7fe8
- `push %rbx`: 0x7fe0
- `push %rbp`: 0x7fd8
- `sub $0x10`: 0x7fd8 − 0x10 = **0x7fc8**

① `0x7fd0`은 call의 push를 빠뜨린 값이다.

**10. ③**
① ISA에 대한 설명이다. ABI는 ISA를 바이너리 수준에서 **어떻게 쓸지(How to use)**에 대한 규약이다.
② 같은 x86-64라도 Linux(System V)와 Windows(Microsoft x64)는 ABI가 다르다.
④ 컴파일러, 링커, 로더 모두 ABI를 지켜야 한다.

**11. ①** — gdb에서는 레지스터를 `%rsp`가 아니라 **`$rsp`**로 쓴다. ③은 `%rsp` 값(주소) 자체를 출력할 뿐, 스택 top의 내용이 아니다.

**12.**
| 명령어       | `%rsp`  | 변화                  |
|--------------|---------|-----------------------|
| `pushq %rax` | `0x1f8` | `[0x1f8] = 0xAA`      |
| `pushq %rbx` | `0x1f0` | `[0x1f0] = 0xBB`      |
| `popq %rcx`  | `0x1f8` | `%rcx = 0xBB`         |
| `pushq $0x5` | `0x1f0` | `[0x1f0] = 0x5`       |
| `popq %rax`  | `0x1f8` | `%rax = 0x5`          |

(a) **`0x1f8`**
(b) `%rax` = **`0x5`**, `%rcx` = **`0xBB`**
(c) `0x1f0` = **`0x5`** (pop 뒤에도 지워지지 않고 남아 있다), `0x1f8` = **`0xAA`**

**13.**
(a) `%rip` = **`0x401120`**, `%rsp` = **`0x7fffe008`**, `*(long *)%rsp` = **`0x401132`**
- call이 return address(call 다음 명령어 `0x401132`)를 push하고 `sq`로 점프한다. 0x7fffe010 − 8 = 0x7fffe008.

(b) `%rip` = **`0x401132`**, `%rsp` = **`0x7fffe010`**, `%rax` = **`0x31`** (= 49)
- ret이 `0x401132`를 pop해서 그 주소로 점프한다. `%rax` = 7 × 7 = 49.

**14.**
(a) **11** (실행해서 확인함)
- `incr2`: `x = *p = 6`, `*p = 6 × 3 = 18` → **v1이 18로 바뀐다**, `return 7`
- `v1 − v2 = 18 − 7 = 11` (원래 v1 값 6을 쓰면 −1로 틀린다)

(b) **v1** — `&v1`로 주소를 넘기므로 메모리에 있어야 한다(레지스터에는 주소가 없다). v2는 리턴 값으로 `%rax`에 받으므로 레지스터로 충분하다.

**15.**
(a) **x** — 두 번째 call의 인자는 v라서 x는 필요 없어 보이지만, 마지막 `x + u + v`에서 쓴다.
(b) **x, v** — 두 번째 call이 `%rax`(v)와 `%rdi`를 덮어쓸 수 있다.
(c) **2개** (예: `%rbx` = x, `%rbp` = v) → 시작에 **push 2개**, 끝에 **pop 2개** (pop은 push의 역순)
- 판단 기준: call을 경계로 그 뒤에 다시 쓰는(reuse) 값의 개수.

**16.**
(a)
- `0x7fffd0c0` = **return address** (`call8`에서 `call sum8` 다음 명령어의 주소)
- `0x7fffd0c8` = **70** (7번째 인자)
- `0x7fffd0d0` = **80** (8번째 인자)
- 인자는 역순(80 먼저)으로 push하므로 7번째 인자가 스택 top 쪽(낮은 주소)에 온다. callee는 `0x8(%rsp)`, `0x10(%rsp)`로 읽는다.

(b) **`0x7fffd0d8`** — push 2번(16) + call(8) = 24 = 0x18. 0x7fffd0c0 + 0x18 = 0x7fffd0d8.

**17.** (a) `push %rbx`  (b) `%rbp,%rax`  (c) `(%rbx)`  (d) `pop %rbx`  (e) `pop %rbp`
- call 이후에 reuse되는 값은 y(`%rsi`)와 dest(`%rdx`) 2개 → preserved register 2개(`%rbp`, `%rbx`)를 쓴다.
- (c)는 `%rbx`가 아니라 `(%rbx)` — dest가 가리키는 메모리에 저장해야 한다.
- pop은 push의 **역순**이다. `pop %rbp`를 먼저 하면 두 레지스터 값이 서로 바뀌어 caller의 값을 망친다.

**18.** (a) `sub $0x8,%rsp`  (b) `(%rsp)`  (c) `%rsp`  (d) `add $0x8,%rsp`
- 파라미터 x도 **주소가 필요하면** 스택에 저장해야 한다. `%rdi`에 있던 x를 스택에 쓰고, 그 주소(`%rsp`)를 첫 번째 인자로 넘긴다.
- (d)를 `pop`으로 쓰면 레지스터 하나를 덮어쓰게 된다. 강의 코드처럼 `add`로 해제한다.

**19.** (a) `$0x50`  (b) `$0x46`  (c) `%r9d`  (d) `add $0x10,%rsp`
- 7, 8번째 인자는 **역순**: 80(0x50)을 먼저, 70(0x46)을 나중에 push한다.
- 6번째 인자 60(0x3c)은 `%r9`. 값이 작아서 32비트 이름 `%r9d`로 써도 상위 32비트가 0이 된다.
- 정리는 caller가 `add $0x10,%rsp`로 한다. 데이터를 꺼낼 필요가 없으니 pop 대신 add.

**20.** (a) `-0x8(%rsp)`  (b) `-0x8(%rsp)`
(c) `h`는 call 명령어가 없는 **leaf procedure**라서, `%rsp`를 조정하지 않고 `%rsp` 아래 공간(red zone)을 바로 쓸 수 있다. 다른 함수가 호출되어 그 공간을 덮어쓸 일이 없기 때문이다.
(d) `volatile`은 **매번 메모리에서 읽고 쓰라고** 컴파일러에게 강제한다. 그래서 레지스터에 남은 값을 재사용하지 않고 `return t`에서 다시 메모리를 읽는다.
