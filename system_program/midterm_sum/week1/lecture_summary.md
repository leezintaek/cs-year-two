# Week 1 — A Tour of Computer Systems

**과목**: CSE3209 System Programming (2026 가을)
**교재**: Computer Systems, 3rd Edition (Bryant), Chapter 1

## 1. 정보는 비트 + 문맥 (Information Is Bits + Context)

- 소스 파일(`hello.c`)은 문자 하나하나가 고유한 정수 값(바이트)으로 매핑되어 저장된다.
- 대부분의 현대 시스템은 텍스트 문자를 **ASCII** 표준으로 표현한다.
- `hello.c`처럼 ASCII 문자로만 이루어진 파일을 **텍스트 파일**이라 하고, 그렇지 않은 파일을 **바이너리 파일**이라 한다.

## 2. 컴파일 시스템의 동작 (How Compilation Systems Work)

GCC(GNU Compiler Collection)는 `hello.c` → 실행 파일 `hello`가 되기까지 4단계를 거친다.

```
hello.c → [전처리기 cpp] → hello.i → [컴파일러 cc1] → hello.s → [어셈블러 as] → hello.o → [링커 ld] → hello
  (텍스트)                    (텍스트)                  (텍스트)                  (바이너리)              (바이너리)
```

### Step 1: 전처리 (Preprocessing)
- 전처리기(`cpp`)가 `#`으로 시작하는 지시문(directive)에 따라 원본 C 프로그램을 수정한다.
- 예: `#include <stdio.h>` → `/usr/include`의 `stdio.h` 내용을 그대로 프로그램 텍스트에 삽입.
- `#define`(매크로 치환), `#ifdef`/`#else`/`#endif`(조건부 컴파일)도 이 단계에서 처리된다.
- 명령: `gcc -E test.c -o test.i`

### Step 2: 컴파일 (Compilation)
- 컴파일러가 `hello.i`를 사람이 읽을 수 있는 **어셈블리어**(`hello.s`)로 번역한다.
- 어셈블리 명령어 하나는 저수준 기계어 명령어 하나에 정확히 대응된다.
- C 컴파일러든 Fortran 컴파일러든 동일한 어셈블리어로 출력 가능.
- 명령: `gcc -S test.c`

### Step 3: 어셈블리 (Assembly)
- 어셈블러(`as`)가 `hello.s`를 기계어 명령으로 번역해 오브젝트 파일 `hello.o`(바이너리)에 저장한다.
- 오브젝트 파일은 완전한 프로그램이 아니므로 그 자체로는 실행 불가능(다른 파일/라이브러리의 함수·변수 참조를 포함할 수 있음).
- 이 단계에서 어셈블러는 **심볼 테이블**(이름, 타입, 주소, bind, size)을 생성하며, 이 테이블은 이후 링킹 단계에서 사용된다.
- 오브젝트 파일 내용 확인 도구: `objdump`, `nm`, `readelf`
- 명령: `gcc -c test.c`, `objdump -d test.o`(디스어셈블), `objdump -t test.o`(심볼 테이블)

### Step 4: 링킹 (Linkage)
- 링커(`ld`)는 여러 오브젝트 파일을 입력받아
  1. **심볼 해결(Symbol Resolution)**: 외부 참조(예: `printf`)를 실제 정의와 연결
  2. **재배치(Relocation)**: 상대 주소를 조정하고 하나로 결합
  하여 최종 실행 가능한 오브젝트 파일(**ELF**)을 만든다.
- **ELF(Executable and Linkable Format)**: 리눅스에서 오브젝트 파일의 표준 바이너리 포맷.
- 명령: `gcc -o hello test.c`, `readelf -h hello`(ELF 헤더 확인)

## 3. hello 프로그램 실행 (Running the hello Program)

- **셸(shell)**은 명령줄 인터프리터로, 프롬프트를 출력하고 사용자의 명령 입력을 기다린다.
- 입력한 명령의 첫 단어가 **내장 명령(built-in)**이 아니면, 셸은 이를 **외부 명령(external command)**으로 간주해 디스크에서 적재한다.
- `./hello` 실행 시, 실행 파일 데이터가 보조기억장치(디스크)에서 주기억장치(메모리)로 이동한 뒤 CPU가 `main` 루틴의 기계어 명령을 실행하기 시작한다.

### 하드웨어 구성 (HW Organization of a Typical System)
- **CPU**: 레지스터 파일, ALU, PC(Program Counter), 캐시(SRAM)로 구성.
- **버스**: 시스템 버스(Front Side Bus), 메모리 버스, I/O 버스가 CPU–메모리–I/O 장치를 연결.
- **I/O 장치**: USB 컨트롤러, 그래픽 어댑터, 디스크 컨트롤러 등이 I/O 버스에 연결.
- CPU가 실행하는 모든 명령은 메모리 접근을 필요로 한다.

### 컴포넌트별 접근 시간 비교 (2GHz 기준 정규화)
| 컴포넌트 | 실제 시간 | 정규화(1사이클=1초 기준) |
|---|---|---|
| 프로세서 사이클 | 0.5 ns | 1초 |
| 캐시 접근 (SRAM) | 2 ns | 4초 |
| 메모리 접근 (DRAM) | 15 ns | 30초 |
| 디스크 I/O 접근 | 7,000,000 ns (7ms) | 162일 |

→ 디스크 접근은 CPU 사이클보다 약 **1,000만 배** 느리다.

## 4. 프로세서 (Processor)

- **CPU**: ALU, 제어 장치(control unit), 레지스터를 이용해 명령어 집합(instruction set)을 수행하는 하드웨어.
- **ALU**: 산술 연산과 논리 비교 수행.
- **멀티프로세서**: 하나의 칩에 여러 코어가 있고, 각 코어는 여러 레벨의 대용량 메모리 캐시를 가짐.
- CPU 클럭 속도와 소비 전력은 세대에 따라 증가해오다 발열 문제로 최근에는 코어 수를 늘리는 방향으로 발전.

## 5. 프로세서의 반복 실행 (Processor repeatedly executes the instruction)

- CPU는 시작부터 종료까지 명령어 시퀀스를 하나씩 읽고 실행(해석)하는 일만 한다.
- 이 시퀀스를 CPU의 **제어 흐름(control flow)**이라 한다.
- 사이클: 명령어 인출(fetch) → 명령어 해독(decode) → 실행(execution) → 읽기/쓰기(read/write) → PC 갱신, 인터럽트 요청 시 인터럽트 핸들러 주소로 PC 이동.

### 메모리 종류
- **SRAM (Static RAM)** → 캐시로 사용. 밀도 낮음(비트당 6개 트랜지스터), 비쌈, 빠름(~2ns), refresh 불필요.
- **DRAM (Dynamic RAM)** → 주기억장치로 사용. 트랜지스터/커패시터 쌍(비트당 1개), 밀도 높음, SRAM보다 느림(~15ns), 주기적 refresh 필요.
- **휘발성(Volatile)**: 전원이 꺼지면 정보 소실 (SRAM, DRAM).
- **비휘발성(Nonvolatile)**: 전원이 꺼져도 정보 유지 (Flash Memory).

### 레지스터가 필요한 이유
- 레지스터는 CPU 내부에 있는 초고속 메모리 단위.
- 예: `F = (X+Y) - (X*Y)`를 레지스터 없이 계산하면 ADD/MUL/SUB 각 단계마다 메모리 load/store가 필요해 총 9번의 메모리 접근이 발생.
- 레지스터를 사용하면 단 3번의 메모리 접근만으로 처리 가능.

## 6. 캐시의 중요성 (Caches Matter)

- 명령어/데이터 흐름: 디스크(원본 저장) → 메모리(프로그램 로드 시 복사) → 프로세서(실행 중 복사).
- 문제점: 시스템은 정보를 한 곳에서 다른 곳으로 옮기는 데 많은 시간을 쓴다 (복사 자체가 오버헤드).
- 해결책: 자주 접근하는 데이터를 캐시에 저장해 대부분의 메모리 연산을 빠른 캐시로 처리.
- 계층 구조 예 (Intel Core i7): 코어별 L1 d-cache/i-cache → L2 unified cache → 코어 전체가 공유하는 L3 unified cache → 메인 메모리.
- **접근 패턴이 성능을 좌우한다**: 2048×2048 배열 복사 시 `for(i) for(j)` 순서(행 우선, 캐시 친화적)는 4.3ms, `for(j) for(i)` 순서(캐시 비친화적)는 81.8ms 소요 (2.0GHz Intel Core i7 기준) — 약 19배 차이.

## 7. 하드디스크 드라이브 (HDD)

- 자기 저장 매체의 일종, **비휘발성** 장치(전원이 꺼져도 데이터 유지).
- 컴퓨터 데이터 저장에 널리 사용되며, 읽기/쓰기 1회에 5~35ms 소요 (메모리보다 훨씬 느림).
- 유사한 자기 저장 매체: 플로피 디스크, 자기 테이프, 신용카드 마그네틱 선.

## 참고: 이 과목(SP)의 커버리지 (Road map)

CS:APP 교재 기반 5개 과목(ORG, ORG+, ICS, ICS+, SP) 중 System Programming(SP)은 다음 챕터를 다룬다:
- Ch.1 시스템 개관, Ch.3 기계어, Ch.6 메모리 계층(하드웨어만), Ch.7 링킹, Ch.8 예외적 제어 흐름, Ch.9 가상 메모리, Ch.10 시스템 레벨 I/O, Ch.11 네트워크 프로그래밍, Ch.12 동시성 프로그래밍.
(Ch.2 데이터 표현은 부분적으로만 다룸 — 부동소수점 제외)
