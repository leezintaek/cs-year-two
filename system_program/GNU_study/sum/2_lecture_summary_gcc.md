# GCC (GNU Compiler Collection) 강의 요약

> 출처: `pdf/GNU gcc (1).pdf` (CSE3209 System Programming)
> 💡 표시가 붙은 부분은 강의자료에 없거나 부족해서 보충한 내용입니다.

---

## 1. GNU 프로젝트와 GCC

- **GNU** = "GNU's Not UNIX" (재귀 약어)
- 1984년 Richard Stallman이 **free software**로 된 OS를 만들기 위해 시작한 프로젝트
  - 라이선스: **GNU GPL (General Public License)**
- GCC는 처음엔 **GNU C Compiler**의 약자였지만, 지금은 C++, Fortran, Ada, Go 등 여러 언어를 지원하므로 **GNU Compiler Collection**의 약자
- 첫 릴리스: 1987년

💡 **free software의 "free"** 는 "무료"가 아니라 "자유"(실행·연구·수정·재배포의 자유)를 뜻합니다. GPL은 수정본을 배포할 때도 같은 GPL로 소스를 공개해야 하는 **copyleft** 라이선스입니다.

---

## 2. 컴파일 과정 (4단계)

`gcc`는 사실 하나의 프로그램이 아니라, 아래 4개 도구를 순서대로 호출하는 **driver**입니다.

| 단계 | 도구 | 입력      | 출력      | 하는 일               |
| ---- | ---- | --------- | --------- | --------------------- |
| 1    | cpp  | program.c | program.i | 전처리 (#include 등)  |
| 2    | cc1  | program.i | program.s | C → 어셈블리 변환     |
| 3    | as   | program.s | program.o | 어셈블리 → 기계어     |
| 4    | ld   | program.o | program   | 링크 → 실행 파일 생성 |

- `program.o` : **ELF relocatable file** (재배치 가능한 목적 파일, 아직 주소가 확정되지 않음)
- `program`   : **ELF executable file** (실행 가능한 파일)

💡 **각 단계에서 멈추는 옵션** (강의자료에 없음, 실습에 매우 유용)

| 옵션          | 멈추는 시점   | 결과 파일     |
| ------------- | ------------- | ------------- |
| `-E`          | 전처리 후     | 표준출력 (.i) |
| `-S`          | 컴파일 후     | `.s`          |
| `-c`          | 어셈블 후     | `.o`          |
| (없음)        | 링크까지 완료 | `a.out`       |
| `-save-temps` | 끝까지 + 보존 | .i .s .o 모두 |

```bash
$ gcc -E hello.c -o hello.i    # 전처리 결과 확인 (#include가 펼쳐짐)
$ gcc -S hello.c               # hello.s 생성 (어셈블리 확인)
$ gcc -c hello.c               # hello.o 생성
$ gcc hello.o -o hello         # 링크
$ gcc -v hello.c               # 내부적으로 cc1, as, ld(collect2)를 호출하는 과정 출력
```

💡 **ELF (Executable and Linkable Format)** : Linux의 표준 실행/목적 파일 형식. `file hello.o`, `readelf -h hello`, `objdump -d hello` 명령으로 내용을 확인할 수 있습니다.

---

## 3. 설치와 환경 확인

```bash
$ uname -orm                   # 커널 버전, 아키텍처, OS 확인
6.8.0-40-generic x86_64 GNU/Linux
$ sudo apt-get install gcc     # 설치
$ gcc --version                # 버전 확인
gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
```

- 강의 환경: **x86_64 GNU/Linux** (arm64 아님)

💡 Apple Silicon Mac(arm64)은 어셈블리, 레지스터, gdb 지원 등이 x86_64와 다릅니다. 이후 어셈블리/디버깅 실습은 x86_64 Linux(VM, 서버 등)에서 하는 것이 안전합니다. `build-essential` 패키지를 설치하면 gcc, make 등이 한 번에 설치됩니다.

---

## 4. 출력 파일 이름 지정: `-o`

```bash
$ gcc hello.c              # 기본 이름 ./a.out 생성
$ gcc hello.c -o hello     # ./hello 생성
```

💡 `-o` 바로 뒤에는 반드시 출력 파일 이름이 와야 합니다. `gcc -o hello.c hello.c`처럼 실수하면 **소스 파일이 덮어써질 수 있으니** 주의하세요.

---

## 5. 경고(Warning)와 에러(Error)

### 메시지 형식
```
test.c:5:10: warning: format '%lf' expects argument of type 'double', but argument 2 has type 'int' [-Wformat=]
```
- `test.c` : 파일 이름
- `5`      : **줄 번호**
- `10`     : **열(column) 번호**
- `[-Wformat=]` : 이 경고를 켜는 옵션 이름

### Error vs Warning

| 구분    | 컴파일 진행 | 의미                        |
| ------- | ----------- | --------------------------- |
| Error   | 중단        | 컴파일 자체가 불가능한 문제 |
| Warning | 계속        | 문제일 가능성이 있는 코드   |

경고는 "프로그램이 정말 의도대로 동작하는지 확인해야 하는 위험 지점"입니다. GNU C의 비표준 기능 사용도 경고 대상입니다.

### 경고 관련 옵션

| 옵션      | 의미                                |
| --------- | ----------------------------------- |
| `-w`      | 모든 경고 끄기                      |
| `-Wall`   | 유용한 경고 대부분 켜기 (항상 권장) |
| `-Werror` | 모든 경고를 에러로 취급             |

`-Wall`이 잡아주는 예:
- `-Wunused-variable` : 사용하지 않는 변수
- `-Wuninitialized`   : 초기화 안 된 변수 사용
- `-Wformat`          : printf/scanf 형식 지정자와 인자 타입 불일치

예제 코드 (`test.c`):
```c
#include <stdio.h>
int main(void)
{
    int i;
    printf("hello world! %lf", i);   // %lf인데 int를 넘김 + i 미초기화
    return 0;
}
```

💡 **보충**
- `-Wall`은 이름과 달리 "모든" 경고가 아닙니다. `-Wextra`를 함께 쓰면 더 많은 경고(예: 사용 안 한 매개변수)를 볼 수 있습니다.
- 표준 C 준수 여부를 엄격히 검사하려면 `-pedantic`(또는 `-Wpedantic`)을 씁니다.
- 실무/과제 권장 조합: `gcc -Wall -Wextra -g -o prog prog.c`
- 초기화 안 된 변수 경고는 최적화 수준에 따라 나오기도, 안 나오기도 합니다(`-O` 이상에서 더 정확).

---

## 6. 최적화 수준: `-On`

최적화 수준을 높이면 프로그램은 대체로 빨라지지만, **컴파일 시간이 늘고 디버깅이 어려워집니다**.

| 옵션        | 의미                                          |
| ----------- | --------------------------------------------- |
| `-O0`       | 최적화 없음 (기본값), 디버깅 결과가 예상대로  |
| `-Og`       | 디버깅을 해치지 않는 선에서 최적화 (gcc 4.8~) |
| `-O1`, `-O` | 기본 최적화, -O0보다 작거나 빠름              |
| `-O2`       | -O1 + 추가 최적화 (배포용으로 흔히 사용)      |
| `-O3`       | -O2 + 비용이 큰 최적화 (루프 벡터화 등)       |

```bash
$ gcc -O1 -o hello hello.c   # 1단계 최적화
$ gcc -c -Og hello.c          # 디버깅 친화적 최적화로 목적 파일만 생성
```

💡 **보충**
- `-Os` : 실행 파일 **크기**를 줄이는 쪽으로 최적화 (임베디드에서 사용)
- 최적화를 켜면 변수가 레지스터에만 존재하거나 아예 사라져서, gdb에서 `<optimized out>`으로 표시되고 `next`가 소스 줄 순서대로 움직이지 않을 수 있습니다. 그래서 디버깅할 때는 `-O0` 또는 `-Og`를 씁니다.
- `-S`로 `-O0`과 `-O2`의 어셈블리를 비교해 보면 최적화의 효과를 직접 볼 수 있습니다.

---

## 7. 디버깅 정보: `-g`

- `-g` (= `-g2`) : 디버깅 정보 생성 → gdb에서 **변수 이름(symbol)과 소스 줄 번호**로 디버깅 가능
- `-g3` / `-ggdb3` : 더 많은 정보 포함 → **매크로(`#define MAX 256`)까지** gdb에서 확인 가능
- 디버깅 정보 = [소스 줄 번호] ↔ [기계어 주소] 대응표

```bash
$ gcc -o hello test.c           # 디버깅 정보 없음
$ gcc -g -o hello_d test.c      # 기본 디버깅 정보
$ gcc -ggdb3 -o hello_d2 test.c # 매크로까지 포함
$ ls -al
-rwxr-xr-x 1 root root  8608 Sep 1 hello
-rwxr-xr-x 1 root root  9632 Sep 1 hello_d
-rwxr-xr-x 1 root root 29416 Sep 1 hello_d2
```
→ 디버깅 정보가 많을수록 **파일 크기가 커집니다**.

💡 디버깅 정보는 **DWARF** 형식으로 ELF 파일 안의 `.debug_*` 섹션에 저장됩니다. `strip hello_d` 명령으로 제거할 수 있고, `-g`는 실행 속도에는 영향이 없습니다(파일 크기만 증가).

### 참고: `ls -al` 출력 읽기
`-rwxr-xr-x 1 root root 8608 Sep 1 hello`
→ 권한, 링크 수, 소유자, 그룹, 크기(byte), 수정 날짜, 이름

첫 글자 (파일 종류):

| 문자 | 종류          |
| ---- | ------------- |
| `-`  | 일반 파일     |
| `d`  | 디렉터리      |
| `l`  | 심볼릭 링크   |
| `b`  | 블록 장치     |
| `c`  | 문자 장치     |
| `p`  | FIFO (파이프) |
| `s`  | 소켓          |

나머지 9글자: owner(u) / group(g) / others(o) 각각의 `rwx` 권한
- `rwxr-xr-x` = `111 101 101` (2진수) = **755** (8진수)
- 💡 r=4, w=2, x=1을 더하면 됩니다. 예: `chmod 644 file` → `rw-r--r--`

---

## 8. 매크로 정의: `-Dname[=definition]`

컴파일할 때 명령줄에서 매크로를 정의합니다. 소스 코드를 고치지 않고 **디버그용 코드를 켜고 끌 때** 유용합니다.

```c
#include <stdio.h>
void test(){};
int main(void)
{
#ifdef DEBUG_TEST
    printf("test\n");
    test();
#else
    test();
#endif
    return 0;
}
```
```bash
$ gcc -DDEBUG_TEST test.c
$ ./a.out
test
```

💡 **보충**
- `-DMAX=100` → 소스 맨 위에 `#define MAX 100`을 쓴 것과 같음
- `-DNAME`처럼 값 없이 쓰면 `#define NAME 1`과 같음
- `-UNAME` : 매크로 정의 해제
- `-I<dir>` : 헤더 파일 검색 경로 추가, `-L<dir>` `-l<lib>` : 라이브러리 경로/링크 (예: `-lm`은 math 라이브러리)

---

## 9. C 언어 표준 버전: `-std=VER`

| 표준 | 발표         | `__STDC_VERSION__` |
| ---- | ------------ | ------------------ |
| C89  | ANSI, 1989   | (정의 안 됨)       |
| C90  | ISO, 1990    | (정의 안 됨)       |
| C99  | ISO, 1999    | 199901L            |
| C11  | ISO, 2011    | 201112L            |
| C17  | ISO, 2017(8) | 201710L            |

- C89와 C90은 **내용이 같은 언어** (ANSI판 / ISO판)
- C17은 새 기능 없이 C11의 결함만 수정한 버전

```c
#include <stdio.h>
int main(void) {
#ifdef __STDC_VERSION__
    printf("__STDC_VERSION__ = %ld \n", __STDC_VERSION__);
#endif
    return 0;
}
```
```bash
$ gcc test2.c && ./a.out
__STDC_VERSION__ = 201710      # gcc 11의 기본값은 gnu17
$ gcc -std=c11 test2.c && ./a.out
__STDC_VERSION__ = 201112
```

💡 **보충**
- C99 이후 대표 기능: `//` 주석, `for (int i = 0; ...)` 반복문 안 변수 선언, `stdbool.h`, `long long`
- C11: `_Static_assert`, `_Generic`, 익명 구조체, `<threads.h>`
- **C23** (ISO/IEC 9899:2024)이 최신 표준이며 `__STDC_VERSION__`은 202311L입니다. (`-std=c23` 또는 구버전 gcc에서는 `-std=c2x`)
- `-std=c11`은 순수 ISO C, `-std=gnu11`은 ISO C + GNU 확장입니다. gcc 기본값은 `gnu` 계열입니다.

---

## 10. 옵션 한눈에 보기

| 옵션           | 의미                     |
| -------------- | ------------------------ |
| `-o file`      | 출력 파일 이름 지정      |
| `-c`           | 목적 파일(.o)까지만 생성 |
| `-E` / `-S`    | 전처리 / 어셈블리까지만  |
| `-w`           | 경고 끄기                |
| `-Wall`        | 주요 경고 켜기           |
| `-Werror`      | 경고를 에러로            |
| `-O0`~`-O3`    | 최적화 수준              |
| `-Og`          | 디버깅 친화적 최적화     |
| `-g`, `-g3`    | 디버깅 정보 추가         |
| `-DNAME[=val]` | 매크로 정의              |
| `-std=c11`     | C 표준 버전 지정         |
