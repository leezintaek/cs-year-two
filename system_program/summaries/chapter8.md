# 8. Procedure Call and Stack — 강의노트

- 과목: CSE3209 System Programming
- 교재: Bryant & O'Hallaron, *Computer Systems* 3rd Ed. §3.7 (p.266–282)
- 강의 영상
  - **A** = `video_1793272095238.mp4` (10/27 강의, 약 70분) — 슬라이드 1–24
  - **B** = `video_1793272267622.mp4` (10/29 강의, 약 50분) — 슬라이드 24–47
- 타임스탬프 표기: `A 12:07` = 영상 A의 12분 7초
- 원문 전사: `video_*.transcript.md`, 슬라이드 원문: `slides.md`

> 이번 장의 핵심: **스택(`%rsp`)이 어떻게 바뀌는가**. 이번 주에 배우는 명령어는 `push`, `pop`, `call`, `ret` 4개뿐이다.

---

## 슬라이드 1: 표지 · 슬라이드 2: Road map  `A 00:00`

- 전반부(정수·부동소수점 표현, 어셈블리, GCC/GDB 소스 레벨 디버깅, 조건문·반복문)는 **단일 프로시저**가 어떻게 실행되는지를 다뤘다.
- 후반부(§3.7~)는 **확장**이다.
  1. 여러 프로시저가 서로 어떻게 상호작용하는가 → 이번 장 (관전 포인트: **스택**)
  2. 배열·포인터·구조체·유니온 같은 복합 데이터 타입이 메모리에 어떻게 표현되는가
  3. 라이브러리와 링킹으로 큰 프로그램을 만드는 방법
  4. 사용자 프로그램이 OS와 어떻게 인터페이스하는가 (syscall, heap, 프로세스 주소 공간)
- 교수님 코멘트: API는 계속 바뀌지만, 폰 노이만 구조가 바뀌지 않는 한 이 근본 원리는 계속 쓸모가 있다. 3학년 OS 수업에도 큰 도움이 된다.

## 슬라이드 3: Content  `A 03:24`

- 스토리라인: 프로시저가 왜 필요한가 → 스택 → ABI → Calling Convention(4가지 범주) → push/pop → call/ret → 데이터 전달 → 레지스터 저장 규약
- Goal: **x86-64/Linux에서 어셈블리가 함수를 어떻게 호출하는지 이해하기**
- ISA가 "하드웨어가 무엇을 제공하는가"라면, ABI는 **그것을 어떻게 쓸 것인가(How to use)**에 대한 약속이다.

## 슬라이드 4: Program Counter와 Stack Pointer  `A 05:39`

| 용어 | x86-64 레지스터 | 역할 |
|---|---|---|
| PC (Program Counter) | `%rip` | **다음에 실행할 명령어의 주소** |
| SP (Stack Pointer) | `%rsp` | 스택의 **top(끝) 위치** |

- 지난 장의 주인공은 `%rflags`(조건 코드 CF/ZF/SF/OF)였고, 이번 장의 주인공은 `%rsp`다.
- `%rsp`를 바꾸는 것과 가장 밀접한 것이 프로시저 호출이라서 장 제목이 "Procedure Call and **Stack**"이다.

## 슬라이드 5: Why Procedure?  `A 06:47`

- 프로시저(= 함수) = 특정 작업을 수행하는 **재사용 가능한 코드 블록**. C, OOP 등 현대의 구조적 프로그래밍은 모두 프로시저 기반이다.
- 장점: 재사용성 → 추상화 → 가독성·모듈화
- 프로그램의 범위를 넓혀 볼 것: **OS(커널)·라이브러리·애플리케이션 모두 프로시저들의 집합**이다. 라이브러리는 실행은 못 하지만 링크할 수 있는 프로그램이다.
  - 예: 김 과장이 만든 라이브러리 + 최 과장이 만든 사용자 프로그램 + 리눅스 커널이 엉켜서 함께 돌아간다 → **로우 레벨에서의 사용법(How to use)이 같아야 한다.**
- 프로시저가 없다면 `Proc2`를 100번 호출할 때 코드를 100번 복사해 넣어야 한다(인라인) → 코드 크기가 폭발한다. 재귀이거나 호출이 깊어지면 몇 번 반복될지 컴파일 타임에는 알 수도 없다.
- **동적 할당**: 지역 변수(예: 10MB 버퍼)는 호출될 때만 할당하면 된다. 호출된다는 보장이 없는데 미리 잡아 둘 이유가 없다.
- 호출(invocation)마다 런타임 상태가 다르다. 예: 같은 `call Proc2`라도 복귀 주소가 4601일 수도, 4651일 수도 있다. `A 12:07`
- ISA가 기본으로 제공하는 것은 **call / return**이다.
  - `jmp`와의 차이: 점프는 가면 끝이지만, call은 **callee가 끝나면 반드시 caller의 복귀 주소(return address)로 돌아와야 한다.**
  - 용어: 호출하는 함수 = **caller**, 호출되는 함수 = **callee**

## 슬라이드 6: Why Stack for Procedure?  `A 14:14`

- 호출마다 **return address를 반드시 저장**해야 한다(오늘의 핵심 키워드). 중첩 호출을 하면 여러 개를 보관해야 한다.
- 저장 후보는 두 가지뿐이다.
  - ① **레지스터**: 레지스터에 복귀 주소를 저장하는 아키텍처도 있지만, 수가 적어서 호출이 깊어지면 결국 메모리를 써야 한다.
  - ② **메모리**: Intel x86은 메모리를 선택했다.
- 이 메모리 영역(프로그램마다 따로 관리)을 **콜 스택(call stack, 런타임 스택)**, 줄여서 **스택**이라 부른다.
- 호출 하나에 필요한 정보의 묶음 = **스택 프레임(stack frame)**. 100번 호출하면 프레임도 100개가 생긴다. 프레임의 필수 정보는 **복귀 주소**다.
- A→B→C 순으로 호출했다면 C가 리턴한 뒤 돌아갈 곳은 B다 → **LIFO(Last-In First-Out)**. `A 17:24`
- 예 (Main 4000 → Proc1 4500 → Proc2 4800):
  - call 직전에 복귀 주소(4101)를 **push**하고 점프한다. 다시 call을 만나면 4601을 push한다.
  - 리턴할 때는 "복귀 주소가 **스택 top**에 있다"고 가정하고, 그것을 **pop**해서 그 주소로 점프한다.

## 슬라이드 7: Application Binary Interface  `A 19:32`

- **ISA** = 프로그램에게 보이는(visible) 하드웨어 인터페이스(레지스터, 메모리, 명령어 집합). 캐시·파이프라인처럼 상태에 영향이 없는 것은 숨긴다. → *하드웨어가 무엇을 제공하는가*
- **ABI** = 특정 ISA를 바이너리 수준에서 **어떻게 사용할 것인가**에 대한 규약
  - 컴파일된 프로그램(OS, 애플리케이션, 라이브러리)끼리의 **바이너리 호환성**을 보장한다.
  - ABI를 지켜야 하는 도구: **컴파일러, 링커, 로더**(실행 파일을 해석해 메모리에 매핑하는 소프트웨어)
  - 예: 리턴 값은 `%rax`에 두기로 약속했다. 누가 `%rbx`에 두면 서로 통신할 수 없다. `A 05:39`
- **같은 ISA라도 ABI는 다를 수 있다**(주로 OS 벤더가 주도한다).
  - x86-64 Linux/Unix/macOS 일부 → **System V AMD64 ABI** (AT&T 벨 연구소의 System V Unix 계열)
  - x86-64 Windows → **Microsoft x64 ABI**
  - 예: 7번째 이후 인자를 스택에 넣는 순서도 규약이다. System V는 **역순(reverse)**으로 push한다(9, 8, 7 순서) → pop할 때 순서대로 나오도록. Windows는 다르다. `A 21:41`

## 슬라이드 8: System V AMD64 ABI  `A 23:48`

- 우리가 따르는 ABI는 **System V AMD64 ABI**(= System V x86-64 ABI)이다.
  - 이름이 AMD64인 이유: AMD가 64비트 확장을 먼저 했기 때문일 뿐, x86-64와 같은 것이다.
- 문서는 약 300쪽(https://uclibc.org/docs/psABI-x86_64.pdf). 크게 두 부분으로 나뉜다.
  - **gABI (Generic ABI)**: 프로세서와 **독립적인** 규약. 예: **ELF** 포맷(헤더에 무엇이 들어가는지, 리틀/빅 엔디언 등)
  - **psABI (Processor Supplement ABI)**: 프로세서에 **종속적인** 규약. 주어진 ISA의 How to use이며, 그 근간이 **Calling Convention**이다.
- 시험 대비 포인트 `A 27:00`: "ABI가 뭡니까?"라고 물으면 "Application Binary Interface"라고만 답하지 말 것. → **"바이너리 수준에서 How to use를 정의한 규약이며, 프로세서 독립적인 부분(gABI)과 프로세서 종속적인 부분(psABI)으로 나뉜다"**라고 설명할 수 있어야 한다.

## 슬라이드 9: System V psABI — Why Calling Convention?  `A 28:04`

- 따로따로 컴파일된 프로그램들은 사실상 모두 **call/return**으로 연결되어 있다.
- **Calling Convention이 없으면 따로 컴파일된 코드끼리 통신할 수 없다.**
- caller와 callee의 역할은 상대적이다. 어떤 함수는 caller이면서 callee일 수 있다.
  - call 명령어가 없는 함수 = **leaf procedure**(콜 트리의 리프 노드). 특별한 최적화가 있다(→ 슬라이드 40).
- Calling Convention의 4가지 범주 `A 30:15`
  1. **Passing control**: 복귀 주소를 어디에 둘 것인가 → 스택 top
  2. **Passing data**: 인자와 리턴 값 → 6개는 레지스터, 나머지는 스택. 리턴 값은 `%rax`
  3. **Stack operation**
  4. **Register saving convention**: 호출이 중첩되면 레지스터가 충돌(오염)할 수 있다. 예: 첫 번째 인자 `x`가 `%rdi`에 있는데 `Q`도 `%rdi`를 쓴다 → call 이후에 `x`를 다시 쓰면 위험하다. `A 31:17`

## 슬라이드 10: Calling Convention Overview  `A 32:17`

- **Stack operation**
  - 호출할 때마다 런타임에 스택 프레임을 할당한다(두 번 호출하면 프레임 2개).
  - **스택은 아래로(높은 주소 → 낮은 주소) 자란다.**
  - push(할당) → `%rsp` **감소**, pop(해제) → `%rsp` **증가**
  - x86-64에서 return address는 **8바이트** → `call`하면 `%rsp -= 8`, `ret`하면 `%rsp += 8` `A 33:19`
- **Passing control**: `call`은 복귀 주소를 push한 뒤 callee로 점프하고, `ret`은 복귀 주소를 pop해서 caller로 복귀한다.
- **Passing data**: 정수/포인터 인자 6개는 `%rdi, %rsi, %rdx, %rcx, %r8, %r9` 순서로 전달하고, 나머지는 스택에 역순으로 넣는다. 리턴 값은 `%rax`.
- **Register saving**: callee-saved 레지스터는 `%rbx, %rbp, %r12–%r15`이다.

## 슬라이드 11: x86-64 Stack and Stack Pointer  `A 35:21`

- 스택은 논리적으로 **스택 프레임들의 집합**이다(호출할 때마다 동적으로 할당).
- 예: `yoo → who → amI` 3단 중첩 호출 → 프레임 3개
- **스택 프레임의 크기는 가변적이다.** 필수인 return address에 더해, **필요할 때만** 지역 변수·인자가 들어간다. → "언제 스택에 들어가는가"를 이해하는 것이 관전 포인트다.
- 관련 레지스터 두 개
  - `%rsp`: 현재 프레임의 top(가장 낮은 주소)
  - `%rbp`: 현재 프레임의 시작(frame pointer / base pointer) — **optional**
    - 32비트 x86에서는 항상 두 개를 유지했지만, **x86-64에서는 효율을 위해 뺐다**. 컴파일러가 `%rsp` 기준으로 모두 계산한다.
    - `-O0`(최적화 없음)으로 컴파일하면 옛날 방식(`%rbp` 사용)으로 나온다. 실무 릴리스에서 그렇게 하면 매우 느려진다. 최소 `-Og`를 쓸 것.

## 슬라이드 12: Stack Operation — Push  `A 38:36`

```asm
pushq %rcx        # 아래 두 명령어와 동일
# subq $8, %rsp
# movq %rcx, (%rsp)
```
- ① `%rsp`를 **8 감소**(공간 할당) → ② src 값을 `%rsp`가 가리키는 곳에 저장
- CISC라서 두 명령어를 하나로 만들어 둔 것이다.

## 슬라이드 13: Stack Operation — Pop  `A 40:49`

```asm
popq %rcx         # 아래 두 명령어와 동일
# movq (%rsp), %rcx
# addq $8, %rsp
```
- ① top의 값을 dst에 복사 → ② `%rsp`를 **8 증가**
- pop한 자리의 데이터는 **지워지지 않고 남아 있다**(그냥 쓰지 않을 뿐) → 초기화하지 않은 지역 변수에 "쓰레기 값"이 보이는 이유와 연관된다.

## 슬라이드 14: Example of pushq and popq (교재 그림 3.9)  `A 41:56`

| 단계 | `%rsp` | 비고 |
|---|---|---|
| 초기 | `0x108` | `%rax = 0x123`, `%rdx = 0` |
| `pushq %rax` | `0x100` | `0x100`에 `0x123`을 저장 |
| `popq %rdx` | `0x108` | `%rdx = 0x123`, `0x100`의 값은 남아 있음 |

> "이 그림만 이해하면 지금까지 잘 따라온 것"

## 슬라이드 15: Passing Control  `A 44:01` ★중요

```asm
400544: call 400550 <mult2>
400549: ...                 # ← return address
```
- **Return address** = call 명령어 **바로 다음** 명령어의 주소(`0x400549`). 매우 중요하다.
- `call label`: ① 복귀 주소를 스택에 push(`%rsp -= 8`) ② label로 점프(`%rip = 0x400550`)
- `ret`: ① 스택 top에서 복귀 주소를 pop(`%rsp += 8`) ② 그 주소로 점프

## 슬라이드 16–20: Procedure Call/Return Example (`multstore` → `mult2`)  `A 46:06`

```c
long mult2(long a, long b) { long s = a * b; return s; }
void multstore(long x, long y, long *dest) { long t = mult2(x, y); *dest = t; }
```

스냅샷을 볼 때는 **제일 먼저 PC(`%rip`)를 보고**, 다음에 실행할 명령어를 화살표로 떠올린다. 함수에 들어온 직후라면 스택 top에는 상위 caller의 복귀 주소가 있을 것이라고 생각하면 된다.

| 슬라이드 | 상황 | `%rip` | `%rsp` | 스택 top |
|---|---|---|---|---|
| 17 (call 실행 전) | `call` 실행 차례 | `0x400544` | `0x120` | (caller의 복귀 주소) |
| 18 (call 실행 후) | push 후 jump | `0x400550` | `0x118` | `0x400549` |
| 19 (ret 실행 전) | `ret` 실행 차례 | `0x400557` | `0x118` | `0x400549` |
| 20 (ret 실행 후) | pop 후 jump | `0x400549` | `0x120` | — |

- 주의: `0x120 - 8 = 0x118`이다(16진수라서 112가 아니다). `A 48:11`

## 슬라이드 21: x86-64/Linux Stack Frame  `A 49:17`

스택 프레임에 들어갈 수 있는 것 — **"if, only if"(필요할 때만)** 사용한다. 스택은 메모리이므로 **스택 사용을 최소화**하는 것이 원칙이다(Minimize stack use).

1. **Return address** (필수, `call`이 push)
2. **Frame pointer** (`old %rbp`) — optional. 32비트 시절에는 필수였지만 지금은 논외. `%rbp`는 범용 레지스터로 쓸 수 있다.
3. **지역 변수** — x86-64에서는 기본적으로 레지스터에 두고, 아래 경우에만 스택에 둔다. `A 51:24`
   - 레지스터가 부족할 만큼 지역 변수가 많을 때
   - **주소가 필요할 때**: 주소 연산자 `&`(레지스터에는 주소가 없다), **배열**(배열명 자체가 주소), **`volatile`**(매번 메모리에 접근하라는 뜻)
4. **인자** — 7번째부터(6개까지는 레지스터)
5. **Preserved registers** — 호출을 넘어 값을 유지해야 할 때(→ 슬라이드 42~)

## 슬라이드 22: X86-64 Procedure Call Highlights  `A 53:26`

```c
long func(long x) { long y = 100; return x + y; }
```
| `-Og` (최적화) | `-O0` (최적화 없음, 옛날 x86 스타일) |
|---|---|
| `lea 0x64(%rdi),%rax`<br>`ret` | `push %rbp` / `mov %rsp,%rbp` *(Set Up)*<br>`mov %rdi,-0x10(%rbp)` / `movq $0x64,-0x8(%rbp)` ...<br>`pop %rbp` / `ret` *(Finish)* |

- `-Og`: `0x64`(=100) + `%rdi`(x)를 `%rax`에 넣고 끝. **레지스터만으로 해결된다.**
- `-O0`: 지역 변수 `y`와 인자 `x`까지 모두 스택에 쓴다 → 메모리 접근이 많아 비효율적이다.
  - Set-up 코드: `old %rbp`를 push해서 보존한 뒤 `%rbp = %rsp`로 설정한다(leaf라서 `%rsp`는 바꾸지도 않는다).
- 요지: 옛날에는 스택을 과하게 썼고, **현대 x86-64는 스택을 최소한으로 쓰고 가급적 레지스터로 동작한다.**
- 대부분의 x86-64 프로시저는 **전체 스택 프레임이 필요 없다**. 복귀 주소만 push된다.

## 슬라이드 23: Example (`call_incr` / `incr`)  `A 57:43`

```c
long call_incr() { long v1 = 100; long inc = 10; long v2 = incr(&v1, inc); return v1 + v2; }
long incr(long *p, long val) { long x = *p; long y = x + val; *p = y; return x; }
```
- Q. 리턴 값은? → **210** (200이 아니다!) `A 58:52`
  - `incr`: `x = *p = 100`, `y = 110`, `*p = 110`(→ **v1이 110으로 바뀐다**), `return 100`
  - `v1 + v2 = 110 + 100 = 210`
- 지역 변수는 블록이 끝나면 자동 해제되지만(자동 변수), **주소를 넘기면 다른 블록에서도 접근할 수 있게 된다**(call by pointer).
- 관전 포인트: 다른 변수는 레지스터에 두지만 **v1은 주소가 필요하므로 스택에 저장된다.**
- Makefile 컴파일 옵션(따라 할 때 꼭 똑같이 줄 것) `A 1:07:25`
  - `-fno-stack-protector`: 오버플로 공격 방어 코드를 빼고 근본 원리만 보기 위함
  - `-mpreferred-stack-boundary=3`: 8(=2³)바이트 정렬
  - `-fcf-protection=none`

## 슬라이드 24–26: Low Level Debugging (gdb -tui)  `A 1:01:03`, `B 00:00`

```
$ gdb -tui myincr        # 또는 gdb 안에서 Ctrl-x + a
(gdb) layout split       # src + asm 동시에 (layout asm: 어셈블리만)
(gdb) focus cmd
(gdb) b main
(gdb) r
(gdb) display /x $rip
(gdb) display /x $rsp
(gdb) display /x *(long *)($rsp)   # 스택 top 내용 (C 문법 형변환 가능)
```
- 소스 레벨이 아니라 **명령어/레지스터 레벨**로 디버깅한다. 창 이름: SRC / ASM / CMD
- 명령어 단위 실행: `n` → **`ni`**, `s` → **`si`** (교재 그림 3.30 참조)
- 주의: 어셈블리 문법에서는 `%rsp`지만 **gdb에서는 `$rsp`**로 쓴다.
- 자주 쓰는 명령: `x`(메모리 분석), `p`(변수 출력), `display`(매 스텝마다 자동 출력)
- **Q. `main`에서 `callq 0x555555555134`를 `si`로 실행하면?** `A 1:04:10`, `B 03:09`

| | 실행 전 | 실행 후 |
|---|---|---|
| `$rip` | `…5122` | `…5134` (callee 시작) |
| `$rsp` | `…dfc8` | `…dfc0` (−8) |
| `*(long*)$rsp` | `…7083` (main의 caller = **스타트업 코드**의 복귀 주소) | `…5133` (call 다음 명령어 = 복귀 주소) |

  - 기존 top의 `7083`이 바뀌는 것이 아니라, 그 아래에 `5133`이 **추가**된다.
  - main도 누군가(스타트업 코드: `argc`, `argv`를 준비해 주는 코드)가 호출한 것이다.
  - 실습 영상은 i-class에 올라와 있다. 직접 따라 해 볼 것.

## 슬라이드 27: Procedure Call Example (initial state)  `B 06:17`

```asm
0x...5134  sub    $0x8,%rsp            # Set up: 스택 할당
0x...5138  movq   $0x64,(%rsp)         # v1 = 100
0x...5140  mov    %rsp,%rdi            # 1st arg = &v1
0x...5143  mov    $0xa,%esi            # 2nd arg = 10
0x...5148  callq  0x...5156 <incr>
0x...514d  add    (%rsp),%rax          # v1 + v2
0x...5151  add    $0x8,%rsp            # Finish: 스택 해제
0x...5155  retq
```
- 초기 스택: top에 caller(main)의 복귀 주소
- `sub $0x8,%rsp` ↔ `add $0x8,%rsp`가 이 프로시저의 **스택 할당/해제 코드**다(빨간색으로 표시해 둘 것).
  - 할당 = **set-up 코드(prologue)**, 해제 = **finish 코드(epilogue)**

## 슬라이드 28: step 1 — Set up stack  `B 07:17`

- 스택을 **8바이트만** 쓴다(나머지는 모두 레지스터). 그 8바이트가 바로 **v1**이다. → callee에게 `&v1`(주소)을 넘기므로 메모리가 필요하다. 컴파일러가 규칙에 따라 컴파일 시점에 결정한다.
- 8바이트인 것은 `-mpreferred-stack-boundary=3`으로 8바이트 정렬을 강제했기 때문이다. **실제 기본값은 16바이트 정렬**이라 패딩이 붙을 수 있다.

## 슬라이드 29: step 2 — Passing data for call  `B 09:25`

- 규약에 따라 caller가 인자를 준비한다: `%rdi = &v1`(= `%rsp`, 스택 top 주소), `%rsi = 10`(즉시값)

## 슬라이드 30: step 3 — call  `B 10:27`

- 복귀 주소 `0x...514d`를 스택 top에 push한 뒤 `%rip = 0x...5156`(incr)으로 점프한다. 스택 프레임이 자라고 있다.

## 슬라이드 31: step 3 — incr 실행  `B 11:27`

```asm
mov (%rdi),%rax     # x = *p = 100
add %rax,%rsi       # y = 100 + 10 = 110
mov %rsi,(%rdi)     # *p = 110  ← callee가 caller의 지역 변수를 직접 수정
retq                # %rax = 100 (리턴 값)
```

## 슬라이드 32: step 4 — ret  `B 12:30`

- 복귀 주소를 pop하고 `0x...514d`로 복귀한다 → incr의 프레임이 자동으로 사라진다.

## 슬라이드 33: step 5 — v1 + v2

- caller는 리턴 값이 `%rax`에 있다고 가정한다(규약). `add (%rsp),%rax` → v2(100) + v1(110, 스택) = **210**

## 슬라이드 34: step 6 — Finish stack

- `add $0x8,%rsp` → v1을 위해 만들었던 공간을 해제한다.

## 슬라이드 35: step 7 — ret  `B 13:35`

- 복귀 주소를 pop해서 call_incr를 호출한 main으로 돌아간다.
- 정리: 스택 프레임에는 복귀 주소뿐 아니라 **지역 변수도 저장될 수 있다**(주소가 필요한 경우).

## 슬라이드 36: Quiz 4-1 — 인자의 주소를 넘기면?  `B 13:35`

| `bar(x)` | `bar(&x)` |
|---|---|
| `call bar`<br>`add $0x64,%rax`<br>`ret` | `sub $0x8,%rsp`<br>`mov %rdi,(%rsp)`<br>`mov %rsp,%rdi`<br>`call bar`<br>`add $0x64,%rax`<br>`add $0x8,%rsp`<br>`ret` |

- **답**: 오른쪽은 **파라미터 x의 주소**가 필요하므로, `%rdi`에 있던 x를 스택에 저장하고 그 주소(`%rsp`)를 `%rdi`로 넘긴다. 그 결과 set-up/finish 코드가 붙는다.
- 교훈: **파라미터도 주소가 필요하면 스택에 저장된다.** 3줄이면 될 코드가 2배 이상 늘어난다. 공간뿐 아니라 메모리 접근도 낭비된다 → **포인터는 꼭 필요할 때만** 쓸 것.

## 슬라이드 37: Quiz 4-2 — `volatile`  `B 15:45`

```asm
sub    $0x8,%rsp
movq   $0x64,(%rsp)     # y = 100 (메모리)
call   bar
mov    (%rsp),%rdx      # y 읽기   ← 메모리 접근 1
add    %rdx,%rax
mov    %rax,(%rsp)      # y 쓰기   ← 메모리 접근 2
mov    (%rsp),%rax      # y 다시 읽기(return y) ← 메모리 접근 3
add    $0x8,%rsp
ret
```
- **답**: `volatile`은 컴파일러에게 **매번(every time) 메모리에서 읽고 쓰라고** 강제한다 → y는 레지스터에 둘 수 없고 반드시 스택에 있어야 하며, 접근할 때마다 메모리 연산이 일어난다.
- 캐시가 있어도 메모리 접근은 성능(지역성)에 영향을 준다. I/O나 memory-mapped 장치처럼 **정말 필요할 때만** 쓸 것.

## 슬라이드 38: Passing Data — x86-64 Linux calling convention  `B 18:52`

- 인자 1–6: `%rdi, %rsi, %rdx, %rcx, %r8, %r9` (레지스터 — 메모리가 아니다)
  - 암기법(슬라이드): **D**iane's **S**ilk **D**ress **C**osts **$8 9** → di, si, dx, cx, 8, 9
- 인자 7~n: 스택에 **역순**으로 push(n부터 먼저) → **스택 top 쪽에 7번째 인자**가 오므로, callee가 순서대로 꺼낼 수 있다.
- 리턴 값: `%rax`

## 슬라이드 39: Passing Data 예시 (인자 8개)  `B 20:00`

```asm
pushq  $0x8          # 8번째 먼저 (역순)
pushq  $0x7
mov    $0x6,%r9d
mov    $0x5,%r8d
mov    $0x4,%ecx
mov    $0x3,%edx
mov    $0x2,%esi
mov    $0x1,%edi
callq  proc
add    $0x10,%rsp    # pop이 아니라 add!
retq
```
- **왜 `pop`이 아니라 `add $0x10`(=16)인가?** `B 22:05`
  - push 8바이트 × 2 = 16바이트를 할당했으니 16을 더해서 해제한다.
  - callee 입장에서 스택 top에는 **복귀 주소**가 있으므로, callee가 인자를 pop하면 안 된다. callee는 **위치(오프셋)로 읽기만** 한다.
  - 따라서 **스택 포인터 정리는 caller가** 한다. 데이터를 꺼낼 필요가 없으니 pop 대신 add로 `%rsp`만 조정한다.

## 슬라이드 40: Quiz 4-3 — Transfer Data (leaf 최적화)  `B 24:10`

```asm
<bar>
movq   $0x1,-0x8(%rsp)    # volatile y = 1 — %rsp를 조정하지 않고 아래 공간에 바로 씀!
add    %rsi,%rdi          # x1+x2 ... x6까지 레지스터로 누적
...
add    0x8(%rsp),%rdi     # +x7 (복귀 주소 바로 위)
add    0x10(%rsp),%rdi    # +x8
mov    -0x8(%rsp),%rax    # y 읽기 (volatile)
add    %rdi,%rax
ret
```
- 7, 8번째 인자는 pop하지 않고 `0x8(%rsp)`, `0x10(%rsp)`처럼 **오프셋으로 접근**한다.
- **`volatile y`인데 왜 `sub`/`add`(할당/해제)가 없는가?** → `bar`는 **leaf procedure**(call 명령어가 없다)이기 때문이다. `B 26:12`
  - 스택 끝에는 여유 공간(room)이 있어서, leaf 함수는 `%rsp`를 조정하지 않고 `%rsp` 아래(`-0x8(%rsp)`)를 바로 쓴다 → 최적화
  - (보충: System V ABI에서는 이 영역을 **red zone**, `%rsp` 아래 128바이트라고 부른다.)
  - x86뿐 아니라 대부분의 아키텍처에 leaf 프로시저 최적화가 있다.

## 슬라이드 41: x86-64/Linux Stack Frame (정리)  `B 29:24`

- 스택 프레임 = 복귀 주소(필수) + 필요할 때만 지역 변수, 인자, preserved register
- 그래서 x86-64의 스택 프레임은 **가변 크기**다. (어떤 아키텍처는 계산을 단순하게 하려고 고정 크기, 예: 96바이트로 잡는다 — 이것도 규약의 차이다.)
- 스택 할당 자체는 **런타임에 동적으로** 일어나지만, **필요한 크기는 컴파일 타임에 결정된다.**
- 이상적으로는 x86-64 함수에는 복귀 주소 외에 스택 프레임이 전혀 필요 없다.

## 슬라이드 42: Register Saving Conventions (1)  `B 30:33`

- 정수 레지스터는 16개뿐이라 호출이 깊어지면 충돌(contamination)이 생길 수 있다.

```c
long P(long x) { Q(x); return 0; }   // → call Q / mov $0x0,%eax / ret  (문제 없음)
long P(long x) { Q(x); return x; }   // → push %rbx / mov %rdi,%rbx / call Q / mov %rbx,%rax / pop %rbx / ret
```
- 판단 기준: **call 명령어를 경계로, 그 이후에 해당 레지스터 값을 다시 쓰는가(reuse)?**
  - `Q`는 `%rdi`를 마음대로 덮어쓸 수 있다(본문이 없어서 알 수 없지만 그렇다고 가정해야 한다).
  - `return x`처럼 call 이후에 x를 다시 쓰면 → 컴파일러가 **preserved register**라는 다른 카드를 꺼낸다.
- 약속: 16개 중 일부(6개)는 제약을 건다 → **preserved register**(대표: **`%rbx`, `%rbp`**. 외울 것)
  - caller 입장: call 전후로 값이 **유지되어야** 한다.
  - callee 입장: 쓰고 싶으면 **진입할 때 스택에 save(push)하고, 리턴 직전에 restore(pop)**해야 한다.
- 위 코드 해석: x(`%rdi`)를 `%rbx`로 피신 → `%rbx`를 쓰기 전에 나의 caller를 위해 push → call 이후에는 `%rbx`가 x 역할 → 리턴 값으로 `%rbx`를 `%rax`에 → pop으로 restore
- "If you use it, you must put it back!" — 의미 없이 call 이후에 변수를 reuse하지 말 것(`-Og` 기준)

## 슬라이드 43: Register Saving Conventions (2) — 왜 `%rdi`를 직접 push하지 않나?  `B 38:08`

- 질문: 어차피 스택을 쓸 거라면 `push %rdi` / `pop %rdi`가 더 짧지 않나? → 호출이 한 번이면 맞다.
- 하지만 프로시저는 **여러 번 호출된다**고 가정해야 한다.

```c
long P(long x) { Q(x); Q(x); return x; }
```
```asm
push %rbx
mov  %rdi,%rbx      # 한 번만 피신
call Q
mov  %rbx,%rdi      # 두 번째 호출의 인자도 %rbx에서
call Q
mov  %rbx,%rax
pop  %rbx
ret
```
- `%rdi`를 push/pop하는 전략이면 **호출할 때마다 메모리에 접근**해야 한다. preserved register 전략은 **한 번만 push/pop**하고 이후에는 `%rbx`를 `%rdi` 대신 쓴다 → 메모리 접근이 줄어든다.

## 슬라이드 44: Register Saving Conventions (3) — 여러 값을 보존할 때  `B 41:16`

```c
long P(long x) { long v = Q(x); long u = Q(x); return x + u + v; }
```
```asm
push %rbp
push %rbx
mov  %rdi,%rbx      # x → %rbx
call Q
mov  %rax,%rbp      # v → %rbp (두 번째 호출의 리턴 값이 %rax를 덮어쓰므로)
mov  %rbx,%rdi
call Q              # u = %rax
add  %rbx,%rax      # u + x
add  %rbp,%rax      # + v
pop  %rbx
pop  %rbp
ret
```
- reuse되는 값이 x(`%rdi`)와 v(`%rax`) 두 개 → preserved register가 2개 필요 → **push 2개, pop 2개**가 나올 것이라고 미리 예상할 수 있어야 한다.
- 더 필요하면 `%r12–%r15`를 쓰고, 그래도 부족하면 스택에 저장한다.

## 슬라이드 45: Callee Saved Registers  `B 45:38`

- **Callee-saved (preserved)**: `%rbx, %rbp, %r12, %r13, %r14, %r15`
  - callee가 쓰기 전에 자기 스택 프레임에 저장하고, 리턴 전에 복원한다.
- 나머지는 **caller-saved** 레지스터다.
- 용어가 통일되어 있지 않다. 교수님은 caller/callee가 상대적이라 헷갈리므로 **"preserved register"**라는 용어를 선호한다. "callee-saved register라고도 불린다" 정도로 정리할 것.

## 슬라이드 46: Quiz 4-4 — 빈칸 채우기 (기출, 기말 출제 가능)  `B 46:39`

```asm
0000000000400540 <multstore>:
400540: push %rbx               # Save %rbx      ← 정답
400541: movq %rdx,%rbx          # Save dest
400544: call 400550 <mult2>
400549: movq %rax,(%rbx)        # Save at dest
40054c: pop  %rbx               # Restore %rbx   ← 정답
40054d: ret
```
- 풀이 관점: **call 이후에 reuse되는 레지스터가 무엇인가?**
  - x(`%rdi`), y(`%rsi`)는 `mult2` 이후에 쓰지 않으니 보존할 필요가 없다.
  - **dest(`%rdx`)는 call 이후에 쓴다.** `mult2`가 `%rdx`를 실제로 쓰는지는 이 오브젝트를 컴파일하는 시점에는 알 수 없다(링크 시점에 결정되며, mult2가 또 다른 함수를 부를 수도 있다) → 오염될 수 있다고 가정한다.
  - → preserved register 중 `%rbx`를 골랐으므로(`movq %rdx,%rbx`), 위는 `push %rbx`, 아래는 `pop %rbx`

## 슬라이드 47: x86-64 Procedure Summary  `B 48:51`

- **스택 사용을 최소화**하고 **레지스터를 적극 활용**한다(인자 전달, 지역 변수).
- frame pointer는 더 이상 쓰지 않고 `%rsp`만 쓴다.
- **복귀 주소는 반드시 스택에 저장된다.**
- 그 외에 스택 프레임이 필요한 경우(= 꼭 필요할 때만):
  - 지역 변수가 너무 많아 레지스터에 다 담을 수 없을 때
  - 지역 변수에 **`&` 연산자**를 쓸 때, **배열/구조체**일 때, **`volatile`**일 때
  - **인자가 6개를 넘는** 함수를 호출할 때
  - call을 넘어 **레지스터 값을 보존**해야 할 때(reuse가 많을 때)

---

## 다음 시간 예고  `A 1:08:28`

- **메모리 데이터 정렬(alignment)** — 다음 시간의 주인공
  - 메모리는 byte-addressable이지만, x86은 데이터 크기에 따라 주소에 제약을 건다: 8바이트 `long` → 8의 배수 주소(하위 3비트가 0), 4바이트 → 4의 배수, `short` → 2의 배수. 성능과 관련이 있다.
  - **스택 프레임의 기본 정렬은 16바이트**다(규약). 이번 예제는 패딩 없이 이해하기 쉽게 하려고 8바이트 정렬(`-mpreferred-stack-boundary=3`)로 강제한 것이다.
