# 기말고사 대비 모의문제 — Set 2

> 범위: 9. Derived Types: Array, Pointer, and Structure
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (C / x86-64 AT&T 어셈블리)
> 환경 가정: x86-64 Linux (LP64: `long`·pointer 8바이트), gcc `-Og`, `-fwrapv`, `-fcf-protection=none`, little endian, w = 32 (int)
> 인자 `%rdi, %rsi, %rdx, %rcx, %r8, %r9` / 반환값 `%rax`
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** `char (*p)[10];`으로 선언한 `p`의 `sizeof`는 10이다.

**2.** `int x = 1; int *const p = &x;` 다음에 오는 `*p = 3;`은 compile error다.

**3.** gcc는 padding을 줄이기 위해 struct member의 선언 순서를 바꿔서 배치할 수 있다.

**4.** `int m[3][4];`에서 `m + 1`과 `m[0] + 1`은 같은 주소를 가리킨다.

**5.** `struct X { short s[3]; char c; };`의 `sizeof`는 8이다.

---

## Part B. 객관식

**6.** `char *(*f[4])(int);`를 바르게 읽은 것은?
① f is a pointer to array[4] of functions (int) returning pointer to char
② f is an array[4] of pointers to functions (int) returning pointer to char
③ f is a function (int) returning pointer to array[4] of pointer to char
④ f is an array[4] of functions (int) returning pointer to pointer to char

**7.** `double (*p[2])[3];`일 때 `sizeof(p)`는?
① 48  ② 8  ③ 16  ④ 24

**8.** 아래 함수를 `long x = 1; f(&x, &x);`로 호출했을 때 리턴 값은?
```c
long f(long *p, long *q) { *p = 5; *q = 7; return *p + *q; }
```
① 12  ② 14  ③ 10  ④ 7

**9.** `int a[3][4];`를 `prn(a);`로 넘기려고 한다. `prn`의 파라미터 선언으로 옳은 것은?
① `void prn(int **p)`  ② `void prn(int *p[4])`  ③ `void prn(int (*p)[4])`  ④ `void prn(int (*p)[3])`

**10.** 다음 중 `sizeof`가 **가장 작은** struct는?
① `struct { char a; double b; char c; }`
② `struct { double b; char a; char c; }`
③ `struct { char a; int i; char c; double b; }`
④ `struct { int i; char a; double b; char c; }`

**11.** Alignment와 array에 대한 설명으로 옳은 것은?
① x86-64에서 align되지 않은 주소로 접근하면 항상 bus error가 나서 프로그램이 종료된다.
② Array는 첫 원소만 K의 배수 주소에 놓으면 나머지 원소도 자동으로 align된다.
③ `alignof`는 runtime에 struct를 검사해서 값을 돌려주는 library 함수다.
④ Multi-level array는 nested array보다 원소 하나를 읽을 때 메모리 접근 횟수가 적다.

---

## Part C. 단답형

**12.** 다음 각 변수의 `sizeof`를 쓰시오.
(a) `int *a[2][3];`
(b) `int (*b)[2][3];`
(c) `int (*c[2])[3];`
(d) `void (*d[16])(int);`
(e) `char (*(*e)[4])[8];`

**13.** 아래 전역 변수들이 `a`, `b`, `c`, `t` 순서로 빈틈없이 배치되고, 각 변수는 alignment를 만족하는 가장 낮은 주소에 놓인다. `a`의 시작 주소는 `0x2000`이다.
```c
int a[3] = {1, 2, 3};
int b[2] = {4, 5};
int c[4] = {6, 7, 8, 9};
int *t[3] = {c, a, b};
```
(a) `b`, `c`, `t`의 시작 주소
(b) `sizeof(t)`, `&t[2]`, `t[2]`
(c) `&t[0][3]`, `t[0][3]`
(d) `t[1][2]`, `*(t[2] + 1)`

**14.** `short s[3][5];`의 시작 주소가 `0x600`이다.
(a) `sizeof(s)`, `sizeof(s[1])`
(b) `&s[2][3]`
(c) `s + 2`의 값(주소)과 그 type
(d) `s[1] + 7`의 값(주소). 이 주소는 `s[i][j]` 중 어느 원소의 주소인가?

**15.** 다음 struct에 대해 답하시오.
```c
struct Q { char a; short b; double c; char d; int e[3]; char *f; };
```
(a) 각 member `a, b, c, d, e, f`의 offset
(b) `sizeof(struct Q)`, `alignof(struct Q)`
(c) `struct Q arr[4];`의 시작 주소가 `x`일 때 `&arr[2].e[1]`

**16.** 다음 struct에 대해 답하시오.
```c
struct R { char a; double b; short c; int d; char e; };
```
(a) `sizeof(struct R)`과 internal / external padding의 총 바이트 수
(b) member의 종류와 개수는 그대로 두고 순서만 바꿀 때 만들 수 있는 최소 `sizeof`와 그때의 선언 순서
(c) (b)처럼 크기가 줄어드는데도, 이미 배포된 프로그램에서 남이 만든 struct의 순서를 함부로 바꾸면 안 되는 이유

---

## Part D. 빈칸 채우기 손코딩

**17.** 아래 C 함수의 어셈블리 빈칸을 채우고 물음에 답하시오.
```c
int mat[6][7];
int get(long i, long j) { return mat[i][j]; }
```
```
get:                            # i in %rdi, j in %rsi
    leaq  0(,%rdi,8), %rax      # 8*i
    subq  ____(a)____, %rax     # 7*i
    addq  ____(b)____, %rax     # 7*i + j
    movl  ____(c)____, %eax     # mat[i][j]
    ret
```
(d) 이 함수가 원소 하나를 읽을 때 메모리에 접근하는 횟수는?

**18.** 아래 C 함수의 어셈블리 빈칸을 채우고 물음에 답하시오.
```c
struct S { char c; short s; long l; int i; } arr[10];
int get_i(long idx) { return arr[idx].i; }
```
```
get_i:                          # idx in %rdi
    leaq  (%rdi,%rdi,2), %rax   # 3*idx
    movl  ____(a)____, %eax     # arr[idx].i
    ret
```
(b) `sizeof(struct S)`와 `i`의 offset
(c) `long l;`을 `int l;`로 바꾸면 (a)의 displacement와 scale은 각각 어떻게 바뀌는가? (`leaq`는 그대로 둔다)

**19.** 아래 어셈블리를 보고 C 코드의 빈칸을 채우시오.
```c
struct node { int key; short tag; struct node *next; long val; };
long sum(struct node *p) {
    long s = 0;
    while (____(a)____) {
        if (____(b)____)
            s += ____(c)____;
        p = ____(d)____;
    }
    return s;
}
```
```
sum:                            # p in %rdi
    movl  $0, %eax
    jmp   .L2
.L3:
    movq  8(%rdi), %rdi
.L2:
    testq %rdi, %rdi
    je    .L5
    cmpw  $0, 4(%rdi)
    jle   .L3
    addq  16(%rdi), %rax
    jmp   .L3
.L5:
    ret
```
(e) `sizeof(struct node)`

**20.** device switch처럼 function pointer table로 함수를 고르는 코드다. 어셈블리 빈칸을 채우고 물음에 답하시오.
```c
long (*ops[4])(long, long);
long dispatch(long k, long a, long b) { return ops[k](a, b) + 1; }
```
```
dispatch:                       # k in %rdi, a in %rsi, b in %rdx
    subq  $8, %rsp
    movq  %rdi, %rax
    movq  ____(a)____, %rdi
    movq  ____(b)____, %rsi
    call  *____(c)____
    addq  $1, %rax
    addq  $8, %rsp
    ret
```
(d) `ops`를 영어로 읽고 `sizeof(ops)`를 쓰시오.

---
---

## 정답 및 해설

**1. X** — `[]`보다 괄호 안의 `*`가 먼저다. p is a **pointer to** array[10] of char → 주소를 저장하는 변수이므로 **8바이트**. 10은 가리키는 대상의 크기다.

**2. X** — `int *const p`는 constant pointer to int다. **주소(p 자체)**를 못 바꿀 뿐, 가리키는 int 값은 바꿀 수 있다. compile error가 나는 것은 `p = &y;` 쪽이다. 반대로 `const int *p`면 `*p = 3;`이 error다.

**3. X** — 선언 순서는 반드시 유지된다(첫 member가 가장 낮은 주소). 그래서 통신이나 file에 쓰는 struct는 순서가 곧 형식이고, padding을 줄이려면 프로그래머가 직접 순서를 바꿔야 한다.

**4. X** — `m`은 decay되면 `int (*)[4]`(첫 번째 덩어리를 가리킴)라서 `m + 1`은 덩어리 하나(4 × 4 = 16바이트)를 건너뛴다. `m[0]`은 `int *`라서 `m[0] + 1`은 4바이트만 이동한다.
- `m + 1` = `m + 16` = `&m[1][0]`
- `m[0] + 1` = `m + 4` = `&m[0][1]`

**5. O** — `s` offset 0~6, `c` offset 6 → 7바이트. largest K는 배열 전체(6)가 아니라 **원소 기준 2(short)**이므로 2의 배수인 8로 맞춘다.
- 함정: 여기서는 우연히 8이 나왔지만 8의 배수로 맞춘 것이 아니다. `short s[4]; char c;`라면 9 → 2의 배수인 **10**이 된다(16이 아님).

**6. ②** — 식별자 f에서 시작: `f[4]` → array[4] of, `*` → pointer to, `(int)` → function (int) returning, `char *` → pointer to char.
① 맨 앞을 pointer로 읽었다. `[]`가 `*`보다 우선이므로 array가 먼저다.
④ function의 array는 C에서 만들 수 없다. 사이에 있는 `*`를 빠뜨린 읽기다.

**7. ③** — p is an array[2] of pointers to array[3] of double → pointer 2개 = **16**.
① 48은 `double p[2][3]`로 착각한 값, ② 8은 `double (*p)[2][3]`처럼 pointer 하나로 착각한 값이다.

**8. ②** — memory aliasing이다(실행해서 확인함). p와 q가 같은 주소이므로 `*q = 7`이 `*p`도 7로 덮어쓴다 → 7 + 7 = **14**.
① 12는 p, q가 서로 다른 주소일 때의 값이다. compiler가 alias가 없다고 확신할 수 없으면 `return 12`로 최적화하지 못하는 이유다.

**9. ③** — `int a[3][4]`의 첫 원소는 첫 번째 덩어리 `int [4]`이므로 decay된 type은 **`int (*)[4]`**(pointer to array[4] of int).
① `int **`는 pointer to pointer다. a가 담고 있는 것은 pointer가 아니라 int 덩어리라 type이 맞지 않는다.
② `int *p[4]`는 파라미터 자리에서 `int **p`와 같다.
④ 덩어리 크기는 행 수(3)가 아니라 **열 수(4)**다. 숫자까지 맞아야 한다.

**10. ②** — (실행해서 확인함)
- ① a 0, b 8, c 16 → 17 → **24**
- ② b 0, a 8, c 9 → 10 → **16**
- ③ a 0, i 4, c 8, b 16 → **24** (char 2개 사이에 int가 끼어서 padding이 생긴다)
- ④ i 0, a 4, b 8, c 16 → 17 → **24**

**11. ②** — array는 homogeneous·contiguous라서 원소 간격이 K로 일정하다. 첫 원소만 맞추면 끝이다.
① x86-64는 alignment가 required가 아니라 advised다. 동작은 하지만 page나 cache line에 걸치면 메모리를 2번 읽어서 느려진다.
③ `sizeof`, `alignof`는 compile time에 계산되는 **연산자**다.
④ 반대다. multi-level은 table에서 주소를 읽고 다시 원소를 읽으므로 **2번**, nested는 1번이다.

**12.** (실행해서 확인함)
(a) **48** — array[2] of array[3] of pointer to int → 2 × 3 × 8
(b) **8** — pointer to array[2] of array[3] of int
(c) **16** — array[2] of pointer to array[3] of int → 2 × 8
(d) **128** — array[16] of pointer to function (int) returning void → 16 × 8
(e) **8** — e is a pointer to array[4] of pointer to array[8] of char. 맨 바깥이 pointer이므로 뒤가 아무리 길어도 8이다.

**13.**
(a) `b` = **`0x200c`**, `c` = **`0x2014`**, `t` = **`0x2028`**
- a는 12바이트 → b는 `0x200c` (int라 4의 배수면 됨)
- b는 8바이트 → c는 `0x2014`, c는 16바이트라 `0x2024`에서 끝남
- t의 원소는 pointer(K = 8)라서 8의 배수여야 한다. `0x2024`는 8의 배수가 아니므로 **`0x2028`**

(b) `sizeof(t)` = **24**, `&t[2]` = 0x2028 + 2 × 8 = **`0x2038`**, `t[2]` = b의 주소 = **`0x200c`**
- `&t[2]`는 table 안의 칸 주소, `t[2]`는 그 칸에 저장된 내용이다. 둘을 헷갈리지 말 것.

(c) `&t[0][3]` = c + 3 × 4 = 0x2014 + 0xc = **`0x2020`**, `t[0][3]` = **9**

(d) `t[1][2]` = a[2] = **3**, `*(t[2] + 1)` = b[1] = **5**

**14.** (실행해서 확인함)
(a) `sizeof(s)` = 3 × 5 × 2 = **30**, `sizeof(s[1])` = 5 × 2 = **10**
(b) 0x600 + (2 × 5 + 3) × 2 = 0x600 + 26 = **`0x61a`**
(c) 0x600 + 2 × 10 = **`0x614`**, type은 **`short (*)[5]`** (pointer to array[5] of short) — 덩어리 단위로 이동한다.
(d) `s[1]`은 `short *`(시작 0x60a)이므로 + 7 × 2 → **`0x618`** = 0x600 + 24 = 원소 번호 12 → **`s[2][2]`**
- row-major로 1차원으로 펴져 있어서, 열 범위(5)를 넘는 index는 다음 행으로 넘어간다. compiler는 막아 주지 않는다.

**15.** (실행해서 확인함)
(a) `a` **0**, `b` **2**, `c` **8**, `d` **16**, `e` **20**, `f` **32**
- a(1) → b는 2의 배수 → padding 1 → b 2~4
- c는 8의 배수 → padding 4 → c 8~16
- d 16 → e는 4의 배수 → padding 3 → e 20~32 (원소 K = 4)
- f는 8의 배수 → 32는 이미 8의 배수 → f 32~40

(b) `sizeof` = **40** (40은 8의 배수라 external padding 없음), `alignof` = **8**
(c) `x + 2 × 40 + 20 + 1 × 4` = **`x + 104`**

**16.**
(a) **32**, padding **16바이트** (internal 9 + external 7)
- a 0, pad 7, b 8, c 16, pad 2, d 20, e 24 → 25 → 8의 배수로 32 (external 7)
- 검산: 데이터 합 1 + 8 + 2 + 4 + 1 = 16, 전체 32 → padding 16

(b) **16** — 큰 type부터 내림차순: `double b; int d; short c; char a; char e;` → b 0, d 8, c 12, a 14, e 15 → 16 (padding 0, 실행해서 확인함)
(c) struct의 물리적 표현은 선언 순서를 그대로 따른다. 그 struct가 **통신이나 file I/O**에 쓰이고 있다면 순서를 바꾸는 순간 offset과 크기가 달라져, 업데이트하지 않은 상대 프로그램이나 이미 저장된 file과 형식이 어긋나 엉뚱한 값을 읽게 된다.

**17.** (a) `%rdi`  (b) `%rsi`  (c) `mat(,%rax,4)`
(d) **1번** — `leaq`, `subq`, `addq`는 레지스터 계산이고, 메모리를 읽는 것은 마지막 `movl` 하나다.
- 주소 = `mat + (7i + j) × 4`. 7은 compiler가 type에서 C = 7을 읽어 낸 값이고, 곱셈 대신 `8i − i`로 만든다.

**18.** (a) `arr+16(,%rax,8)`
- `arr + 24 × idx + 16`. 24 × idx = 8 × (3 × idx)이므로 scale 8, displacement 16.

(b) `sizeof` = **24**, `i`의 offset = **16** (c 0, s 2, l 8, i 16 → 20 → 8의 배수로 24, 실행해서 확인함)
(c) displacement **8**, scale **4** → `arr+8(,%rax,4)`
- c 0, s 2, l 4, i 8 → 12 (largest K = 4라 12 그대로). 12 × idx = 4 × (3 × idx), i의 offset 8.

**19.** (a) `p` (또는 `p != NULL`)  (b) `p->tag > 0`  (c) `p->val`  (d) `p->next`
(e) **24**
- offset 대응: key 0, tag 4, next 8, val 16 (실행해서 확인함)
- `cmpw $0, 4(%rdi)` + `jle .L3`: tag ≤ 0이면 더하기를 건너뛴다 → C 조건은 반대인 `p->tag > 0`. `cmpw`의 w는 short(2바이트) 비교라는 단서다.
- `.L3`의 `movq 8(%rdi), %rdi`가 `p = p->next`이고, `.L2`의 `testq`가 while 조건이다.

**20.** (a) `%rsi`  (b) `%rdx`  (c) `ops(,%rax,8)`
- 호출되는 함수 입장에서 a, b는 1, 2번째 인자이므로 `%rdi`, `%rsi`로 옮겨야 한다. k를 먼저 `%rax`로 빼 둔 이유는 `%rdi`를 덮어쓰기 위해서다.
- `ops + 8k` 칸에 저장된 **함수 주소를 메모리에서 읽어서** 그 주소로 call한다(indirect call, `*`). `call *%rax`처럼 쓰면 k 값 자체로 점프하므로 틀린다.

(d) ops is an **array[4] of pointers to functions** (long, long) **returning long** → **32**
