# SP 3-4 풀이 (Quiz No.3 ~ No.5)

- 원본: `SP 3-4.pdf`
- 환경: x86-64 Linux, gcc, AT&T 문법 (`mov Src, Dst`)
- 인자: `%rdi`, `%rsi`, `%rdx`, `%rcx`, `%r8`, `%r9` / 반환값: `%rax`

---

## No.3 — Data Movement Instructions and Operand Forms

### Q1. (예시) immediate → register
```
mov $0xffffffffffffffff,%rax
retq
```

### Q2. absolute memory address
```
mov $0xffffffffffffffff,0x104
retq
```
- 주소 `0x104`에 `$` 없이 쓰면 **절대 주소 메모리**를 뜻한다 (`$0x104`는 상수).
- 크기는 `long *`이므로 8바이트 (`movq`).

### Q3. return value
```
mov 0x104,%rax
retq
```
- 메모리 `M[0x104]`를 읽어 반환 레지스터 `%rax`에 넣는다.
- 참고: `return ret;`이 없으면 dead code로 제거되어 `retq`만 남는다.

### Q4. indirect memory address
```
mov %rsi,(%rdi)
retq
```
- `xp` = 1번째 인자 `%rdi`, `x` = 2번째 인자 `%rsi`
- `(%rdi)` = `M[%rdi]` = `*xp`

### Q5. scaled indexed
```
movq $0xffffffffffffffff,(%rdi,%rsi,8)
retq
```
- `&buf[idx]` = `buf + idx * 8` (long = 8바이트) → `(%rdi,%rsi,8)`
- 레지스터 operand가 없어 크기를 추론할 수 없으므로 suffix `q`가 필요하다.

### Q6. memory → memory
```
mov (%rsi),%rax
mov %rax,(%rdi,%rdx,8)
retq
```
- mem → mem `mov`는 인코딩이 없으므로 `%rax`를 임시로 거친다.
- `buf` = `%rdi`, `xp` = `%rsi`, `idx` = **3번째 인자** `%rdx`
- PDF의 `$rax`는 `%rax`의 오타

---

## No.4 — Instruction Class with Different Sizes

### Q1. 큰 source → 작은 destination (truncation)
```
f2 (short *x, long y): mov %si,(%rdi)
f3 (int   *x, long y): mov %esi,(%rdi)
f4 (long  *x, long y): mov %rsi,(%rdi)
```
- 하위 비트만 쓰면 되므로 `%rsi`의 하위 레지스터 이름을 사용한다.
- 레지스터 이름으로 크기가 정해지므로 suffix(`w`, `l`, `q`) 생략 가능

### Q2. 작은 source → 큰 destination (sign extend, `movs`)
```
f6 (long *x, short y): movswq %si,%rsi    / mov %rsi,(%rdi)
f7 (long *x, int   y): movslq %esi,%rsi   / mov %rsi,(%rdi)
f8 (long *x, long  y): mov %rsi,(%rdi)
```
- `movs` + source 크기 + dest 크기: `b`(1) `w`(2) `l`(4) `q`(8)
- f8은 크기가 같아 확장이 필요 없다.

### Q3. 작은 source → 큰 destination (zero extend, `movz`)
```
f10(unsigned long *x, unsigned short y): movzwl %si,%esi  / mov %rsi,(%rdi)
f11(unsigned long *x, unsigned int   y): mov %esi,%eax    / mov %rax,(%rdi)
```
- 32비트 레지스터에 쓰면 **상위 32비트가 자동으로 0**이 된다.
  - f10: `movzwl`로 `%esi`에 쓰면 `%rsi` 전체가 zero extension된 값 → `movzwq`와 같은 효과
  - f11: `movzlq`는 존재하지 않는다 → `mov %esi,%eax`가 그 역할을 한다.

### Q4. movabsq (예시)
- `0x0011223344556677`은 32비트 immediate로 표현할 수 없음 → `movabs`로 `%rax`에 먼저 넣은 뒤 저장

---

## No.5 — Arithmetic Operations

### Q1, Q2. (예시) mov vs lea
- `mov (%rdi,%rsi,8),%rax` → 주소의 **메모리 값**을 읽음 (`buf[idx]`)
- `lea (%rdi,%rsi,8),%rax` → **주소 자체**를 계산 (`&buf[idx]`)

### Q3. lea (int 배열)
```
lea (%rdi,%rsi,4),%rax
retq
```
- int = 4바이트 → scale 4

### Q4. lea로 곱셈 (x * 48)
```
lea (%rdi,%rdi,2),%rax     # x + 2x = 3x
shl $0x4,%rax              # 3x * 16 = 48x
retq
```
- scale은 1, 2, 4, 8만 가능 → 48 = 3 × 16으로 분해

### Q5. Swap
```
mov (%rdi),%rax      # t1 = *xp
mov (%rsi),%rdx      # t2 = *yp
mov %rdx,(%rdi)      # *xp = t2
mov %rax,(%rsi)      # *yp = t1
retq
```

### Q6. arith
```
xorq %rsi, %rdi                     # t1 = x ^ y
leaq (%rdx,%rdx,2), %rax            # 3*z
salq $4, %rax                       # t2 = 48*z
andl $252645135, %edi               # t3 = t1 & 0x0F0F0F0F
subq %rdi, %rax                     # return t2 - t3
ret
```
- AT&T `sub S, D` → **D = D - S** → `%rax = t2 - t3`
- 반환값이 `%rax`에 있어야 하므로 `subq %rax,%rdi`(t3 - t2, 결과가 `%rdi`)는 오답

### Q7. 어셈블리 → C
```
lea (%rsi,%rsi,1),%rax     # %rax = x + x = 2x
sub %rdx,%rax              # %rax = 2x - y
mov %rax,(%rdi,%rsi,8)     # M[buf + 8x] = %rax  →  buf[x]
retq
```
```c
void quiz(long buf[], long x, long y) {
    buf[x] = 2 * x - y;
}
```
