# GDB (GNU Debugger) 강의 요약

> 출처: `pdf/GNU gdb (1).pdf` (CSE3209 System Programming)
> 💡 표시가 붙은 부분은 강의자료에 없거나 부족해서 보충한 내용입니다.

---

## 1. 버그와 디버깅

- **최초의 컴퓨터 버그**: Harvard 대학의 Mark II 컴퓨터가 계속 오류를 내서 살펴보니 릴레이에 **나방(moth)** 이 끼어 있었음 → 문자 그대로 "de-bug" (💡 1947년 9월 9일, Grace Hopper 팀의 기록으로 유명)
- **Bug** : 프로그램/시스템이 잘못되거나 예상치 못한 결과를 내게 하는 오류
- **Debugging** : 버그를 찾아 해결하는 과정
  - 버그는 다른 함수, 다른 모듈로 **전파**되어 더 복잡한 문제를 일으킬 수 있음
  - 문제가 커지기 전에 **최대한 빨리** 찾아 고치는 것이 목표

---

## 2. Debugger

- 소스 코드를 조사하고 디버깅하는 도구
- **Dynamic analysis** (동적 분석) : 프로그램을 **실행하면서** 동작을 관찰
  - ↔ **Static analysis** (정적 분석) : 실행하지 않고 코드만 검사 (💡 예: 컴파일러 경고, cppcheck, clang-tidy)
- 주요 기능
  1. 프로그램을 시작하고, **지정한 조건에서 멈추게** 함
  2. 실행을 **제어**함 (한 줄씩 진행 등)
  3. 멈췄을 때 **무슨 일이 일어났는지 조사**함

---

## 3. 디버깅 4단계

| 단계       | 내용                                |
| ---------- | ----------------------------------- |
| Test       | 다양한 입력으로 시험                |
| Stabilize  | 특정 오류를 **재현**할 수 있게 만듦 |
| Localize   | 오류 원인의 **위치**를 좁혀 나감    |
| Correction | 결함 자체를 수정                    |

### Debugging Heuristic
- 버그를 **재현하고 위치를 찾는 것이 문제 해결의 90%**
  - 어떻게 발생하는가 → 위치 특정 (파일 이름과 줄 번호)
- **익숙한 버그 패턴부터 의심하기**

```c
switch (i) {
case 0:
    ...
    /* break 누락 → case 1로 넘어감(fall-through) */
case 1:
    ...
    break;
}

int i;
scanf("%d", i);     /* &i 가 아니라 i → 잘못된 주소에 쓰기 */

if (i = 5)          /* == 대신 = → 항상 참 */

if (i & j)          /* && 대신 & → 비트 AND (1 & 2 == 0) */
```
→ 컴파일러 경고(`-Wall`)를 켜면 이 중 일부(전부는 아님)를 잡을 수 있음

💡 `-Wall`로 잡히는 것: `scanf("%d", i)`(-Wformat), `if (i = 5)`(-Wparentheses). `switch` fall-through는 `-Wextra`(-Wimplicit-fallthrough)에서, `&` vs `&&`는 대부분 잡히지 않습니다.

### 디버깅 전략
- **Divide and Conquer** : 의심 범위를 반씩 줄여 나가기
- **printf 넣기** : printf를 더 넣을수록 오류 범위를 좁힐 수 있음
  - 💡 단, `printf` 출력은 버퍼링되므로 프로그램이 crash하면 출력이 안 보일 수 있습니다. `fprintf(stderr, ...)`(버퍼링 없음)를 쓰거나 `\n`/`fflush(stdout)`를 붙이세요.
- **최근에 바꾼 부분**에 집중해서 debugger 사용

---

## 4. GDB 개요

`(gdb) help`로 볼 수 있는 명령 분류:

| 분류         | 내용                         |
| ------------ | ---------------------------- |
| running      | 프로그램 실행                |
| breakpoints  | 특정 지점에서 멈추기         |
| watchpoints  | 식의 값이 바뀔 때마다 멈추기 |
| data         | 데이터 조사                  |
| stack        | 스택 조사                    |
| user-defined | 사용자 정의 명령             |
| aliases      | 명령 별칭                    |

### 기본 사용 흐름
1. `-g` 옵션으로 빌드 ("debug mode compile") : `gcc -g hello.c -o hello`
2. `gdb hello`로 시작 → 이 시점엔 **프로그램이 아직 실행되지 않음**
3. `run` 전에 **breakpoint를 먼저 설정**
4. breakpoint에서 멈추면 `print`, `x`, `display`로 변수 조사
5. `kill`로 실행 중인 프로그램 종료
6. `quit`로 gdb 종료

- `gdb`만 입력해서 시작한 후 `file program`으로 실행 파일을 불러올 수도 있음
- `Ctrl-l` : 화면 지우기

💡 `-g` 없이 빌드하면 `No symbol table is loaded` 메시지가 나오고, 소스 줄/변수 이름으로 디버깅할 수 없습니다. 또 최적화(`-O2` 등)를 켜면 변수가 `<optimized out>`으로 보이므로 디버깅 시엔 `-O0`(기본) 또는 `-Og`를 사용합니다.

---

## 5. 주요 GDB 명령

| 명령 (약어)        | 의미                                      |
| ------------------ | ----------------------------------------- |
| `break` (`b`)      | breakpoint 설정 (함수 이름/줄 번호)       |
| `info b`           | breakpoint 목록 보기                      |
| `delete N` (`d`)   | N번 breakpoint 삭제 (`d`만 쓰면 전부)     |
| `run` (`r`)        | 프로그램 실행 (인자 전달 가능)            |
| `next` (`n`)       | 한 줄 실행, 함수는 **건너뜀** (step over) |
| `step` (`s`)       | 한 줄 실행, 함수 **안으로** (step into)   |
| `nexti`/`stepi`    | 기계어 명령어 한 개 단위로 실행           |
| `continue` (`c`)   | 다음 breakpoint까지 계속 실행             |
| `finish`           | 현재 함수 끝까지 실행 후 호출자로 복귀    |
| `advance N`        | N번 줄까지 실행                           |
| `print E` (`p`)    | 변수/식 E의 값 출력                       |
| `backtrace` (`bt`) | 함수 호출 스택 출력                       |
| `up` / `down`      | 스택 프레임 위(호출자)/아래로 이동        |
| `list` (`l`)       | 소스 코드 보기                            |
| `info args`        | 현재 함수의 인자 값                       |
| `info locals`      | 현재 함수의 지역 변수 값                  |
| `kill`             | 실행 중인 프로그램 종료                   |
| `quit` (`q`)       | gdb 종료                                  |

예:
```
(gdb) break main       # main 함수에서 멈춤
(gdb) break 8          # 8번 줄에서 멈춤
(gdb) run arg1 arg2    # 명령줄 인자와 함께 실행
```

💡 **`list` 사용법**

| 명령               | 의미                |
| ------------------ | ------------------- |
| `list`             | 다음 10줄 보기      |
| `list -`           | 이전 10줄 보기      |
| `list [file:]num`  | 해당 줄 주변 보기   |
| `list [file:]func` | 해당 함수 주변 보기 |
| `info source`      | 현재 소스 파일 이름 |

💡 **강의자료에 없지만 자주 쓰는 명령**

| 명령              | 의미                                   |
| ----------------- | -------------------------------------- |
| `Enter` (빈 입력) | 직전 명령 반복 (n, s 반복에 편리)      |
| `display E`       | 멈출 때마다 E 값을 자동 출력           |
| `watch E`         | E 값이 **바뀔 때** 멈춤 (watchpoint)   |
| `x/Nfu addr`      | 메모리 내용 직접 보기 (예: `x/4xw &a`) |
| `p/x E`           | 16진수로 출력 (`/d` `/t` `/c` 등)      |
| `ptype E`         | 변수/식의 타입 출력                    |
| `set var x = 3`   | 실행 중에 변수 값 변경                 |
| `until`           | 루프 끝까지 실행                       |
| `info frame`      | 현재 스택 프레임 상세 정보             |
| `tbreak`          | 한 번만 멈추는 breakpoint              |

---

## 6. 실습: Matloff 소수 찾기 프로그램

### 배경
k가 소수인지 확인하려면 **√k 이하의 소수**로 나누어 떨어지는지만 보면 됩니다.
- 예: 101 → √101 ≈ 10.05 이하의 소수 2, 3, 5, 7로 나누어 떨어지지 않으므로 소수
- 2를 제외한 짝수는 검사할 필요 없음 (짝수로 나누어지면 2로도 나누어지므로)

### 코드 (버그 포함)
```c
// prime.h
#ifndef _PRIME_H_
#define _PRIME_H_
#define MAX_PRIMES 100000
#include <stdbool.h>
extern bool is_prime[MAX_PRIMES];
void check_prime(int k);
#endif

// main.c
#include "prime.h"
#include <stdio.h>
int main() {
    int N;
    int cnt = 1;
    int upper_bound;
    printf("Find all primes between 3 and ?\n");
    scanf("%d", upper_bound);                 // 버그 1
    is_prime[2] = true;
    printf("2 is a prime\n");
    for (N = 3; N <= upper_bound; N += 2) {
        check_prime(N);
        if (is_prime[N]) {
            printf("%d is a prime\n", N);
            cnt++;
        }
    }
    printf("The number of primes is %d \n", cnt);
    return 0;
}

// prime.c
#include "prime.h"
bool is_prime[MAX_PRIMES] = {0};   // is_prime[i]: i가 소수면 1
void check_prime(int k) {
    int j = 2;
    while (1) {                        // 버그 2
        if (is_prime[j] == 1)
            if (k % j == 0) {
                is_prime[k] = 0;
                return;
            }
        j++;
    }
    is_prime[k] = 1;   // 약수가 없으면 소수
}
```

💡 `prime.h`의 `#ifndef _PRIME_H_ ... #endif`는 **include guard**입니다. 같은 헤더가 여러 번 include되어도 한 번만 처리되게 합니다. `extern`은 "변수의 정의는 다른 파일(prime.c)에 있다"는 **선언**입니다.

### 컴파일
```bash
$ gcc -g main.c prime.c -o matloff
main.c:15:8: warning: format '%d' expects argument of type 'int *', but argument 2 has type 'int' [-Wformat=]
```
→ **이미 경고가 버그 1을 알려주고 있음!** 경고를 무시하지 말 것.

### 실행 → Segmentation fault
```
$ ./matloff
Find all prime numbers between 3 and ?
20
Segmentation fault
```
- **Segmentation fault** : OS가 할당하지 않았거나 접근이 허용되지 않은 메모리에 접근하려 할 때 발생

💡 OS가 프로세스에 **SIGSEGV** 시그널을 보내 강제 종료시키는 것입니다. 대표 원인: NULL/초기화 안 된 포인터 역참조, 배열 범위 초과, 스택 오버플로(무한 재귀), 읽기 전용 메모리에 쓰기.

---

### 버그 1: `scanf`에 주소 대신 값 전달

```
(gdb) run
Program received signal SIGSEGV, Segmentation fault.
0x00007ffff7a6cdf5 in _IO_vfscanf_internal (...) at vfscanf.c:1902
1902    vfscanf.c: No such file or directory.
```
- 시스템 함수 안에서 죽음 → 라이브러리 함수가 틀렸을 가능성은 낮음
- `backtrace`로 어떻게 여기까지 왔는지 확인

```
(gdb) backtrace
#0  0x00007ffff7a6cdf5 in _IO_vfscanf_internal (...) at vfscanf.c:1902
#1  0x00007ffff7a785ef in __isoc99_scanf (...) at isoc99_scanf.c:37
#2  0x0000000000400603 in main () at main.c:15
```
- 스택 프레임 3개: `main()` → `__isoc99_scanf()` → `_IO_vfscanf()`
- **사용자 코드인 main.c:15가 의심 지점** → Localize!

```
(gdb) list main.c:15
15  printf("Find all prime numbers between 3 and ?\n");
16  scanf("%d", upper_bound);
```
- 초기화 안 된 `upper_bound`의 **값(쓰레기 값)을 scanf가 주소로 사용** → 잘못된 메모리에 쓰기
- **수정**: `scanf("%d", &upper_bound);`

```
(gdb) kill
Kill the program being debugged? (y or n) y
(gdb) quit
```
- 실제로는 gdb를 끄지 않고 **두 번째 터미널**에서 수정·재컴파일하는 것이 일반적
- 재컴파일 후 gdb에서 `run`하면 `'matloff' has changed; re-reading symbols.`로 자동 반영

💡 backtrace에서 `#0`은 현재 실행 중인(가장 안쪽) 함수, 숫자가 커질수록 호출한 쪽입니다. `up`/`frame 2`로 main 프레임으로 이동하면 그 시점의 main의 지역 변수를 볼 수 있습니다. 화면의 줄 번호(15/16)가 1줄 차이 나는 것은 강의자료 캡처 시점 차이일 뿐입니다.

---

### 버그 2: 무한 루프로 배열 범위 초과

```
(gdb) run
Program received signal SIGSEGV, Segmentation fault.
0x000000000040071e in check_prime (k=3) at prime.c:9
9       if(is_prime[j])
```
- `check_prime(3)` 안에서 `is_prime[j]` 접근 중 사망 → **j가 범위를 벗어났다고 가정**

```
(gdb) print j
$3 = 147328
(gdb) print is_prime[147328]
Cannot access memory at address 0x625000
(gdb) print is_prime
$4 = {false, false, true, false <repeats 99997 times>}
(gdb) print *is_prime@20
$5 = {false, false, true, false <repeats 17 times>}
```
- `j = 147328` > `MAX_PRIMES(100000)` → 배열 범위 초과
- 💡 `*배열@개수` : 배열의 앞부분 N개만 출력하는 gdb 문법 (포인터로 받은 동적 배열을 볼 때 특히 유용)
- 원인: `while (1)`은 소수인 약수를 못 찾으면 **끝나지 않음** (k=3일 때 is_prime[3]이 아직 0이라 j가 계속 증가)
- **수정**: √k까지만 검사
```c
for (j = 2; j * j <= k; j++) {
    if (is_prime[j])
        if (k % j == 0) {
            is_prime[k] = 0;
            return;
        }
    j++;            // ← 남아 있음 (버그 3)
}
```

💡 배열 범위를 조금 넘는 접근은 segfault 없이 다른 변수를 조용히 덮어쓰기도 합니다. 이번엔 j가 매우 커져 매핑되지 않은 주소에 닿았기 때문에 crash가 났습니다. 이런 버그는 `gcc -g -fsanitize=address`(AddressSanitizer)나 `valgrind`로 더 쉽게 잡을 수 있습니다.

---

### 버그 3: 9와 15를 소수로 판정

```
$ ./matloff
20
2 is a prime
3 is a prime
5 is a prime
7 is a prime
9 is a prime       ← 틀림
11 is a prime
13 is a prime
15 is a prime      ← 틀림
17 is a prime
19 is a prime
The number of primes is 10
```
segfault는 사라졌지만 **논리 오류**가 남음 → 실행을 추적(trace)해 보자.

#### breakpoint와 next
```
(gdb) break main
Breakpoint 1 at 0x40064e: file main.c, line 9.
(gdb) info b
Num  Type        Disp Enb Address            What
1    breakpoint  keep y   0x000000000040064e in main at main.c:9
(gdb) r
Breakpoint 1, main () at main.c:9
(gdb) next
11  int cnt = 1;
(gdb) n
14  printf("Find all prime numbers between 3 and ?\n");
(gdb) n
15  scanf("%d", &upper_bound);
20                  ← scanf가 입력을 기다리므로 값을 입력해야 진행
```

#### step (함수 안으로)
```
(gdb) n
22  check_prime(N);
(gdb) step
check_prime (k=5) at prime.c:7
7   int j = 2;
(gdb) bt
#0  check_prime (k=5) at prime.c:7
#1  0x00000000004006a8 in main () at main.c:22
(gdb) info args
k = 5
(gdb) info locals
j = 32767          ← 아직 초기화 전이라 쓰레기 값
```

#### finish, up, down
```
(gdb) up             # 호출자(main) 프레임으로
#1  main () at main.c:22
(gdb) down           # 다시 check_prime 프레임으로
#0  check_prime (k=3) at prime.c:7
(gdb) finish         # 현재 함수를 끝까지 실행하고 main으로 복귀
Run till exit from #0 check_prime (k=3) ...
main () at main.c:23
23  if (is_prime[N]){
```

#### Conditional Breakpoint (조건부 breakpoint)
```
(gdb) break prime.c:7 if k >= 9     # k가 9 이상일 때만 멈춤
Breakpoint 2 at 0x400712: file prime.c, line 7.
(gdb) d 1                           # 1번 breakpoint 삭제
(gdb) cond 2 k >= 15                # 2번의 조건을 변경
(gdb) ignore 2 10                   # 2번을 다음 10번은 무시
```
- 조건은 **C 문법**으로 작성 (`==` 대신 `=`을 쓰는 실수 주의 → 값을 바꿔버림!)
- 💡 `cond 2` (조건 없이) : 조건 제거 → 무조건 멈춤

#### 원인과 수정
- `for` 문에서 이미 `j++`를 하는데 **본문에도 `j++`가 남아 있어** j가 2씩 증가
  → j = 2, 4, 6 ... 만 검사하고 **3은 건너뜀**
  → 9(=3×3), 15(=3×5)를 3으로 나눠보지 않아 소수로 판정
- **수정**: 본문의 `j++` 삭제

```
(gdb) r
Breakpoint 2, check_prime (k=9) at prime.c:7
(gdb) d                       # 모든 breakpoint 삭제
Delete all breakpoints? (y or n) y
(gdb) advance 19              # 19번 줄까지 실행
(gdb) c
Continuing.
11 is a prime
13 is a prime
17 is a prime
19 is a prime
The number of primes is 8
[Inferior 1 (process 16128) exited normally]
```
→ 20 이하의 소수 2, 3, 5, 7, 11, 13, 17, 19 = **8개** 정답

💡 **세 버그 정리**

| 버그 | 증상        | 원인                | 사용한 명령       |
| ---- | ----------- | ------------------- | ----------------- |
| 1    | segfault    | scanf에 `&` 누락    | run, bt, list     |
| 2    | segfault    | while(1) 무한 증가  | print, `*arr@N`   |
| 3    | 잘못된 결과 | j++ 중복 → 3 건너뜀 | break, step, cond |

💡 이 상황에선 `watch j`(j가 바뀔 때마다 멈춤)를 걸면 j가 2→3→4…가 아니라 2→4→6…으로 한 번에 2씩 뛰는 것을 바로 확인할 수 있습니다.

---

## 7. gdb TUI (Text User Interface)

```bash
$ gcc -g exbitfield.c
$ gdb -tui a.out
```

| 명령              | 의미                           |
| ----------------- | ------------------------------ |
| `gdb -tui`        | 소스 창과 명령 창을 함께 표시  |
| `Ctrl-x` `Ctrl-a` | TUI 모드 켜기/끄기             |
| `layout src`      | 💡 소스 창                     |
| `layout asm`      | 💡 어셈블리 창                 |
| `layout split`    | 소스 + 어셈블리 함께           |
| `layout regs`     | 💡 레지스터 창 추가            |
| `focus cmd`       | 명령 창에 포커스 (방향키 사용) |
| `disp /bt &x`     | 멈출 때마다 x를 2진수로 표시   |
| `ni`              | 기계어 한 명령씩 진행          |
| `p sizeof(x)`     | x의 크기 출력                  |

- 이후 강의에서 gdb TUI로 **저수준(low-level) 디버깅**을 배울 예정

💡 `display /bt &x`는 `x/tb &x`로 표시됩니다: **x**(examine) 명령으로 `&x` 주소의 메모리를 **t**(2진수) 형식, **b**(byte, 1바이트) 단위로 보여 줌.
`x/Nfu` 형식 정리

| 자리 | 의미 | 값          |
| ---- | ---- | ----------- |
| N    | 개수 | 숫자        |
| f    | 형식 | x d t c s i |
| u    | 단위 | b h w g     |

- f: x(16진수), d(10진수), t(2진수), c(문자), s(문자열), i(기계어 명령어)
- u: b(1바이트), h(2바이트), w(4바이트), g(8바이트)

예: `x/4xw &arr` → arr 주소부터 4바이트(word) 4개를 16진수로

---

## 8. [선택] 저수준 시스템 프로그래밍용 gdb 플러그인

기본(vanilla) GDB는 저수준 작업에 불편하므로 플러그인을 사용하기도 함.
- gef : https://github.com/hugsy/gef
- peda : https://github.com/longld/peda
- pwngdb : https://github.com/scwuaptx/Pwngdb
- **pwndbg** : https://github.com/pwndbg/pwndbg
  - 저수준 SW 개발자, 하드웨어 해커를 위한 기능에 초점
  - Ubuntu 18.04/20.04/22.04, GDB 8.1 이상 지원

```bash
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh
```

💡 이런 플러그인은 멈출 때마다 레지스터, 스택, 디스어셈블리를 자동으로 보여줍니다. 플러그인은 `~/.gdbinit`에서 로드되므로, 여러 개를 동시에 쓰면 충돌할 수 있습니다(하나만 사용 권장).
