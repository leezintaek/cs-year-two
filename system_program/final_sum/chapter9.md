# 9. Derived Types: Array, Pointer, and Structure — 강의노트

- 과목: CSE3209 System Programming
- 교재: Bryant & O'Hallaron, *Computer Systems* 3rd Ed. §3.8–3.9 (+ aliasing은 4장 optimization), K&R *The C Programming Language* (특히 5장)
- 강의 영상
  - **A** = `hls-converted-1794641500759.mp4` (약 19분) — 슬라이드 1–8 (8장 강의 마지막 부분에서 이어짐)
  - **B** = `hls-converted-1794641540364.mp4` (11/3 강의, 약 67분) — 슬라이드 8–30
  - **C** = `hls-converted-1794641569708.mp4` (그다음 강의, 약 52분) — 슬라이드 31–50 (이후 7장 linking 시작 예고)
- 타임스탬프 표기: `A 12:07` = 영상 A의 12분 7초
- 원문 전사: `hls-converted-*.transcript.md` (`_workspace/system_program/chapter9/`)

> 이번 장의 핵심: **high-level의 index·member 표기는 machine level에서 전부 address로 변환된다.** 그러려면 type을 해석해서 메모리상의 **형상(layout)과 정확한 size**를 머릿속에 그릴 수 있어야 한다. Array는 homogeneous·contiguous라 계산이 쉽고, structure는 heterogeneous라 **alignment / padding** 규칙을 알아야 한다.

---

## 슬라이드 1–3: 표지 · Content · C Data Types  `A 00:00`

- 교재는 Bryant 3.8, 3.9절. 배경 지식이 필요한 부분은 K&R 교재(Dennis Ritchie, Brian Kernighan — C 언어를 만든 사람, Turing Award 수상)로 보충한다. 학년마다 아는 정도가 달라서 기본을 한 번 정리해 준다고 하심.
- 지금까지의 흐름은 **확장**이다. 8장이 procedure의 확장이었다면 이번 장은 **data type의 확장**이다.
  - 전반부에서는 primitive type 10개(signed integer 4개, unsigned integer 4개, floating point single/double 2개)가 어떻게 표현·해석되는지 봤다.
  - 이제 derived type(array, pointer, structure, union, function)과 이것들의 **combination**(structure의 array, structure 안의 array·pointer·function pointer …)으로 만들어지는 complex data type이 low level에서 어떻게 처리되는지 본다.
- 정확한 size와 물리적 형상을 이해하지 못하면 compile error뿐만 아니라 "나중에 아주 큰 재앙"이 온다.

## 슬라이드 4: C Operators  `A 02:02`

- 하나의 expression도 low level에서는 operator 단위로 쪼개져 instruction으로 수행되므로, **어떤 순서로 계산하느냐(operator precedence)**가 프로그래머의 의도와 logically equivalent해야 한다.
- 대략 단항 → 산술(`*`가 `+`보다 높음) → 관계 → 논리(비트곱이 비트합보다 높음) → 대입 순.
- 우선순위가 같으면 **associativity**로 정한다. 대부분 left to right이지만 **단항 연산자와 대입 연산자는 right to left**다 (`x = y = z`는 오른쪽부터).

## 슬라이드 5: C Derived Type Tokens  `A 05:06`

Type token은 세 가지다. 영어로 읽는 연습을 하라고 강조하셨다.

| Token | 읽는 법              |
|-------|----------------------|
| `*`   | pointer to …         |
| `[]`  | array of …           |
| `()`  | function returning … |

- 같은 기호가 operator로도 쓰여서 헷갈린다: `*`는 dereferencing operator, `[]`는 index operator, `()`는 function call.
- **Good news: type 해석의 우선순위는 operator precedence와 같다.** → **`[]`, `()` > `*`** (이것만 기억하라고 하심) `A 06:15`
- 예 (식별자 = 변수, 나머지는 전부 type token)
  - `char *foo;` → foo is a pointer to char → **8바이트** (뒤가 char든 double이든 struct든 pointer로 끝나면 8)
  - `int foo[5];` → foo is an array of 5 ints → 머릿속에 덩어리 5개가 그려져야 함 → **20바이트**
  - `double foo();` → foo is a function returning double → 선언일 뿐 변수가 아님. `sizeof`에 function 이름을 넣으면 UB이지만 **GNU 기준 1**로 기억하자. `A 09:21`

## 슬라이드 6: Clockwise Spiral Rule  `A 09:21`

**식별자에서 시작해 inside → outside로**, 우선순위(`[]`, `()` > `*`)를 따라 확장해 나간다.

- `char *foo[3];` → foo is an **array[3] of pointers** to char → 3개짜리 array를 그리고 각 item이 pointer → **24바이트**
  - 1학년 때 "포인터 배열"이라고 외웠을 수도 있지만 용어는 중요하지 않다. 영어로 type을 읽고 형상이 떠오르면 된다.
- `char (*foo)[3];` → 여기 괄호는 function이 아니라 **우선순위 괄호** → foo is a **pointer to array**[3] of char → **8바이트**. 주소로 가면 3개짜리 char array가 있다("배열 포인터").

## 슬라이드 7: Function Pointers  `A 12:30`

- Function을 compile하면 label이 붙은 instruction block이 되고, **function 이름은 그 code block의 시작 주소(constant)**다. High level에서도 function 이름을 주소로 인지하라.
- 이 주소를 저장하는 변수가 function pointer 변수다: `Return-type (*fptr)(parameter-type list);`
- `int (*f)(int, int);` → f is a pointer(8바이트 변수) to function (int 2개를 받아) returning int. **Signature가 맞아야** 저장할 수 있다.
  ```c
  f = add;                    // add 함수의 시작 주소 저장
  int answer = (*f)(4, 5);    // dereference하면 add처럼 동작 → 9
  // f = mul로 바꾸면 같은 호출이 20 → runtime에 동적으로 함수 교체
  ```
- **활용: system programming에서 device switch.** 마우스·키보드·SSD 등 device마다 read 요청이 오면 해당 device driver의 read 함수로 function pointer를 바꿔 호출한다. Function pointer들을 관리하는 table도 있다. `A 15:36`

## 슬라이드 8: Type Expressions Puzzle (1)  `A 16:42`, `B 01:01`

학습 목표는 각 type의 **정확한 size**와 low level에서의 처리 방식. (LP-64 가정)

| 선언          | 읽기                         | `sizeof` |
|---------------|------------------------------|----------|
| `int A1[3]`   | array[3] of int              | 12       |
| `int *A2[3]`  | array[3] of pointer to int   | 24       |
| `int (*A3)[3]`| pointer to array[3] of int   | 8        |

- A2는 각 pointer가 가리키는 곳도 살아 있어야 dereference할 수 있다(나중에 heap에 할당). A3는 주소를 따라가면 int 3개짜리 array가 나와야 하며, 안 맞으면 compiler가 type matching에서 compile error를 낸다. `A 17:43`

## 슬라이드 9: Type Expressions Puzzle (2)  `B 03:05`

| 선언                | 읽기                                  | `sizeof`       |
|---------------------|---------------------------------------|----------------|
| `int *A1[3][5]`     | array[3] of array[5] of pointer to int| 3×5×8 = 120    |
| `int (*A2)[3][5]`   | pointer to array[3] of array[5] of int| 8              |
| `int (*A3[3])[5]`   | array[3] of pointer to array[5] of int| 3×8 = 24       |

- A1: 40바이트(pointer 5개) 덩어리가 3개. 1학년 때는 2차원 배열을 논리적인 행렬로 봤지만, machine level에서 메모리는 **linear한 byte 배열**이다. 2차원을 1차원으로 mapping하는 형상을 그릴 줄 알아야 address translation이 자연스러워진다. `B 04:06`
- High level은 index 기반(비전공자에게도 설명 가능)이지만, 물리 메모리에서 index는 사라지고 **address로 변환**된다.
- A3: pointer 3개(24바이트)짜리 array, 각 주소로 가면 1차원 array가 주렁주렁 달려 있다.

## 슬라이드 10: Type Expressions Puzzle (K&R 5.12)  `B 07:10`

| 선언              | 읽기                                              | size |
|-------------------|---------------------------------------------------|------|
| `int p;`          | integer                                           | 4    |
| `int p[7];`       | array[7] of integer                               | 28   |
| `int *p;`         | pointer to integer                                | 8    |
| `int *p[7];`      | array[7] of pointer to integer                    | 56   |
| `int (*p)[7];`    | pointer to array[7] of integer                    | 8    |
| `int **p;`        | pointer to pointer to integer                     | 8    |
| `void f();`       | function returning void                           | 1    |
| `void *f();`      | function returning pointer to void                | 1    |
| `void (*fp)();`   | pointer to function returning void                | 8    |
| `void *(*fp)();`  | pointer to function returning pointer to void     | 8    |
| `void (*fp[7])();`| array[7] of pointer to function returning void    | 56   |

- 다중 pointer(`**`, `***`)도 compiler 입장에서는 그냥 **주소를 저장하는 8바이트 변수**일 뿐이다.
- Function은 변수가 아니라 선언이다(linking에서 자세히). `sizeof(function)`은 UB지만 GNU 기준 1.
- `void`와 `void *`는 다르다. `void *`는 주소(8바이트)다. `B 09:12`
- 마지막 `fp[7]`은 **function pointer table**(함수 주소 테이블)로 해석할 수 있다.

## 슬라이드 11: Type Expressions Puzzle (sizeof 출력)  `B 11:17` ★기말 출제

```c
int f1(int, int);              // function → 1
int (*f2)(int, int) = add;     // pointer → 8
void *(*f3)();                 // pointer → 8
void *(*f4)(void *);           // pointer → 8
void *(*f5[3])(void *);        // array[3] of pointer → 24
```

- 답: **`f5: 24`**. `%lu`는 unsigned long 출력용 형식 지정자(size는 `%zu`로도 출력).
- "이런 식으로 기말고사가 나온다"고 하심.

## 슬라이드 12: Complex Type Expression Puzzle  `B 12:18` ★기출

- `int (*(*x[3])())[5];` → x is an array[3] of pointers to functions returning a pointer to array[5] of ints
  - **`sizeof(x)` = 24 → 답 D**
- `void (*y[NR])();` (`NR = 128`) → array[128] of pointer to function returning void → `128 × 8 = 2^7 × 2^3 = 2^10 =` **1024**
  - 인자 없이 void를 리턴하는 함수들의 table. 나중에 OS의 **system call table**이나 device table이 이런 형태다. `B 14:35`
- "x의 값/y의 크기/출력값은?" 형태로 기말 기출문제가 나온다.

## 슬라이드 13–14: Const Keyword  `B 14:35`

`const`는 read-only(수정 불가). 위치가 달라도 type token 해석 순서대로 읽으면 된다.

- `const int *p;` → p is a pointer to **int constant** → pointer(주소)는 바꿀 수 있지만, 그 주소로 dereference한 **값**은 못 바꾼다.
- `int *const p;` → p is a **constant pointer** to int → **주소 자체**는 못 바꾸고, 가리키는 int 값은 바꿀 수 있다.

슬라이드 14 예제 결과:

| 코드           | 결과                                              |
|----------------|---------------------------------------------------|
| `*p1 = 30;`    | (1) **error**: assignment of read-only location   |
| `p1 = &value3;`| (2) OK                                            |
| `*p2 = 40;`    | (3) OK                                            |
| `p2 = &value4;`| (4) **error**: assignment of read-only variable   |

## 슬라이드 15–17: Array  `B 17:45`

"Array는 큰 이슈가 없다, 복습한다고 생각하고 편하게 들으라"고 하심.

- `T A[N];` → type T, 길이 N. 핵심 정의는 **homogeneous**(모든 원소가 같은 type T)하고 **contiguous**하게 allocation된다는 것. `B 18:51`
- High level의 index 접근(`A[1] = 1`)은 low level에서 **address로 translation**된다. 원소 크기 `K = sizeof(T)`만큼 stepping한다 (char면 1, int면 4씩).
- `T A[N];`의 두 가지 효과
  1. `N × K` 바이트의 contiguous 영역 할당
  2. 식별자 `A`가 배열의 시작 주소로 쓰인다. Type은 `T *` — **pointer to 첫 번째 원소**
- **Array-pointer decay rule** `B 23:00`: `int a[3]`의 `a`는 "int 3개짜리 array"인데, pointer로 보면 `int *`다. 직관과 달리 주소로 가면 array가 아니라 **첫 번째 원소**가 튀어나온다. 배열 시작 주소 = 첫 원소의 시작 주소이므로 "3개짜리"라는 정보를 decay시킨 것.
  - 이렇게 설계한 이유: 배열 이름을 `int *p`로 받아서 `*p`, `*(p+1)`처럼 시작 주소 기반으로 각 원소에 접근할 수 있게 하려고.
  - **`*(a+i)` ≡ `a[i]`** — compiler도 같은 것으로 보고 address 계산 instruction을 낸다.
- 예: `E[i]` → `movl (%rdx,%rcx,4), %eax` (`%rdx` = E의 시작 주소, `%rcx` = i, int라서 ×4) `B 26:04`
  - 배열·구조체는 local이면 **stack**, global이면 data 영역 — 즉 **메모리**에 저장되므로 시작 주소가 필요하다. (최적화 레벨을 높이고 원소가 적으면 register에 둘 수도 있는 예외는 있음)

**슬라이드 17 Quiz** `B 28:18`

| Array             | Element size | Total size | Element i  |
|-------------------|--------------|------------|------------|
| `char A[12]`      | 1            | 12         | `x_A + i`  |
| `char *B[8]`      | 8            | 64         | `x_B + 8i` |
| `int C[6]`        | 4            | 24         | `x_C + 4i` |
| `double *D[5]`    | 8            | 40         | `x_D + 8i` |

Start address는 각 식별자. 단, 그 식별자의 type은 "주소로 가면 첫 번째 원소가 나온다"(decay rule).

## 슬라이드 18–19: Two-Dimensional (Nested) Arrays  `B 29:20`

- 2차원 배열은 논리적으로는 행렬이지만, 물리적으로는 byte 단위 1차원으로 저장된다.
- 저장 방식은 역사적으로 **row-major ordering**(행 중심)과 column-major ordering(열 중심) 두 가지. **C와 대부분의 최근 언어는 row-major**. 교재도 row-major로 가정한다.
- `int A[3][4];` → A is an array[3] of array[4] of int → **덩어리(chunk, sub-array) 3개**, 덩어리 하나 = int 4개 = 16바이트. "array of array"라서 nested array라고 부른다. `B 31:32`
- `T A[R][C];` → 전체 크기 **`R × C × K`** 바이트
- 2차원 배열의 원소 주소를 찾으려면 **sub-array의 크기(`C × K`)**가 중요하다.

## 슬라이드 20: Nested Array Row Access Code  `B 35:57`

```c
int sea[4][5];                       // 덩어리 4개, 덩어리 = 4×5 = 20바이트
int *get_sea_zip(int index) { return sea[index]; }
```
```
leaq (%rdi,%rdi,4), %rax    # 5 * index
leaq sea(,%rax,4), %rax     # sea + 20 * index
```

- `sea[index]`는 index번째 **덩어리**(sub-array)의 주소 → 20의 배수가 나올 것을 예측해야 한다. 주소 계산이므로 `lea`.
- Row address = `A + i × (C × K)`
- **2차원 배열 이름의 type** `B 38:07`: `int a[3][4]`의 `a`를 decay시키면, 첫 번째 원소 = **첫 번째 덩어리**이므로 `int (*)[4]` (pointer to array[4] of int). 그래서 2차원 배열을 함수에 넘길 때 array pointer가 등장한다 — **array pointer를 공부하는 이유**.

## 슬라이드 21–22: Nested Array Element Access  `B 39:12`

```
A[i][j]의 주소 = A + i×(C×K) + j×K  ==  A + (i×C + j)×K
```

- 앞의 식: 덩어리 주소(`A + i×C×K`)를 먼저 구하고, 그 안에서 j번째(`j×K`)를 더함.
- 뒤의 식이 직관적으로 더 쉽다: `i×C + j`는 1차원으로 폈을 때 **몇 번째 원소**인지이고, 거기에 원소 크기 K를 곱한다. 곱셈 횟수도 줄어든다.

```c
int get_sea_digit(int index, int digit) { return sea[index][digit]; }
```
```
leaq (%rdi,%rdi,4), %rax    # 5*index          (C*index)
addl %rax, %rsi             # 5*index + digit
movl sea(,%rsi,4), %eax     # sea + 4*(5*index + digit)
```

- 5는 compiler가 type을 해석해서 **C = 5**임을 알고 만든 것이다.
- **메모리 접근은 1번** (`lea`는 메모리 접근이 아니므로 `movl`만). `B 44:28`

## 슬라이드 23–24: Multi-Level Array  `B 45:30`

```c
int cmu[5] = {1, 5, 2, 1, 3};
int uw[5]  = {9, 8, 1, 9, 5};
int ucb[5] = {9, 4, 7, 2, 0};
int *univ[3] = {uw, cmu, ucb};   // array[3] of pointer to int → 24바이트
```

- 1차원 배열들을 엮어서 2차원 배열처럼 쓰는 방법. 배열 이름은 주소(pointer to 첫 원소)이므로 `int *` 3개에 담는 것은 전혀 이상하지 않다. 순서도 자유롭게 재구성할 수 있다.
- 그림의 160/168/176은 univ table의 실제 주소, 36/16/60은 그 안에 저장된 **내용(각 배열의 주소)**.
- **`univ[1][1]` = 5** → index 1은 cmu, cmu에서 index 1 → 5 `B 47:37`
- **Nested array와의 차이: sub-array끼리 contiguous하지 않다(불연속).**

```
salq $2, %rsi               # rsi = 4*digit             (K*digit)
addq univ(,%rdi,8), %rsi    # p = univ[index] + 4*digit (Mem[univ+8*index])
movl (%rsi), %eax           # return *p
```

- `addq`의 source operand가 메모리 → table에서 sub-array 시작 주소(예: 16)를 읽어 옴. 그다음 `movl`로 실제 값을 읽음 → **메모리 접근 2번**: `Mem[Mem[univ+8*index] + 4*digit]` `B 51:41`
- Nested array는 sub-array 주소를 공식(`20i`)으로 계산하지만, multi-level은 table에서 **읽어야** 한다.
- 대신 inner array의 길이가 서로 달라도 된다.

**Trade-off** `B 51:41`

- **시간 효율성: nested array**가 유리 (원소 하나에 메모리 접근 1번 vs 2번 — loop·traverse하면 성능 차이가 크다).
- **공간 효율성: multi-level array**가 유리. 예를 들어 1000×1000 이미지에서 nested array는 contiguous 가정 때문에 의미 없는 데이터까지 공간이 이미 정해진다. Multi-level은 필요한 만큼만(3개든 5개든) 만들 수 있어 sparse한 데이터에서 공간을 아낀다.
- "Is a multilevel array the same thing as a 2D array?" → **NO**

## 슬라이드 25: Quiz  `B 53:51` ★기출

```c
int db[4] = {1, 2, 3, 4};      // 0x...7010
int os[4] = {5, 6, 7, 8};      // 0x...7020
int sp[4] = {9, 10, 11, 12};   // 0x...7030
int *p[3] = {sp, os, db};      // 0x...7040
```

배열 4개의 시작 주소만 주면 모든 원소의 주소를 계산할 수 있느냐를 묻는 문제. (각 배열은 16바이트이고 가상 메모리상 contiguous하게 잡혀 있다.)

- `sizeof(p)` = **24** (array[3] of pointer to int)
- `*sp` = **9**, `*(sp+2)` = **11**
- `&p[1]` = `0x...7048` (p의 주소 7040 + 8), `p[1]` = **`0x...7020`** (os의 주소)
- `&p[1][1]` = **`0x...7024`**, `p[1][1]` = **6** — "`&p[1][1]`을 많이 틀렸다"고 하심. `B 58:04`

## 슬라이드 26–28: Pointers  `B 58:04`

- Pointer의 정의는 **주소**이고, 주소를 저장하는 변수는 엄밀히 **pointer 변수**다. 하지만 "pointer"는 둘 다를 아우르는 우산 용어로 혼용되므로 문맥에 따라 구분해서 해석해야 한다.
- **슬라이드 27 (`swap_add`)**: call-by-value는 값을 복사해 register로 효율적으로 처리한다. 다른 procedure의 local variable을 실제로 바꾸려면 **주소**를 넘겨야 하는데, 여기에는 비용이 든다. `&` 연산자를 쓴 local variable 2개(long 2개 = **16바이트**)는 반드시 **stack에 allocation**되어야 하고, 그 주소를 `%rdi`, `%rsi`로 passing해야 한다.
  ```
  sub  $0x10,%rsp
  movq $0xa,0x8(%rsp)    # arg1 = 10
  movq $0x14,(%rsp)      # arg2 = 20
  mov  %rsp,%rsi         # &arg2
  lea  0x8(%rsp),%rdi    # &arg1
  ```
  → 메모리 접근 overhead가 있지만, 다른 procedure의 지역 변수에 접근할 수 있게 해 주는 메커니즘이 pointer다.
- **슬라이드 28: Pointer to pointer — 왜 필요한가** `B 1:00:11`
  - `"success"`는 high level에서는 문자열이지만 실제로는 **char의 array(read-only data)**이고, compile되면 그 시작 주소(constant)가 된다. `char *ap`로 받으며 `*ap` = `'s'`, `*(ap+3)` = `'c'`.
  - 다른 함수에서 `ap`와 `bp`가 가리키는 대상을 서로 바꾸고 싶다면 **pointer 변수 자체를 바꿔야** 하므로 그 변수의 주소, 즉 `char **`를 넘긴다. 결과: `ap -> failure, bp -> success`
  - 같은 논리로 삼중 pointer는 이중 pointer를 다른 곳에서 바꿀 때 필요하지만 거의 쓰이지 않는다. 실무에서는 이중 pointer까지가 흔하다.

## 슬라이드 29–30: Arrays and Pointers  `B 1:02:19`

- K&R 교재에서 중요한 부분: **왜 array와 pointer가 같은 것으로 설계되었나?**
  - Array를 다른 procedure의 인자로 넘기고 싶은데, 원소가 1000개면 다 넘길 수 없다. Homogeneous·contiguous하니까 **시작 주소(= 배열 이름)만 넘기자**는 설계다.
  - 배열 이름은 정확히는 **첫 번째 원소의 주소**이므로, 인자 type은 "pointer to 첫 번째 원소의 type"이다.
- 1차원: `int ary[5]` → 첫 원소 type `int` → `void ary_prn(int *ap)`
- 2차원: `int ary[3][4]` → 첫 원소는 첫 번째 덩어리 `int [4]` → `void ary_prn(int (*ap)[4])`
- 3차원 (`int a[2][3][4]`, 요즘 image 처리의 tensor 등): 덩어리 2개, 각 덩어리가 `[3][4]` 2차원 배열 → `int (*p)[3][4]`. **숫자(3, 4)도 맞아야** 한다. `B 1:05:34`

## 슬라이드 31–32: Memory Aliasing  `C 01:08`

Bryant 교재 4장(optimization)에 나오는 내용으로, pointer와 연관해서 추가됨.

```c
void twiddle1(long *xp, long *yp) { *xp += *yp; *xp += *yp; }
void twiddle2(long *xp, long *yp) { *xp += 2 * *yp; }
```

- `*xp = 10`, `*yp = 20`이면 둘 다 50. twiddle2가 메모리 접근이 적으니 이렇게 **최적화해도 되지 않나?** 라는 질문에서 출발.
- **Memory aliasing**: 변수(pointer)는 다르지만 실제로는 **같은 주소**를 가리키는 경우.
  - `twiddle1(&x, &x)` (x = 10): 10+10 = 20 → 20+20 = **40** (4배)
  - twiddle2라면 10 + 2×10 = **30** → 결과가 다르다.
- 한 줄 요약: **aliasing일 때는 다르다. 두 pointer가 절대 같을 수 없다는 게 보장되면 최적화할 수 있다.** `C 05:12`
  - Compiler는 compile time에 주소를 추적하는 정적 분석(**alias checking**)을 해서 "같을 수 없다" 또는 "알 수 없다"를 판단하고, 그에 따라 최적화 여부를 정한다. 알 수 없으면 twiddle1을 최적화하지 않는다. (이런 연구는 software 공학·검증, compiler 분야에서 한다.)
- 슬라이드 32 (`alias(&x, &x)`): `*q = 3000; *p = 1000; return *q;`
  - **aliasing이면 1000**, p와 q가 다른 주소면 **3000** `C 06:13`

## 슬라이드 33–35: Heterogeneous Data Structures  `C 07:19`

- Array는 homogeneous한 집합 object, **structure는 heterogeneous**한 집합 object다. 원소 크기가 다를 수 있으므로 원소마다 이름(**member** 또는 **field**)을 붙인다. (Array는 번호로만 부름)
- High level에서는 `.`(점) 연산자와 `->`(간접 참조) 연산자로 편하게 접근하지만, machine level에서는 역시 **address**로 계산된다. Array는 "초등학생 수준"으로 깔끔하지만 structure는 **alignment** 이슈가 있어 ABI를 알아야 한다.
- 복습 (슬라이드 34)
  - `typedef struct { int a, b, c, d; } FourInts;` → `FourInts f1;`은 **16바이트** 할당 (local이면 stack, 아니면 data 영역). `f1.a = 0;`
  - `FourInts *f2;` → 8바이트 pointer. Local pointer 변수에는 쓰레기 값이 있어서 할당 없이 바로 접근하면 **crash**. `malloc(sizeof(FourInts))`로 heap에 할당하면 OS가 16바이트를 풀어 주며 시작 주소를 리턴 → `f2->b = 17;` (heap은 후반부에 배움)
- 슬라이드 35: `struct rec { int a[4]; long i; struct rec *next; };` → `struct rec r;`은 16 + 8 + 8 = **32바이트**, `struct rec *p;`는 8바이트. `struct rec {...} r, *p;`처럼 변수와 pointer 변수를 동시에 정의할 수도 있다. 닫는 괄호 뒤 **semicolon**을 잊기 쉽다.

## 슬라이드 36: Structure Representation  `C 12:33`

`struct rec { int a[4]; size_t i; struct rec *next; };` (`size_t` = unsigned long)

- 각 member가 시작하는 위치를 **offset**(또는 position)이라 한다: `a` = **0**, `i` = **16**, `next` = **24**, 전체 크기 = **32**
- **실제 전체 크기는 단순 합보다 같거나 크다(작아지지 않는다).** Alignment 때문에 중간(internal)이나 끝(external)에 **padding**이 붙을 수 있다.
- **선언 순서는 반드시 유지된다.** 첫 member가 가장 낮은 주소. Compiler가 순서를 바꾸지 않는다.
  - 그래서 network로 주고받거나 file system에 저장할 때도 순서가 그대로다 → 회사에서 struct의 member 순서를 마음대로 바꾸면 안 된다. `C 14:39`
- Machine-level program은 source의 structure를 모른다. Compiler가 크기와 offset을 정해서 instruction에 반영할 뿐이다.

## 슬라이드 37: Generating Pointer to Structure  `C 15:42`

```c
int *get_ap(struct rec *r, size_t idx) { return &r->a[idx]; }
```
```
leaq (%rdi,%rsi,4), %rax    # r + 4*idx
```

- Member의 offset만 알면 `시작 주소 + offset`으로 각 member 주소를 계산할 수 있다. `a`의 offset은 0이므로 `r + 4·idx`. 주소 계산이라 `lea`.
- idx가 4가 되면 `a`를 넘어 `i`를 읽게 된다(큰일).

## 슬라이드 38: Following Linked List  `C 18:52`

```c
void set_val(struct rec *r, int val) {
    while (r) { int i = r->i; r->a[i] = val; r = r->next; }
}
```
```
.L11:
  movslq 16(%rdi), %rax       # i = M[r+16]      (memory read)
  movl   %esi, (%rdi,%rax,4)  # M[r+4*i] = val   (memory write)
  movq   24(%rdi), %rdi       # r = M[r+24]      (next 읽기)
  testq  %rdi, %rdi
  jne    .L11
```

- Linked list를 NULL이 나올 때까지 돌며 각 node의 `a[i]`를 val로 바꾼다. 의미보다 **각 member 접근이 offset(16, 4i, 24)으로 바뀌는 과정**이 중요하다.

## 슬라이드 39–40: Memory Alignment in x86-64  `C 21:01`

**Aligned**: K바이트 primitive object는 주소가 **K의 배수**여야 한다.

| K  | Type                 | 주소 조건                   |
|----|----------------------|-----------------------------|
| 1  | `char`               | 제한 없음                   |
| 2  | `short`              | 하위 1비트 0                |
| 4  | `int`, `float`       | 하위 2비트 0                |
| 8  | `long`, `double`, `*`| 하위 3비트 0                |
| 16 | `long double`        | 하위 4비트 0                |

→ 하위 `log2(K)` 비트가 0. Debugging할 때 `&`로 주소를 찍어 보면 눈으로 확인할 수 있다.

- RAM은 byte addressable이라 어느 주소에 저장해도 물리적으로는 동작한다. 하지만 Intel은 **성능**을 위해 제약을 권고한다(x86-64는 advised, 일부 machine은 required).
- **이유** `C 22:08`
  - x86은 **paging** 기반: 메모리를 고정 4KB page로 쪼개 관리한다. 아무 데나 저장할 수 있으면 2바이트 short가 page 경계에 걸칠 수 있고, 그러면 **메모리 접근이 2번** 필요하다.
  - Cache line(Intel은 **64바이트**)도 마찬가지로 걸치면 효율이 떨어진다.
  - K가 1, 2, 4, 8, 16처럼 `2^k`라서 딱 떨어지게 설계됐다.
- **Array는 문제가 안 된다**: 첫 원소만 K의 배수에 맞추면 homogeneous·contiguous하니까 나머지가 자동으로 맞는다. **Structure는 다르다**: member 크기가 제각각이고, struct가 다시 array로 쓰일 수도 있어 다음 struct까지 고려해야 한다. `C 24:21`

## 슬라이드 41: Structures & Alignment — 두 가지 규칙  `C 26:31`

맞추는 방법은 많지만 compiler와 architecture가 모두 알아야 하는 binary-level **convention(ABI)**으로 두 규칙을 정했다.

1. **각 field는 struct 내에서 align되어야 한다** → 안 맞으면 **internal padding**. (`offsetof`로 확인)
2. **전체 struct 크기는 largest field의 K의 배수여야 한다** → **external padding**. (`sizeof`로 확인)

예: `struct { int a; long b; char c; }` `C 27:36`

- `a` offset 0 (4바이트) → `b`는 8의 배수여야 하므로 4바이트 padding → `b` offset 8 → `c` offset 16 (char는 아무 데나)
- 여기까지 17바이트. Largest K = 8(long)이므로 8의 배수인 24로 → external padding 7바이트 → **총 24바이트**
- **`alignof`** (`<stdalign.h>`): largest field의 K를 리턴 (여기서는 8). `sizeof`, `alignof`는 runtime procedure가 아니라 compile time에 계산되므로 함수가 아니라 **연산자**다. `C 29:43`
- 슬라이드의 `struct rec`(`int a[4]; int i; struct rec *next;`) → `alignof` = **8**
- **Second rule의 목적**: struct가 array로 반복될 때도 모든 원소가 align되게 하려는 것. 전체 크기가 largest K(가장 큰 값, 다른 K들은 그 약수)의 배수이고 struct 시작이 그 배수에 놓이면, 반복해도 다 맞는다. `C 31:51`
- 이 규칙은 Intel x86만이 아니라 Linux 기반 **System V** 계열 전반이 따르는 ABI라서 중요하다. `C 33:56`

## 슬라이드 42–43: Satisfying Alignment — `struct S1`  `C 33:56`

```c
struct S1 { char c; int i[2]; double v; } *p;
```

- 1학년 직관: 1 + 8 + 8 = 17바이트. 하지만 `sizeof`는 그렇게 나오지 않는다.
- `c` offset **0** → 3바이트 padding → `i` offset **4** (`i[0]`, `i[1]`) → 12에서 끝남 → `v`는 8의 배수여야 하므로 4바이트 padding → `v` offset **16** → 24에서 끝
- Second rule: largest K = 8, 24는 8의 배수 → external padding 없음 → **`sizeof` = 24**
- Struct 자체도 8의 배수 주소에 놓인다.

## 슬라이드 44: Satisfying Alignment — `struct S2`  `C 36:58`

```c
struct S2 { double v; int i[2]; char c; } *p;
```

- `v` offset 0 → `i` offset 8 (16에서 끝) → `c` offset **16** (`offsetof(struct S2, c)` = 16, `<stddef.h>` 필요) → 17
- `alignof` = **8**. 주의: `int i[2]`는 K가 8이 아니라 **원소 기준 4**다. 배열이 `i[3]`(12바이트)이어도 K는 4. Largest K는 member의 **원소 단위**로 본다. `C 38:03`
- 17 → 8의 배수 24로 **external padding 7바이트** → **`sizeof` = 24**

## 슬라이드 45: Arrays of Structures  `C 38:03`

- `struct S2 a[10];` → 각 struct가 24바이트이므로 `a[i]`의 시작은 `a + 24i`
- 원소 i의 member 주소 = **`24·i + offset`**. 예: `a[3].c` → `24×3 + 16`
- 이 **규칙성**을 만들고 싶어서 second rule이 있는 것이다.

## 슬라이드 46: Accessing Array Elements — `struct S3`  `C 40:11`

```c
struct S3 { short i; float v; short j; } a[10];
short get_j(int idx) { return a[idx].j; }
```

- `i`(2) + padding 2 + `v`(4) + `j`(2) + external padding 2 = **12바이트** (4의 배수), `sizeof(a)` = **120**
- `j`의 offset = **8** → `a[idx].j`의 주소 = `a + 12·idx + 8`
```
leaq   (%rdi,%rdi,2), %rax     # 3*idx
movzwl a+8(,%rax,4), %eax      # a + 8 + 12*idx
```
- `a+8`의 8이 displacement. `a`는 전역 변수 덩어리의 시작 주소이며, 실제 값은 linking 때 결정된다.

## 슬라이드 47–48: How the Programmer Save  `C 43:17`

```c
struct S4 { char c; int i; char d; } *p;   // c,3pad,i,d,3pad → 12바이트
struct S5 { int i; char c; char d; } *p;   // i,c,d,2pad      →  8바이트
```

- Member 수와 종류는 같고 **순서만 바꿨는데 크기가 다르다.**
- **실무 경고** `C 43:17`: 신입 사원들이 "high level에서는 잘 돌아가니까" 순서를 바꾸는 경우가 꼭 있다. Struct의 물리적 표현은 선언 순서대로 저장되므로, 그 struct가 **통신이나 file I/O**에 쓰이는 것이라면 offset과 크기가 달라져 엉뚱한 값이 나온다. 고객은 평생 업데이트를 안 하기도 한다. 경찰서에 납품하는 보안 시스템 같은 경우 돈과 직결되어 리콜이 온다. **남이 만든 struct는 건드리지 말고, 추가하려면 물어보라.**
- **메모리가 극도로 제한된 환경**(embedded는 RAM이 4KB인 경우도 있음)에서 아끼고 싶다면: **큰 type부터 내림차순**(또는 일관된 오름차순)으로 선언하면 padding이 줄어든다. `C 46:33`
- **슬라이드 48 퀴즈**
  - `struct old { char a; int b; short c; };` → a 0, pad 3, b 4, c 8 → 10 → **12**
  - `struct new { char a; short c; int b; };` → a 0, pad 1, c 2, b 4 → **8**
- **왜 padding으로 공간을 낭비하나?** Alignment를 하지 않아도 동작은 하지만, 걸치면 메모리를 2번 읽는 **성능 하락**이 있다. 즉 **시간 효율을 위해 공간 효율을 희생한** 사례다. 반대로 공간이 극한이면 alignment를 포기하는 선택을 할 수도 있다 — 선택의 문제. `C 47:34`

## 슬라이드 49: Structure Example  `C 48:39` ★기출

```c
struct P1 { short i; int c; int *j; short *d; };
struct P2 { char a; int b; short c; };
```

layout만 그리면 다 맞출 수 있는 문제. 말로 풀면:

- P1: `i` offset 0 → padding 2바이트 → `c` offset **4** → `j`는 8의 배수라 padding 없이 offset **8** → `d` offset **16** → 끝 24, 8의 배수 → **`sizeof(P1)` = 24**
- P2: `a` 0, `b` 4, `c` 8 → 10 → 4의 배수로 → **`sizeof(P2)` = 12**
- `offsetof`, `sizeof`, `alignof`가 모두 시험에 나올 수 있다.

## 슬라이드 50: Summary  `C 49:40`

- 복잡한 data type도 machine level에서 처리하려면 결국 메모리에 저장되고, linear한 메모리 위에서 **address로 변환**된다.
- **Array**: row-major ordering만 기억하면 됨. Homogeneous·contiguous라서 array와 pointer를 address로 바꾸는 것은 "식은 죽 먹기". 2차원에서 nested array와 multi-level array의 구조 차이만 주의.
- **Structure**: heterogeneous라서 alignment 이슈 → internal / external padding을 고려해 offset을 계산해야 한다.
- 더 공부하고 싶다면: **class**(struct의 확장)는 어떻게 처리될지, **union**(struct의 special case)은 어떨지 file로 저장하고 메모리를 분석해 보라. 결국 다양한 data type이 low level에서 같은 방식으로, 주소가 instruction에 반영되는 과정임을 정리하면 된다.

---

## 강조 사항

- **Type 해석 우선순위 `[]`, `()` > `*`** — 식별자부터 inside → outside. 영어로 읽고("pointer to / array of / function returning") 형상과 size를 바로 떠올릴 것.
- **기말 출제 예고·기출**
  - 슬라이드 11: `sizeof(f1..f5)` 출력 (`f5` = 24)
  - 슬라이드 12: `sizeof(x)` = 24 (D), `sizeof(y)` = 1024 — "x의 값/y의 크기/출력값은?" 형태
  - 슬라이드 25: 배열 주소 빈칸 채우기 (`&p[1][1]` = `...7024`를 많이 틀림)
  - 슬라이드 49: `offsetof` / `sizeof` / `alignof` — layout 그림만 그리면 다 맞출 수 있음
- `sizeof(function 이름)`은 UB지만 **GNU 기준 1**.
- Nested array는 메모리 접근 1번(시간 효율), multi-level array는 2번(공간 효율) — trade-off.
- Struct의 member **순서는 유지**되며, 통신·file에 쓰이는 struct의 순서를 함부로 바꾸면 안 된다.
- Alignment = 시간 효율을 위해 공간을 희생한 설계.

## 다음 시간 예고  `C 00:00`

3장을 마무리하고 **7장 Linking**으로 넘어간다. (B 마지막에 "aliasing부터는 다음 시간에"라고 하셨고, C에서 aliasing → structure를 마친 뒤 linking 시작)
