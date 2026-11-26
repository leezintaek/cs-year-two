# 인공지능개론 기말 퀴즈 1

- 범위: `final_sum/` 전체 (9_2 Deep Learning, 10_1·10_2·11_1 CNN, 12_1·12_2 RNN)
- 문제 유형: T/F, 객관식, 단답형 주관식, 빈칸 채우는 손코딩 (순서 무작위)
- 코드는 모두 Python
- 계산기 사용 가능. tanh 값은 문제에 주어진 것을 쓴다.
- 정답과 해설: `quiz_1_explanation.md`

---

### Q1. [단답형]
Input channel이 2개인 3×3 입력에 2×2 kernel을 padding 0, stride 1로 적용한다. Bias는 `1`이다.

```
channel 1 입력     kernel 1          channel 2 입력     kernel 2
1  0  2            1  -1             2  1  0            0   1
3  1  0            0   2             0  1  3            1  -1
0  2  1                              1  0  2
```

- (1) 출력 feature map(2×2)을 구하시오.
- (2) 이 layer의 parameter 수를 구하시오. (output channel 1개)
- (3) 같은 입력에 output channel을 8개로 늘리면 parameter 수, 출력 feature map의 크기와 장수는 각각 어떻게 되는가?

### Q2. [T/F]
주가 예측 RNN에서 time window를 7에서 30으로 늘리면, 시점마다 계산을 반복하는 횟수가 늘어날 뿐 아니라 `Wx`와 `Wh`의 크기도 window 길이에 비례해 커진다.

답: ☐ T ☐ F

### Q3. [단답형]
Input 2개, hidden layer 1개(neuron 2개, sigmoid), output neuron 1개(sigmoid)인 network가 있다. Loss는 `L = (ŷ − y)²`이다. 어떤 입력에 대한 forward 결과가 다음과 같다.

```
x₀ = 0.5
o₁,₀ = 0.6,  o₁,₁ = 0.8      (hidden layer 출력)
ŷ = o₂,₀ = 0.7,  y = 0.5
w₂,₀,₀ = 0.4  (o₁,₀ → output),  w₁,₀,₀ = 0.2  (x₀ → hidden neuron 0)
learning rate η = 0.1
```

- (1) `∂L/∂w₂,₀,₀`를 구하시오.
- (2) `∂L/∂w₂,₁,₀`를 구하시오.
- (3) `∂L/∂w₁,₀,₀`를 구하시오.
- (4) Gradient descent로 한 번 update한 뒤의 `w₂,₀,₀`와 `w₁,₀,₀`를 구하시오.
- (5) (1)은 (3)의 몇 배인가? Layer가 훨씬 깊어져 이런 현상이 심해지면 무엇이라 부르는가?

### Q4. [객관식]
다음 상황을 RNN의 input/output sequence 유형과 바르게 짝지은 것은?

- (가) 일주일 동안 매일의 기온 sequence를 보고 다음 날 비가 올지 하나만 예측
- (나) 사진 한 장을 보고 설명 문장을 생성
- (다) 한국어 문장을 끝까지 읽은 뒤 영어 문장으로 번역
- (라) 지난 N일의 주가를 넣어 하루씩 민 N일의 주가를 예측

① 가-seq-to-vec, 나-vec-to-seq, 다-seq-to-seq, 라-encoder-decoder
② 가-seq-to-vec, 나-vec-to-seq, 다-encoder-decoder, 라-seq-to-seq
③ 가-seq-to-seq, 나-vec-to-seq, 다-encoder-decoder, 라-seq-to-vec
④ 가-vec-to-seq, 나-seq-to-vec, 다-encoder-decoder, 라-seq-to-seq
⑤ 가-seq-to-vec, 나-seq-to-seq, 다-encoder-decoder, 라-vec-to-seq

추가: (다)에서 seq-to-seq RNN보다 encoder-decoder가 잘 되는 이유를 한 문장으로 쓰시오.

### Q5. [빈칸 손코딩]
padding `P`, stride `S`를 지원하는 grayscale convolution 함수다. 빈칸을 채우시오. (bias 없음)

```python
import numpy as np

def conv2d(image, filt, P, S):
    H, W = image.shape
    M = filt.shape[0]
    padded = np.pad(image, pad_width=____(a)____, mode="constant", constant_values=0)
    out_h = ____(b)____
    out_w = (W + 2 * P - M) // S + 1
    feature_map = np.zeros((out_h, out_w), dtype=np.float32)
    for row in range(out_h):
        for col in range(out_w):
            r, c = row * ____(c)____, col * S
            patch = padded[r:r + ____(d)____, c:c + M]
            feature_map[row, col] = ____(e)____
    return feature_map
```

- (f) `image`가 7×7, `filt`가 3×3, `P=1`, `S=2`일 때 출력 크기는?
- (g) `image`가 8×8, `filt`가 3×3, `P=0`, `S=2`일 때 출력 크기는? 이때 마지막 `row`의 patch는 입력의 몇 번째 행부터 몇 번째 행까지를 덮는가? (0부터 셈) 계산에 한 번도 쓰이지 않는 행이 있다면 몇 번째 행인가?

### Q6. [T/F]
Batch normalization 식 `âᵢ = (aᵢ − μ) / √(σ² + ε)`에서 `ε = 0`으로 두면 Z-score normalization과 같은 식이 된다. 따라서 batch normalization도 data normalization처럼 학습을 시작하기 전에 한 번만 수행하면 된다.

답: ☐ T ☐ F

### Q7. [단답형]
AlexNet의 feature 추출부는 다음과 같다. (conv의 형식: kernel / stride / padding / output channel)

```
Input  227×227×3
C1     conv     11×11 / 4 / 0 / 96
S2     max pool  3×3  / 2 / 0
C3     conv      5×5  / 1 / 2 / 256
S4     max pool  3×3  / 2 / 0
C5     conv      3×3  / 1 / 1 / 384
C6     conv      3×3  / 1 / 1 / 384
C7     conv      3×3  / 1 / 1 / 256
S8     max pool  3×3  / 2 / 0
```

- (1) C1부터 S8까지 각 layer 출력의 `가로×세로×장수`를 쓰시오.
- (2) Flatten 후 첫 fully connected layer의 입력 neuron 수는?
- (3) C1과 C3의 parameter 수를 구하시오.
- (4) 입력이 224×224×3이라면 C1 출력의 가로 크기는?

### Q8. [단답형]
Recurrent neuron 하나가 `y(t) = tanh( x(t)·Wx + y(t−1)·Wy + b )`로 계산한다.

```
x(0) = [1, 2],  x(1) = [3, −1],  x(2) = [0, 2]
Wx = [0.4, −0.2]ᵀ,  Wy = [0.5],  b = 0.1,  time window = 3
```

각 단계의 결과는 소수 둘째 자리로 반올림한 뒤 다음 단계에 쓴다. 필요한 tanh 값은 아래에서 고른다.

```
tanh(0.1) ≈ 0.10    tanh(0.155) ≈ 0.15    tanh(0.255) ≈ 0.25
tanh(1.45) ≈ 0.90   tanh(1.55)  ≈ 0.91    tanh(1.6)   ≈ 0.92
```

- (1) `y(0)`, `y(1)`, `y(2)`를 구하시오.
- (2) Mini-batch 크기가 `m = 8`일 때 `X(t)`, `Wx`, `Y(t−1)`, `Wy`의 shape을 쓰시오.

### Q9. [객관식]
이미지 처리에 대한 설명으로 옳은 것을 **모두** 고르시오.

① Invariance는 `f[t[x]] = t[f[x]]`로, 입력이 변환된 만큼 출력도 똑같이 변환되는 성질이다.
② Image classification은 산 사진을 조금 옮기면 출력도 그만큼 옮겨져야 하므로 equivariance가 필요한 task다.
③ Image segmentation에서는 이미지를 옮긴 뒤 segmentation한 결과와, segmentation한 뒤 그 결과를 옮긴 것이 같아야 한다.
④ 이미지를 flatten해 fully connected layer에 넣으면 parameter가 많아지는 문제만 있고, 주변 pixel 사이의 관계(local correlation)는 그대로 유지된다.
⑤ 720×720 RGB 이미지를 flatten해 hidden neuron 1개짜리 fully connected layer에 넣으면 parameter가 1,555,201개 필요하다.

### Q10. [단답형]
Input 1개, output 1개이고 activation으로 ReLU를 쓰는 network를 생각한다.

- (1) Hidden layer 3개, 각 layer에 neuron 4개일 때 최대 linear region 수와 parameter 수를 구하시오.
- (2) Hidden layer 1개로 (1)과 같은 최대 linear region 수를 얻으려면 neuron이 최소 몇 개 필요한가? 그때 parameter 수는?
- (3) `y = ReLU(x − 1) + ReLU(2x − 2) + ReLU(x − 3)`의 linear region은 몇 개인가?

### Q11. [T/F]
LeNet-5에서 5×5×16 출력을 받는 C5를 `nn.Conv2d(16, 120, kernel_size=5)`로 구현하든, flatten 후 `nn.Linear(400, 120)`으로 구현하든 parameter 수는 같다. 그리고 Conv2d로 구현했을 때 출력 feature map의 크기는 1×1이다.

답: ☐ T ☐ F

### Q12. [단답형]
다음 4×4 입력에 pooling을 적용한다.

```
1  3  2  0
5  2  7  1
0  4  6  8
2  2  1  3
```

- (1) Max pooling, 2×2, stride 2의 결과는?
- (2) Average pooling, 2×2, stride 2의 결과는?
- (3) Max pooling, 3×3, stride 1의 결과는?
- (4) 1차원 값 `[2, 6, 4]`를 2배로 upsampling한다. Duplicate 방식과 bi-linear interpolation 방식의 결과를 각각 쓰시오. (Interpolation에서 오른쪽 끝 바깥은 수업처럼 0으로 가정한다.)

### Q13. [빈칸 손코딩]
Hidden state가 있는 RNN cell의 forward를 numpy로 구현했다. `h(t) = tanh( x(t)·Wx + h(t−1)·Wh )`, `y(t) = h(t)·Wy`이고 bias는 없다. 빈칸을 채우시오.

```python
import numpy as np

def rnn_forward(X, Wx, Wh, Wy):
    # X: (window, n_inputs)
    window = X.shape[0]
    h = np.____(a)____((1, Wh.shape[0]))           # h(−1)
    ys = []
    for t in range(____(b)____):
        h = np.tanh(X[t:t+1] @ Wx + ____(c)____)   # h(t)
        y = ____(d)____                            # y(t)
        ys.append(y)
    return ys[____(e)____]                         # seq-to-vec
```

- (f) 수업의 주가 예측처럼 input 4, hidden 64, output 1, window 7이면 `X`, `Wx`, `Wh`, `Wy`의 shape과 반환값의 shape은?
- (g) `h = np.____(a)____(...)` 줄을 `for` 문 **안쪽 첫 줄**로 옮기면 이 network는 어떤 성질을 잃는가?

### Q14. [객관식]
Normalization과 gradient 문제에 대한 설명으로 옳은 것을 **모두** 고르시오.

① Batch normalization은 데이터 하나에 대해, 그 layer neuron들의 activation 사이에서 `μ`, `σ`를 구한다.
② Layer normalization은 mini-batch에 데이터가 1개뿐이어도 `μ`, `σ`를 계산할 수 있다.
③ `ε`은 variance가 0에 가까울 때 나눈 값이 지나치게 커지는 것을 막기 위해 넣는다.
④ Vanishing gradient는 chain rule로 곱해지는 항들이 대부분 1보다 클 때 생긴다.
⑤ Shallow network는 곱해지는 항이 적어서 deep network보다 vanishing/exploding gradient가 덜하다.

### Q15. [단답형]
어떤 grayscale 이미지의 한 3×3 영역이 다음과 같다.

```
9  9  1
9  9  1
9  9  1
```

수업의 세 filter를 이 영역에 적용한다.

```
Vertical      Horizontal    Laplacian
-1  0  1      -1 -1 -1      -1 -1 -1
-1  0  1       0  0  0      -1  8 -1
-1  0  1       1  1  1      -1 -1 -1
```

- (1) 세 filter의 출력 값을 각각 구하시오.
- (2) Vertical filter 출력의 부호는 밝기 변화에 대해 무엇을 뜻하는가?
- (3) 이 영역에 있는 edge의 방향은 세로와 가로 중 무엇인가? Horizontal filter의 출력이 그렇게 나온 이유는?

### Q16. [단답형]
하루마다 `[Open, High, Low, Close]` 4개 값이 있는 주가 데이터 `x(0)`, …, `x(29)`(30일치)가 있다. 수업처럼 time window 5의 sliding window로, 각 시점 `x(t)`에서 다음 날 종가 `x(t+1)[3]`을 예측하도록 학습한다. 마지막 window 하나는 test로 쓴다.

- (1) 첫 번째 training set의 input과 target을 쓰시오.
- (2) 마지막 training set의 input과 target을 쓰시오.
- (3) Training set은 모두 몇 개인가?
- (4) Test set의 input은 무엇이고, 그 마지막 target은 무엇인가?

### Q17. [T/F]
어떤 convolution layer의 input channel 수를 1에서 3으로 바꾸면 그 layer의 parameter 수는 늘어나지만, 출력 feature map의 크기와 장수는 바뀌지 않는다.

답: ☐ T ☐ F

### Q18. [단답형]
MNIST용 LeNet-5를 Implementation (2) 방식으로 구현했다.

```python
self.c1 = nn.Conv2d(1, 6, kernel_size=5, stride=1, padding=2)
self.c3 = nn.Conv2d(6, 16, kernel_size=5, stride=1, padding=0)
self.pool = nn.AvgPool2d(kernel_size=2, stride=2)
self.f5 = nn.Linear(400, 120)
self.f6 = nn.Linear(120, 84)
self.output = nn.Linear(84, 10)
```

- (1) CIFAR-100(100 class) 분류에 쓰려면 바꿔야 하는 줄과 값을 모두 쓰시오.
- (2) 바꾼 뒤 `c1`, `c3`, `output`의 parameter 수를 구하시오.
- (3) CIFAR-100에서 padding을 2 그대로 두면 c1, S2, c3, S4 출력 크기와 flatten 후 neuron 수는? 어느 줄에서 문제가 생기는가?
- (4) Superclass로 분류한다면 `output`의 parameter 수는?

### Q19. [단답형]
Feature A의 값이 `2, 4, 6, 8, 80`이다. (σ는 모집단 표준편차, 소수 셋째 자리에서 반올림)

- (1) 6의 min-max normalization 값을 구하시오.
- (2) `μ`, `σ`와 6의 Z-score normalization 값을 구하시오.
- (3) 80을 뺀 `2, 4, 6, 8`만으로 min-max normalization을 하면 6은 얼마가 되는가?
- (4) (1)과 (3)을 비교해, outlier의 영향을 크게 받는 방법과 그 이유를 쓰시오.

### Q20. [단답형]
수업의 주가 예측 seq-to-vec 모델(input 4, hidden 64, output 1, window 7)을 다음 식으로 계산한다고 하자.

```
H(t) = tanh( X(t)·Wx + H(t−1)·Wh + b_h )
Y(t) = H(t)·Wy + b_y
```

- (1) `Wx`, `Wh`, `b_h`, `Wy`, `b_y`의 shape을 쓰시오.
- (2) 위 식 기준 전체 parameter 수를 구하시오.
- (3) Window를 30으로 늘리면 parameter 수와 `H(t)` 계산 횟수는 각각 어떻게 되는가?
- (4) 이 모델에서 30 시점 전의 input 정보가 현재 `H(t)`에 잘 반영되지 않는 이유를 쓰시오.
