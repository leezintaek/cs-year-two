# GDB (GNU Debugger)

**과목**: CSE3209 System Programming
**출처**: GNU_study/pdf/GNU gdb (1).pdf, https://www.gnu.org/software

## 1. 디버깅의 기본 개념

- **버그(bug)**: 컴퓨터 프로그램/시스템이 잘못되거나 예기치 않은 결과를 내게 만드는 오류.
- **디버깅(debugging)**: 소프트웨어/시스템에서 버그를 찾아 해결하는 과정. 버그는 다른 함수·모듈로 전파되어 더 복잡한 문제를 일으킬 수 있으므로, 가능한 한 빨리 찾아 고치는 것이 목표.
- 일화: "세계 최초의 컴퓨터 버그"는 하버드 대학 Mark II 컴퓨터에서 발견된 나방(moth)이었고, 이를 제거(remove)한 것이 문자 그대로 "de-bug"의 유래.

## 2. 디버거(Debugger)란

- 소스 코드를 조사·디버깅하기 위한 도구.
- **동적 분석(Dynamic analysis)**: 프로그램을 실제로 실행하며 동작을 관찰 (↔ 코드를 실행하지 않고 분석하는 **정적 분석**).
- 주요 기능:
  1. 프로그램을 시작하고, 지정한 조건에서 멈추게 함 (breakpoint)
  2. 실행을 제어함 (step, next, continue 등)
  3. 멈춘 시점의 상태(변수, 스택 등)를 조사함

## 3. 디버깅 4단계

1. **Test**: 다양한 입력으로 테스트
2. **Stabilize**: 특정 에러를 재현 가능하게 만듦
3. **Localize**: 에러의 원인 위치를 좁혀나감 (파일명·줄번호까지)
4. **Correction**: 결함 자체를 수정

> 버그 재현과 위치 파악(localize)이 문제 해결의 **90%**를 차지한다는 경험칙이 있다.

### 흔한 버그 유형 (경고를 켜면 일부는 잡히지만 전부는 아님)
- `switch` 문에서 `break` 누락 → fall-through
- 초기화하지 않은 변수 사용 (`int i; ... scanf("%d", i);` — `&` 누락도 대표적 실수)
- `if (i = 5)` 처럼 비교(`==`) 대신 대입(`=`) 사용
- `if (i & j)` 처럼 논리 연산자(`&&`) 대신 비트 연산자(`&`) 사용

## 4. GDB 시작하기

1. 디버깅 정보를 포함해 빌드: `gcc -g hello.c -o hello`
2. gdb 실행: `gdb hello`
3. gdb 진입 시 프로그램은 아직 실행되지 않은 상태 → `run` 명령으로 실행 시작.
4. 보통 `run` 전에 **breakpoint**를 설정해둔다.
5. breakpoint에서 멈추면 `print`/`x`/`display`로 변수를 조사할 수 있다.
6. `kill`로 실행 중단, `quit`으로 gdb 종료.

## 5. 주요 GDB 명령어

| 명령 | 설명 |
|---|---|
| `break place` (`b`) | `place`(함수명 또는 줄번호)에 브레이크포인트 설정. 예: `break main`, `break 8` |
| `info b` | 설정된 모든 브레이크포인트 확인 |
| `run [args]` (`r`) | 프로그램 실행 시작 (인자 전달 가능) |
| `next` (`n`) / `nexti` | 현재 줄(명령)을 실행하고 다음 줄로 이동 (함수 호출은 **건너뜀**) |
| `step` (`s`) / `stepi` | 현재 줄이 함수 호출이면 그 **함수 내부로 진입** |
| `print E` (`p`) | 변수/표현식 `E`의 값 출력 |
| `continue` (`c`) | 다음 브레이크포인트까지 계속 실행 |
| `delete N` (`d N`) | 번호 `N`인 브레이크포인트 삭제 |
| `finish` | 현재 스택 프레임(함수)을 끝까지 실행하고 호출자로 복귀 |
| `backtrace` (`bt`) | 현재까지의 콜스택(스택 프레임) 출력 |
| `up` / `down` | 콜스택에서 상위/하위 프레임으로 이동 |
| `list [file:]num` (`l`) | 지정 위치 주변 소스코드 출력 (기본: 다음 10줄) |
| `list -` | 이전 10줄 출력 |
| `info source` | 현재 소스 파일명 확인 |
| `info args` / `info locals` | 현재 프레임의 인자 / 지역변수 확인 |
| `kill` | 디버깅 중인 프로그램 종료 |
| `quit` (`q`) | gdb 종료 |

### 조건부 브레이크포인트
```
(gdb) break prime.c:7 if k >= 9   # k>=9일 때만 정지 (C 문법 사용, ==와 = 주의)
(gdb) cond 2 k >= 15              # 이미 설정된 2번 브레이크포인트에 조건 재설정
(gdb) ignore 2 10                 # 2번 브레이크포인트를 10번 무시
(gdb) advance 19                  # 19번 줄까지 실행 후 정지
```

## 6. 실전 예제: Matloff 소수 판별 프로그램 디버깅

`main.c`(입력 받아 소수 판별 반복 호출) + `prime.c`/`prime.h`(소수 판별 로직) 구조.

### 버그 ①: Segmentation Fault (주소 누락)
- `scanf("%d", upper_bound);` → `upper_bound`가 값 그 자체를 주소처럼 취급해 잘못된 메모리에 접근 → **Segmentation fault**(할당되지 않았거나 접근 권한이 없는 메모리에 접근할 때 발생).
- `gdb ./matloff` → `run` → SIGSEGV 발생, `backtrace`로 콜스택 확인:
  ```
  #0 _IO_vfscanf_internal (...) at vfscanf.c:1902
  #1 __isoc99_scanf (...) at isoc99_scanf.c:37
  #2 main () at main.c:15
  ```
- 라이브러리 내부(`vfscanf`)가 아니라 **호출부(main.c:15)**가 원인일 가능성이 높음 → `list main.c:15`로 확인.
- **수정**: `scanf("%d", &upper_bound);` (주소 연산자 `&` 추가)

### 버그 ②: 배열 범위 초과 (out of bounds)
- 재실행 후 `check_prime()` 내부 `prime.c:9`에서 다시 SIGSEGV.
- `print j` → `j = 147328` (비정상적으로 큰 값) → `while(1)` 무한 루프 안에서 `j++`가 루프 탈출 조건 없이 계속 증가하며 배열 범위를 넘어섬.
- **수정**: `while(1)` 대신 `for(j = 2; j*j <= k; j++)`로 탈출 조건을 명시 (나눗셈 확인은 `sqrt(k)`까지면 충분).

### 버그 ③: 논리 오류 (9, 15가 소수로 잘못 판정됨)
- 세그폴트는 사라졌지만 9, 15 같은 합성수가 소수로 출력되는 **논리적 버그** 발생.
- `break main`, `next`/`step`(함수 내부 진입), `bt`(콜스택), `info args`/`info locals`(인자·지역변수 확인)로 흐름을 추적.
- `finish`로 현재 함수 실행을 마치고 호출자로 복귀하며 값을 확인.
- 원인: 반복문 리팩터링 과정에서 `j++`가 주석 처리되어 있었음(무한 루프 방지용 `for`문으로 바꿨지만 증가식이 중복 제거되지 않음) → 조건부 브레이크포인트(`break prime.c:7 if k >= 9`)와 `advance`/`continue`로 반복 확인 후 수정.

## 7. 기타 유용한 기능

- **GDB TUI(Text User Interface)**: 소스/어셈블리를 화면 분할로 보여주는 모드.
  ```
  $ gdb -tui a.out
  (gdb) layout split      # 화면 분할
  (gdb) focus cmd         # 포커스를 cmd/asm/src 중 하나로 전환
  (gdb) disp /bt &x       # 특정 주소를 반복적으로 출력하도록 등록
  (gdb) p sizeof(x)       # 표현식 결과 출력
  ```
  - `ctrl-x`, `ctrl-a`: TUI 전환 단축키. `ctrl-l`: 화면 새로고침.
- **[선택] 저수준 시스템 프로그래밍용 GDB 확장 플러그인**: 순정 GDB는 로우레벨 분석(리버싱/시스템 해킹)에 불편하므로 아래와 같은 플러그인을 사용하기도 함.
  - `gef` (https://github.com/hugsy/gef)
  - `peda` (https://github.com/longld/peda)
  - `pwngdb` (https://github.com/scwuaptx/Pwngdb)
  - `pwndbg` (https://github.com/pwndbg/pwndbg) — 저수준 SW 개발자·하드웨어 해커를 위한 기능에 특화. Ubuntu 18.04/20.04/22.04 + GDB 8.1 이상 지원.
    ```
    git clone https://github.com/pwndbg/pwndbg
    cd pwndbg
    ./setup.sh
    ```

## 요약 체크리스트
- 디버깅은 `-g`(또는 `-ggdb3`) 옵션으로 빌드하는 것에서 시작.
- `break` → `run` → (정지 시) `print`/`list`/`bt` → `next`/`step`/`continue`/`finish` 순환이 기본 루틴.
- Segmentation fault 발생 시 `backtrace`로 콜스택을 보고, 라이브러리 함수보다 **내 코드의 호출 지점**을 먼저 의심할 것.
- 조건부 브레이크포인트(`break ... if ...`)와 `ignore`, `advance`는 반복문 안 특정 조건에서만 멈추고 싶을 때 유용.
