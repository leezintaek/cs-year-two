# 기말 퀴즈 2 – RNN 집중

- 범위: `final_sum/` 중 RNN 부분 (12_1, 12_2, 13_1 앞부분: Loss, BPTT, LSTM, GRU)
- 문제 유형: T/F, 객관식, 단답형 주관식, 빈칸 채우는 손코딩 (순서 무작위)
- 코드는 모두 Python
- 계산기 사용 가능. tanh 값은 문제에 주어진 것을 쓴다.
- 계산 중간 결과는 **소수 둘째 자리로 반올림한 뒤** 다음 단계에 쓴다.
- 정답과 해설: `quiz_2_explanation.md`

---

### Q1. [T/F]
Recurrent neuron에서 첫 시점(`t = 0`)의 이전 output `y(−1)`은 알 수 없으므로, 일반적으로 첫 시점의 input `x(0)`을 그대로 복사해서 쓴다.

답: ☐ T ☐ F

### Q2. [계산]
Recurrent neuron 하나가 다음 식으로 계산한다.

```
y(t) = tanh( x(t)·Wx + y(t−1)·Wy + b )
x(0) = 2,  x(1) = −1,  x(2) = 3
Wx = 0.4,  Wy = 0.5,  b = 0.1,  time window = 3
```

필요한 tanh 값은 아래에서 고른다.

```
tanh(0.06) ≈ 0.06   tanh(0.11) ≈ 0.11   tanh(0.4)  ≈ 0.38
tanh(0.9)  ≈ 0.72   tanh(1.2)  ≈ 0.83   tanh(1.33) ≈ 0.87
```

- (1) `y(0)`, `y(1)`, `y(2)`를 구하시오.
- (2) 이 neuron을 seq-to-vec으로 쓴다면 최종 output은 무엇인가?

### Q3. [객관식]
Mini-batch 크기 `m = 32`, 시점마다 input feature 수 `n_inputs = 5`, recurrent neuron 수 `n_neurons = 8`인 recurrent layer가 있다. `Y(t) = φ( X(t)·Wx + Y(t−1)·Wy + b )`일 때 **틀린** 것은?

1. `X(t)`의 크기는 `32 × 5`
2. `Wx`의 크기는 `5 × 8`
3. `Wy`의 크기는 `32 × 8`
4. `Y(t)`의 크기는 `32 × 8`
5. `b`의 원소 수는 8

### Q4. [단답형]
Q3의 layer를 `[X(t)  Y(t−1)] · W + b` 처럼 **이어 붙인 형태**로 계산하려고 한다. mini-batch 하나에 대해

- (1) `[X(t)  Y(t−1)]`의 크기는?
- (2) `W`의 크기는?
- (3) `Wx`, `Wy`, `b`를 모두 합친 이 layer의 parameter 수는? (bias는 neuron마다 하나)

### Q5. [T/F]
주가 예측 RNN에서 time window를 7에서 30으로 늘리면, 시점마다 다른 `Wx`를 써야 하므로 학습해야 할 parameter 수도 늘어난다.

답: ☐ T ☐ F

### Q6. [계산]
Hidden state가 있는 RNN cell이다. bias는 없고, output에는 activation 없이 linear만 적용한다.

```
h(t) = tanh( x(t)·Wx + h(t−1)·Wh ),   h(−1) = 0
y(t) = h(t)·Wy

x(0) = [2, 1],  x(1) = [1, 3],  x(2) = [3, −1]
Wx = [0.3, −0.2]ᵀ,  Wh = 0.5,  Wy = 2
```

필요한 tanh 값은 아래에서 고른다.

```
tanh(−0.11) ≈ −0.11   tanh(0.26) ≈ 0.25   tanh(0.4)   ≈ 0.38
tanh(0.5)   ≈ 0.46    tanh(1.0)  ≈ 0.76   tanh(1.045) ≈ 0.78
```

- (1) `h(0)`, `h(1)`, `h(2)`를 구하시오.
- (2) `y(0)`, `y(1)`, `y(2)`를 구하시오.

### Q7. [계산]
Q6의 output sequence에 대해 ground truth가 `y0 = 1, y1 = 0, y2 = 2`이다. Loss는 squared error의 합이다.

- (1) seq-to-seq로 학습할 때의 loss는?
- (2) seq-to-vec으로 학습할 때의 loss는?
- (3) 두 loss 중 어느 쪽을 쓰느냐가 바꾸는 것은 무엇인지 한 문장으로 쓰시오.

### Q8. [객관식]
Hidden state 구조 RNN의 세 weight에 대한 설명으로 옳은 것은?

1. `Wx`는 hidden → output, `Wh`는 input → hidden, `Wy`는 hidden → hidden
2. `Wx`는 input → hidden, `Wh`는 hidden → 다음 시점 hidden, `Wy`는 hidden → output
3. `Wh`는 시점마다 새로 만들어지므로 window 길이만큼 존재한다
4. `Wy`는 이전 시점 output `y(t−1)`에 곱해지는 weight이다
5. 기본 memory cell과 마찬가지로 `Y`가 다음 시점으로 순환한다

### Q9. [빈칸 손코딩]
주가 예측(input 4, hidden 64, output 1)의 seq-to-vec RNN이다. 빈칸을 채우시오.

```python
import torch.nn as nn

class RNN(nn.Module):
    def __init__(self, input_size=4, hidden_layer_size=64, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        self.rnn = nn.RNN(____(a)____, ____(b)____)
        self.linear = nn.Linear(____(c)____, ____(d)____)

    def forward(self, input_seq):
        rnn_out, hidden_out = self.rnn(input_seq.view(len(input_seq), 1, -1))
        predictions = self.linear(rnn_out.view(len(input_seq), -1))
        return predictions[____(e)____]
```

추가: window = 7일 때 `rnn_out.view(len(input_seq), -1)`의 크기와 `predictions`의 크기를 쓰시오.

### Q10. [단답형]
IBM 주가 데이터에서 날짜순으로 `x(0), x(1), …, x(49)`가 있다(각 `x(t)`는 Open, High, Low, Close 4개 값). Time window = 10으로 sliding window를 만들고, 각 시점 `x(t)`의 정답은 다음 날 종가 `x(t+1)[3]`이다.

- (1) `x(5)`부터 시작하는 input sequence는 `x(5)`부터 `x(?)`까지다. `?`는?
- (2) 그 sequence의 **마지막** output이 맞춰야 하는 ground truth는?
- (3) 정답 label까지 모두 데이터 안에 있는 (input, label) 세트는 최대 몇 개 만들 수 있는가?

### Q11. [객관식]
다음 상황과 input/output sequence 유형을 바르게 짝지은 것은?

- (가) 영화 리뷰 문장을 읽고 1–5점 평점 하나를 예측
- (나) 사진 한 장으로 설명 문장 생성
- (다) 영어 문장을 한국어 문장으로 번역
- (라) 지난 N일 주가로 하루씩 밀린 N일 주가를 예측

1. 가: vec-to-seq, 나: seq-to-vec, 다: seq-to-seq, 라: encoder-decoder
2. 가: seq-to-vec, 나: vec-to-seq, 다: encoder-decoder, 라: seq-to-seq
3. 가: seq-to-seq, 나: vec-to-seq, 다: encoder-decoder, 라: seq-to-vec
4. 가: seq-to-vec, 나: encoder-decoder, 다: seq-to-seq, 라: vec-to-seq

### Q12. [단답형]
RNN의 단점 세 가지를 쓰고, 그중 encoder-decoder 구조가 해결하려고 나온 단점이 무엇인지 고르시오. 또 encoder와 decoder가 각각 하는 일을 "말을 끝까지 듣는다"는 관점에서 설명하시오.

### Q13. [T/F]
기본 memory cell에서 `y(3)`은 `x(3)`과 `y(2)`만의 함수이므로 `x(0)`의 정보는 `y(3)`에 전혀 들어 있지 않다.

답: ☐ T ☐ F

### Q14. [계산]
기본 cell에서 과거 정보가 `Wy`를 한 번 거칠 때마다 `Wy`배가 된다고 단순화하자.

- (1) `Wy = 0.5`일 때 10 시점 전 정보에 곱해지는 값은 대략 얼마인가? (소수 넷째 자리까지)
- (2) 이 현상 때문에 기본 cell이 학습하기 어려운 pattern은 어떤 것인가?

### Q15. [객관식]
BPTT에서 `∂L/∂Wh`를 구할 때 나타나는 현상으로 옳은 것은?

1. `Wh`는 한 번만 곱해지므로 sequence 길이와 무관하게 gradient 크기가 일정하다
2. chain rule을 적용할 때마다 `Wh`가 한 번씩 더 곱해져, `Wh < 1`이면 exploding, `Wh > 1`이면 vanishing gradient가 생긴다
3. chain rule을 적용할 때마다 `Wh`가 한 번씩 더 곱해져, `Wh < 1`이면 vanishing, `Wh > 1`이면 exploding gradient가 생긴다
4. `Wy`만 반복해서 곱해지고 `Wh`는 gradient에 나타나지 않는다
5. sequence가 길수록 가장 오래된 정보를 더 잘 기억한다

### Q16. [단답형]
`Wh = 0.9`인 경우와 `Wh = 1.1`인 경우 각각 50 time step 동안 `Wh`가 반복 곱해지면 값이 대략 얼마가 되는가? (아래 값을 참고)

```
0.9⁵⁰ ≈ 0.0052     1.1⁵⁰ ≈ 117.4
```

각각 어떤 문제에 해당하는지 쓰시오.

### Q17. [빈칸]
LSTM에 대한 설명이다. 빈칸을 채우시오.

- LSTM은 두 가지 state를 가진다. 오래 가져가는 long-term state `____(a)____`와 이번 시점 output이 되는 short-term state `____(b)____`.
- `____(c)____` gate는 이전 long-term 기억을 가져갈지(copy) 버릴지(reset to zero)를 정한다.
- `____(d)____` gate는 현시점에서 새로 알게 된 것 `g(t)`를 long-term state에 반영할지를 정한다. 반영은 `____(e)____`(곱셈/덧셈)으로 한다.
- `____(f)____` gate는 long-term state를 이번 시점에 얼마나 내보낼지를 정한다.
- 세 gate는 모두 `____(g)____` 함수를 써서 출력이 항상 `____(h)____` 범위다.

### Q18. [객관식]
LSTM이 basic RNN보다 vanishing gradient 문제가 적은 이유로 가장 적절한 것은?

1. Gate가 ReLU를 써서 gradient가 항상 1이기 때문
2. Long-term state가 매 step마다 `Wh`를 곱하지 않고 gate로 얼마나 copy할지만 정해서 전달되기 때문
3. Hidden size를 64보다 크게 쓰기 때문
4. 미래 input을 미리 읽을 수 있기 때문
5. Output gate가 long-term state에 weight를 반복해서 곱하기 때문

### Q19. [T/F 묶음]
각각 T/F를 고르시오.

- (1) GRU는 LSTM의 `c(t)`와 `h(t)`를 하나의 `h(t)`로 합친 단순화 버전이다.
- (2) GRU는 forget, input, output gate를 각각 따로 둔다.
- (3) GRU에서 gate controller `z(t)`가 1이면 forget gate가 열리고 0이면 input gate가 열린다.
- (4) Seq-to-vec RNN은 마지막 시점의 output만 쓰고 나머지 output은 무시한다.

### Q20. [서술]
"RNN은 input sequence가 100개든 10,000개든 model size가 커지지 않는다." 이 말이 성립하는 이유를 **weight sharing** 관점에서 설명하고, 반대로 이 구조 때문에 생기는 단점 두 가지(계산 속도, 오래된 정보)를 연결지어 설명하시오. 또 여러 time step(예: 0–5일만 알 때 6, 7일)을 예측하는 방법을 쓰시오.
