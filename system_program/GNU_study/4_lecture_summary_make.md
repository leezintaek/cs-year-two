# Make와 Makefile 강의 요약

> 출처: `pdf/GNU make (1).pdf` (CSE3209 System Programming)
> 💡 표시가 붙은 부분은 강의자료에 없거나 부족해서 보충한 내용입니다.

---

## 1. Make란?

- **build automation tool** (빌드 자동화 도구)
- 큰 프로그램에서 **어떤 부분을 다시 컴파일해야 하는지 자동으로 판단**
- 1970년대 Bell Lab에서 만들어졌고, 지금도 Linux 커널 빌드 등 대부분 프로젝트의 핵심 엔진

### Make가 없다면?
```bash
$ gcc -Wall -c sum.c
$ gcc -Wall -c main.c
$ gcc -Wall -o sum main.o sum.o
```
- 파일이 많아지면 명령이 길어지고 관리가 어려움
- 파일 하나만 바꿔도 **전부 다시 컴파일**해야 함
- 예: Mozilla 소스 트리 = 파일 26,000개, 하위 디렉터리 2,500개, 파일 형식 240종
  → 빌드 과정과 의존성(dependency)을 어떻게 관리할 것인가?

---

## 2. make 명령과 Makefile

- **make 명령** : Makefile을 읽고 프로젝트 구조를 파악해 실행 파일을 만듦
- **Makefile** : 다음 내용을 담은 스크립트
  - 프로젝트 구조와 **파일 간 의존 관계**
  - 각 파일을 만드는 **명령**
- 의존 관계는 **트리(dependency tree)** 로 표현 가능

### 예: main.c, sum.c, sum.h (sum.h는 두 .c 파일 모두에 include)

```
              sum (실행 파일)
             /              \
        main.o              sum.o
        /    \              /    \
    main.c  sum.h       sum.c  sum.h
```

```makefile
sum: main.o sum.o
	gcc -o sum main.o sum.o

main.o: main.c sum.h
	gcc -c main.c

sum.o: sum.c sum.h
	gcc -c sum.c
```

---

## 3. 규칙(Rule)의 문법

Makefile은 **규칙(rule)** 들로 이루어집니다.

```makefile
target: prerequisites      ← Dependency line (의존성 줄)
<TAB>command1              ← Recipe (명령)
<TAB>command2
```

| 구성 요소     | 의미                                       |
| ------------- | ------------------------------------------ |
| target        | 만들 파일 (또는 작업 이름)                 |
| prerequisites | target을 만드는 데 필요한 파일들           |
| recipe        | target을 만드는 명령 (반드시 TAB 들여쓰기) |

- recipe의 각 줄은 **별도의 셸(bash)** 에서 실행됨

💡 **자주 하는 실수**
- recipe 앞을 **공백(space)** 으로 들여쓰면 `*** missing separator. Stop.` 에러가 납니다. 반드시 **TAB** 문자여야 합니다. (vi에서 `:set list`로 탭이 `^I`로 보이는지 확인 가능)
- 각 줄이 별도 셸에서 실행되므로 아래 코드는 의도대로 동작하지 않습니다.
  ```makefile
  wrong:
  	cd subdir
  	ls          # subdir가 아니라 원래 디렉터리에서 실행됨
  right:
  	cd subdir && ls
  ```
- 명령 앞에 `@`를 붙이면 명령 자체는 출력되지 않고 결과만 보입니다 (예: `@echo done`).
- 명령 앞에 `-`를 붙이면 그 명령이 실패해도 make가 멈추지 않습니다 (예: `-rm *.o`).

---

## 4. make가 Makefile을 처리하는 방법

1. `make`만 입력하면 현재 디렉터리의 Makefile을 읽음
   - 💡 찾는 순서: `GNUmakefile` → `makefile` → `Makefile`. 다른 파일은 `make -f 파일명`
2. **첫 번째 규칙의 target = default goal** (예: `sum`)
3. goal의 prerequisites를 따라 트리 아래로 내려가며 다시 만들어야 할 target이 있는지 확인
4. **파일 수정 시각(modification time)을 비교**
   - target이 prerequisite 중 **하나라도 더 오래되었으면** recipe로 다시 생성
   - 그 결과 다른 target도 연쇄적으로 다시 만들어질 수 있음
5. goal이 의존하지 않는 규칙(예: `clean`)은 처리하지 않음

### 예: 수정 시각 비교

| 파일   | 수정 시각 |
| ------ | --------- |
| sum    | 10:03     |
| main.o | 09:56     |
| sum.o  | 09:35     |
| main.c | 10:45     |
| sum.c  | 09:14     |
| sum.h  | 08:39     |

- `main.c`(10:45)가 `main.o`(09:56)보다 새로움 → `main.o` 재컴파일
- 그러면 `main.o`가 `sum`보다 새로워짐 → `sum` 재링크
- `sum.o`는 `sum.c`, `sum.h`보다 새로우므로 그대로

```
$ make
gcc -c main.c
gcc -o sum main.o sum.o
```

💡 시간 비교 방식이라 **수정 시각이 과거로 유지되면 실패**합니다 (예: 다른 곳에서 오래된 파일을 복사해 온 경우, 시스템 시계가 틀린 경우). 또한 Makefile에 헤더 의존성(`sum.h`)을 빠뜨리면 헤더를 바꿔도 재컴파일되지 않으니 주의하세요.

---

## 5. 실습 1: Makefile 작성

```c
// sum.h
int sum(int a, int b);

// sum.c
#include "sum.h"
int sum(int a, int b) { return a + b; }

// main.c
#include <stdio.h>
#include "sum.h"
int main() {
    printf("[%s] in %s:%d \n", __FILE__, __func__, __LINE__);
    printf("sum: %d", sum(1, 2));
    return 0;
}
```
```bash
$ make
gcc -c main.c
gcc -c sum.c
gcc -o sum main.o sum.o
$ ./sum
[main.c] in main:5
sum: 3
```

💡 `__FILE__`(파일 이름), `__LINE__`(줄 번호)는 전처리기가 제공하는 **predefined macro**이고, `__func__`(함수 이름)는 C99부터 지원하는 **predefined identifier**입니다. 간단한 printf 디버깅에 유용합니다.

---

## 6. 실습 2: touch

```bash
$ make
make: 'sum' is up to date.   # 바뀐 게 없으므로 아무것도 안 함
$ touch sum.c                # sum.c의 수정 시각을 현재로 갱신
$ make
gcc -c sum.c                 # sum.c만 다시 컴파일
gcc -o sum main.o sum.o
$ make sum.o                 # 특정 target만 만들기
```

💡 **보충 (슬라이드 설명 정정)**
슬라이드에는 touch를 "target을 실제로 바꾸지 않고 최신 상태로 표시"한다고 적혀 있지만, 이는 `make -t`(`--touch`) 옵션의 설명입니다.
- `touch 파일` (셸 명령) : 파일 내용은 그대로 두고 **수정 시각만 현재로** 갱신 (파일이 없으면 빈 파일 생성) → make는 그 파일이 바뀐 것으로 판단해 **다시 빌드**
- `make -t` : recipe를 실행하지 않고 target들의 시각만 갱신 → **빌드한 것처럼** 표시

---

## 7. Phony Target

**실제 파일 이름이 아닌 target** (작업 이름).

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
```bash
$ make clean          # 빌드 결과물 삭제
$ make everything     # clean 후 backup 실행
```

- `rm`은 `clean`이라는 파일을 만들지 않으므로 `clean` 파일은 존재하지 않음
- recipe가 target 파일을 만들지 않으면 → **호출할 때마다 매번 실행됨**

💡 **`.PHONY` 선언 (꼭 알아둘 것)**
만약 디렉터리에 진짜로 `clean`이라는 파일이 생기면, make는 "clean은 prerequisite가 없고 이미 존재하니 최신"이라고 판단해 `make clean`이 동작하지 않습니다(`make: 'clean' is up to date.`). 이를 막으려면 다음과 같이 선언합니다.
```makefile
.PHONY: clean backup everything
```
관례적으로 `all`(전체 빌드, 보통 첫 번째 규칙), `clean`, `install` 등을 phony target으로 둡니다.

---

## 8. 변수(Variable, Macro)

- 변수 이름: `:`, `#`, `=`, 공백을 포함하지 않는 문자열
- 사용: `$(이름)` 또는 `${이름}`

```makefile
OBJECTS = main.o sum.o
TARGET  = sum
CC      = gcc
CFLAGS  = -Wall

$(TARGET): $(OBJECTS)
	$(CC) -o $(TARGET) $(OBJECTS)
	ls $(PWD)

main.o: main.c sum.h
	$(CC) -c main.c
sum.o: sum.c sum.h
	$(CC) -c sum.c

clean:
	rm $(TARGET)
	rm $(OBJECTS)
```

- `$(PWD)`처럼 **환경 변수**도 make 변수로 사용할 수 있음

💡 **보충**
- 슬라이드 예제는 `CFLAGS`를 정의만 하고 쓰지 않았습니다. 실제로 적용하려면 `$(CC) $(CFLAGS) -c main.c`처럼 recipe에 넣어야 합니다.
- 명령줄에서 덮어쓰기 가능: `make CFLAGS="-g -O0"`
- 대입 연산자 종류

| 연산자 | 의미                              |
| ------ | --------------------------------- |
| `=`    | 사용 시점에 값을 펼침 (recursive) |
| `:=`   | 정의 시점에 값을 확정 (simple)    |
| `?=`   | 아직 정의되지 않았을 때만 대입    |
| `+=`   | 기존 값 뒤에 추가                 |

- 셸 변수를 recipe에서 쓰려면 `$$`로 써야 합니다 (예: `echo $$HOME`). `$` 하나는 make가 먼저 해석합니다.

---

## 9. 자동 변수 (Automatic Variable)

규칙이 실행될 때마다 그 규칙의 target과 prerequisites에 따라 값이 정해지는 변수.

| 변수 | 의미                           |
| ---- | ------------------------------ |
| `$@` | target 이름                    |
| `$^` | 모든 prerequisites (중복 제거) |
| `$<` | 첫 번째 prerequisite           |
| `$?` | 💡 target보다 새로운 prereq    |

```makefile
$(TARGET): $(OBJECTS)
	$(CC) -o $@ $^          # gcc -o sum main.o sum.o

main.o: main.c sum.h
	$(CC) -c $<             # gcc -c main.c

sum.o: sum.c sum.h
	$(CC) -c $<             # gcc -c sum.c
```

💡 **패턴 규칙 (Pattern Rule)** — 자동 변수와 함께 쓰면 .c 파일이 늘어나도 규칙을 추가할 필요가 없습니다.
```makefile
CC      = gcc
CFLAGS  = -Wall -g
TARGET  = sum
OBJECTS = main.o sum.o

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c sum.h          # 모든 xxx.o는 xxx.c로부터
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f $(TARGET) $(OBJECTS)
```
- `rm -f`는 파일이 없어도 에러를 내지 않습니다.
- 사실 make에는 `.c → .o` **내장 규칙(implicit rule)** 이 있어서, `main.o: main.c sum.h`처럼 의존성만 써도 `$(CC) $(CFLAGS) -c`로 알아서 컴파일합니다.

---

## 10. 💡 유용한 make 옵션

| 옵션        | 의미                             |
| ----------- | -------------------------------- |
| `make 타겟` | 특정 target만 빌드               |
| `-f 파일`   | 다른 이름의 Makefile 사용        |
| `-n`        | 실행하지 않고 실행될 명령만 출력 |
| `-B`        | 모든 target을 무조건 다시 빌드   |
| `-j N`      | N개 작업을 병렬로 실행           |
| `-t`        | 빌드 없이 target 시각만 갱신     |
| `-C dir`    | dir로 이동한 뒤 make 실행        |
