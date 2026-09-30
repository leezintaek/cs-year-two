# GCC (GNU Compiler Collection)

**과목**: CSE3209 System Programming
**출처**: GNU_study/pdf/GNU gcc (1).pdf, https://www.gnu.org/software

## 1. GCC란 무엇인가

- **GNU 프로젝트**: 1984년 Richard Stallman이 "자유 소프트웨어(free software)"이자 "GNU GPL(General Public License)" 라이선스를 따르는 OS를 만들기 위해 시작한 프로젝트. GNU는 "GNU's Not UNIX"의 재귀적 약자.
- GCC는 원래 **GNU C Compiler**의 약자였으나, 현재는 여러 언어를 지원하면서 **GNU Compiler Collection**으로 의미가 확장되었다.
- 1987년 최초 릴리스.
- 버전 확인: `gcc --version`

## 2. 컴파일 파이프라인 (GCC 내부 구성 요소)

GCC는 사실 아래 4개 도구를 순서대로 호출하는 드라이버 프로그램이다.

| 단계 | 도구 | 입력 → 출력 | 역할 |
|---|---|---|---|
| 전처리 | `cpp` | `program.c` → `program.i` | C 전처리기 |
| 컴파일 | `cc1` | `program.i` → `program.s` | C 컴파일러 본체 (어셈블리 생성) |
| 어셈블 | `as` | `program.s` → `program.o` | 어셈블러 (ELF 재배치 가능 오브젝트 생성) |
| 링크 | `ld` | `program.o` → `program` | 링크 에디터 (ELF 실행 파일 생성) |

- 설치(Ubuntu 기준): `sudo apt-get install gcc`
- 환경 확인: `uname -orm` → 커널/아키텍처 확인 (예: `x86_64 GNU/Linux`)

## 3. 자주 쓰는 옵션

### `-o` : 출력 파일 이름 지정
```
$ gcc hello.c            # ./a.out 생성 (기본값)
$ gcc hello.c -o hello   # ./hello 생성
```

### 에러 메시지 표준 형식
```
파일명:줄번호:칼럼번호: 종류: 메시지
```
- 줄 번호(첫 번째 정수) = 파일 내 라인, 칼럼 번호(두 번째 정수) = 그 라인 내 위치.
- **Errors**: 컴파일 자체를 불가능하게 만드는 문제. 파일명·줄번호와 함께 보고됨.
- **Warnings**: 컴파일은 진행되지만 의심스러운 코드에 대한 경고. `warning:` 문구로 에러와 구분. GNU C/C++의 비표준 기능 사용 시에도 발생할 수 있음.

### `-w`, `-Wall`, `-Werror` : 경고 제어
- `-w`: 모든 경고 메시지 억제.
- `-Wall`: 유용한 경고를 모두 활성화 (미사용 변수 `-Wunused-variable`, 초기화되지 않은 변수 사용 `-Wuninitialized` 등). **항상 사용을 권장**하는 옵션.
- `-Werror`: 모든 경고를 에러로 승격시켜 컴파일을 중단시킴.

### `-On` (n=0,1,2,3) : 최적화 레벨
| 옵션 | 설명 |
|---|---|
| `-O0` (기본값) | 최적화 없음. 컴파일 시간 단축, 디버깅 결과가 소스코드와 정확히 일치 |
| `-Og` | (gcc 4.8+) 디버깅 친화적인 최적화. 최적화 학습용으로도 사용 |
| `-O1` (`-O`) | `-O0`보다 작고 빠른 실행 파일 생성 |
| `-O2` | `-O1`의 최적화 + 추가 최적화 |
| `-O3` | `-O2`의 모든 최적화 + 더 비용이 큰(aggressive) 최적화 |

- 최적화 레벨이 높을수록 실행은 빨라지지만 컴파일 시간이 늘고 디버깅이 어려워질 위험이 있음.
- 예: `gcc -O1 -o hello hello.c`, `gcc -c -Og hello.c`

### `-gn` (n=1,2,3) : 디버깅 정보 생성
- `-g`(=`-g2`) 이상, 또는 `-g3`(`-ggdb3`)을 사용하면 소스 줄 번호와 심볼 정보가 실행 파일에 포함되어 디버거가 **소스 라인 ↔ 기계어 주소**를 매핑할 수 있게 된다.
- `-ggdb3`으로 컴파일하면 매크로 정의(예: `#define MAX 256`)까지 gdb에서 확인 가능.
```
$ gcc -o hello test.c            # 디버깅 정보 없음
$ gcc -g -o hello_d test.c       # 기본 디버깅 정보
$ gcc -ggdb3 -o hello_d2 test.c  # 매크로까지 포함한 최대 디버깅 정보
```
- 디버깅 정보를 추가할수록 실행 파일 크기가 커진다 (강의 예시: 8608B → 9632B → 29416B).

#### 참고: `ls -al` 파일 권한 표기
- `-rwxr-xr-x` (8진수 755) 형태로 표시: 파일 종류 + 소유자(u)/그룹(g)/기타(o) 권한.
- 파일 타입 문자: `-` 일반 파일, `d` 디렉터리, `l` 심볼릭 링크, `b` 블록 장치, `c` 캐릭터 장치, `p` FIFO, `s` 소켓.

### `-Dname[=definition]` : 매크로 정의
- 컴파일 시점에 매크로를 정의할 수 있다. 소스 안에 `#ifdef`로 조건부 컴파일을 구성해두면, 커맨드라인에서 빌드 옵션에 따라 다른 코드를 활성화할 수 있다.
```c
#ifdef DEBUG_TEST
    printf("test\n");
    test();
#else
    test();
#endif
```
```
$ gcc -DDEBUG_TEST test.c
$ ./a.out
test    # DEBUG_TEST 매크로가 정의되어 printf 실행됨
```

### `-std=VER` : C 언어 표준 버전 지정
| 표준 | 연도 | 비고 |
|---|---|---|
| C89 | 1989 | ANSI 최초 공식 표준 |
| C90 | - | C89와 동일 내용의 ISO 버전 |
| C99 | 1999 | ISO |
| C11 | 2011 | ISO |
| C17 | 2017 | C11의 결함 수정 (새 기능 없음). `__STDC_VERSION__` 값이 `201710`으로 증가 |

- 예: `gcc -std=c11 test.c`
- 프로그램에서 `__STDC_VERSION__` 매크로로 적용된 표준 버전을 런타임에 확인 가능 (C11 → `201112`, 기본/C17 → `201710`).

## 요약 체크리스트
- 컴파일 파이프라인: `cpp → cc1 → as → ld` (전처리 → 컴파일 → 어셈블 → 링크)
- 실무에서는 항상 `-Wall`로 경고를 켜두고, 디버깅 시엔 `-g`(또는 `-ggdb3`)를 추가하는 것이 좋은 습관.
- 최적화(`-O`)와 디버깅 편의성은 트레이드오프 관계 → 개발 중엔 `-O0`/`-Og`, 배포 시 `-O2`/`-O3`.
