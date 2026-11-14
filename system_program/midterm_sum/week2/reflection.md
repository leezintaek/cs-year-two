# Week 2 학습성찰 — Integer 수준의 Surprise (Casting, Overflow)

## 제출용 (한 문단, 문답형)

`-1 < sizeof(int)`는 왜 거짓일까? signed와 unsigned가 섞이면 -1이 unsigned로 바뀌어 아주 큰 수가 되기 때문이다. 그렇다면 `INT_MAX + 1`은 왜 음수가 될까? C는 overflow를 에러로 알리지 않고 조용히 wrap-around하기 때문이다. 결국 두 surprise 모두 비트는 그대로인데 해석만 달라져서 생기므로, 앞으로는 연산 전에 타입과 범위를 꼭 확인하겠다.

## 제출용 B (심화 버전)

`-1 < sizeof(int)`는 왜 거짓일까? `sizeof`는 unsigned 타입인 `size_t`를 반환하므로, C의 암묵적 형변환 규칙에 따라 -1이 unsigned로 바뀌는데, 2의 보수 비트 패턴 `0xFFFFFFFF`는 그대로인 채 4,294,967,295(2³²−1)로 재해석되기 때문이다. 그렇다면 `INT_MAX + 1`은 왜 음수가 될까? 32비트 int의 표현 범위(−2³¹ ~ 2³¹−1)를 넘으면 C는 에러 없이 wrap-around하여 TMin(−2,147,483,648)이 되기 때문이며, 이를 gdb에서 `x /4bx`로 메모리 바이트를 직접 확인하며 검증해 보았다. 결국 두 surprise 모두 "비트는 그대로, 해석만 달라진다"는 원리에서 비롯되므로, 앞으로는 `-Wsign-compare` 같은 컴파일 옵션을 활용해 연산 전에 타입과 범위를 꼭 점검하겠다.

---

## 1. 개인별로 정리한 내용

### 핵심: "비트는 그대로, 해석만 바뀐다"
- casting은 비트 패턴을 바꾸지 않는다. 같은 `0xFFFFFFFF`가 `int`로는 -1이고 `unsigned`로는 4294967295다.
- 그래서 signed ↔ unsigned 사이를 오가면 값이 2^w만큼 차이 나고, 큰 음수가 큰 양수로 바뀌는 **순서 역전(ordering inversion)** 이 생긴다.

### Casting Surprise
- 하나의 식에 signed와 unsigned가 섞이면 **signed가 unsigned로 암묵적 변환**된다. `<`, `==` 같은 비교 연산도 마찬가지다.
  - `-1 < 0U` → 거짓, `-1 < sizeof(int)` → 거짓(`sizeof`의 결과가 `size_t`, 즉 unsigned이기 때문)
  - `for (unsigned i = n; i >= 0; i--)` → `i >= 0`이 항상 참이라 무한 루프가 된다.
- 확장(expanding): unsigned는 zero extension, signed는 sign extension을 한다. sign extension에서 앞을 1로 채워도 값이 유지되는 이유는 `-2^(w-1) = 2^(w-1) - 2^w`라는 등식 때문이다(Q&A Q2에서 정리).
- 축소(truncating): 상위 비트를 버리고 **최하위 바이트**만 남긴다. `int 15213(0x3B6D)` → `char`로 바꾸면 `0x6D = 109`가 된다. 처음에는 `0x3B`가 남는다고 잘못 생각했었다(Q&A Q3).

### Overflow
- C는 overflow가 일어나도 에러를 내지 않고 **조용히 wrap-around** 한다.
  - `INT_MAX + 1` → `INT_MIN`, `SHRT_MAX + 1` → 음수
  - `-INT_MIN == INT_MIN`: TMin에는 대응하는 양수가 없다(2의 보수 범위가 비대칭이므로).
- 실제 사례: YouTube "강남스타일" 조회수가 32비트 int 범위를 넘어서 64비트로 바꿔야 했다.
- 곱셈을 shift로 최적화하는 경우(`2*x` ↔ `x << 1`)에도 overflow는 똑같이 일어난다.

## 2. 느낀 점
- 지금까지는 "결과가 이상하면 타입을 바꾸면 된다" 정도로만 생각했다. 비트 수준에서 보니 이상한 결과에도 다 이유가 있었다. 컴파일러는 규칙대로 동작했을 뿐이고, 문제는 그 규칙을 몰랐던 프로그래머 쪽에 있었다.
- 특히 `sizeof`나 `strlen`처럼 **unsigned를 반환하는 표준 함수와 int를 비교하는 코드**는 평소에 아무 생각 없이 써 왔던 것이라 가장 인상 깊었다.
- 보안 측면에서도 중요하다. 길이 검사에서 signed/unsigned가 섞이면 음수 길이가 검사를 통과해 buffer overflow로 이어질 수 있다(예: `memcpy`의 길이 인자가 `size_t`인 경우).

## 3. 앞으로의 계획
- 직접 짠 C 코드에서 비교문을 쓸 때 양쪽 피연산자의 **타입(signed/unsigned, 크기)** 을 확인하는 습관을 들인다.
- `gcc -Wall -Wextra -Wsign-compare`로 컴파일해서 signed/unsigned 비교 경고를 확인한다.
- 이해가 헷갈릴 때는 `show_bytes`나 gdb의 `x /4bx`로 실제 메모리 바이트를 확인해 본다.
- 다음 주 floating point에서도 "비트 패턴 ↔ 해석" 관점이 그대로 이어지므로, int ↔ float casting에서 어떤 surprise가 생기는지 비교하며 공부한다.

## 4. 팀원과 공유하고 싶은 내용
- **자주 하는 실수 체크리스트**
  1. unsigned 변수로 감소하는 루프를 돌리고 있지 않은가? (`i >= 0` 무한 루프)
  2. `sizeof`, `strlen`의 결과를 음수가 될 수 있는 int와 비교하고 있지 않은가?
  3. 큰 타입을 작은 타입에 대입할 때(truncation) 값이 잘리지 않는가?
  4. `INT_MAX` 근처 값끼리 더하거나 곱하지 않는가?
- **제안**: 각자 위와 같은 "surprise 코드"를 하나씩 만들어 와서, 출력값을 서로 맞혀 보는 활동을 해 보면 좋겠다. 퀴즈 형식(`week2/quiz.md`)으로 이미 몇 문제 만들어 두었으니 같이 풀어 봐도 좋다.
