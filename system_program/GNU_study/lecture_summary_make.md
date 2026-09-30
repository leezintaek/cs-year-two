# Make and Makefile

**과목**: CSE3209 System Programming
**출처**: GNU_study/pdf/GNU make (1).pdf, https://www.gnu.org/software

## 1. Make란

- **빌드 자동화 도구(build automation tool)**: 빌드 프로세스를 관리하는 데 사용됨.
- 대규모 프로그램에서 **어떤 파일들을 다시 컴파일해야 하는지** 자동으로 판단해준다.
- 1970년대 Bell Lab에서 처음 만들어졌으며, 지금도 대부분의 프로그래밍 프로젝트(리눅스 커널 빌드 포함)에서 핵심 빌드 엔진으로 쓰이고 있다.
- 특히 Unix/Unix 계열 운영체제에서 널리 사용됨.

### Make 없이 빌드한다면?
```
$ gcc -Wall -c sum.c
$ gcc -Wall -c main.c
$ gcc -Wall -o sum main.o sum.o
```
- Mozilla처럼 **26,000개 파일, 2,500개 서브디렉터리, 240종 파일 타입**으로 이루어진 대형 소스 트리에서는:
  - 빌드 프로세스를 어떻게 제어할 것인가? (파일이 많으면 관리가 어려움)
  - 의존성을 어떻게 제어할 것인가? (매번 전체를 다시 컴파일하면 시간 낭비)
  → 이 두 문제를 해결하는 것이 Make의 목적.

## 2. Make 명령과 Makefile

- **`make` 명령**: `Makefile`을 읽어 프로젝트 구조를 파악하고 실행 파일을 만들어낸다.
- **`Makefile`**: 다음을 담고 있는 스크립트 파일.
  1. 파일 간 프로젝트 구조 및 의존 관계
  2. 파일 생성을 위한 명령들
- 프로젝트 구조는 **의존성 트리(dependency tree)**로 표현 가능.

### 예제: main.c, sum.c, sum.h → 실행 파일 sum
```makefile
sum: main.o sum.o
	gcc -o sum main.o sum.o

main.o: main.c sum.h
	gcc -c main.c

sum.o: sum.c sum.h
	gcc -c sum.c
```
- `sum.h`는 두 `.c` 파일 모두에 포함(include)되어 있음.

## 3. Makefile 규칙(Rule)의 문법

하나의 **규칙(rule)**은 다음으로 구성된다.

```
타깃(target): 전제조건(prerequisite1) 전제조건(prerequisite2) ...
<TAB>명령1
<TAB>명령2
```

- **Dependency(의존성) 라인**: 타깃 이름 + 콜론(`:`) + (선택적으로) 의존하는 파일/타깃들의 나열.
- **Recipe(레시피/액션)**: 파일 생성을 위한, **반드시 TAB으로 들여쓴** 명령줄들. 각 명령은 별도의 셸(bash)에서 실행됨.
- 예시의 첫 번째 규칙(`sum: main.o sum.o`)이 **기본 목표(default goal)**가 된다.

## 4. Make가 Makefile을 처리하는 방식

1. 기본적으로 make는 **첫 번째 타깃(default goal)**부터 시작한다. (`$ make`만 입력하면 이 타깃을 빌드)
2. 현재 디렉터리의 Makefile을 읽고 **첫 번째 규칙부터** 처리한다.
3. 목표(goal)가 의존하는 파일들을 트리를 따라 내려가며, 다시 생성(recreate)해야 하는 타깃이 있는지 확인한다.
   - 목표의 의존 파일로 등장하는 타깃들만 처리되며, 목표와 관련 없는 규칙은 처리되지 않는다.
4. **파일 수정 시각(modification time) 비교**로 타깃 재생성 여부를 결정한다.
   - 타깃이 의존 파일 중 하나보다 **오래된(older)** 경우, 레시피를 실행해 타깃을 다시 만든다.
   - 이로 인해 더 많은 파일이 연쇄적으로 재생성될 수 있다 (예: `main.o`가 갱신되면 → 그보다 오래된 `sum`도 재링크됨).
   - 한계: 파일의 수정 시각이 과거로 되돌아가면(예: 시스템 시간 오류) make가 오작동할 수 있음.

### 예시 (수정 시각 비교)
| 파일 | 최종 수정 시각 |
|---|---|
| sum | 10:03 |
| main.o | 09:56 |
| sum.o | 09:35 |
| main.c | 10:45 |
| sum.c | 09:14 |
| sum.h | 08:39 |

- `main.c`(10:45)가 `main.o`(09:56)보다 최신 → `main.o` 재컴파일 필요.
- `main.o`가 갱신되면 `sum`(10:03)보다 최신이 되므로 → `sum`도 재링크됨.

## 5. 실습 예제

### Exercise 1: 최초 빌드
```
$ ls
main.c Makefile sum.c sum.h
$ make
gcc -c main.c
gcc -c sum.c
gcc -o sum main.o sum.o
$ ./sum
[main.c] in main:5
sum: 3
```
(`__FILE__`, `__func__`, `__LINE__`은 각각 현재 파일명·함수명·줄번호를 나타내는 컴파일러 내장 매크로)

### Exercise 2: `touch`와 재빌드
```
$ make
make: 'sum' is up to date.   # 변경사항 없으면 아무 것도 하지 않음
$ touch sum.c                # sum.c의 수정 시각만 "지금"으로 갱신 (내용 변경 없음)
$ make
gcc -c sum.c
gcc -o sum main.o sum.o      # sum.c가 최신이므로 sum.o, sum만 재생성
```
- `touch`: 파일 내용은 바꾸지 않고 수정 시각만 최신으로 표시 → make가 해당 파일을 "변경됨"으로 간주하게 만드는 테스트 방법.

## 6. Phony Target (가짜 타깃)

- **실제 파일 이름이 아닌 타깃**. 예: `clean`은 `rm` 명령을 실행할 뿐 `clean`이라는 이름의 파일을 만들지 않는다.
- 레시피가 타깃과 동일한 이름의 파일을 생성하지 않는 규칙은, **호출될 때마다 매번 실행**된다 (수정 시각 비교 대상이 없으므로).

```makefile
sum: main.o sum.o
	gcc -o sum main.o sum.o
main.o: main.c sum.h
	gcc -c main.c
sum.o: sum.c sum.h
	gcc -c sum.c
clean:
	rm sum *.o
backup:
	cp main.c main_bak.c
	cp sum.c sum_bak.c
everything: clean backup
```
- `everything`처럼 여러 phony 타깃을 전제조건으로 나열해 한 번에 여러 단계를 실행할 수 있다.
- 참고: 실제 프로젝트에서는 `.PHONY: clean backup everything`을 선언해 make에게 이들이 파일이 아님을 명시하는 것이 일반적 관례(강의 슬라이드에는 없지만 실무에서 꼭 필요).

## 7. 변수(Variable, 매크로)

- 변수 이름: `:`, `#`, `=`, 공백을 포함하지 않는 임의의 문자열 (Makefile에서는 이를 **매크로**라고도 부름).
- 변수 참조: `$(변수명)` 형태로 괄호와 함께 사용.

```makefile
OBJECTS= main.o sum.o
TARGET= sum
CC= gcc
CFLAGS= -Wall

$(TARGET): $(OBJECTS)
	$(CC) -o sum main.o sum.o
	ls $(PWD)
main.o: main.c sum.h
	$(CC) -c main.c
sum.o: sum.c sum.h
	$(CC) -c sum.c
clean:
	rm $(TARGET)
	rm $(OBJECTS)
```
- 변수를 사용하면 컴파일러/옵션/파일 목록을 한 곳에서만 바꾸면 되므로 유지보수가 쉬워진다.

## 8. 자동 변수(Automatic Variable)

- 규칙이 실행될 때마다 **그 규칙의 타깃/전제조건 값에 따라 자동으로 계산되는 변수**.

| 자동 변수 | 의미 |
|---|---|
| `$@` | 현재 규칙의 **타깃** 이름 |
| `$^` | 현재 규칙의 **모든 전제조건** |
| `$<` | 현재 규칙의 **첫 번째 전제조건** |

```makefile
OBJECTS= main.o sum.o
TARGET= sum
CC= gcc
CFLAGS= -Wall

$(TARGET): $(OBJECTS)
	$(CC) -o $@ $^        # gcc -o sum main.o sum.o 와 동일
	ls $(PWD)
main.o: main.c sum.h
	$(CC) -c $<            # gcc -c main.c 와 동일 ($<는 main.c)
sum.o: sum.c sum.h
	$(CC) -c $<
clean:
	rm $(TARGET)
	rm $(OBJECTS)
```
- 자동 변수를 사용하면 타깃/전제조건 이름이 바뀌어도 레시피를 수정할 필요가 없어 **일반화된(generic)** 규칙을 작성할 수 있다.

## 요약 체크리스트
- `make`는 파일 **수정 시각**을 비교해 다시 빌드해야 할 대상만 골라 다시 빌드 → 대형 프로젝트의 빌드 시간을 크게 줄여준다.
- 규칙 = `타깃: 전제조건` + TAB으로 들여쓴 레시피.
- `clean`, `backup`처럼 실제 파일을 만들지 않는 타깃은 phony target이며 항상 재실행됨.
- 변수(`$(VAR)`)와 자동 변수(`$@`, `$^`, `$<`)를 조합하면 Makefile을 훨씬 간결하고 재사용 가능하게 작성할 수 있다.
