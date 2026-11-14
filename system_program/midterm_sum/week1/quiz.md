# No. 1 System Programming Quiz — Chapter 1. A Tour of Computer Systems

## §1. Information Is Bits + Context
- 소스 파일의 각 문자는 ASCII 표준에 따라 1바이트 정수로 저장된다.
- ASCII 문자로만 이루어진 파일은 text file, 그 외는 binary file.

### Q1) hello.c의 첫 바이트들
`hello.c`의 첫 4바이트를 `xxd`로 확인한 결과이다. 원래 문자는? (ASCII: '#'=35, 'c'=99, 'i'=105, 'n'=110)
```
$ xxd -l 4 hello.c
00000000: 2369 6e63
```
- 0x23 0x69 0x6e 0x63 → `__ __ __ __`
- hello.c는 (text / binary) file이고, hello.o는 (text / binary) file이다.

## §2. Compilation System
- hello.c → [cpp] → hello.i → [cc1] → hello.s → [as] → hello.o → [ld] → hello

### Q2) 단계별 명령어와 출력 파일
| 명령어 | 수행 단계 | 출력 파일 | text/binary |
|---|---|---|---|
| `gcc -E hello.c -o hello.i` | ________ | hello.i | ____ |
| `gcc -S hello.c` | ________ | ________ | ____ |
| `gcc -c hello.c` | ________ | ________ | ____ |
| `gcc -o hello hello.c` | ________ (최종) | hello | ____ |

### Q3) Linker의 두 가지 역할
```c
#include <stdio.h>
int main() { printf("hello, world\n"); return 0; }
```
- `printf` 같은 외부 참조를 실제 정의와 연결하는 작업: ________________
- 상대 주소를 조정하여 하나의 실행 파일로 합치는 작업: ________________
- 리눅스 실행 파일의 표준 포맷 이름: ________ (확인 명령: `readelf -h hello`)

## §3. Hardware Organization & Memory
### Q4) 레지스터의 필요성
`F = (X+Y) - (X*Y)` 를 계산할 때 (X, Y는 메모리에 있고 F도 메모리에 저장)
- 레지스터 없이 매 연산마다 메모리에서 load/store 할 경우 메모리 접근 횟수: ____
- 레지스터를 사용할 경우 메모리 접근 횟수: ____

## §4. Caches Matter
### Q5) 접근 패턴과 성능
```c
int src[2048][2048], dst[2048][2048];
void copyij() {                       void copyji() {
  for (i = 0; i < 2048; i++)            for (j = 0; j < 2048; j++)
    for (j = 0; j < 2048; j++)            for (i = 0; i < 2048; i++)
      dst[i][j] = src[i][j];                dst[i][j] = src[i][j];
}                                     }
```
- 더 빠른 함수: ________ (이유: C 배열은 ________-major 순서로 저장되어 ________ 친화적)
- 캐시로 사용되는 메모리 종류: ________ / 주기억장치로 사용되는 메모리 종류: ________

---
## 정답
- Q1) `# i n c` / text / binary
- Q2) 전처리(text) / 컴파일, hello.s(text) / 어셈블, hello.o(binary) / 링킹(binary)
- Q3) Symbol Resolution / Relocation / ELF
- Q4) 9 / 3
- Q5) copyij, row, cache / SRAM, DRAM
