# No. 2 System Programming Quiz — Chapter 2. Bits, Bytes, and Integers

## §1. Two's-Complement
- B2T: MSB의 가중치는 −2^(w−1), 나머지는 양수 가중치.
- 같은 비트 패턴이라도 signed/unsigned 해석에 따라 값이 다르다.

### Q1) 같은 비트, 다른 해석
```c
int main() {                                   <Output>
    char c = 0xF6;                             __________
    printf("%d %u\n", c, (unsigned char)c);
    return 0;
}
```

## §2. Byte Ordering
- Little Endian: 최하위 바이트가 가장 낮은 주소에 저장 (x86-64)

### Q2) show_bytes
```c
typedef unsigned char *pointer;                <Output>
void show_bytes(pointer start, size_t len) {   __________
    for (size_t i = 0; i < len; i++)           __________
        printf("%#.2x\n", start[i]);           __________
}                                              __________
int main() {
    int x = 0x12345678;
    show_bytes((pointer)&x, sizeof(int));
}
```

## §3. Mixed Signed/Unsigned
- signed와 unsigned가 함께 쓰이면 signed가 unsigned로 변환된다.
- `sizeof`의 결과 타입은 `size_t` (unsigned long).

### Q3) sizeof 비교
```c
int main() {                                   <Output>
    if (-1 < sizeof(int))                      __________
        printf("yes\n");
    else
        printf("no\n");
}
```

## §4. Expanding
- Zero extension (unsigned), Sign extension (signed, MSB로 채움)

### Q4) short → int 확장
```c
int main() {                                   <Output>
    short s = -2;                              i=____
    unsigned short us = 0xFFFE;                bytes of i: ____ ____ ____ ____
    int i = s;                                 j=____
    int j = us;                                bytes of j: ____ ____ ____ ____
    printf("i=%d\n", i); show_bytes((pointer)&i, 4);
    printf("j=%d\n", j); show_bytes((pointer)&j, 4);
}
```

## §5. Shift and Division
- 음수 signed 값의 `>>`는 arithmetic shift → 결과는 내림(round down).
- C의 정수 나눗셈 `/`는 0 방향으로 버림(round toward zero).

### Q5) Shift vs Division
```c
int main() {                                   <Output>
    int x = -17;                               x>>2 = ____
    printf("x>>2 = %d\n", x >> 2);             x/4  = ____
    printf("x/4  = %d\n", x / 4);
}
```

---
## 정답
- Q1) `-10 246` (0xF6 = 11110110 → −128+118 = −10)
- Q2) 0x78 / 0x56 / 0x34 / 0x12
- Q3) `no` (−1이 unsigned로 변환되어 매우 큰 수가 됨)
- Q4) i=-2, 0xfe 0xff 0xff 0xff / j=65534, 0xfe 0xff 0x00 0x00
- Q5) −5 (−4.25 내림) / −4 (0 방향 버림)
