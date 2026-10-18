# SP 연습 문제 정답 및 해설

- 원본: `SP_practice_quiz.md`
- C 출력 문항(P1 ~ P8, P10, P15 ~ P18)은 gcc로 실제 실행해 확인함

---

## Part 1. Bits, Bytes, and Integers

### P1. `Value: -56`
- `200 = 0xC8` → `char`(signed)로 해석하면 MSB가 1 → 200 - 256 = **-56**
- 비트 패턴은 그대로, 해석만 바뀐다.

### P2.
- (a) `done`만 출력. `i >= n`에서 `n`(-1)이 unsigned로 변환되어 `4294967295`(UINT_MAX)가 된다 → `2 >= UINT_MAX`는 거짓 → 루프를 한 번도 돌지 않음.
- (b) **무한 루프**. `i: 2`, `i: 1`, `i: 0` 후 `i--`로 `i`가 `UINT_MAX`가 되고(`%d`로는 `-1`), `-2`, `-3`, ... 계속 출력된다. unsigned는 항상 `>= 0`이므로 `done`은 출력되지 않는다.

### P3.
```
cx=-2
0xfe

x=-2
0xfe
0xff
0xff
0xff
```
- signed `char` → `int`는 **sign extension** (MSB 1로 채움) → `0xFFFFFFFE`
- little endian이므로 최하위 바이트 `0xfe`가 가장 먼저 출력된다.

### P4.
```
x=128
0x80
00
00
00
```
- source가 `unsigned char`이므로 **zero extension** → `0x00000080`
- 함정: `%#.2x`에서 값이 0이면 `#` 플래그가 `0x`를 붙이지 않는다 → `00`

### P5.
```
x=300
0x2c
0x01
00
00

cx=44
0x2c
```
- `300 = 0x0000012C` → truncation으로 하위 1바이트 `0x2C`만 남음 → **44**

### P6. (a) 4번 (b) 0번
- (a) cnt = -3, -2, -1, 0 일 때 `-cnt >= 0` 참 → 4번. cnt = 1이면 `-1 >= 0` 거짓.
- (b) `-INT_MIN == INT_MIN` (TMIN은 양수 짝이 없음) → 처음부터 음수 → 0번

### P7. `positive x 0`
- `0x80000000 + 0x80000000 = 0x1_00000000` → 하위 32비트만 남아 **0**
- 음수 + 음수 = 0 (negative overflow)

### P8.
- (1) `INT_MAX / 2 + 1` = `0x3FFFFFFF + 1` = **`0x40000000`**
- (2) `negative x -2147483648`
- `2 * x` = `x << 1` = `0x80000000` = INT_MIN

### P9.
floating point(100) > integer divide(30) > integer multiply(20) > function call(10) > shift(5) > pointer dereference(2)

---

## Part 2. Floating Point

### P10.
- f1 = -6.5 = -110.1₂ = -1.101₂ × 2² → s = 1, exp = 2 + 127 = 129 = `10000001`, frac = `101000...`
  → **`11000000110100000000000000000000`** (`0xC0D00000`)
- f2: s = 0, exp = `01111110` = 126 → E = -1, frac = `1000...` → 1.1₂ × 2⁻¹ = **0.75**
- f3 = 10.0 = 1010₂ = 1.01₂ × 2³ → exp = 130 = `10000010`
  → **`01000001001000000000000000000000`** (`0x41200000`)

### P11.
- d1: `-inf` / d2: `nan` (x86에서는 `-nan`으로 출력될 수 있음) / d3: `0.000000` / d4: `inf`
- NaN 조건: exponent **모두 1** (2047), fraction **≠ 0**
- 참고: exponent 모두 1 + fraction = 0 → ±∞

### P12. (1/4/3 형식)
- (1) bias = 2⁴⁻¹ - 1 = **7**
- (2) 1.0 = 1.0 × 2⁰ → exp = 0 + 7 = 7 → **`0 0111 000`**
- (3) exp = `1110`(14, `1111`은 특수값) → E = 7, M = 1.111₂ = 1.875 → 1.875 × 128 = **240**
- (4) `0 1001 001` → exp = 9 → E = 2, M = 1.001₂ = 1.125 → 1.125 × 4 = **4.5**

### P13. (1/3/4 형식)
- (1) bias = 2³⁻¹ - 1 = **3**
- (2) 1.0 → exp = 3 → **`0 011 0000`**
- (3) exp = `110`(6) → E = 3, M = 1.1111₂ = 1.9375 → 1.9375 × 8 = **15.5**
- (4) denorm: E = 1 - bias = -2, M = 0.0001₂ = 1/16 → 1/16 × 1/4 = **1/64 = 0.015625**
- (5) `0 101 1010` → exp = 5 → E = 2, M = 1.1010₂ = 1.625 → **6.5**

### P14.
```
10.00011₂ → 10.00₂   (나머지 011 < 100 → 버림)
10.00110₂ → 10.01₂   (나머지 110 > 100 → 올림)
10.11100₂ → 11.00₂   (정확히 절반, 10.11은 홀수 → 짝수 쪽 올림)
10.10100₂ → 10.10₂   (정확히 절반, 10.10은 이미 짝수 → 버림)
```
- 정확히 절반일 때만 round-to-even 규칙이 적용된다 (마지막 비트가 0이 되는 쪽).

### P15. `True`
- float에서는 `0.1f + 0.2f`와 `0.3f`가 모두 `0.3000000119`로 같은 값으로 반올림된다 (실행 확인).
- 반면 `0.1f + 0.6f` = `0.7000000477` ≠ `0.7f` = `0.6999999881` → `False`
- 교훈: 결과가 우연히 같을 수도, 다를 수도 있다 → 부동소수점은 `==` 비교를 피한다.

### P16.
```
16777216.000000
33554436.000000
2147483648.000000
2147483647.000000
```
- float의 유효 비트는 24비트(1 + 23) → 2²⁴ 초과 정수는 정확히 표현 못 함
- `2²⁴ + 1`: 간격 2 → 16777216과 16777218의 정확히 중간 → 짝수 쪽 **16777216**
- `2²⁵ + 3`: 간격 4 → 33554432(거리 3)보다 33554436(거리 1)이 가까움 → **33554436**
- INT_MAX = 2³¹ - 1 → **2³¹**로 반올림 / double은 53비트라 정확
- f3 = 1.0 × 2³¹ → exp = 158 = `10011110` → **`0x4F000000`**

### P17.
```
-2147483648 -2147483648
3 -3 0
```
- 범위를 벗어난 변환은 x86에서 TMIN(`0x80000000`)이 된다 (양수 overflow도 음수 TMIN).
- 소수 부분 버림 = **0 방향 반올림**: 3.7 → 3, -3.7 → **-3** (-4 아님), -0.5 → 0

### P18.
```
f1=4.00 f2=2.00 f3=3.00
g1=3.14 g2=0.00
```
- 2²⁴ 근처 float 간격은 2
- `3 + 2²⁴` = 16777219 → 16777218과 16777220의 정확히 중간 → 짝수 mantissa 쪽인 **16777220** → 빼면 **4**
- `2 + 2²⁴` = 16777218은 정확히 표현됨 → **2**
- `-1e20 + 3.14`는 3.14가 묻혀서 `-1e20` → `1e20 + (-1e20)` = **0**

---

## Part 3. Data Movement

### P19.
```
%rdi              → 0x100   (레지스터 값)
$0x108            → 0x108   (immediate)
0x108             → 0xAB    (절대 주소 0x108의 메모리)
(%rdi)            → 0xFF    (M[0x100])
8(%rdi)           → 0xAB    (M[0x108])
(%rdi,%rsi,8)     → 0x11    (M[0x100 + 3*8 = 0x118])
-8(%rdi,%rsi,8)   → 0x13    (M[0x118 - 8 = 0x110])
0x104(,%rsi,4)    → 0x13    (M[0x104 + 3*4 = 0x110])
```

### P20.
- (a) `movq $0x5, 0x200`
- (b) `mov 0x200, %rax`
- (c) `movl $0xffffffff, (%rdi,%rsi,4)` — int는 4바이트 → scale 4
- (d) `movw $0xffff, (%rdi,%rsi,2)` — short는 2바이트 → scale 2

### P21.
```
mov (%rsi), %eax
mov %eax, (%rdi,%rdx,4)
retq
```
- 메모리 → 메모리 mov는 불가 → 임시 레지스터를 거친다. int이므로 32비트 `%eax`, idx는 3번째 인자 `%rdx`

### P22. 잘못된 것: 1, 2, 4, 5, 6
- 1: `l`(4바이트)인데 64비트 레지스터 `%rdx` → 크기 불일치
- 2: 메모리 → 메모리 이동 불가
- 4: `b`(1바이트)인데 16비트 레지스터 `%si` → 크기 불일치 (`%sil`이어야 함)
- 5: immediate는 destination이 될 수 없다
- 6: `movq`의 immediate는 32비트(sign extend)까지만 → 64비트 상수는 `movabsq` 필요
- 3, 7은 정상

### P23.
```
%rax  %eax  %ax   %al
%rdx  %edx  %dx   %dl
%rsi  %esi  %si   %sil
%r8   %r8d  %r8w  %r8b
```

---

## Part 4. Instruction Size & Extension

### P24.
- f2: `%si` / f3: `%esi` / f4: `%rsi`
- 큰 → 작은 대입은 하위 비트만 쓰면 된다 (truncation)

### P25.
```
f6 : movswq %si,  %rsi
f7 : movslq %esi, %rsi
f10: movzwl %si,  %esi
f11: mov    %esi, %eax
g1 : movsbq %sil, %rsi
g2 : movzbl %sil, %esi
```
- 확장 방식은 **source 타입**으로 결정: g1은 dest가 unsigned여도 source `char`가 signed → sign extension
- g2는 dest가 signed여도 source가 `unsigned char` → zero extension
- `movzwl`/`movzbl`로 32비트 레지스터에 쓰면 상위 32비트는 자동으로 0 → `movzwq`처럼 동작
- f11: `movzlq`는 없다. `mov %esi,%eax`가 32비트 쓰기로 상위를 0으로 만든다.

### P26.
```
movb $-1, %al    → 0x00112233445566FF
movw $-1, %ax    → 0x001122334455FFFF
movl $-1, %eax   → 0x00000000FFFFFFFF   (32비트 쓰기 → 상위 0)
movq $-1, %rax   → 0xFFFFFFFFFFFFFFFF
```

### P27.
```
movb   %dl, %al   → 0x00112233445566AA
movsbq %dl, %rax  → 0xFFFFFFFFFFFFFFAA   (0xAA의 MSB = 1)
movzbq %dl, %rax  → 0x00000000000000AA
```

### P28. c
- a: `-1`은 32비트 `0xFFFFFFFF`를 sign extension하면 64비트 -1 → `movq $-1` 가능
- b: `0x7fffffff`는 32비트 양수 범위 → 가능
- c: 32비트로 표현할 수 없는 64비트 상수 → `movabs $0x11223344556677,%rax` 후 `mov %rax,(%rdi)`

---

## Part 5. Arithmetic Operations

### P29.
- (a) `lea (%rdi,%rsi,4), %rax`
- (b) `lea 0x10(%rdi,%rsi,8), %rax` — `&buf[idx+2]` = buf + 8*idx + 16
- (c) `lea (%rdi,%rsi,1), %rax` (= `(%rdi,%rsi)`)

### P30.
- lea: 주소 계산값 자체 → 0x100 + 24 - 8 = **0x110**
- mov: 그 주소의 메모리 → M[0x110] = **0x13**

### P31.
```
m9 : lea (%rdi,%rdi,8), %rax              # x + 8x = 9x
m12: lea (%rdi,%rdi,2), %rax / shl $2     # 3x * 4 = 12x
m40: lea (%rdi,%rdi,4), %rax / shl $3     # 5x * 8 = 40x
```
- scale은 1, 2, 4, 8만 가능 → 3, 5, 9배는 `x + k*x` 형태로 만든다.

### P32.
```
mov (%rdi), %eax
mov (%rsi), %edx
mov %edx, (%rdi)
mov %eax, (%rsi)
retq
```
- int라서 32비트 레지스터(`%eax`, `%edx`)를 사용한다.

### P33.
```
addq %rsi, %rdi
leaq (%rdx,%rdx,2), %rax
salq $3, %rax                    # 3z * 8 = 24z
andl $3855, %edi                 # 0x0F0F = 15*256 + 15
subq %rdi, %rax                  # %rax = t2 - t3
ret
```
- AT&T 문법 `sub S, D`는 **D = D - S** → `subq %rdi,%rax`

### P34. `x + 4*y + 12*z`
- 1행: `%rax = x + 4y`
- 2행: `%rdx = z + 2z = 3z`
- 3행: `%rax = (x + 4y) + 4*(3z)`

### P35. `buf[x] = 3*x - y;`
- `%rax = x + 2x = 3x` → `%rax = 3x - y` → `M[buf + 8x] = %rax`
