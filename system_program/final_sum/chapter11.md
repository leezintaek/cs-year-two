# 11. Library and Interpositioning 요약

- 과목: CSE3209 System Programming / 교재: Bryant & O'Hallaron, *Computer Systems* 3rd Ed. 7장 (p.707–753)
- 녹음
  - A = `video_1795085296960.mp4` (약 23:30) — 슬라이드 1–10, static library
  - B = `video_1795085311560.mp4` (2026-11-19, 약 1:05:40) — 슬라이드 11–28, shared library·run-time linking
  - C = `video_1795521541839.mp4` (2026-11-24, 약 27:00) — 슬라이드 29–44, interpositioning·퀴즈
- 진도: 슬라이드 1–44 (45–47 퀴즈는 직접 풀어보라고 함)
- 원문 전사: `_workspace/system_program/chapter11/video_*.transcript.md`

> 라이브러리는 **static library**(`.a`, archive)와 **shared library**(`.so`)로 나뉜다. Static은 필요한 object만 골라 executable에 merge해서 빠르고 의존성이 없지만 disk·memory에 중복이 생긴다. Shared는 disk·memory에 한 copy만 두고 load time에 연결하는데, 주소가 고정되지 않고 `.text`는 read-only라서 **PLT(jump table, code)와 GOT(address table, data)를 거치는 indirect mechanism**과 **lazy binding**(첫 호출 때 dynamic linker가 GOT를 채움)으로 해결한다. 재시작 없이 라이브러리를 쓰려면 `dlopen`/`dlsym`으로 **run-time linking**을 하고, 원본 소스 수정 없이 `malloc` 같은 함수 호출을 가로채는 **interpositioning**은 compile/link/run time 세 시점에서 할 수 있다.

## 개요: 분할 컴파일에서 라이브러리로  `A 00:00`

- 분할 컴파일은 협업과 생산성을 위해 했고, 나누다 보니 자주 쓰는(commonly used) 것을 reuse할 수 있게 라이브러리로 만들자는 흐름이 생겼다. 이번 장의 주인공은 라이브러리다.
- 내용(슬라이드 2): static library의 archive file, shared library의 PLT·GOT(보안 하는 학생들은 많이 들어봤겠지만 여기서는 시스템 측면에서 본다), linking 시점 구분(compile time, load time, run time), run-time linking용 Linux `dl` library API, interpositioning

## Static library와 archive file  `A 02:08`

- 라이브러리를 만드는 두 극단
  - 모든 함수를 **하나의 큰 object**로: 개발자는 그 파일 하나만 link하면 되어 **편리**하지만, linker가 그 안의 symbol을 다 찾아야 하고 file I/O도 생겨 **비효율적**
  - **함수마다 object 하나씩**: 효율적이지만 개발자가 쓰는 object를 일일이 기억해서 link해야 해서 불편
- 그 중간(hybrid)으로 **관련 있는 object끼리 grouping**한 것이 **archive**(꾸러미) 파일이다. 예: 수학 함수(sin, cos 등)를 모은 `libm.a`. 편리함과 효율성의 **균형**을 맞춘 전략이다.
- 핵심: link할 때 archive 전체가 붙는 것이 아니라 **참조된 symbol이 있는 object만** executable에 포함된다(슬라이드 3).
- **Archive 구조 (슬라이드 4)** `A 05:16`: object들의 collection + 앞에 **archive symbol index**
  - index가 없으면 linker는 archive 안의 object `m`개의 symbol table을 모두 scan해야 한다.
  - index는 "symbol `x`는 object `f`에 있다"는 길잡이 정보다. 반면 ELF symbol table은 그 object 안에서의 symbol을 설명한다.
- **자주 쓰는 라이브러리 (슬라이드 5)** `A 07:25`
  - `libc` (C standard library): `printf`, `scanf`, startup·exit 코드 등. **명시하지 않아도 기본으로 link**된다.
  - `libm` (math library) 등 나머지는 compile할 때 **반드시 option으로 명시**해야 한다.
  - 위치는 보통 `/usr/lib`나 `/lib` 아래(Ubuntu: `/usr/lib/x86_64-linux-gnu`). 교재 기준 `libc.a`는 object 1496개, `libm.a`는 444개(약 2 MB).
  - `ar -t <archive>`로 포함된 object 목록을 볼 수 있다. `ar`는 archiver.

## Static library 만들기와 배포  `A 10:37`

- 다음 시간에 **간단한 과제(나만의 라이브러리 만들기)**가 나갈 예정이라 만들 줄 알아야 한다. 외주나 아르바이트로 소프트웨어를 줄 때도 소스 코드를 다 주는 대신 라이브러리로 숨겨서 주는 것이 일반적이다.
- **만드는 3단계 (슬라이드 6)**

```
$ gcc -Og -c foo.c bar.c          # 1) object file 생성
$ ar -r libmy.a foo.o bar.o       # 2) archive 생성
$ ar -t libmy.a                   # 3) 확인: 포함된 object 목록
$ nm -s libmy.a                   #    archive index와 각 object의 symbol
```

- `ar` option: `r` 있으면 replace/없으면 추가, `c` 없으면 생성, `s` symbol index 생성. 요즘은 `c`, `s`가 기본이라 **`-r`만 주면 된다**.
- 이름 규칙: **`lib<NAME>.a`**. 강제는 아니지만 표준 linker 도구들과 호환되려면 반드시 지킨다.
- `nm`은 name의 줄임말로 symbol table을 본다. `nm -s` 결과의 `Archive index:`가 앞에서 말한 archive symbol index다(`foo in foo.o`, `bar in bar.o`, `baz in bar.o`).
- **배포 (슬라이드 7)** `A 14:50`: archive만 주면 못 쓴다. 함수·data의 선언(signature)을 담은 **header file**을 함께 준다. 받는 쪽은 `ar -x`로 object를 풀어낼 수도 있다.

## Static library 사용과 command line order  `A 15:51`

- 두 가지 방법(슬라이드 8)

```
$ gcc main.o ./libmy.a              # 경로 직접 지정 (이름 자유)
$ gcc -static main.o -L. -lmy       # 회사에서는 이 방식
```

- `-static`: linker에게 **static linking(= merge, embedding)**을 강제
- `-L.`: library search path에 `.`(current working directory)를 추가. 원하는 경로를 full path로 써도 된다. 못 찾으면 기본 경로(`/lib`, `/usr/lib`)를 찾는다.
- `-lmy`: `libmy.a`(static) 또는 `libmy.so`(shared)를 찾는다. `my`라는 파일을 찾는 것이 아니다. 둘 다 없으면 `undefined reference to 'foo'`
- **Linker의 resolution algorithm (슬라이드 9)** `A 18:58`
  - command line을 **왼쪽에서 오른쪽**으로 scan하며 unresolved reference 목록을 유지하고, 새 `.o`/`.a`를 만날 때마다 그 정의로 해결한다. 끝까지 남으면 error.
  - 라이브러리(definition)가 먼저 나오면 그 시점에는 해결할 reference가 없어서 그냥 지나가고 기억하지 않는다 → 뒤의 `main.o` reference를 해결하지 못함
  - **교훈: object(reference)를 앞에, library(definition)를 뒤에**

```
$ gcc -static main.o -L. -lmy        # OK
$ gcc -static -L. -lmy main.o        # undefined reference to `foo'
```

- **확인 (슬라이드 10)** `A 21:09`
  - `nm -s a.out | grep bar` → 아무것도 안 나옴(쓰지 않은 `bar.o`는 link 안 됨), `grep foo` → `T foo`
  - `|`는 pipe: 앞 명령의 표준 출력을 뒤 명령의 input으로 넘긴다. `grep`은 그중 문자열이 매칭되는 줄만 출력한다.
  - `ldd`(List Dynamic Dependencies): dynamic link된 `.so` 목록. `-static`이면 `libmy`, `libc` 모두 static link되므로 `not a dynamic executable`
  - 사용하지 않은 것 같아도 `_start`, `_exit` 같은 system library object가 `libc.a`에서 함께 embedding된다.

## `-static`을 빼면?  `B 04:24`

- 가정(슬라이드 11): `libmy.a`는 있지만 `libmy.so`는 없다. `libc.a`, `libc.so`는 system에 built-in되어 있다.
- **기본값은 dynamic linking**이다. linker는 먼저 `.so`를 찾고, 없으면 `.a`로 static linking을 시도한다.
  - `libmy` → `.so`가 없으므로 static link
  - `libc` → `.so`가 있으므로 **dynamic link** (`ldd prog`에 `libc.so`가 나옴)
- `-static`을 주면 system library까지 다 embedding되어 binary가 생각보다 훨씬 커진다: `progstatic` 900,280 bytes vs `prog` 15,832 bytes
- **교재 예제 (슬라이드 12–13)** `B 07:32`: `addvec`, `multvec`를 `libvector.a`로 만들고 `main.c`에서 `addvec`만 사용 → `addvec.o`만 fully linked executable에 들어가고 `multvec.o`는 붙지 않는다.

```
$ ar -r libvector.a addvec.o multvec.o
$ gcc -static main.c -L. -lvector -o prog1
```

- 라이브러리는 기술적인 이유뿐 아니라 **사업·저작권** 이유로도 만든다. 소스 공개 여부는 회사가 정하는 것이고, dynamic library·static library·일반 object는 법적으로도 구분되는 개념이라 "dynamic linking으로 해라" 같은 지시가 내려올 수 있다. `B 08:33`

## Static library의 장단점  `B 11:42`

- 장점: fully linked라 **외부 의존성 없이** 실행된다(안정적인 버전). run-time resolution이 없어서 dynamic linking **보다** 빠르다(상대적 개념).
- 단점(슬라이드 14)
  - 저장된 executable들에 같은 코드가 중복(모든 프로그램이 `libc`를 씀)
  - 실행 중 memory에도 중복
  - system library의 작은 버그 수정에도 **전부 rebuild·restart**
- 예: **CVE-2015-7547**, glibc `getaddrinfo`의 stack 취약점. CVE(Common Vulnerabilities and Exposures)는 취약점에 붙이는 표준 식별 번호다. 이런 게 나오면 static link된 프로그램은 다 다시 만들어야 한다. `B 13:46`

## Shared library  `B 14:49`

- 아이디어(슬라이드 15): build time에 fully link하면 중복이 생기므로, "프로그램 A는 `printf`를 쓰고 그건 `libc.so`에 있다"는 **map 정보만 남긴다**. 실행(load time, disk → memory)할 때 dynamic linker가 이미 memory에 올라와 있으면 그대로 쓰고, 없으면 올린다.
- **disk에도 한 copy, memory에도 한 copy**(`.text`를 여러 process가 공유)
- 대신 찾아야 하므로 static보다 느릴 수밖에 없다 = **run-time overhead**. 크지는 않지만 무시할 수준도 아니다.
- Linux `.so`, Windows `.dll`, Mac `.dylib` 모두 같은 기법이라 한 번 배우면 어디서나 통한다.

### Challenge  `B 17:05`

- 2단계 linking(symbol resolution, relocation) 중 static linking은 build time에 reference를 다 고쳐 두었다. Dynamic linking에서는 (슬라이드 16)
  1. **주소가 고정되지 않는다**: library는 계속 추가될 수 있어 `printf`=1번 같은 식으로 고정할 수 없고, **ASLR**(Address Space Layout Randomization)로 code·heap·library 시작 주소가 보안상 랜덤화된다.
  2. **`.text`는 read-only**: memory에 올라온 text segment는 보호를 위해 수정할 수 없다. 그러니 load 후 `printf` 주소를 code에 써넣을 수 없다.
- 디스크에 있을 때는 section, memory에 올라오면 segment라고 부른다.

### Solution 1: indirect mechanism  `B 20:16`

- reference가 **변하지 않는 주소**(jump table)로 가게 하고, 거기서 **수정 가능한 data segment의 table**을 참조해 진짜 주소로 가게 한다(슬라이드 17). "한 쿠션 맞고 가는" 방식이다.
  - **PLT (Procedure Linkage Table)** = jump table, `.text`(read-only)에 있다. 각 entry는 **16-byte code**(첫 instruction이 `jmp`인 instruction 3개)
  - **GOT (Global Offset Table)** = address table, `.data`(writable)에 있다. 각 entry는 **8-byte address**
- 프로그램이 쓰는 **외부 library symbol마다 PLT entry와 GOT entry가 한 쌍**씩 생긴다. `printf`, `sin`, `foo` 3개를 쓰면 PLT 16 B × 3 = 48 B, GOT entry도 3개
- 16 B, 8 B 크기는 compiler·linker·loader가 모두 알아야 하는 약속, 즉 **ABI**다. `B 30:43`
- build time에는 `printf` 주소를 몰라도, load time에 GOT만 업데이트하면 **code(text) 수정 없이** 연결된다.

### Solution 2: lazy binding  `B 25:24`

- 실제 프로그램은 hidden system library까지 포함해 외부 symbol이 수백·수천 개다. load time에 전부 resolve하면 로딩이 엄청 길어진다.
- **2:8 법칙**: 실제로 쓰는 건 20%도 안 된다. 그래서 resolve를 **실제로 처음 호출될 때(first invocation)까지 미룬다** → **lazy binding**. load time의 불필요한 relocation 수백·수천 개를 피하고 비용을 분산시킨다.
- GOT는 처음에 모두 **dynamic linker 쪽 경로**로 채워져 있다(unresolved). 첫 호출 때 dynamic linker가 깨어나 주소를 찾아 GOT에 기록하고, 두 번째 호출부터는 GOT가 바로 진짜 함수로 보낸다.
- 그래서 첫 호출은 느리고, 두 번째부터도 한 번 거쳐 가므로 static보다는 약간 느리다.

### PLT/GOT 동작 따라가기 (슬라이드 18–20)  `B 31:43`

```c
int main() {
  printf("hello");          // callq 0x4005c0 <printf@plt>
  printf("hello, again");   // callq 0x4005c0 <printf@plt>  ← 같은 주소
}
```

- `printf@plt`: static linking이었다면 call 주소로 step into하면 바로 libc의 `printf` 코드가 나온다. dynamic에서는 PLT의 `printf` entry로 간다.

```
# PLT[0]: call dynamic linker           # GOT (data segment)
4005a0: pushq *GOT[1]                   GOT[0]: addr of .dynamic
4005a6: jmpq  *GOT[2]                   GOT[1]: addr of reloc entries
…                                       GOT[2]: addr of dynamic linker
# PLT[2]: call printf()                 GOT[3]: 0x4005b6  # sys startup
4005c0: jmpq  *GOT[4]                   GOT[4]: 0x4005c6  # printf() => plt
4005c6: pushq $0x1                      GOT[5]: 0x4005d6  # exit() => plt
4005cb: jmpq  4005a0
```

- PLT entry는 16 B씩이므로 `printf` entry가 `4005c0`이면 다음 entry는 `4005d0`, 이전은 `4005b0`, PLT[0]은 `4005a0`
- **First invocation** `B 37:00`
  1. `callq 0x4005c0` → PLT[2]
  2. `jmpq *GOT[4]` → GOT[4] 값은 `0x4005c6`, 즉 **바로 다음 instruction**("dynamic linker path")
  3. `pushq $0x1`: dynamic linker와 stack으로 통신하는 parameter("`printf`를 찾아 달라" 같은 정보). 지금은 control만 보면 된다.
  4. `jmpq 4005a0` → PLT[0]: `pushq *GOT[1]`, `jmpq *GOT[2]` → GOT[2] = **dynamic linker** 실행
  5. dynamic linker가 `printf`를 찾아 **GOT[4]를 `&printf`로 고친다**.
- **Second invocation** `B 40:12`: 같은 `0x4005c0` → 같은 PLT entry → 그런데 GOT[4]가 바뀌어 있으므로 바로 진짜 `printf`로 간다.
- PLT는 procedure로 가는 연결(linkage) 역할을 하는 code block이다. jmp 하나만 넣으면 lazy binding을 못 하므로 instruction 2~3개를 더 넣었다.

### gdb 실습 (슬라이드 21–23)  `B 43:19`

- `gcc -g hello.c -o hello -fcf-protection=none`, `gdb -tui hello`, breakpoint 후 `ni` … `si`(step into)
- 이 예시에서 PLT entry는 `0x401030`. 그 안의 `jmp`는 `%rip` 기준 상대 주소로 GOT entry `0x404018`을 참조한다. 그 거리는 build time에 고정된 값이다.
- 첫 호출 때 `x 0x404018` → `0x401036`(PLT entry의 다음 instruction = dynamic linker path). 두 번째 호출 때 → `0x00007ffff7e24c90`(`7ff…`로 시작하는 shared library의 진짜 `printf`)
- `%rip`(PC) 기준 상대 주소로 표현해서 위치가 바뀌어도 text를 수정할 필요가 없는 code가 **PIC(position-independent code)**다.
- 동영상도 있고 어렵지 않으니 직접 해 보라고 하며 넘어갔다. `B 48:44`

## Shared library 만들고 쓰기  `B 48:44`

```
$ gcc -Og -c -fpic foo.c bar.c                # PIC로 object 생성
$ gcc -shared -o libmy.so foo.o bar.o         # ar 대신 gcc -shared
$ gcc main.c -L. -lmy                         # -static 없으면 .so부터 찾음
$ export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH   # run-time library 경로 추가
```

- 기본 library 경로를 바꾸고 싶으면 환경변수 `LD_LIBRARY_PATH`에 기존 값과 current working directory를 합쳐 assign한다(오픈소스SW개론에서 배운 내용).
- 교재 그림 7.16(슬라이드 25): 두 단계를 한 번에 `gcc -fpic -shared -o libvector.so addvec.c multvec.c`, 그다음 `gcc -o prog2 main.c libvector.so`. link 결과는 **partially linked** executable이고, loader(`execve`)가 올릴 때 dynamic linker(`ld-linux.so`)가 `libc.so`, `libvector.so`와 연결해 memory에서 fully linked가 된다.

## Load-time vs run-time linking  `B 51:51`

- 지금까지 배운 것(lazy binding 포함)은 엄밀히 **load-time dynamic linking**이다. static은 build time에 다 붙이고, dynamic은 link time에 정보만 남겨 partially link한 뒤 load time에 찾는다.
- 한계: 프로그램이 load될 때 shared library가 **다 준비되어 있어야** 한다. Windows에서 "DLL 파일이 없습니다"로 실행이 안 되는 것과 같은 맥락이다.
- 또 라이브러리 버그 수정이나 새 기능 추가 시 결국 **restart**해야 한다.
- 그런데 서버급 프로그램은 멈출 수 없다. 예: 삼성 반도체 공정 관리 소프트웨어. 온도·습도·웨이퍼 건조 등 수많은 장비가 매년 바뀌고 새 장비 제어 라이브러리가 추가되는데, restart는 곧 돈이다. `B 53:54`
- 그래서 나온 것이 **run-time linking**: 프로그램이 필요한 시점에 **명시적으로** 특정 `.so`를 열고 함수 이름으로 주소를 얻어 쓰는 방식. `malloc`/`free`로 명시적으로 memory를 요청·해제하는 것과 같은 개념이다(슬라이드 26). `B 56:12`
- restart 없이 USB나 네트워크로 `.so`만 배포해 원격 software update를 할 수 있다. 실무에서 꼭 쓰게 될 기술이라 **과제로 낸다**.

## `dl` library API (슬라이드 27)  `B 58:16`

- OS가 지원해야 하며 Linux에서는 `dl` library. API는 `dlopen`, `dlsym`, `dlclose`와 error용 `dlerror`의 4개뿐이다.
- `void *dlopen(const char *filename, int flag)`: 라이브러리를 열고 **handle**(라이브러리 식별자, file descriptor·FILE pointer와 같은 개념)을 return. 실패하면 `NULL`
  - `RTLD_LAZY`: open 때 resolve하지 않고 실제로 symbol을 요청할 때까지 또 미룬다. 주로 이걸 쓴다.
- `void *dlsym(void *handle, const char *symbol)`: 이 시점에 dynamic linker가 resolve해서 진짜 주소를 return
- `int dlclose(void *handle)`: 다 쓰면 unload
- `char *dlerror(void)`: 가장 최근 `dl*` 호출의 error 문자열(파일을 못 찾음, permission 없음 등)
- handle은 보통 **global variable**로 관리한다. 카메라, 센서처럼 run-time 라이브러리가 여러 개일 수 있기 때문이다.

## Run-time linking 예제 (슬라이드 28)  `B 1:01:23`

```c
void *handle;
void (*addvec)(int *, int *, int *, int);   // pointer to function returning void (8 B)

handle = dlopen("./libvector.so", RTLD_LAZY);
if (!handle) { fprintf(stderr, "%s\n", dlerror()); exit(1); }

addvec = dlsym(handle, "addvec");
if ((error = dlerror()) != NULL) { fprintf(stderr, "%s\n", error); exit(1); }

addvec(x, y, z, 2);          // 진짜 함수처럼 호출
if (dlclose(handle) < 0) { … }
```

```
$ gcc -rdynamic -o prog main.c -ldl
```

- `addvec`은 함수 주소를 저장하는 **function pointer**다. 개발자는 **signature를 알고 있어야**(header나 문서로) 이렇게 선언할 수 있다. 주소만으로는 쓸 수 없다.
- `fprintf`는 다음 주에 배운다. 지금은 `printf`라고 생각하면 된다.
- 응용: GUI의 browse 버튼으로 라이브러리 경로의 `.so` 목록을 띄우고, 선택하면 `dlopen`, `go` 버튼을 누르면 `dlsym`으로 `go` 함수를 얻어 호출한다. function pointer도 매번 resolve하지 말고 global로 저장해 둔다. `B 1:04:33`
- `dl` 자체도 라이브러리이므로 **`-ldl`**을 줘야 한다(3학년 때 multithreading에서 `-lpthread`를 쓰는 것과 같다).

## Library interpositioning  `C 00:00`

- 7장 마지막 주제이고, 끝나면 **8장**으로 넘어간다.
- 정의(슬라이드 29): 프로그램이 library function을 호출할 때 그 호출을 **redirect**해서 원래 함수 대신 user-defined 함수가 실행되게 하는 기법. intercept, hooking이라고도 한다. 핵심은 **원본 소스 수정 없이**다.
- 용도: debugging/profiling(memory 사용 추적), monitoring, behavior modification, prototype에 기능을 붙여 보는 테스트
- **예제 문제 (슬라이드 31)** `C 01:06`: `malloc(32)`, `free(p)`만 있는 `int.c`를 고치지 않고 할당·해제되는 block의 주소와 크기를 trace하라.
  - 왜 필요한가: 대규모 프로젝트에서는 `malloc`과 `free`가 서로 다른 module, multithread·multiprocess에서 흩어져 호출되어 **memory leak**이 생긴다. 서버 application은 1~2년씩 꺼지지 않으므로 4 B leak도 누적되면 언제 터질지 모르는 시한폭탄이다. 회사에서는 **1급(critical) bug**로 분류하고, 찾으려면 동적 분석(monitoring, tracing)이 필요하다.
  - 그냥 `mymalloc`/`myfree`로 소스를 바꾸면 "원본 수정 없이"라는 조건 위반이다. 이미 배포된 코드를 고치면 side effect와 검증 비용이 생겨서 팀장급이 싫어하는 방식이다.
- 시점에 따라 세 가지(슬라이드 30): **compile time**(preprocessor 치환), **link time**(linker가 다른 구현으로 resolve), **load/run time**(dynamic linking 때 다른 `.so`의 symbol로 override)

### Compile-time interpositioning (슬라이드 32–34)  `C 06:16`

- `-I.`: header를 찾을 디렉터리를 추가. `-I.`이면 system 디렉터리(`/usr/include`)보다 **current working directory를 먼저** 찾는다.
- `#include <malloc.h>`를 만난 preprocessor가 `/usr/include/malloc.h` 대신 직접 만든 `./malloc.h`를 붙여 넣는다.

```c
/* ./malloc.h */
#define malloc(size) mymalloc(size)
#define free(ptr)    myfree(ptr)
void *mymalloc(size_t size);
void myfree(void *ptr);
```

- 소스는 그대로 두고 치환을 preprocessor에게 위임한 것이다.
- `mymalloc.c`는 `#ifdef COMPILETIME … #endif`로 감싸져 있고, `gcc -DCOMPILETIME -c mymalloc.c`의 `-D`는 맨 위에 `#define COMPILETIME`을 넣은 것과 같다. 실무에서는 Linux/Windows용 코드, debug/release 빌드를 이런 식으로 골라 compile한다. `C 10:32`

```
gcc -Wall -DCOMPILETIME -c mymalloc.c
gcc -Wall -I. -o intc int.c mymalloc.o
./intc  →  malloc(32)=0x1edc010 / free(0x1edc010)
```

- wrapper가 있는 `mymalloc.c`는 표준 `malloc.h`로 compile된다는 점에 주의(그래야 wrapper 안의 `malloc`이 진짜 `malloc`이다).

### Link-time interpositioning (슬라이드 35–37)  `C 11:35`

- 옵션 없이 compile하면 dynamic linking이 되어 `malloc`, `free` reference는 "`libc.so`에 있다"는 정보만 남고 첫 호출 때 PLT/GOT로 resolve된다.
- `-Wl,<args>`: 뒤의 인자를 **linker에게 전달**한다(comma는 space로 바뀜). `--wrap,malloc`은 "`malloc`을 wrapping하겠다"는 뜻이다.
  - `malloc`에 대한 reference → **`__wrap_malloc`**으로 resolve
  - `__real_malloc`에 대한 reference → 원래 **`malloc`**으로 resolve
- wrapper 안에서 그냥 `malloc`을 부르면 또 `__wrap_malloc`이 되므로, 원래 함수는 `__real_malloc`으로 부르기로 미리 약속한 것이다. 이름은 고정된 규칙이니 기계적으로 따르면 된다.

```c
void *__wrap_malloc(size_t size) {
    void *ptr = __real_malloc(size);   /* Call libc malloc */
    printf("malloc(%d) = %p\n", (int)size, ptr);
    return ptr;
}
```

```
gcc -Wall -DLINKTIME -c mymalloc.c
gcc -Wall -c int.c
gcc -Wall -Wl,--wrap,malloc -Wl,--wrap,free -o intl int.o mymalloc.o
```

### Run-time interpositioning (슬라이드 39–42)  `C 18:09`

- 그냥 `gcc int.c`로 compile(dynamic linking)하고, `malloc` 정의를 가진 `mymalloc.so`를 따로 만든다.
- 환경변수 **`LD_PRELOAD="./mymalloc.so"`**를 설정하면, 첫 호출 때 dynamic linker가 `malloc`을 찾을 때 **link map chain**에서 미리 load된 `mymalloc.so`를 `libc.so`보다 먼저 보고 거기서 `malloc`을 찾는다.
- wrapper 안에서 원래 `malloc`을 부르려면 `dlsym`의 첫 인자에 predefined 상수 **`RTLD_NEXT`**를 준다. 현재(`mymalloc.so`) 다음 link 정보, 즉 `libc.so`에서 `malloc`을 찾아 그 주소를 return한다.

```c
void *malloc(size_t size) {
    void *(*mallocp)(size_t size);
    mallocp = dlsym(RTLD_NEXT, "malloc");   /* Get addr of libc malloc */
    …
    char *ptr = mallocp(size);              /* Call libc malloc */
    printf("malloc(%d) = %p\n", (int)size, ptr);
    return ptr;
}
```

```
gcc -Wall -DRUNTIME -shared -fpic -o mymalloc.so mymalloc.c -ldl
gcc -Wall -o intr int.c
LD_PRELOAD="./mymalloc.so" ./intr
```

## 기출 퀴즈 풀이  `C 22:26`

- **Problem 1 (Static linking, 슬라이드 43)**: 성공하는 명령은? → **1번, 4번** (`main.o ./libfunc.a`, `-L. main.o -lfunc`). left-to-right scan이므로 library가 command line 오른쪽에 있어야 한다.
- **Problem 2 (Dynamic linking, 슬라이드 44)** `C 23:36`
  - Q1. PLT/GOT의 주 목적 → **4번**(고정되지 않는 dynamic library 함수 주소를 run time에 효율적으로 resolve). challenge(주소 고정 불가, code read-only) → indirect mechanism(data segment의 GOT를 수정)
  - Q2. 첫 번째와 두 번째 `printf` 호출의 차이 → 둘 다 같은 PLT entry로 가지만, GOT entry가 첫 호출 때는 **dynamic linker path 주소**, 두 번째는 **`printf`의 real address**
  - Q3. Lazy binding을 쓰는 주된 이유 → **2번**(프로그램 startup time 단축). 2:8 법칙으로 쓰지 않을 symbol까지 미리 resolve할 필요가 없다.
- 나머지(Problem 3–5)는 직접 풀어 보라고 했다. "이런 식으로 나올 수 있다"며 개념 체크를 당부했다.

## 강조 사항

- **과제**: run-time linking(`dlopen`/`dlsym`) 관련 과제가 나간다. 실무에서 요긴하게 쓰는 기술이라 직접 써 보라는 취지다. (A에서는 "라이브러리 만들기" 과제가 다음 시간에 나간다고 했고, B 시작에서 수업 말미에 과제를 소개하겠다고 했지만 녹음에는 소개 부분이 없다. 세부 내용은 확인 필요)
- 기출 형태: command line order(library는 뒤에), PLT/GOT 목적, first vs second invocation 차이, lazy binding 이유
- Command line order: **object 앞, library 뒤**
- `-static`이 없으면 기본은 dynamic linking이고, `.so`부터 찾고 없으면 `.a`로 간다.
- PLT = 16 B code(text, read-only), GOT = 8 B address(data, writable). 외부 symbol마다 한 쌍이다.
- Memory leak은 회사에서 1급 bug이고, interpositioning이 그 추적에 쓰인다.
- gdb로 PLT/GOT를 따라가는 실습은 직접 해 보라고 했다.

## 수업에서 다루지 않은 슬라이드

- 슬라이드 38: Link-time Interpositioning (요약 슬라이드)
- 슬라이드 45: Quiz [Problem 3] Runtime Linking — 직접 풀어보기
- 슬라이드 46: Quiz [Problem 4] Interposition — 직접 풀어보기
- 슬라이드 47: Quiz [Problem 5] System Call — 직접 풀어보기
- 슬라이드 48: Summary
