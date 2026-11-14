# Procedure Call and Stack (x86-64 / Linux)

## 1. 들어가며: 이번 장의 주인공 `%rsp`

지금까지는 함수 하나가 어떻게 실행되는지를 봤다. 이번 장에서는 **여러 함수(프로시저)가 서로를 호출할 때 바이너리 수준에서 무슨 일이 일어나는지**를 본다.

먼저 알아야 할 레지스터는 두 개다.

- `%rip` (Program Counter): **다음에 실행할 명령어의 주소**
- `%rsp` (Stack Pointer): **스택의 top 주소**

지난 장의 주인공이 조건 코드를 담는 `%rflags`였다면, 이번 장의 주인공은 `%rsp`다. 함수 호출과 `%rsp`의 변화는 떼어 놓을 수 없다.

## 2. 왜 프로시저를 쓰는가

프로시저(함수)는 특정 작업을 수행하는 **재사용 가능한 코드 블록**이다. 장점은 재사용성, 추상화, 가독성·모듈화다.

어떤 함수를 100번 호출해야 하는데 프로시저가 없다면, 그 코드를 100번 복사해 넣어야 한다. 코드 크기가 폭발할 뿐 아니라, 재귀처럼 몇 번 호출될지 컴파일 시점에 알 수 없는 경우에는 아예 불가능하다.

또 하나의 장점은 **동적 할당**이다. 함수의 지역 변수는 그 함수가 실제로 호출될 때만 메모리를 잡으면 된다.

ISA가 프로시저를 위해 기본으로 제공하는 것은 `call`과 `ret`이다. `jmp`와 다른 점은, `call`로 간 곳(callee)이 끝나면 **반드시 부른 곳(caller)으로 돌아와야 한다**는 것이다.

- **caller**: 함수를 부르는 쪽
- **callee**: 부름을 받는 쪽

이 역할은 상대적이다. `main → A → B`라면 A는 main의 callee이면서 B의 caller다. `call` 명령어가 없는 함수, 즉 다른 함수를 부르지 않는 함수는 **leaf procedure**라고 부른다.

## 3. 왜 스택인가

돌아오려면 **돌아갈 주소(return address)를 어딘가에 저장해야 한다.** 호출이 중첩되면 이런 주소를 여러 개 보관해야 한다.

저장할 수 있는 곳은 레지스터 아니면 메모리다. 레지스터는 개수가 적어서 호출이 깊어지면 결국 부족해진다. 그래서 x86은 **메모리**를 선택했고, 이 영역을 **콜 스택(call stack)**, 줄여서 스택이라고 부른다.

A → B → C 순으로 호출했다면 C가 끝난 뒤에는 B로, B가 끝난 뒤에는 A로 돌아가야 한다. 마지막에 들어온 것이 먼저 나가므로 **LIFO(Last-In First-Out)** 구조이고, 그래서 스택이 딱 맞는다.

호출 한 번에 필요한 정보의 묶음을 **스택 프레임(stack frame)**이라고 한다. 100번 호출하면 프레임도 100개가 생긴다.

## 4. ABI: 바이너리 수준의 약속

- **ISA**: 하드웨어가 소프트웨어에게 **무엇을 제공하는가** (레지스터, 메모리, 명령어)
- **ABI (Application Binary Interface)**: 그 ISA를 바이너리 수준에서 **어떻게 사용할 것인가**에 대한 약속

예를 들어 "리턴 값은 `%rax`에 둔다"는 약속이 있다. 누군가 `%rbx`에 리턴 값을 둔다면, 따로 컴파일된 코드끼리는 통신할 수 없다. OS, 라이브러리, 애플리케이션이 함께 돌아가려면 모두 같은 ABI를 지켜야 한다. 이 약속을 지켜야 하는 도구는 컴파일러, 링커, 로더다.

**같은 ISA라도 ABI는 다를 수 있다.**

- x86-64 Linux / Unix → **System V AMD64 ABI**
- x86-64 Windows → **Microsoft x64 ABI**

이 글은 Linux 기준이므로 System V AMD64 ABI를 따른다. 이름에 AMD64가 붙은 이유는 AMD가 64비트 확장을 먼저 했기 때문이고, x86-64와 같은 것이다.

ABI는 크게 두 부분으로 나뉜다.

- **gABI (Generic ABI)**: 프로세서와 **무관한** 규약. 예: ELF 실행 파일 포맷
- **psABI (Processor Supplement ABI)**: 프로세서에 **종속적인** 규약. 그 핵심이 **Calling Convention**이다.

> 시험 포인트: "ABI가 뭔가요?"에 "Application Binary Interface"라고만 답하면 부족하다. "바이너리 수준에서 ISA를 어떻게 사용할지 정한 규약이고, 프로세서 독립적인 gABI와 프로세서 종속적인 psABI로 나뉜다"까지 말할 수 있어야 한다.

## 5. Calling Convention의 4가지 범주

1. **Stack operation**: 스택 프레임을 어떻게 할당·해제하는가
2. **Passing control**: 어떻게 callee로 가고 caller로 돌아오는가
3. **Passing data**: 인자와 리턴 값을 어디로 전달하는가
4. **Register saving convention**: 호출 전후로 레지스터 값을 어떻게 보존하는가

하나씩 보자.

## 6. Stack operation

x86-64의 스택은 **높은 주소에서 낮은 주소 방향으로(아래로) 자란다.** 그래서 할당하면 `%rsp`가 **감소**하고, 해제하면 **증가**한다.

```asm
pushq %rcx        # = subq $8, %rsp      (공간 할당)
                  #   movq %rcx, (%rsp)  (저장)

popq  %rcx        # = movq (%rsp), %rcx  (읽기)
                  #   addq $8, %rsp      (공간 해제)
```

pop을 해도 그 자리의 데이터는 지워지지 않고 남아 있다. 그냥 더 이상 쓰지 않을 뿐이다. 초기화하지 않은 지역 변수에 "쓰레기 값"이 보이는 이유가 여기에 있다.

### 스택 프레임의 크기는 가변적이다

스택 프레임에 반드시 들어가는 것은 **return address 하나뿐**이다. 나머지는 **필요할 때만** 들어간다. 스택은 메모리이고 메모리 접근은 레지스터보다 느리기 때문에, 현대 x86-64는 **스택 사용을 최소화**하는 것을 원칙으로 한다.

필요한 크기는 **컴파일 시점에 결정**되고, 실제 할당은 호출될 때(런타임) 일어난다.

### `%rbp`(frame pointer)는 이제 optional

옛날 32비트 x86에서는 프레임의 시작을 가리키는 `%rbp`와 끝을 가리키는 `%rsp`를 둘 다 유지했다. x86-64에서는 효율을 위해 `%rbp`를 빼고 `%rsp` 기준으로 모두 계산한다. 그래서 `%rbp`도 범용 레지스터로 쓸 수 있다.

```c
long func(long x) { long y = 100; return x + y; }
```

- `-Og`로 컴파일하면 `lea 0x64(%rdi),%rax` / `ret` 두 줄로 끝난다. 레지스터만으로 해결된다.
- `-O0`로 컴파일하면 `push %rbp` / `mov %rsp,%rbp`로 시작해서 x와 y를 모두 스택에 쓴다. 메모리 접근이 많아 느리다.

## 7. Passing control: `call`과 `ret`

```asm
400544: call 400550 <mult2>
400549: ...                  # ← return address
```

**return address는 `call` 명령어 바로 다음 명령어의 주소**다. 위 예에서는 `0x400549`다.

- `call label`
  1. return address를 스택에 push한다 (`%rsp -= 8`)
  2. label로 점프한다 (`%rip = label`)
- `ret`
  1. 스택 top에서 return address를 pop한다 (`%rsp += 8`)
  2. 그 주소로 점프한다

x86-64에서 주소는 8바이트이므로 `%rsp`가 8씩 움직인다. 이때 16진수 계산에 주의하자. `0x120 - 8 = 0x118`이다.

스냅샷 문제를 풀 때는 **먼저 `%rip`를 보고** 다음에 실행할 명령어가 무엇인지 확인하는 습관을 들이면 좋다. 함수에 막 들어온 직후라면 스택 top에는 그 함수를 부른 caller의 return address가 있다.

## 8. Passing data: 인자와 리턴 값

정수와 포인터 인자는 **6개까지 레지스터**로 전달한다.

```
1번째: %rdi
2번째: %rsi
3번째: %rdx
4번째: %rcx
5번째: %r8
6번째: %r9
리턴 값: %rax
```

> 암기법: **D**iane's **S**ilk **D**ress **C**osts **$8 9** → di, si, dx, cx, 8, 9

7번째부터는 **스택**으로 전달하는데, **역순으로** push한다. 그래야 스택 top 쪽에 7번째 인자가 와서 callee가 순서대로 읽을 수 있다.

```asm
pushq  $0x8          # 8번째 인자 먼저
pushq  $0x7          # 7번째 인자
mov    $0x6,%r9d
mov    $0x5,%r8d
mov    $0x4,%ecx
mov    $0x3,%edx
mov    $0x2,%esi
mov    $0x1,%edi
callq  proc
add    $0x10,%rsp    # pop이 아니라 add로 정리
```

**왜 `pop`이 아니라 `add $0x10,%rsp`일까?**

- callee에 들어간 순간 스택 top에는 return address가 있으므로, callee는 인자를 pop할 수 없다. 대신 `0x8(%rsp)`, `0x10(%rsp)`처럼 **오프셋으로 읽기만** 한다.
- 호출이 끝난 뒤 caller는 그 값을 다시 꺼낼 필요가 없으니, 16바이트(8 × 2)만큼 `%rsp`를 올려서 공간만 해제한다.
- 즉 **스택 인자의 정리는 caller가 한다.**

## 9. 지역 변수가 스택에 올라가는 경우

x86-64에서 지역 변수는 기본적으로 레지스터에 둔다. 스택에 올라가는 경우는 다음과 같다.

1. **레지스터가 부족할 만큼** 지역 변수가 많을 때
2. **주소가 필요할 때**. 레지스터에는 주소가 없기 때문이다.
   - `&` 연산자를 쓸 때
   - 배열·구조체일 때
   - `volatile`일 때 (매번 메모리에서 읽고 쓰라는 뜻이므로)

이 외에 7번째 이후 **인자**, 그리고 뒤에서 볼 **preserved register**를 보존할 때도 스택을 쓴다.

### 예제: `call_incr` / `incr`

```c
long incr(long *p, long val) {
    long x = *p;
    long y = x + val;
    *p = y;
    return x;
}

long call_incr() {
    long v1 = 100;
    long inc = 10;
    long v2 = incr(&v1, inc);
    return v1 + v2;
}
```

```asm
call_incr:
  sub    $0x8,%rsp          # v1을 위한 공간 할당
  movq   $0x64,(%rsp)       # v1 = 100
  mov    %rsp,%rdi          # 1번째 인자 = &v1
  mov    $0xa,%esi          # 2번째 인자 = 10
  callq  incr
  add    (%rsp),%rax        # v1 + v2
  add    $0x8,%rsp          # 공간 해제
  retq
```

- `inc`는 레지스터만으로 충분하지만, **v1은 주소(`&v1`)가 필요하므로 스택에 올라간다.**
- `incr`는 `*p = 110`으로 caller의 v1을 직접 바꾸고, 원래 값 100을 리턴한다.
- 그래서 결과는 200이 아니라 **110 + 100 = 210**이다.

`callq incr`를 실행한 직후의 스택은 이렇다. 위가 높은 주소, 아래가 낮은 주소(스택 top)다.

```
┌────────────────────────────┐
│ return addr (→ main)        │  call_incr의 프레임
├────────────────────────────┤
│ 100 (v1)                    │  call_incr의 프레임
├────────────────────────────┤
│ return addr (0x...514d)     │  incr의 프레임   ← %rsp
└────────────────────────────┘
```

return address가 두 개 있다는 점에 주의하자. 위쪽은 main이 call_incr를 부를 때 쌓은 것이고, 아래쪽은 call_incr가 incr를 부를 때 쌓은 것이다.

### Quiz: 파라미터의 주소를 넘기면?

`bar(x)`를 호출하는 함수는 세 줄이면 끝나지만, `bar(&x)`로 바꾸면 **파라미터 x도 스택에 저장**해야 한다. `%rdi`에 있던 x를 스택에 쓰고, 그 주소(`%rsp`)를 다시 `%rdi`로 넘긴다. 할당·해제 코드가 붙어서 코드가 두 배 이상 길어진다. **포인터는 꼭 필요할 때만 쓰자.**

### Quiz: `volatile`

`volatile long y = 100;`이면 y는 레지스터에 둘 수 없고 반드시 스택에 있어야 한다. 그리고 y를 읽고 쓸 때마다 매번 메모리에 접근한다. I/O나 memory-mapped 장치처럼 정말 필요할 때만 쓰자.

### Leaf procedure 최적화

`call`이 없는 leaf 함수는 `sub`/`add`로 `%rsp`를 조정하지 않고, **`%rsp` 아래 공간(`-0x8(%rsp)` 등)을 바로 쓰기도 한다.** 다른 함수를 부르지 않으니 그 공간을 덮어쓸 일이 없기 때문이다. System V ABI에서는 이 영역(`%rsp` 아래 128바이트)을 **red zone**이라고 부른다.

## 10. Register saving convention

정수 레지스터는 16개뿐이라, 호출이 이어지면 레지스터 값이 덮어써질(오염될) 수 있다.

```c
long P(long x) { Q(x); return x; }
```

x는 `%rdi`에 들어 있다. 그런데 Q도 `%rdi`를 마음대로 쓸 수 있다. Q의 내용은 컴파일 시점에 알 수 없으니, 컴파일러는 "Q가 `%rdi`를 덮어쓴다"고 가정해야 한다. 그러면 Q가 끝난 뒤 `return x`를 할 때 x가 이미 사라져 있을 수 있다.

판단 기준은 하나다. **`call`을 경계로, 그 이후에 해당 레지스터 값을 다시 쓰는가(reuse)?**

- `Q(x); return 0;`이라면 x를 다시 쓰지 않으니 아무 문제가 없다.
- `Q(x); return x;`라면 x를 보존해야 한다.

### Preserved register (callee-saved register)

그래서 ABI는 16개 중 일부 레지스터에 약속을 걸어 두었다.

- **preserved(callee-saved)**: `%rbx, %rbp, %r12, %r13, %r14, %r15`
- 나머지는 **caller-saved**

약속의 내용은 이렇다.

- caller 입장: preserved register에 넣어 둔 값은 **call 이후에도 그대로 유지된다**고 믿을 수 있다.
- callee 입장: preserved register를 쓰고 싶으면 **진입할 때 push로 저장하고, 리턴 직전에 pop으로 복원**해야 한다.

> "If you use it, you must put it back!"

```asm
P:
  push %rbx          # 나도 %rbx를 쓸 거니까, 나의 caller를 위해 원래 값 저장
  mov  %rdi,%rbx     # x를 %rbx로 피신
  call Q             # Q가 %rdi를 덮어써도 %rbx는 안전
  mov  %rbx,%rax     # return x
  pop  %rbx          # %rbx 원래 값 복원
  ret
```

### 왜 그냥 `%rdi`를 push/pop하지 않을까?

호출이 한 번뿐이면 `push %rdi` / `pop %rdi`가 더 짧다. 하지만 함수는 여러 번 호출될 수 있다.

```c
long P(long x) { Q(x); Q(x); return x; }
```

`%rdi`를 push/pop하는 방식은 **call할 때마다** 메모리에 접근해야 한다. preserved register 방식은 처음에 **한 번만** push하고, 그 뒤로는 `%rbx`를 `%rdi` 대신 계속 쓰면 된다. 메모리 접근이 줄어든다.

보존할 값이 두 개라면 preserved register도 두 개(`%rbx`, `%rbp`)를 쓰고, push 두 번과 pop 두 번이 나온다. 더 필요하면 `%r12`~`%r15`를 쓰고, 그래도 부족하면 스택에 저장한다.

### Quiz: 빈칸 채우기 (기출)

```c
void multstore(long x, long y, long *dest) {
    long t = mult2(x, y);
    *dest = t;
}
```

```asm
400540: ______________     # (1)
400541: movq %rdx,%rbx     # dest 보존
400544: call 400550 <mult2>
400549: movq %rax,(%rbx)   # *dest = t
40054c: ______________     # (2)
40054d: ret
```

- x(`%rdi`)와 y(`%rsi`)는 mult2 이후에 다시 쓰지 않으니 보존할 필요가 없다.
- **dest(`%rdx`)는 call 이후에 다시 쓴다.** 그래서 preserved register인 `%rbx`로 옮겨 두었다.
- `%rbx`를 쓰니까 (1)은 `push %rbx`, (2)는 `pop %rbx`다.

## 11. 정리

- 현대 x86-64는 **스택 사용을 최소화**하고 레지스터를 적극 활용한다.
- frame pointer(`%rbp`)는 더 이상 필수가 아니고, `%rsp`만으로 계산한다.
- **return address는 반드시 스택에 저장된다.**
- 그 외에 스택을 쓰는 경우는 꼭 필요할 때뿐이다.
  - 지역 변수가 너무 많을 때
  - 주소가 필요할 때 (`&`, 배열·구조체, `volatile`)
  - 인자가 6개를 넘을 때
  - call 이후에 다시 쓸 값을 preserved register로 보존할 때

## 다음 이야기: 정렬(alignment)

이번 예제는 이해하기 쉽도록 `-mpreferred-stack-boundary=3`(8바이트 정렬)로 컴파일했다. 실제 기본값은 **스택 프레임 16바이트 정렬**이라 프레임에 패딩이 붙을 수 있다. 다음 장에서는 메모리 데이터 정렬을 다룬다.
