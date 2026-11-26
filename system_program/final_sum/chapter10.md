# 10. Separate Compile and Linking 요약

- 과목: CSE3209 System Programming / 교재: Bryant & O'Hallaron, *Computer Systems* 3rd Ed. 7장 Linking (p.707–753)
- 녹음
  - A = `video_1795085213004.mp4` (약 16:40) — 슬라이드 1–10
  - B = `video_1795085232620.mp4` (약 1:10:10) — 슬라이드 11–40
  - C = `video_1795085251279.mp4` (2026-11-17, 약 46:25) — 슬라이드 38–51 (끝에 library로 넘어감)
- 진도: 슬라이드 1–51
- 원문 전사: `_workspace/system_program/chapter10/video_*.transcript.md`

> 분할 컴파일은 **프로그램 개발 생산성**(reuse, 협업, 개발 시간 단축)을 위해 진화했고, 그 과정에서 `extern`, `static`, header file, library가 필요해졌다. Linker는 object file들을 입력받아 **symbol 단위로** 두 단계를 수행한다. ① **Symbol resolution**: 모든 reference를 정확히 하나의 definition에 연결한다(strong/weak 규칙). ② **Relocation**: 같은 종류의 section을 합쳐 실제 주소를 정하고, relocation entry를 보고 reference를 고친다.

## 왜 Bryant 7장인가, 학습 목표  `A 00:00`

- 3장에서 7장으로 바로 넘어간다. 그 사이 내용은 3학년 컴퓨터구조 시간에 보충하라고 하셨고, 모든 분반 교수님과 협의된 내용이다.
- Linking: 여러 object를 combine해서 **single executable**을 만드는 과정(1장에서 설명)
- 학습 목표: object의 구조와 형태, linking 과정, 최종 결과물인 실행 파일의 모습을 이해한다. Linking 단계에서 생기는 bug는 compile error보다 잡기가 훨씬 어려워서 고도의 지식이 필요하다.
- 1학년 때 분할 컴파일을 배운 정도가 분반마다 달라서 복습부터 한다.

## 분할 컴파일이 필요한 이유  `A 02:02`

- C 프로그램은 **파일 단위 = module 단위**로 작업한다. 한 파일에는 특정 task를 수행하는, 서로 연관된 함수와 data(전역 변수 등)를 모은다.
- 장점
  1. **Reuse**: 한번 만들어 두면 library처럼 다시 쓸 수 있다.
  2. **협업**: 김과장, 정과장, 최과장이 한 파일에서 작업하면 conflict가 나고 관리가 어렵다.
  3. 교수님이 더 중요하게 보는 맥락은 **개발 시간 단축**이다. `make`처럼 고친 파일만 다시 compile하고 나머지는 link만 하면 된다. Monolithic compile은 하나만 고쳐도 전부 다시 compile해야 한다.
- **Rebuild All 계산 (슬라이드 4)** `A 05:10`
  - 회사 소스 파일은 수천, 수만 개이고 오픈소스로 소프트웨어 크기는 계속 커지는데, **disk는 여전히 ms 단위**로 느리다. Compiler는 여러 pass로 읽고 중간 파일을 쓰기도 한다.
  - 100명 × 100 page × 3 sector/page(3000 char ÷ 1000 char/sector) × 20 ms/sector × 3 pass ≈ **30분**
  - (참고: 실제 곱은 1,800,000 ms = 30분. 슬라이드의 "900,000 ms" 표기는 계산이 맞지 않는다.)
  - 릴리즈 날 모두 commit한 뒤 안정성 테스트를 위해 rebuild all을 하면 I/O 때문에 1시간이 넘게 걸린다. Linux kernel은 3–4시간. 그동안 팀 전체가 멈춘다. 지금은 CI 도구로 incremental update를 하지만, 이런 이유로 분할 컴파일이 진화했다.
- 한 줄 요약 `B 00:00`: 분할 컴파일은 **프로그램 개발 생산성**을 위한 것이고, **프로그램 성능과는 상관없다.**

## 어떻게 나눌까: `extern`의 등장  `A 07:11`

| 방법                  | 결과                                        |
|-----------------------|---------------------------------------------|
| (1) 그냥 나눔         | `b.c`, `c.c`에 x 없음 → **compile error**   |
| (2) 각 파일에 `int x` | 각각 compile은 됨 → **multiple definition** |
| (3) `extern int x`    | 선언만 함 → linking 때 x를 resolve          |

- (1) `a.c`에 `int x; x = 0;`, `b.c`에 `x++;`, `c.c`에 `x--;`로 나누면 b, c는 "x not defined" **compile error**다.
- (2) 각 파일에 `int x;`를 넣으면 object는 각각 만들어지지만, 묶을 때 같은 이름의 전역 변수가 세 개라서 "multiple definition" **linking error**가 난다. 전역 변수는 유일해야 한다. (최신 compiler는 이걸 슬쩍 넘어가기도 하는데, 그게 더 큰 폭탄이 될 수 있다는 내용은 뒤에서 다룬다.)
- (3) **`extern`**: compiler에게 "x라는 게 있다고 치고 넘어가라, linking 때 누군가 가지고 있을 것이다"라고 알려주는 정보다. 정의(definition)가 아니라 **선언(declaration)**이다.
  - 그래서 분할 compile 결과는 **불완전한 binary**(relocatable object, `*.o`)다. 1장에서 "object file은 실행할 수 없다"고 한 이유가 이것이다. Linker(`ld`)가 external 변수를 resolve해야 executable binary가 된다.

## Header file이 필요한 이유  `A 10:20`

- 최과장이 `int x`를 정의하고 정과장, 김과장이 `extern int x`로 쓰는데, 최과장이 `int`를 `char`로 바꾸면 쓰는 사람 모두 **수동으로** 고쳐야 한다. 파일이 1000개면 Ctrl+F로 다 찾아 고쳐야 하고, 놓치면 type이 다른 같은 변수가 되어 나중에 큰 사단이 난다.
- 해결: **정의한 사람이 header file**(`a.h`)에 `extern int x;`를 두고, 쓰는 사람은 `#include`한다. **Preprocessor(CPP)**가 compile 전에 내용을 치환하므로 header 한 곳만 고치면 자동으로 전파된다.
- Header file을 열어 보면 **죄다 `extern`**이다. 함수 선언 앞에도 (생략된) `extern`이 있다.
- 시험식 답 `B 00:00`: header file은 **분할 컴파일 환경에서 각 module에 정의된 함수나 전역 변수의 선언부를 모아, 일관된 interface를 공유**하기 위한 것이다. 수정할 때 중복 작업을 최소화한다.

## Library가 필요한 이유  `A 13:26`

- Object는 함수 단위로 수십만, 수백만 개(`sin`, `cos`, `printf`, `scanf` …)다. 어떻게 묶어서 재사용할까?

| 방법                       | 장점          | 단점                                     |
|----------------------------|---------------|------------------------------------------|
| Single big library         | 쓰기 편함     | 매번 큰 파일을 disk에서 찾음 → 비효율    |
| 함수마다 별도 object       | 찾기 효율적   | 100개 쓰면 100개 다 적어야 함, 실수 위험 |
| **관련 object를 grouping** | 중간 (해결책) |                                          |

- 해결: 논리적으로 묶는다. `sin`, `cos`, `tan` → **math library**(`-lm`), `printf` → standard I/O library. 사용자는 "탄젠트를 쓰니 `-l math`"처럼 개념 단위로 적으면 된다.

## Define vs. Declare  `B 01:05`

- **Define**: 변수는 실제로 create/allocate하는 것(예: `int`면 4 byte를 만든다). 함수는 **body가 있는 것**이다.
  - `int x;`, `int sum(int *a, int n) { … }`
- **Declare**: create하지 않고 "이걸 reference할 건데 definition은 다른 module에 나올 것"이라는 **compiler용 정보**다. 메모리 할당 없음.
  - `extern int x;`, `int sum(int *a, int n);` (body 없는 함수 선언은 앞에 `extern`이 생략된 것, 명시해도 된다)

## 변수의 attribute: scope, duration, linkage  `B 02:12`

|           | Scope       | Storage duration    | Linkage             |
|-----------|-------------|---------------------|---------------------|
| 지역 변수 | block scope | dynamic (temporary) | no linkage          |
| 전역 변수 | file scope  | static (permanent)  | external / internal |

- 지역 변수(automatic variable): block 시작 때 allocate, 끝날 때 deallocate. Procedure에서 배운 것처럼 **register나 stack**에 잠깐 생긴다. 다른 module은 존재 자체를 모른다 → no linkage.
- 전역 변수: block 바깥에서 정의되어 모든 block에서 참조 가능(file scope). **프로그램과 생사를 같이**한다(loading 시점부터 process 종료까지). 기본적으로 다른 module에서 참조 가능(external)하고, `static`을 붙이면 internal이 된다.
- 전역 변수는 모든 module에서 유일해야 한다. 지역 변수는 전역 변수와 이름이 겹쳐도 되고, 이때 **지역 변수가 우선**하며 전역 변수는 hidden된다.
- `static`, `extern`은 이 attribute를 바꾸는 **modifier**다.

## Multiple definition과 팀장의 역할  `B 05:31`

- `main.c`에 `int x = 1;`, `sub.c`에 `int x = 2;` → `multiple definition of 'x'` linking error (`ld returned 1 exit status`)
- 이 error를 보면 팀장은 두 가지 경우를 판단해 **교통정리**해야 한다.
  1. 다른 의미인데 우연히 이름이 같다 → 혼자 쓸 거면 **`static`**(internal linkage)
  2. 정말 같은 변수를 공유한다 → 둘 중 하나가 실수한 것. 개념상 맞는 쪽에 정의를 두고 나머지는 **`extern`**, header file로 정리한다.
- 배타적으로 쓸지 공유할지 정하는 것이 **module 간 interface의 첫 단추**이고 팀장의 역할이다.

## `static`의 두 가지 의미  `B 07:38`

- **전역 변수/함수 앞**: "이 파일 전용(private)" → **internal linkage**. `main.c`와 `sub.c`의 `static int x`는 완전히 다른 변수다. 그래도 헷갈리지 않게 이름을 다르게 짓는 것이 좋다.
- **지역 변수 앞**: duration을 temporary → **permanent**로 바꾼다. Register나 stack이 아니라 전역 변수와 나란히 **data section**에 저장되어 프로그램과 생명주기를 함께한다. **초기화는 startup 때 한 번만** 된다.

```c
for (counter = 0; counter < 3; ++counter) {
    int temporary = 1;          /* 매번 1 */
    static int permanent = 1;   /* 1, 2, 3 */
    ...
}
```

- 공통점: 둘 다 **permanent**하고 data section에 있으며 외부 module에서는 접근하지 못한다.
- 같은 이름의 static 지역 변수가 여러 함수에 있어도 된다. Data section에서는 `x.1`, `x.2`처럼 **unique symbol name**으로 indexing한다.
- `extern`은 변수뿐 아니라 함수에도 쓴다. 함수 선언 앞의 `extern`은 대부분 **생략**되니 유심히 볼 것.

## Quiz: 지역·전역·정적 변수 출력 (슬라이드 19–20)  `B 11:55`

`test1.c`(`extern int x;` + 함수들)와 `test2.c`(`int x = 1;`)를 함께 compile

| 호출                 | 출력     | 이유                          |
|----------------------|----------|-------------------------------|
| main outer           | 5        | main의 지역 변수              |
| main inner block     | 7        | 익명 block의 지역 변수가 우선 |
| main outer           | 5        | inner block 끝나면 7은 사라짐 |
| `useLocal`           | 25 → 26  | 매번 새로 allocate            |
| `useStaticLocal`     | 50 → 51  | data section, 초기화 1번      |
| `useGlobal`          | 1 → 10   | `test2.c`의 전역 x에 binding  |
| `useLocal` (2번째)   | 25 → 26  | 다시 새로 allocate            |
| `useStaticLocal` (2) | 51 → 52  | 값이 남아 있음                |
| `useGlobal` (2번째)  | 10 → 100 | `x *= 10`                     |
| main                 | 5        |                               |

## Linking 시점: static vs. dynamic linking  `B 15:00`

- **Static linking**: compile time에 relocatable object들을 묶어 완전히 link된 executable을 만든다.
  - 단점: `printf` 같은 자주 쓰는 library가 **모든 실행 파일마다 복사**된다. **Disk와 memory 모두에 redundancy**가 생긴다.
  - 장점: 이미 주소를 다 찾아 놓았으므로 **더 빠르고 안정적**이다.
- **Dynamic linking**: linking을 미룬다. "`printf`를 쓸 거니 나중에 묶어 달라"는 hint 정보만 남기고, 실행 때 **dynamic linker**가 memory에 이미 올라와 있는 **shared object**를 찾아 연결한다.
  - **Load-time dynamic linking**: loader가 disk에서 memory로 올릴(loading) 때 link
  - **Run-time dynamic linking**: 더 미뤄서 실제로 호출될 때 link
  - Redundancy는 없지만 runtime 비용이 약간 든다. 큰 프로젝트에서는 버전 문제 등으로 꼬이기도 한다.
- 정리하면 linking 방법은 **static, load-time dynamic, run-time dynamic** 세 가지이고, 이것들이 어떻게 동작하는지가 7장의 목표다.
- 같은 hello 프로그램: `-static`으로 만든 `hellos`는 **852K**, dynamic으로 만든 `hellod`는 **17K**

## Object file의 세 종류  `B 21:19`

| 종류                        | 용도                    | 비고                           |
|-----------------------------|-------------------------|--------------------------------|
| Relocatable object (`.o`)   | static linking 입력     | `.c` 하나당 `.o` 하나          |
| Shared object (`.so`)       | dynamic linking 입력    | Windows `.dll`, macOS `.dylib` |
| Executable object (`a.out`) | linking 출력, 실행 파일 | memory에 바로 복사해 실행      |

- 위 두 개가 linking의 **input**, 아래 하나가 **output**이다.
- 현대 프로그램은 all-or-nothing이 아니라 **일부는 static, 일부는 dynamic**으로 link한다. License 회피, 성능 등 전략적으로 섞어 쓰므로 둘 다 알아야 한다.
- Shared object는 loadable해야 한다. 즉 올라갈 location을 미리 약속해 둔다.

## Linker가 하는 일: symbol 단위의 두 단계  `B 24:29`

1. **Symbol resolution**: symbol table을 보고 각 symbol reference가 **정확히 하나의 definition**에 연결되는지 보장한다. 이 단계가 끝나면 실행 파일이 나올 수 있다는 확신이 생긴다.
2. **Relocation**: code는 code끼리, data는 data끼리 합친다. Object 안의 주소는 **가짜 주소**였으므로 합친 뒤 실제 주소가 정해지면 reference들을 고쳐야 한다.

- **지역 변수는 linking 대상이 아니다.** 이미 register나 stack 주소로 code에 반영되어 있다. 대상은 **symbol**(function, 전역 변수, static 변수)이다.

## Symbol과 symbol table  `B 27:39`

- Symbol: 함수나 전역 data에 대한 정보를 담은 lexical entity. 대략 name, type, binding, address(value), size …
  - ELF symbol entry 구조체의 bit field(`:`)는 type처럼 1 bit면 충분한 값에 char 8 bit를 다 쓰지 않으려는 것이고, reserved 영역은 padding 자리다.
  - **Value는 address라고 기억하되, 엄밀히는 section 안에서의 offset**이다.
  - 이런 형식도 약속, 즉 **ABI**다. Processor 의존적인 psABI와 processor 독립적인 ABI 두 종류가 있다고 앞에서 설명했다.
- **Symbol table**: symbol entry의 배열이고 ELF의 `.symtab` section에 있다. `strip`으로 지우지 않는 한 모든 relocatable object에 있다. **지역 변수 entry는 없다.**

```
$ objdump -t main.o
0000000000000000 g     O .data  0000000000000008 array
0000000000000000 g     F .text  000000000000001f main
0000000000000000         *UND*  0000000000000000 sum
```

- `main.c`의 symbol은 `array`, `main`, `sum` **3개**다(`val`은 지역 변수라 symbol이 아님).
  - `array`: size 8(int 2개), address 0x0 = `.data`의 첫 item
  - `main`: Function, size 0x1f = 31 byte, `.text`의 첫 함수
  - `sum`: 정의 없이 참조만 → **`*UND*`(undefined)**. 다른 module에서 나올 것이라고 linker에게 알려준다.
- `*UND*` 같은 것을 **pseudo section**이라 한다. Relocatable object에만 있고, linker가 나머지 n−1개 object에서 진짜 definition을 찾으면 없어진다. **실행 파일에는 없다.** 못 찾으면 `undefined reference to 'sum'`.

## Definition과 reference, symbol type  `B 31:52`

- Definition: create(allocate)한 것, body가 있는 함수
- Reference: 사용하는 것. 함수 호출(procedure call), 변수 접근, 주소가 필요한 것
  - `int *xp = &x;` → `xp`를 define하면서 `x`를 reference
  - `void swap() {…}` → define, `swap();` → reference
- Symbol type은 두 가지뿐이다: **Function(F)** 또는 **Object(O)**(전역/static 변수). **C의 지역 변수는 symbol이 아니다.**

## Symbol binding: local, global, external  `B 34:00`

| Binding              | 정의                                 | C에서                                 |
|----------------------|--------------------------------------|---------------------------------------|
| Local (지역 심벌)    | module 안에서만 정의·참조            | `static` 함수, `static` 전역 변수     |
| Global (전역 심벌)   | 이 module이 정의, 외부에서 참조 가능 | `static`/`extern` 없는 함수·전역 변수 |
| External (참조 심벌) | 이 module이 참조, 정의는 다른 module | `extern` 선언, body 없는 함수 선언    |

- **Local symbol ≠ local variable.** 지역 변수는 대상이 아니다.
- 외우는 법: `static`이 붙으면 local, `extern`이 붙으면 external, 둘 다 없으면 global. 단 **함수 선언 앞에 `extern`이 생략**되는 경우만 조심하면 된다.
- 예 (슬라이드 29): `main.c`의 `sum` 선언은 external, `array`와 `main`은 global
- 예 (슬라이드 30) `B 36:05`
  - `main.c`: `buf` global, `swap` (선언) external, `main` global
  - `swap.c`: `buf` external, `bufp0` global, `bufp1` (static) local, `swap` global, `temp`는 지역 변수라 linker가 모른다.

## Symbol section: `.text`, `.rodata`, `.data`, `.bss`  `B 38:13`

- Section: object file 안에서 **같은 속성을 가진 연속 영역**. Symbol 위치는 `[section index : section 내 offset]`으로 정의된다.
- 프로그램의 실체는 결국 **code(함수)와 data(전역 변수)**다. 지역 변수는 code 안에 register나 stack 주소로 들어 있다. 같은 속성끼리 모으되, 나중에 memory에 올릴 때의 **접근 권한(protection: read / write / execute)**을 기준으로 세분화했다.
  - `.text`: machine code. Executable + read-only
  - `.rodata`: read-only data. **`const` 전역 변수**, jump table 등. 나중에 memory에서 read-only로 처리하면 효율적이다.
  - `.data`: **0이 아닌 값으로 초기화된** 전역·static 변수
  - `.bss`: **초기화되지 않았거나 0으로 초기화된** 전역·static 변수
- **`.data`와 `.bss`를 나누는 이유** `B 41:22`: 초기화된 로고 이미지 배열 같은 것은 값을 object에 담아야 한다. 하지만 초기화 안 된 40KB 배열은 미리 공간을 잡을 필요 없이 "4 byte짜리가 만 개 필요" 같은 **요약 정보만** 남기고, **loading 때 allocate하며 0으로 초기화**하면 된다(전역 변수는 0으로 초기화하기로 약속). → object의 **disk space 절약**
  - 이름은 역사적으로 "Block Started by Symbol"이고, 교재에서는 **"Better Save Space"**로 외우라고 한다.
  - **예외**: 0으로 초기화한 것도 초기화 안 한 것과 같으므로 `.bss`로 간다. 의미 없는 초기값이면 1이 아니라 0으로 초기화하라.
  - Static 지역 변수도 같다: 초기화 안 했거나 0이면 `.bss`, 0이 아닌 값이면 `.data`. Symbol table에는 `x.1`, `x.2` 같은 unique 이름의 local symbol로 들어간다.
- 한 줄 요약 `B 45:40`: 전역이든 static이든 **초기화 안 함 → `.bss`**, **0으로 초기화 → `.bss`**, **0이 아닌 값 → `.data`**, **`const` → `.rodata`**

## ELF object file format  `B 45:40`

- 역사: 초기 UNIX의 **a.out** → **COFF**(초기 System V) → **ELF**(Executable and Linkable Format). Dynamic linking 지원 정도에 따라 진화했다. AT&T Bell Labs(System V)가 주도했고 BSD 계열 기능도 흡수해서 오늘날 UNIX, Linux, macOS가 사실상 ELF로 호환된다.
- Relocatable, executable, shared object를 **하나의 통일된 format**으로 표현한다.

```
ELF header            word size(32/64), byte order, file type(.o/exec/.so), machine type …
.text                 code (procedure 단위 = symbol 단위)
.rodata               read-only data (const 전역 변수, jump table)
.data                 초기화된 전역 변수
.bss                  초기화 안 된 전역 변수 (section header는 있지만 공간 차지 안 함)
.symtab               symbol table
.rel.text             .text 안의 reference들에 대한 relocation entry
.rel.data             .data 안의 reference(포인터 data)에 대한 relocation entry
.debug                gcc -g 소스 레벨 디버깅 정보
Section header table  각 section의 offset과 size
```

- `.symtab`부터 아래는 **memory에 load되지 않는다.**
- **어떤 symbol의 실제 위치 찾기** `B 52:04`: symbol table에서 그 symbol의 offset을 보고 section header table에서 해당 section의 시작 위치를 찾아 **더하면** 된다. ELF 파일만 보고 code와 변수의 map을 그릴 수 있다. AI 도움을 받아 binary 분석기나 시각화 도구를 직접 만들어 보라고 하셨다.

### `readelf -h main.o`  `B 53:11`

- **Magic number** `7f 45 4c 46`: `0x7f` 다음 `0x45 = 'E'`, `0x4c = 'L'`, `0x46 = 'F'` → "ELF"의 ASCII (`'A' = 65 = 0x41`부터 세면 된다). 이어지는 `02`는 64-bit, `01`은 little endian을 뜻한다.
- Type `REL (Relocatable file)`, Machine `X86-64`, Entry point `0x0`
- **별표**: `Start of section headers: 672`, `Size of section headers: 64`, `Number of section headers: 12`
  - Section header table은 파일 시작에서 672 byte 위치에 있고, 64 byte짜리 header가 12개 있다.
  - 따라서 **파일 크기 = 672 + 64 × 12 = 1440 byte**. 이 그림을 그릴 수 있어야 한다.

## Step 1: Symbol resolution  `B 58:32`

- Linker 입장: n개 object를 입력받아 하나씩 symbol table을 보며 symbol을 세 종류로 처리한다.
  - **Local symbol**: 문제없다. Compile이 성공했다는 것은 module 안에서 잘 정의되고 사용됐다는 뜻이다. Compiler가 module 내 unique 이름을 보장한다.
  - **External symbol** (`UND`): 나머지 n−1개를 뒤져서 definition이 **딱 하나** 나오는지 확인한다. 없으면 **undefined reference**(unresolved symbol) linking error.
  - **Global symbol**: definition이 있으므로 n−1개에서 같은 이름이 또 나오면 안 된다. 원칙은 multiple definition error인데, 역사적으로 **허용**해 주게 되었다.
- 허용한다는 것은 definition 두 개를 다 쓴다는 뜻이 아니라 **linker가 하나를 골라(choose one) 나머지를 `extern` 처리**한다는 뜻이다. 여기서 **모호함**이 생긴다. 그래서 팀장이라면 이걸 놔두면 안 되고 `static`이나 `extern`으로 정리하라고 지시해야 한다.
- `gcc -fno-common` 옵션을 주면 그냥 multiple definition error를 낸다. (교수님은 기본값이 꺼져 있다고 하셨다.)

### Strong / weak symbol과 linker의 규칙  `B 1:02:48`

- **Strong**: ① procedure(함수) ② **초기화된** 전역 변수
- **Weak**: **초기화되지 않은** 전역 변수(또는 static 변수). Weak만 외우면 된다.

| 규칙   | 상황                      | Linker 동작                             |
|--------|---------------------------|-----------------------------------------|
| Rule 1 | strong 2개 이상           | **linking error** (multiple definition) |
| Rule 2 | strong 1개 + weak 여러 개 | strong 선택, weak는 `extern` 처리       |
| Rule 3 | weak만 여러 개            | **임의로 하나** 선택                    |

- Rule 1은 진짜 error라서 차라리 고맙다. Rule 2, 3은 **개발자가 의도하지 않은 결과**가 나올 수 있다. 예: 자기만 쓰는 줄 알았던 `x`가 다른 module 때문에 갑자기 15212로 바뀐다.

### Nightmare scenario (슬라이드 40)  `B 1:05:56` / `C 02:09`

```c
/* foo.c */                         /* bar.c */
int x = 15213;   /* strong */       double x;      /* weak */
int y = 15212;   /* strong */       void f() { x = -0.0; }
```

- Linker는 **type을 추적하지 않는다**(size가 다르다는 warning만 낸다: `alignment 4 of symbol 'x' … is smaller than 8`). Warning을 무시하면 실행 파일이 만들어진다.
- Rule 2에 의해 `bar.c`의 `x`가 `foo.c`의 `x`(4 byte int)로 extern 처리된다. 그런데 `f()`는 `double`이므로 **8 byte를 쓴다.**
- 결과: `x = 0x0 y = 0x80000000`. 디버깅하기 매우 어렵다.
- **값 해석** `C 04:12`
  - Data끼리 모이므로 `x`가 `0x100`에 있다면 `y`는 바로 뒤 `0x104`에 있다.
  - `-0.0`(double)은 sign bit만 1이고 나머지 63 bit는 0 → `0x8000000000000000`
  - **Little endian**이므로 낮은 주소에 LS byte: `0x100–0x106`에는 `00`, `0x107`에 `80`
  - `x`(`0x100–0x103`)를 읽으면 `0x0`, `y`(`0x104–0x107`)를 읽으면 `0x80000000`(TMin)

### Linker puzzles (슬라이드 41)  `C 06:17`

| Module 1               | Module 2           | 결과                                                               |
|------------------------|--------------------|--------------------------------------------------------------------|
| `int x; p1(){}`        | `p1(){}`           | strong 2개(`p1`) → **link time error**                             |
| `int x; p1(){}`        | `int x; p2(){}`    | weak 2개 → 같은 초기화 안 된 int. 이게 정말 원한 건가?             |
| `int x; int y; p1(){}` | `double x; p2(){}` | weak 2개, 어느 걸 고르냐에 따라 `y`를 덮어쓸 **수도** 있음 (might) |
| `int x=7; int y=5;`    | `double x; p2(){}` | strong 선택 → `p2`의 쓰기가 `y`를 **덮어씀** (will)                |
| `int x=7; p1(){}`      | `int x; p2(){}`    | strong 선택 → 같은 초기화된 변수를 참조                            |

- 세 번째 줄: 왼쪽 `int x`가 선택되면 nightmare scenario와 같아 `y`가 덮어써지고, 오른쪽 `double x`가 선택되면 문제가 없을 수도 있다. 그래서 슬라이드에 **might**라고 썼다.
- **이 슬라이드에 별표.** Linking 파트에서 가장 중요한 내용 중 하나다.

### COMMON pseudo section (슬라이드 42)  `C 08:22`

```c
int a = 1;  int b = 0;  int c;
static int x = 1;  static int y = 0;
const int z = 3;
void bar();
void foo() { bar(); }
```

| Symbol | Binding  | Section     | 이유                               |
|--------|----------|-------------|------------------------------------|
| `a`    | global   | `.data`     | 0이 아닌 값으로 초기화             |
| `b`    | global   | `.bss`      | 0으로 초기화                       |
| `c`    | global   | **`*COM*`** | 초기화 안 된 전역 = weak → 미확정  |
| `x`    | local    | `.data`     | static, 초기화 → `a` 다음 offset 4 |
| `y`    | local    | `.bss`      | static, 0 → `b` 다음 offset 4      |
| `z`    | global   | `.rodata`   | `const`, offset 0                  |
| `foo`  | global   | `.text`     | 함수 정의                          |
| `bar`  | external | `*UND*`     | 선언만, pseudo section             |

- Symbol은 **8개**다.
- `a`와 `x`는 같은 `.data`지만 binding이 다르다(`a` global, `x` local). Address는 section 내 offset이므로 `a`가 0, `x`가 4다. `b`와 `y`도 같은 관계다. 이렇게 **map을 그릴 수 있어야** 한다.
- **`c`가 오늘의 주인공(별표).** 배운 대로면 `.bss`로 추정되지만, weak symbol은 Rule 2, 3에 의해 **extern 처리될 수도 있다.** 아직 link 전이라 진짜 definition인지 모르는 **미확정** 상태이므로 **COMMON**(미확정 심벌)으로 둔다. Linker의 선택을 받아야 `.bss`로 확정된다. `*UND*`와 마찬가지로 **pseudo section**이다.
- `nm foo.o`로도 볼 수 있다: `D a`, `B b`, `U bar`, `C c`, `T foo`, `d x`, `b y`, `R z`(소문자는 local).
- 시험에서는 file 이름이나 section 이름 같은 meta symbol은 무시하고 **user symbol 중심**으로 보면 된다. `C 21:44`

## Practical considerations (슬라이드 43)  `C 18:34`

- **전역 변수를 쓰지 마라.** 1학년 때는 scope가 넓어 편하게 썼지만, 3학년 multi-threading에서는 공유 자원이라 동기화 문제가 생기고 bottleneck이 된다. 반드시 필요할 때만 쓴다.
- 불가피하게 쓴다면
  1. **반드시 초기화하라** → strong symbol로 만들어 모호함을 없앤다. 의미 없는 초기값이면 **0으로** 초기화해서 `.bss`로 보내 object size를 줄인다.
  2. 외부 전역 변수를 참조하면 **`extern`**을 쓴다. `extern` 선언은 header file에 두고 정의는 정확히 하나의 `.c`에서 한다.
  3. 가능하면 **`static`**을 쓴다.
- 팀장이라면 linker가 애먹지 않도록 module 간 interface를 조율해야 한다.

## Quiz (슬라이드 44–45, 기출)  `C 20:36`

- **Problem 1** (슬라이드 42와 같은 코드): `x`는 `.data`, `y`는 `.bss`, `c`는 **COMMON**
- **Problem 2**

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

- `id`는 지역 변수라 symbol이 아니다. `static` 지역 변수 `cnt`는 0으로 초기화되어 `.bss`에 들어가는 symbol이다. → **symbol 6개**
- 각 symbol의 attribute (직접 정리, 참고)

| Symbol          | Type | Binding  | Section |
|-----------------|------|----------|---------|
| `done`          | O    | global   | `.data` |
| `wins`          | O    | global   | `.bss`  |
| `mask`          | O    | global   | `*COM*` |
| `player_status` | F    | external | `*UND*` |
| `master_status` | F    | global   | `.text` |
| `cnt`           | O    | local    | `.bss`  |

## Step 2: Relocation  `C 23:47`

- Symbol resolution이 끝났다 = 모든 reference가 정확히 하나의 definition과 연결됐다 = linking error 없이 combine할 수 있다. 이제 **기계적으로 합치는** 단계다. Linker는 각 object의 section 크기도 정확히 안다.
- 두 단계
  1. **Section과 symbol definition의 relocation**: 같은 종류의 section을 하나의 aggregate section으로 merge한다(모든 `.data` → 실행 파일의 `.data`). 각 section과 symbol에 run-time memory 주소를 부여한다. 이 단계가 끝나면 모든 symbol이 unique한 실제 주소를 가진다.
  2. **Section 안의 symbol reference 수정**: definition 주소는 정해졌지만 그걸 사용하는 code는 아직 업데이트된 적이 없다.
- 합칠 때 우리가 만든 object뿐 아니라 숨겨진 **system code와 system data**도 포함된다. 프로그램이 OS와 상호작용하며 정상적으로 시작하는 startup code, 끝나면 정리하는 finish code 등이다. `main`의 return은 process 종료를 의미한다.

### Relocation entry  `C 27:03`

```
$ objdump -d -r main.o
0000000000000000 <main>:
   0:  48 83 ec 08      sub    $0x8,%rsp
   4:  be 02 00 00 00   mov    $0x2,%esi
   9:  bf 00 00 00 00   mov    $0x0,%edi        # %edi = &array
                  a: R_X86_64_32   array          # relocation entry 1
   e:  e8 00 00 00 00   callq  13 <main+0x13>   # sum()
                  f: R_X86_64_PC32 sum-0x4        # relocation entry 2
  13:  48 83 c4 08      add    $0x8,%rsp
  17:  c3               retq
```

- `main.c`에는 reference가 2개다. `array`(data, Object type)와 `sum`(code, Function type)으로 성격이 다른 예시다.
- Object에서는 `call`의 주소도, 첫 번째 인자 `%rdi`에 넣는 `array`의 주소도 **전부 0**이다. Linking이 끝나야 실제 주소가 정해지므로 compiler가 넣어 봤자 의미가 없다. 그래서 object는 불완전한 파일이다.
- 대신 compiler(assembler)는 0을 넣고 **linker에게 메시지를 남긴다.** 이것이 **relocation entry**다(ELF에서 정의한 ABI, 교재 그림 7.9).
  - `offset`: 고칠 위치(section 시작부터의 거리)
  - `type`: 몇 byte를 어떤 방식으로 고칠지
  - `symbol`: 어느 symbol의 주소로
  - `addend`: 보정값
- `.text` 쪽 reference의 entry는 `.rel.text`, `.data` 쪽은 `.rel.data`에 모인다. `objdump`에 `-r` 옵션을 줘야 보인다.
- 관심 있는 두 type `C 31:24`
  - **`R_X86_64_32`**: 32-bit **절대 주소**. x86-64 주소는 8 byte지만 다 쓰면 instruction이 길어지므로 4 byte로 줄여 표현한다. 64-bit 주소를 어차피 다 쓰지 않으니 제약은 있지만 약속하면 찾아갈 수 있다.
  - **`R_X86_64_PC32`**: 32-bit **PC 상대 주소**. 함수들은 code 영역에 모여 있어서 거리가 가깝다. 현재 PC 기준 ± 거리로 작게 표현해 instruction size를 줄인다.

### 주소 계산  `C 36:34`

실행 파일 `prog`에서 `.text`(`main`) 시작 = `0x4004d0`, `array` = `0x601018`, `sum` = `0x4004e8`

- **Entry 1** (`R_X86_64_32`, offset `0xa`, `array`, addend 0)
  - 고칠 위치 `P = 0x4004d0 + 0xa = 0x4004da`
  - 값 = `S + A = 0x601018 + 0 = 0x601018` → little endian으로 `18 10 60 00`
  - 결과: `4004d9: bf 18 10 60 00  mov $0x601018,%edi`
- **Entry 2** (`R_X86_64_PC32`, offset `0xf`, `sum`, addend −4) `C 38:38`
  - 고칠 위치 `P = 0x4004d0 + 0xf = 0x4004df`
  - 값 = `S + A − P = 0x4004e8 − 4 − 0x4004df = 0x5`
  - 결과: `4004de: e8 05 00 00 00  callq 4004e8 <sum>`
  - 개념적으로는 **`call` instruction의 끝(다음 instruction 주소 `0x4004e3`)을 기준**으로 `sum`까지의 거리다. 1, 2, 3, 4, 5 → 5 byte. 기준점을 이렇게 잡은 것은 그냥 ABI의 약속이다. (Addend −4는 고칠 위치에서 4 byte짜리 필드 끝까지의 보정이다.)
- 공식을 기계적으로 외우기보다 **어떤 메시지인지** 큰 틀에서 이해하라고 하셨다. 모든 reference가 업데이트되면 실제 주소로 동작하는 executable이 만들어진다.

### Quiz Problem 3: Symbol relocation (슬라이드 51)  `C 42:48`

```
/* Before Linking */
  12:  e8 00 00 00 00   call 17 <main+0x17>
                 13: R_X86_64_PC32  func-0x4
/* After Linking */
  0000000000001129 <main>:
  113b:  e8 ___________   call ___________
  1140:  83 c0 01         add  $0x1,%eax
  0000000000001148 <func>:
```

- Relocation entry가 하나 있다 = 전역 변수나 함수에 접근하는 code이고 주소가 0으로 비어 있다.
- `S = 0x1148`, `A = −4`, `P = 0x1129 + 0x13 = 0x113c`
- `S + A − P = 0x1148 − 4 − 0x113c = 0x8`
- 개념적으로도 `call` 다음 instruction(`0x1140`)에서 `func`(`0x1148`)까지 **8 byte**
- 답: `113b: e8 08 00 00 00   call 1148 <func>`

## 강조 사항

- 분할 컴파일은 **개발 생산성**(reuse, 협업, 개발 시간)을 위한 것이고 **성능과 무관**하다.
- Header file의 정의: 분할 컴파일 환경에서 module들이 정의한 함수·전역 변수의 **선언을 모아 일관된 interface를 공유**하는 것
- `static`의 두 의미(전역: internal linkage / 지역: permanent duration), 함수 선언 앞의 **생략된 `extern`**
- Section 규칙: 초기화 안 함 / 0 → `.bss`, 0이 아닌 값 → `.data`, `const` → `.rodata`, 초기화 안 된 전역은 object 단계에서 **COMMON**
- Symbol binding 분류(local/global/external)와 **지역 변수는 symbol이 아니다**
- **Strong/weak 3 rules와 linker puzzles 슬라이드(41)에 별표.** Linking 파트에서 가장 중요한 내용 중 하나
- `readelf -h`의 **Start of section headers**(672)와 section header 크기·개수로 파일 크기와 구조를 그릴 수 있어야 한다.
- 기출: symbol table 채우기(section, binding, symbol 개수), PC-relative relocation 값 계산(`S + A − P`)

## 수업에서 다루지 않은 슬라이드

- 슬라이드 52: Linking Summary
