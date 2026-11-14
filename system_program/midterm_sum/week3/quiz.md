# No. 3 System Programming Quiz — Chapter 2. Floating Point

## §1. IEEE 754
- Single: 1 sign + 8 exponent + 23 fraction, bias = 127
- Value = (−1)^S × M × 2^E, Normalized: M = 1.f, E = e − bias

### Q1) 10진수 → 비트 패턴
```c
int main() {          (gdb) x /wt &f
    float f = -6.5f;  _ ________ _______________________
    return 0;         (gdb) x /wx &f
}                     0x________
```

### Q2) 비트 패턴 → 10진수
```
(gdb) x /wx &g
0x3f400000
```
- S = __, e = ____, E = ____, M = ________ → g = ________

## §2. Denormalized / Special Values
- Denormalized(e = 0): M = 0.f, E = 1 − bias
- e = 모두 1: f = 0이면 ±∞, f ≠ 0이면 NaN

### Q3) 8-bit floating point (s:1, e:4, f:3, bias = 7)
| 설명 | 비트 패턴 | 값 |
|---|---|---|
| 가장 작은 양의 denormalized | 0 0000 001 | ______ |
| 가장 큰 denormalized | 0 0000 111 | ______ |
| 가장 작은 양의 normalized | ____________ | ______ |
| 가장 큰 normalized | ____________ | ______ |
| +∞ | ____________ | ∞ |

## §3. Rounding
- 기본 반올림 모드: Round-to-even (정확히 중간값이면 짝수 쪽으로)

### Q4) Round-to-even
```c
int main() {                                     <Output>
    printf("%.0f %.0f %.0f %.0f\n",              ____ ____ ____ ____
           0.5, 1.5, 2.5, 3.5);
}
```

## §4. FP Arithmetic Properties
- 부동소수점 덧셈은 교환법칙은 성립하지만 결합법칙은 성립하지 않는다.

### Q5) Associativity
```c
int main() {                                     <Output>
    float a = 1e20f, b = -1e20f, c = 3.14f;      ____________
    printf("%f\n", (a + b) + c);                 ____________
    printf("%f\n", a + (b + c));
}
```

---
## 정답
- Q1) `1 10000001 10100000000000000000000` / 0xc0d00000 (6.5 = 110.1₂ = 1.101₂ × 2², e = 129)
- Q2) S=0, e=126, E=−1, M=1.1₂ → 0.75
- Q3) 1/512 / 7/512 / `0 0001 000` = 1/64 / `0 1110 111` = 240 / `0 1111 000`
- Q4) `0 2 2 4`
- Q5) 3.140000 / 0.000000 (b + c에서 3.14가 반올림되어 사라짐)
