# Separate Compile and Linking (Bryant 7장)

## 1. 분할하고 링킹하는 이유

C 프로그램은 **파일 단위 = module 단위**로 작업한다. 한 파일에는 특정 task를 하는, 서로 연관된 함수와 data(전역 변수)를 모은다. 프로그램 전체를 파일 하나에 넣는 것을 monolithic이라고 한다.

1. **재사용성**: 어떤 역할을 하는 파일을 만들어 두면 나중에 불러오기만 하면 된다.
2. **협업**: 전체에서 각자 맡은 파트를 나눠 만들어 합친다. 한 파일을 여러 명이 고치면 conflict가 나고 관리가 어렵다.
3. **개발 시간 단축**: 어떤 부분을 고쳤을 때 그 파일만 다시 compile하고 나머지는 link만 하면 된다(`make`). Monolithic은 한 줄만 고쳐도 전부 다시 compile해야 한다. 강의 예시로 100명 × 100 page를 매번 rebuild all하면 disk I/O만으로 약 30분이 걸린다.

> 시험 포인트: 분할 컴파일은 **프로그램 개발 생산성**을 위한 것이고, **프로그램 성능과는 무관**하다.

## 2. extern이 필요한 이유

어떤 변수를 여러 파일이 같이 쓴다면 어떻게 나눠야 할까?

| 방법                  | 결과                                        |
|-----------------------|---------------------------------------------|
| (1) 그냥 나눔         | `b.c`, `c.c`에 x 없음 → **compile error**   |
| (2) 각 파일에 `int x` | 각각 compile은 됨 → **multiple definition** |
| (3) `extern int x`    | 선언만 함 → linking 때 x를 resolve          |

- `extern`은 compiler에게 "x가 있다고 치고 넘어가라, linking 때 누군가 가지고 있을 것이다"라고 알려주는 **선언(declaration)**이다.
- 그래서 분할 compile의 결과물(`.o`, relocatable object)은 **불완전한 binary**다. 실행할 수 없고, linker가 external 변수를 resolve해야 실행 파일이 된다.

## 3. 헤더 파일이 존재하는 이유

- **문제**: 어떤 변수를 여러 파일이 `extern`으로 참조하는데 정의한 사람이 type을 바꾸면, 쓰는 파일 모두를 수동으로 고쳐야 한다. 하나라도 놓치면 type이 다른 같은 변수가 되어 치명적인 bug가 된다.
- **해결**: 정의한 사람이 header file(`a.h`)에 `extern` 선언을 두고, 쓰는 사람은 `#include`한다. Preprocessor(CPP)가 compile 전에 내용을 치환하므로 header 한 곳만 고치면 전부 반영된다.
- Header file 안은 거의 다 `extern` 선언이다(함수 선언은 `extern`이 생략되어 있다).

> 시험 포인트: header file은 **분할 컴파일 환경에서 각 module이 정의한 함수·전역 변수의 선언을 모아, 일관된 interface를 공유**하기 위한 것이다.

## 4. 라이브러리가 필요한 이유

재사용이 가장 큰 목적이다.

- 하나의 파일에 모든 함수를 넣으면 매번 큰 파일을 뒤져야 해서 비효율적이다.
- 함수마다 파일을 만들면 사용자가 100개를 쓰면 100개를 모두 적어야 해서 귀찮고 실수하기 쉽다.
- → 관련된 함수들을 **논리적으로 grouping**한다. 예: `sin`, `cos`, `tan` → math library(`-lm`), `printf` → standard I/O library

## 5. Define vs Declare

- **Define**: 변수나 함수 자체를 만드는 것이다. 변수는 실제로 메모리를 할당하고(`int`면 4 byte), 함수는 **body가 있어야** define이다.
  - 예: `int x;`, `int sum(int *a, int n) { ... }`
- **Declare**: 만들지 않고, 다른 module에 definition이 있다고 가정하고 넘어가게 하는 **compiler용 정보**다. 메모리를 할당하지 않는다.
  - 예: `extern int x;`, `int sum(int *a, int n);`
- 함수 선언은 앞에 `extern`이 생략되어 있다. 명시해도 된다.

## 6. 변수의 속성

|           | Scope       | Storage duration    | Linkage             |
|-----------|-------------|---------------------|---------------------|
| 지역 변수 | block scope | dynamic (temporary) | no linkage          |
| 전역 변수 | file scope  | static (permanent)  | external / internal |

1. **Scope**: 지역 변수는 block 안에서만, 전역 변수는 파일 전체에서 사용할 수 있다.
2. **Duration**: 지역 변수는 block이 실행되는 동안만 register나 stack에 존재한다. 전역 변수는 프로그램의 시작부터 끝까지 존재한다.
3. **Linkage**: 지역 변수는 다른 module이 존재 자체를 모른다. 전역 변수는 기본적으로 다른 module에서 참조할 수 있고(external), `static`을 붙이면 internal이 된다.

- 블록 안에 같은 이름의 전역 변수와 지역 변수가 있으면 **지역 변수가 우선**이고 전역 변수는 가려진다.
- `static`과 `extern`은 이 속성을 바꾸는 modifier다.

### static의 두 가지 의미

- **전역 변수/함수 앞**: **internal linkage**가 되어 다른 파일에서 이름으로 참조(linking)할 수 없다. 다른 파일에 같은 이름의 `static` 변수가 있어도 완전히 다른 변수다.
- **지역 변수 앞**: duration이 **permanent**가 된다. Register나 stack이 아니라 전역 변수처럼 data section에 저장되어 프로그램과 생명주기를 함께한다.
  - **초기화는 startup 때 한 번만** 된다. 함수를 다시 불러도 값이 이어진다(quiz에서 50 → 51 → 52).
  - **Scope는 그대로 block 안**이다. 수명만 길어질 뿐 block 밖에서 이름으로 접근할 수는 없다.
  - 다른 함수에 같은 이름의 static 지역 변수가 있어도 된다. Symbol table에는 `x.1`, `x.2`처럼 **unique한 이름의 local symbol**로 들어간다.

### Multiple definition이 났을 때 (팀장의 역할)

`main.c`에 `int x = 1;`, `sub.c`에 `int x = 2;`가 있으면 multiple definition linking error가 난다.

- 다른 의미인데 이름만 같다 → 각자 **`static`**으로
- 정말 같은 변수를 공유한다 → 한 곳에만 정의하고 나머지는 **`extern`**, 선언은 header file로

## 7. 링킹

여러 object 파일의 code와 data를 묶어 **executable한 파일 하나**로 만드는 과정이다.

### Static vs Dynamic

1. **Static linking**: compile time에 `.o` 파일들을 묶어 완전히 link된 실행 파일을 만든다.
   - 장점: **이미 주소를 다 찾아 놓았으므로** 더 빠르고 안정적이다.
   - 단점: `printf` 같은 자주 쓰는 library가 모든 실행 파일에 복사되어 **disk와 memory 모두에 redundancy**가 생긴다.
2. **Dynamic linking**: "이 함수를 나중에 묶어 달라"는 정보만 남기고 linking을 미룬다. 실행할 때 **dynamic linker**가 memory에 있는 shared object(`.so`)와 연결한다.
   - **Load-time**: loader가 disk에서 memory로 올릴 때 link
   - **Run-time**: 실제로 호출될 때 link
   - 장점: redundancy가 없다. 단점: runtime 비용이 조금 들고, 큰 프로젝트에서는 버전 문제로 꼬이기도 한다.

- 같은 hello 프로그램이 static이면 **852K**, dynamic이면 **17K**다.
- 현대 프로그램은 일부는 static, 일부는 dynamic으로 **섞어 쓰기 때문에**(license, 성능 등) 둘 다 알아야 한다.

### Object file의 세 종류

| 종류                        | 용도                    | 비고                           |
|-----------------------------|-------------------------|--------------------------------|
| Relocatable object (`.o`)   | static linking 입력     | `.c` 하나당 `.o` 하나          |
| Shared object (`.so`)       | dynamic linking 입력    | Windows `.dll`, macOS `.dylib` |
| Executable object (`a.out`) | linking 출력, 실행 파일 | memory에 바로 복사해 실행      |

`.o`, `.so`가 **input**이고 `a.out`이 **output**이다.

### Static linking 과정 (linker는 symbol 단위로 일한다)

1. **Symbol resolution**: symbol table을 보며 각 symbol reference가 **정확히 하나의 definition**과 연결되는지 보장한다.
2. **Relocation**: code는 code끼리, data는 data끼리 모아 실제 주소를 정하고, 그 주소로 reference들을 고친다. Object 안의 주소는 **section 안의 offset이거나 0으로 비워 둔 자리**(가짜 주소)였다.

**지역 변수는 linking 대상이 아니다.** 이미 register나 stack 주소로 code에 반영되어 있다. 대상은 함수, 전역 변수, static 변수다.

## 8. Symbol

Symbol은 전역 변수, static 변수, 함수의 정보를 담는다. Symbol table(`.symtab`)은 symbol entry의 배열이고, 지역 변수 entry는 없다.

```c
typedef struct {
    int   name;        /* 이름 (string table offset) */
    char  type:4,      /* Function or Object */
          binding:4;   /* Local, Global (External은 *UND*로 표시) */
    char  reserved;    /* 사용 안 함 */
    short section;     /* section header index */
    long  value;       /* section 안의 offset */
    long  size;        /* 크기 */
} Elf64_Symbol;
```

1. **name**: symbol의 이름
2. **type**: Object와 Function 두 가지뿐이다. 함수는 Function, **전역 변수와 static 변수**는 Object다.
3. **binding**: Local, Global, External
   - **Local**: **static 함수와 static 변수**(static 지역 변수 포함). 파일 안에서만 쓸 수 있다. Local symbol ≠ 지역 변수다.
   - **Global**: 이 module이 정의하고 다른 파일이 참조할 수 있는 것. `static`도 `extern`도 없는 함수와 전역 변수다.
   - **External**: 이 module이 참조만 하고 정의는 다른 module에 있는 것. `extern` 선언한 변수와 **body 없이 선언만 한 함수**다. Section은 `*UND*`로 표시된다.
   - 외우는 법: `static`이면 local, `extern`이면 external, 둘 다 없으면 global. 함수 선언 앞에 `extern`이 생략되는 것만 조심한다.
4. **reserved**: 1 byte padding이다. 뒤에 오는 `section`(short)과 `value`(long)가 2 byte, 8 byte 경계에 맞게(alignment) 자리를 채운다. `type:4, binding:4` 같은 bit field도 공간을 아끼기 위한 것이다.
5. **section**: 9절에서 따로 정리한다.
6. **value**: 주소를 의미한다. 엄밀히는 **section 시작 기준 offset**이고, relocation이 끝나면 실제 주소가 된다.
7. **size**: 크기(byte)

### Definition과 Reference

- Definition은 create하는 것, reference는 use하는 것이다. 함수는 body가 있으면 definition이다.
  - `int *xp = &x;` → `xp`를 define하면서 `x`를 reference
- 정의뿐 아니라 **참조한 것도 symbol에 기록된다**(external, `*UND*`). Linker가 무엇을 찾아야 하는지 알아야 하기 때문이다. 기록되지 않는 것은 (static이 아닌) 지역 변수뿐이다.

```
$ objdump -t main.o
0000000000000000 g     O .data  0000000000000008 array
0000000000000000 g     F .text  000000000000001f main
0000000000000000         *UND*  0000000000000000 sum
```

- `main.c`의 symbol은 `array`, `main`, `sum` **3개**다. `val`은 지역 변수라 없다.
- `*UND*`는 **pseudo section**이다. Relocatable object에만 있고, linker가 definition을 찾으면 사라지므로 실행 파일에는 없다.

## 9. Symbol Section

Section은 object file 안에서 **같은 속성을 가진 연속 영역**이다. 기준은 memory에 올릴 때의 **접근 권한(read / write / execute)**이다.

- `.text`: 기계어 code. 함수(body)라고 생각하면 된다. Executable + read-only
- `.rodata`: 읽기만 가능한 data. `const` 전역 변수, jump table 등
- `.data`: **0이 아닌 값으로 초기화된** 전역·static 변수
- `.bss`: **초기화하지 않았거나 0으로 초기화된** 전역·static 변수

**data와 bss를 나눈 이유**: 초기화된 값은 object 파일에 값을 저장해야 한다. 하지만 초기화 안 된 것은 "4 byte짜리 만 개" 같은 **크기 정보만** 남기고, **loading 때 allocate하면서 0으로 초기화**하면 된다. 그래서 `.bss`는 object 파일에서 공간을 차지하지 않고 **disk 공간을 절약**한다("Better Save Space"). 의미 없는 초기값이라면 1이 아니라 0으로 초기화하는 게 좋다.

> 한 줄 요약: 초기화 안 함 → `.bss`, 0 → `.bss`, 0이 아닌 값 → `.data`, `const` → `.rodata`. 단, 초기화 안 된 **전역** 변수는 object 단계에서 `*COM*`이다(10절).

## 10. ELF

a.out → COFF → **ELF**(Executable and Linkable Format) 순으로 진화했다. Relocatable, executable, shared object를 **하나의 통일된 format**으로 표현한다.

```
ELF header            word size, byte order, file type, machine type …
.text
.rodata
.data
.bss                  section header는 있지만 공간 차지 안 함
.symtab               symbol table
.rel.text             .text 안 reference의 relocation entry
.rel.data             .data 안 reference(pointer 초기값)의 relocation entry
.debug                gcc -g 디버깅 정보
Section header table  각 section의 offset과 size
```

- `.symtab`부터 아래는 **memory에 load되지 않는다.** Linker나 debugger용 정보이고, 실행에는 필요 없다.
- 어떤 symbol의 실제 위치는 symbol의 offset + section header table에서 찾은 section 시작 위치로 구한다.

### readelf -h main.o

- **Magic**: `7f 45 4c 46` → `7f` 다음 수들을 ASCII로 바꾸면 "ELF"다. 앞 4 byte는 모든 ELF 파일에서 같다. 이어지는 `02`는 64-bit, `01`은 little endian이고, 이 값은 machine에 따라 달라진다.
- Type `REL`(relocatable), Machine `X86-64`
- ★ `Start of section headers: 672`, `Size of section headers: 64`, `Number of section headers: 12`
  - Section header table은 파일 시작에서 672 byte 위치부터 64 byte짜리 12개가 있다.
  - 따라서 **파일 크기 = 672 + 64 × 12 = 1440 byte**. 이 구조를 그릴 수 있어야 한다.

## 11. Symbol Resolution

n개의 object를 입력받아 symbol table을 보며 세 종류로 처리한다.

- **Local**: 따로 처리하지 않는다. Compile에 성공했다면 module 안에서 잘 정의되고 쓰인 것이고, compiler가 module 안에서 unique한 이름을 보장한다.
- **External**: 나머지 n−1개(본인 제외)를 찾아 definition이 정확히 하나 있는지 확인한다. 없으면 **`undefined reference`** linking error다.
- **Global**: 나머지 n−1개에 같은 이름이 또 나오면 안 된다. 원칙은 multiple definition error인데, **역사적으로 허용**하게 되었다. 허용한다는 것은 둘 다 쓴다는 게 아니라 **linker가 하나를 고르고 나머지를 `extern` 처리**한다는 뜻이다. 그 기준이 strong/weak 규칙이다. (`gcc -fno-common`이면 그냥 error를 낸다.)

### Strong / Weak

- **Strong**: 함수(body가 있는 definition), 초기화된 전역 변수(**0으로 초기화해도 strong**)
- **Weak**: **초기화되지 않은** 전역 변수
- Body 없는 함수 선언이나 `extern` 변수는 definition이 아니므로 strong도 weak도 아니다(external).

| 규칙   | 상황                      | Linker 동작                             |
|--------|---------------------------|-----------------------------------------|
| Rule 1 | strong 2개 이상           | **linking error** (multiple definition) |
| Rule 2 | strong 1개 + weak 여러 개 | strong 선택, weak는 `extern` 처리       |
| Rule 3 | weak만 여러 개            | **임의로 하나** 선택                    |

→ Rule 2, 3은 error 없이 link되어 **의도하지 않은 결과**가 생길 수 있다.

### ★ Nightmare scenario (슬라이드 40)

```c
/* foo.c */                         /* bar.c */
int x = 15213;   /* strong */       double x;      /* weak */
int y = 15212;   /* strong */       void f() { x = -0.0; }
```

- Rule 2로 `foo.c`의 `int x`(4 byte)가 선택되고, `bar.c`의 `x`는 그 주소를 가리키게 된다.
- Linker는 **type을 추적하지 않는다**(size가 다르다는 warning만 낸다).
- `foo.c`의 `x`, `y`는 `.data`에 연달아 있다. `f()`는 `x`를 double로 알고 **8 byte를 쓰므로 `y`까지 덮어쓴다.**
- `-0.0` = `0x8000000000000000`이고 little endian이라 낮은 주소부터 `00 00 00 00 | 00 00 00 80`
- 결과: `x = 0x0`, `y = 0x80000000`. 원인과 증상이 다른 파일에 있어서 디버깅이 매우 어렵다.

### ★ Linker puzzles (슬라이드 41)

| Module 1               | Module 2           | 결과                                    |
|------------------------|--------------------|-----------------------------------------|
| `int x; p1(){}`        | `p1(){}`           | strong 2개(`p1`) → link time error      |
| `int x; p1(){}`        | `int x; p2(){}`    | weak 2개 → 같은 변수. 정말 원한 건가?   |
| `int x; int y; p1(){}` | `double x; p2(){}` | weak 2개 → `y` 덮어쓸 **수도** (might)  |
| `int x=7; int y=5;`    | `double x; p2(){}` | strong 선택 → `y`를 **덮어씀** (will)   |
| `int x=7; p1(){}`      | `int x; p2(){}`    | strong 선택 → 같은 초기화된 변수 참조   |

- 셋째 줄: 어느 weak가 선택되느냐에 따라 다르다. `int x`가 선택되면 nightmare scenario와 같고, `double x`가 선택되면 문제가 없을 수도 있어서 **might**다.
- 넷째 줄: strong `int x`가 확정적으로 선택되므로 **will**이다.

### COMMON (`*COM*`)

초기화되지 않은 전역 변수는 object 단계에서 `.bss`가 아니라 **`*COM*`**으로 처리된다. Weak symbol이라 다른 파일에 strong이 있으면 `extern` 처리될 수도 있어서, link 전에는 진짜 definition인지 **미확정**이기 때문이다. `*UND*`처럼 **pseudo section**이고, linker에게 선택되면 `.bss`로 확정된다.

```c
int a = 1;  int b = 0;  int c;
static int x = 1;  static int y = 0;
const int z = 3;
void bar();
void foo() { bar(); }
```

| Symbol | Binding  | Section   | 이유                               |
|--------|----------|-----------|------------------------------------|
| `a`    | global   | `.data`   | 0이 아닌 값으로 초기화             |
| `b`    | global   | `.bss`    | 0으로 초기화 (strong)              |
| `c`    | global   | `*COM*`   | 초기화 안 된 전역 = weak → 미확정  |
| `x`    | local    | `.data`   | static, 초기화 → `a` 다음 offset 4 |
| `y`    | local    | `.bss`    | static, 0 → `b` 다음 offset 4      |
| `z`    | global   | `.rodata` | `const`                            |
| `foo`  | global   | `.text`   | 함수 정의                          |
| `bar`  | external | `*UND*`   | 선언만                             |

- Symbol은 **8개**다.
- `nm foo.o`로 보면 `D a`, `B b`, `C c`, `d x`, `b y`, `R z`, `T foo`, `U bar`다. 글자는 section을 뜻하고, **대문자는 global, 소문자는 local**이다(type이 아니다).

### Practical considerations

- 전역 변수는 가능하면 **쓰지 않는다**(multi-threading에서 동기화 문제, bottleneck).
- 꼭 쓴다면
  1. **반드시 초기화한다** → strong으로 만들어 모호함을 없앤다. 의미 없는 값이면 0으로 초기화해서 `.bss`로 보낸다.
  2. 외부 전역 변수를 참조하면 **`extern`**을 쓰고, 선언은 header에, 정의는 정확히 하나의 `.c`에 둔다.
  3. 가능하면 **`static`**을 쓴다.

## 12. Relocation

Symbol resolution이 끝났으므로 모든 reference가 정확히 하나의 definition과 연결된 상태다. 이제 기계적으로 합친다.

### 1단계: section과 symbol definition의 relocation

- 같은 종류의 section을 하나로 합친다(모든 `.text` → 실행 파일의 `.text`, 모든 `.data` → `.data`).
- 우리가 만든 object뿐 아니라 **system code와 data**(startup code 등)도 함께 합쳐진다.
- 각 section과 symbol에 run-time 주소를 부여한다. 여기서 모든 symbol의 **실제 주소가 확정**된다. 예: `main = 0x4004d0`, `sum = 0x4004e8`, `array = 0x601018`

### 2단계: section 안의 symbol reference 수정

Compiler는 object를 만들 때 reference의 주소를 몰라서 그 자리에 **0을 넣어 두고**, linker에게 **relocation entry**라는 메시지를 남긴다. Linker는 이 entry를 보고 빈칸을 채운다.

```
$ objdump -d -r main.o
   9:  bf 00 00 00 00   mov    $0x0,%edi        # array 주소 자리
                  a: R_X86_64_32   array          # relocation entry 1
   e:  e8 00 00 00 00   callq  13 <main+0x13>   # sum 호출 자리
                  f: R_X86_64_PC32 sum-0x4        # relocation entry 2
```

- **Relocation entry 필드**
  - `offset`: 고칠 위치(section 시작 기준)
  - `type`: 몇 byte를 어떤 방식으로 고칠지
  - `symbol`: 어느 symbol의 주소로 고칠지
  - `addend`: 보정값
- `.text` 안의 reference는 `.rel.text`에, `.data` 안의 reference(예: `int *xp = &x;`)는 `.rel.data`에 모인다.

| Type            | 방식              | 써 넣는 값  | 주 용도        |
|-----------------|-------------------|-------------|----------------|
| `R_X86_64_32`   | 32-bit 절대 주소  | `S + A`     | 전역 변수 주소 |
| `R_X86_64_PC32` | 32-bit PC 상대    | `S + A − P` | 함수 호출      |

- `S`: symbol의 실제 주소, `A`: addend, `P`: 고칠 위치의 실제 주소(section 시작 + offset)
- offset은 "**어디에** 쓸지", symbol과 type은 "**무슨 값을** 쓸지"를 알려준다.

**비유**

- Compiler: "`.text`의 0xa 위치를 비워 뒀어. 거기에 `array`의 주소를 넣어 줘."
- Linker: "`array`의 definition은 `0x601018`에 배치했으니까, `.text` 시작 + 0xa 위치에 `0x601018`을 넣을게."

### 계산 예시 (`.text` 시작 = `0x4004d0`)

- **Entry 1** (`R_X86_64_32`, offset `0xa`, `array`, A = 0)
  - P = `0x4004d0 + 0xa = 0x4004da`
  - 값 = S + A = `0x601018` → little endian `18 10 60 00`
  - 결과: `4004d9: bf 18 10 60 00   mov $0x601018,%edi`
- **Entry 2** (`R_X86_64_PC32`, offset `0xf`, `sum`, A = −4)
  - P = `0x4004d0 + 0xf = 0x4004df`
  - 값 = S + A − P = `0x4004e8 − 4 − 0x4004df = 0x5`
  - 결과: `4004de: e8 05 00 00 00   callq 4004e8 <sum>`
  - 직관: `call` 다음 instruction(`0x4004e3`)에서 `sum`(`0x4004e8`)까지의 거리 = 5

## 13. 기출 Quiz

**Problem 1** (11절 COMMON 예시와 같은 코드): `x`는 `.data`, `y`는 `.bss`, `c`는 `*COM*`

**Problem 2**

```c
int done = 1;
int wins = 0;
int mask;
void player_status(int, int, int);
void master_status() {
    static int cnt = 0;
    int id = 0;
    player_status(id, mask, wins);
    cnt++;
}
```

| Symbol          | Type | Binding  | Section |
|-----------------|------|----------|---------|
| `done`          | O    | global   | `.data` |
| `wins`          | O    | global   | `.bss`  |
| `mask`          | O    | global   | `*COM*` |
| `player_status` | F    | external | `*UND*` |
| `master_status` | F    | global   | `.text` |
| `cnt`           | O    | local    | `.bss`  |

→ `id`는 지역 변수라 제외하고 **symbol 6개**

**Problem 3** (Symbol relocation)

```
/* Before */  12:  e8 00 00 00 00   call ...
                         13: R_X86_64_PC32  func-0x4
/* After */   0000000000001129 <main>:
              113b:  e8 ___________   call ___________
              1140:  83 c0 01         add  $0x1,%eax
              0000000000001148 <func>:
```

- S = `0x1148`, A = −4, P = `0x1129 + 0x13 = 0x113c`
- S + A − P = `0x1148 − 4 − 0x113c = 0x8`
- 검산: `call` 다음 instruction `0x1140` → `func` `0x1148` = 8
- 답: `113b: e8 08 00 00 00   call 1148 <func>`
