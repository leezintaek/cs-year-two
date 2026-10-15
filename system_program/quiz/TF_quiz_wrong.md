# TF_quiz 오답 노트

- 원본: `TF_quiz.md` / 정답: `TF_quiz_answer.md`
- 자세한 해설은 각 항목의 qna 위치 참고

---

### Q12. (week2) — 정답: F
`int x, y;`에 대해 `int64_t pll = x * y;`라고 쓰면 곱셈이 64비트로 수행되므로 overflow 없이 정확한 곱을 얻는다.

- **핵심:** 연산 크기는 대입받는 변수가 아니라 **피연산자 타입**으로 정해진다. `x * y`는 32비트 `int` 곱셈으로 먼저 계산되어 overflow가 나고, 그 결과가 64비트로 sign extension된다.
- **올바른 코드:** `int64_t pll = (int64_t) x * y;`
- **해설:** `week2/qna.md` Q9

### Q15. (week5) — 정답: F
`long f(long x){ return x*3; }`를 컴파일하면 lea 한 번으로 `lea (,%rdi,3),%rax`가 생성될 수 있다.

- **핵심:** scale factor는 **1, 2, 4, 8**만 가능하다. 3은 쓸 수 없다.
- **실제 코드:** `lea (%rdi,%rdi,2),%rax` → x + 2x = 3x
- **해설:** `week5/qna.md` Q6

### Q19. (week3) — 정답: T
Single precision에서 가장 큰 denormalized 값은 정확히 $2^{-126} - 2^{-149}$이다.

- **핵심:** e = 0, f = 1이 23개 → M = $0.111\ldots1_2 = 1 - 2^{-23}$, denorm의 E = **1 - 127 = -126**
- **계산:** $(1 - 2^{-23}) \times 2^{-126} = 2^{-126} - 2^{-149}$ → 가장 작은 normalized($2^{-126}$)와 간격 $2^{-149}$로 이어짐
- **해설:** `week3/qna` Q13

### Q27. (week5) — 정답: T
`void f(){ long ret = *((long *)0x104); }`를 `-Og`로 컴파일하면 메모리 load 없이 `retq` 한 줄만 남는다.

- **핵심:** 읽은 값을 반환·저장·출력하지 않으면 **dead code**로 보고 최적화가 제거한다 (`-Og`도 최적화 옵션).
- **비교:** 같은 load라도 `return ret;`이 있으면(`f4`) `mov 0x104,%rax`가 남는다.
- **해설:** `week5/qna.md` Q8

### Q31. (week3) — 정답: F
`float f = -3.99f; int i = (int)f;`를 실행하면 `i`는 `-4`이다.

- **핵심:** float → int 변환은 소수 부분을 버린다(truncate) = **0 방향으로 반올림** → `-3`
- **비교:** floor(내림)는 `-4`. 양수에서는 truncate와 floor가 같지만 **음수에서는 다르다.**
- **해설:** `week3/qna` Q15

### Q37. (week7) — 정답: F
8-bit 덧셈 `0xFF + 0x01`을 수행하면 CF = 1, ZF = 1, OF = 1이 된다.

- **핵심:** OF는 **signed로 해석**해서 판단한다. `0xFF` = -1 → -1 + 1 = 0으로 정상 → **OF = 0**
- **규칙:** 부호가 다른 두 수의 덧셈은 절대 overflow가 나지 않는다. CF(unsigned)와 OF(signed)는 독립적이다.
- **비교:** `0x7F + 0x01` → CF = 0, OF = 1 (Q23)
- **해설:** `week7/qna.md` Q9

### Q44. (week6) — 정답: T
`void f11(unsigned long *x, unsigned int y){ *x = y; }`는 `movzlq` 대신 `mov %esi,%eax`와 `mov %rax,(%rdi)`로 컴파일된다.

- **핵심:** 32비트 레지스터에 쓰면 상위 32비트가 자동으로 0 → `mov %esi,%eax`가 **논리적으로 movzlq** 역할 (`movzlq`는 존재하지 않음)
- **비교:** signed(`long *x, int y`)라면 `movslq %esi,%rsi` (sign extension은 전용 명령어 필요)
- **해설:** `week6/qna.md` Q9 (관련: Q5)

### Q49. (week3) — 정답: F
아래 코드의 출력은 `True ...`로 시작한다.

```c
float f1 = 0.1f, f2 = 0.6f, f3 = 0.7f;
if (f1 + f2 == f3) printf("True f1+f2=%.10f\n", f1 + f2);
else               printf("False f1+f2=%.10f\n", f1 + f2);
```

- **핵심:** 0.1, 0.6, 0.7은 2진수로 무한 반복 소수 → 저장 시점부터 반올림됨 (f1, f2는 조금 크게, f3는 조금 작게)
- **결과:** `f1 + f2` = 0.7000000477 ≠ `f3` = 0.6999999881 → `False`
- **교훈:** 부동소수점은 `==` 비교를 피한다.
- **해설:** `week3/qna` Q19
