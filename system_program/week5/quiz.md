# No. 5 System Programming Quiz — Chapter 3. Machine-Level Representation Basics

## §1. Assembly Syntax
- AT&T: `mov src, dst`, `%` 레지스터, `()` 메모리 / Intel: `mov dst, src`, `[]` 메모리
- 두 문법 모두 같은 기계어로 어셈블된다.

### Q1) AT&T → Intel 변환 (`objdump -M intel -d`)
| AT&T | Intel |
|---|---|
| `mov (%rdi),%rax` | `mov rax,QWORD PTR [rdi]` |
| `mov %rdx,(%rsi)` | __________________________ |
| `mov %rax,0x8(%rdi,%rsi,8)` | __________________________ |

## §2. Operand Forms
- `$imm` → imm, `%r` → R[r], `imm` → M[imm], `Imm(rb,ri,s)` → M[Imm + R[rb] + R[ri]×s]

### Q2) Operand Value
| Register | Value |   | Address | Value |
|---|---|---|---|---|
| %rax | 0x100 |   | 0x100 | 0xFF |
| %rcx | 0x1 |     | 0x104 | 0xAB |
| %rdx | 0x3 |     | 0x108 | 0x13 |
|  |  |             | 0x10C | 0x11 |

| Operand | Value |
|---|---|
| `%rax` | ______ |
| `0x104` | ______ |
| `$0x108` | ______ |
| `(%rax)` | ______ |
| `4(%rax)` | ______ |
| `9(%rax,%rdx)` | ______ |
| `0xFC(,%rcx,4)` | ______ |
| `(%rax,%rdx,4)` | ______ |

## §3. Calling Convention
- 인자: %rdi, %rsi, %rdx, %rcx, %r8, %r9 순서 / 반환값: %rax

### Q3) 5번째, 6번째 인자
```c
void func(long a, long b, long c, long d, long e, long *p)
{
    *p = e;              mov   ______,______
}                        retq
```

## §4. C → Machine Code
### Q4) Displacement / Scaled Indexed
```c
void f1(long *xp, long y)          mov   ______,____________
{                                  retq
    xp[2] = y;
}

long f2(long *xp, long i)          mov   ____________________,%rax
{                                  retq
    return xp[i + 1];
}
```

## §5. mov 제약
- Immediate는 src로만 사용 가능
- src, dst 중 최대 하나만 memory
- scale은 1, 2, 4, 8 중 하나

### Q5) 잘못된 명령어 찾기 (올바르면 O, 틀리면 X와 이유)
| 명령어 | O/X | 이유 |
|---|---|---|
| `movq %rax,$0x10` | ___ | ______________ |
| `movq (%rax),(%rdx)` | ___ | ______________ |
| `movq (%rax,%rdx,3),%rcx` | ___ | ______________ |
| `movq $-1,(%rdi,%rsi,8)` | ___ | ______________ |
| `movq 0x10(,%rdx,2),%rax` | ___ | ______________ |

---
## 정답
- Q1) `mov QWORD PTR [rsi],rdx` / `mov QWORD PTR [rdi+rsi*8+0x8],rax`
- Q2) 0x100 / 0xAB / 0x108 / 0xFF / 0xAB / 0x11 (0x10C) / 0xFF (0x100) / 0x11 (0x10C)
- Q3) `mov %r8,(%r9)`
- Q4) `mov %rsi,0x10(%rdi)` / `mov 0x8(%rdi,%rsi,8),%rax`
- Q5) X: dst에 immediate 불가 / X: memory→memory 불가 / X: scale 3 불가 / O / O
