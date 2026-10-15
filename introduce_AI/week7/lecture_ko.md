# Week 07 - Lecture 01: Neural Networks (3) — 한국어 번역

> 원본: `CSE2302_003_week07_1.pdf` (2026-10-13)
> 슬라이드 번호는 PDF 오른쪽 아래 번호와 같다. 전문 용어는 영어로 두었고, 그림은 "[그림]"으로 설명만 적었다.
> 요약본은 `lecture_summary.md` 참고.

---

## 슬라이드 2. Artificial Neural Network (ANN, 인공신경망)

- Artificial Neural Network(ANN)는 **artificial neuron**이라 불리는 연결된 **unit** 또는 **node**들로 이루어지며, 이 neuron들은 **edge**로 연결되어 있다.
- 각 artificial neuron은 연결된 neuron들로부터 **신호를 받아**, 그것을 **처리한 뒤**, 연결된 다른 neuron들에게 **신호를 보낸다**.
- 신호는 실수(real number)이며, 각 연결에서 신호의 세기는 **weight**로 결정된다.

[그림] Input(빨강) → Hidden(파랑) → Output(초록) 층으로 연결된 신경망. "이 구조는 뒤에서 더 자세히 설명할 예정..."

## 슬라이드 3. Perceptron (퍼셉트론) (cont.)

- artificial neuron (**threshold logic unit, TLU**라고 부름)은
  - 입력들의 **weighted sum**을 계산한다.
    - z = w₁x₁ + w₂x₂ + ⋯ + wₙxₙ = **xᵀw**
  - 그 합에 step function(즉, **activation function**, 활성 함수)을 적용하고 그 결과를 출력한다.
    - h_w(x) = step(z) = step(xᵀw)

[그림] 입력 x₁, x₂, x₃ → weight w₁, w₂, w₃ → Σ(weighted sum) → step function → 출력 h_w(x)

## 슬라이드 4. Binary Classifier Using Perceptron (퍼셉트론을 이용한 이진 분류기)

- 퍼셉트론을 이용한 이진 분류기: **h_{w,b}(x) = φ(xᵀw + b)**
  - **x**: 입력 feature (n×1 행렬)
  - **w**: weight (n×1 행렬)
  - **b**: bias (1×1 행렬)
  - **φ**: activation function

[그림] 값이 항상 1인 입력 x₀와 그 weight w₀가 bias 역할을 한다.

## 슬라이드 5. Single-Layer Perceptron (단층 퍼셉트론)

- 하나의 fully connected layer: **h_{W,b}(X) = φ(WX + b)**
  - **X**: 입력 feature (n×1 행렬)
  - **W**: weight (m×n 행렬)
  - **b**: bias (m×1 행렬)
  - **φ**: activation function
  - W와 b가 **Parameters**(학습되는 값)이다.
- 행렬 크기: (m×n)(n×1) + (m×1) = m×1

[그림] 입력 2개와 출력 3개를 가진 퍼셉트론. Bias neuron(항상 1을 출력)과 Input neuron(값을 그대로 전달, passthrough)이 Input layer를 이루고, TLU 3개가 Output layer를 이룬다.

## 슬라이드 6. Single-Layer Perceptron (cont.)

[그림] Iris 예시. 입력: Petal Width(x₁), Petal Length(x₂) / 출력: Setosa, Versicolor, Virginica

## 슬라이드 7. Last Check-in Quiz (지난 시간 체크인 퀴즈)

- 우리의 퍼셉트론은 다음으로 구성된다.
  ```
  W = [[-0.8, -1.2 ],   # Setosa         b = [[-0.4 ],   # Setosa
       [ 0.1, -0.05],   # Versicolor          [-0.01],   # Versicolor
       [ 0.7,  1.3 ]]   # Virginica           [ 0.5 ]]   # Virginica
  ```
  activation function은 Heaviside이다.
- 입력이 Petal Width = 0.2, Petal Length = 1.4일 때, 예측 클래스는 무엇인가?

## 슬라이드 8. Implementation (구현)

```python
import numpy as np

# Petal Width = 0.2, Petal Length = 1.4
x = np.array([[0.2], [1.4]])        # Shape: (2, 1)

W = np.array([
    [-0.8, -1.2],    # Setosa의 weight
    [ 0.1, -0.05],   # Versicolor의 weight
    [ 0.7,  1.3]     # Virginica의 weight
])                                   # Shape: (3, 2)

b = np.array([
    [-0.4],          # Setosa의 bias
    [-0.01],         # Versicolor의 bias
    [ 0.4]           # Virginica의 bias
])                                   # Shape: (3, 1)

# z = W * x + b
z = np.matmul(W, x) + b              # Shape: (3, 1)

# Heaviside (z >= 0이면 1)
y = np.where(z >= 0, 1, 0)

print("z = \n", z)
print("h = \n", y)
```

## 슬라이드 9. Multi-Layer Perceptron (다층 퍼셉트론)

| Single-Layer Perceptron (원래 형태)  | Multi-Layer Perceptron (현대)                       |
|--------------------------------------|-----------------------------------------------------|
| input layer와 output layer로 구성    | input layer, output layer, **hidden layer**로 구성  |

## 슬라이드 10. Implementation (구현) — Hidden Layer

```python
################
# Hidden Layer #
################
# Petal Width = 0.2, Petal Length = 1.4
input_features = np.array([[0.2], [1.4]])

hidden_layer_W = np.array([
    [ 0.5, -0.3],
    [-0.2,  0.8],
    [ 0.1,  0.4],
    [-0.6, -0.1]
])                                   # Shape: (4, 2)

hidden_layer_b = np.array([
    [ 0.1],
    [-0.2],
    [ 0.0],
    [ 0.3]
])                                   # Shape: (4, 1)

# z = W * x + b
hidden_layer_z = np.matmul(hidden_layer_W, input_features) + hidden_layer_b   # Shape: (4, 1)

# Heaviside (z >= 0이면 1)
hidden_layer_y = np.where(hidden_layer_z >= 0, 1, 0)                           # Shape: (4, 1)
```

## 슬라이드 11. Implementation (cont.) — Output Layer

**이 코드의 신경망을 그려볼 수 있는가?**

```python
################
# Output Layer #
################
output_layer_W = np.array([
    [-0.8, -1.2,  0.5, -0.2],   # Setosa
    [ 0.1, -0.05, 0.3,  0.1],   # Versicolor
    [ 0.7,  1.3, -0.4,  0.8]    # Virginica
])                               # Shape: (3, 4)

output_layer_b = np.array([
    [-0.4],                      # Setosa
    [-0.01],                     # Versicolor
    [ 0.4]                       # Virginica
])                               # Shape: (3, 1)

# z = W * x + b
output_layer_z = np.matmul(output_layer_W, hidden_layer_y) + output_layer_b   # Shape: (3, 1)

# Heaviside (z >= 0이면 1)
output_layer_y = np.where(output_layer_z >= 0, 1, 0)                           # Shape: (3, 1)

print("z = \n", output_layer_z)
print("y = \n", output_layer_y)
print("=> Predicted Class: ", np.argmax(output_layer_y, axis=0))
```

## 슬라이드 12. Neural Network Architecture (신경망 구조)

- 입력 feature 2개로 클래스 3개를 분류하는 신경망
  - neuron 4개짜리 hidden layer 하나
- 층 번호와 neuron 수: l = 0, 1, 2 / n₀ = 2, n₁ = 4, n₂ = 3
- **Parameter**
  - **w_{l,i,j}**: l ∈ {0, …, L−1}, i ∈ {0, …, n_{l−1}−1}, j ∈ {0, …, n_l−1}
  - **b_{l,j}**: l ∈ {0, …, L−1}, j ∈ {0, …, n_l−1}
  - L: layer 수
  - n_l: l번째 layer의 neuron 수
- 예시 (빨간 neuron):
  - z₁,₃ = o₀,₀·w₁,₀,₃ + o₀,₁·w₁,₁,₃ + b₁,₃
  - o₁,₃ = heaviside(z₁,₃)
- [그림] 초록 점선은 w₁,₁,₂ (입력 1번 → 은닉 2번), 파란 점선은 w₂,₀,₁ (은닉 0번 → 출력 1번)

## 슬라이드 13. Activation Function (활성 함수) (revisit)

| 이름                           | 식                                   |
|--------------------------------|--------------------------------------|
| Identity                       | x                                    |
| Binary step = Heaviside        | 0 (x < 0), 1 (x ≥ 0)                 |
| Logistic = Sigmoid             | 1 / (1 + e⁻ˣ)                        |
| Hyperbolic tangent (tanh)      | (eˣ − e⁻ˣ) / (eˣ + e⁻ˣ)              |
| Rectified linear unit (ReLU)   | 0 (x ≤ 0), x (x > 0) = max(0, x)     |
| Softmax                        | e^{xᵢ} / Σⱼ₌₁ᴶ e^{xⱼ}, i = 1, …, J   |

## 슬라이드 14. Activation Functions — ReLU

```python
########################
# Activation Functions #
########################
import torch
import torch.nn.functional as F

x = torch.tensor(output_layer_z)

# ReLU: max(0, x)
relu_output = F.relu(x)
print('--- ReLU ---')
print(relu_output)
print("=> Predicted Class: ", np.argmax(relu_output, axis=0))
```

## 슬라이드 15. Activation Functions (cont.) — Sigmoid, Softmax

```python
# Sigmoid: 1 / (1 + exp(-x))
sigmoid_output = torch.sigmoid(x)
print('--- Sigmoide ---')
print(sigmoid_output)
print("=> Predicted Class: ", np.argmax(sigmoid_output, axis=0))

# Softmax: exp(x) / sum(exp(x))
softmax_output = F.softmax(x, dim=0)
print('--- Softmax ---')
print(softmax_output)
print("=> Predicted Class: ", np.argmax(softmax_output, axis=0))
```

## 슬라이드 16. Softmax Activation Function

- Softmax = Softargmax ⇒ **분류(classification)에 널리 쓰인다**
  - 참고: **argmax**는 함수의 출력값이 최대가 되는 입력 지점을 반환한다.
  - `print("=> Predicted Class: ", np.argmax(output_layer_y, axis=0))`
  - [그림] Heaviside 출력 y = [0, 1, 1] → Predicted Class: [1]
- J개의 실수를 J개의 가능한 결과에 대한 **확률 분포**로 바꾸기 위해 ⇒ **음이 아니고(non-negative), 합이 1**
  - e^{xᵢ} / Σⱼ₌₁ᴶ e^{xⱼ}, i = 1, …, J
  - [그림] 같은 z = [−1.3, 0.34, 2.1]에 Softmax를 적용 → [0.0277, 0.1427, 0.8296] → Predicted Class: [2]
  - [그림] eˣ 그래프: (0, 1), (1, e)를 지나며 급격히 증가

## 슬라이드 17. Implementation with PyTorch (PyTorch로 구현)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MLP(nn.Module):
    def __init__(self):
        super().__init__()

        # 랜덤 초기화
        self.hidden_layer = nn.Linear(2, 4)
        self.output_layer = nn.Linear(4, 3)
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        # Hidden layer
        hidden_z = self.hidden_layer(x)
        hidden_o = self.sigmoid(hidden_z)

        # Output layer
        output_z = self.output_layer(hidden_o)
        output_o = self.softmax(output_z)

        return hidden_z, hidden_o, output_z, output_o

model = MLP()
```

## 슬라이드 18. Implementation with PyTorch (cont.)

```python
# Petal Width = 0.2, Petal Length = 1.4
x = torch.tensor([[0.2, 1.4]])

hidden_z, hidden_o, output_z, output_o = model(x)
predicted_class = output_z.argmax(dim=1).item()

print("Hidden layer z:\n", hidden_z)
print("Hidden layer o:\n", hidden_o)
print("Output layer z:\n", output_z)
print("Output layer o:\n", output_o)

class_names = ["Setosa", "Versicolor", "Virginica"]
print("=> Predicted class:", class_names[predicted_class])
```

## 슬라이드 20. Today... (오늘은...)

*주차별 강의계획은 상황에 따라 변경될 수 있음

| 주차 | 강의 내용                 | 비고        |
|------|---------------------------|-------------|
| 1    | 과목 및 인공지능 소개     |             |
| 2    | 문제해결                  |             |
| 3    | 지식과 추론 (1)           | 과제 1 공지 |
| 4    | 지식과 추론 (2)           |             |
| 5    | 기계학습 기초             |             |
| 6    | 신경망 (1)                | 과제 1 마감 |
| 7    | **신경망 (2)** ← 오늘     |             |
| 8    | 중간고사                  |             |

## 슬라이드 21. Outline (목차)

- Softmax Activation Function
- Neural Network Training (신경망 학습)
- Loss Function (손실 함수)
- Neural Network Training Process (신경망 학습 과정)
- Propagation (전파)
- Backpropagation and Optimizer (역전파와 옵티마이저)
- MNIST Dataset
- Batch and Epoch

## 슬라이드 22. Neural Network Training (신경망 학습)

- (loss function으로부터 나온) **오차를 최소화하는 model parameter를 찾는 것**
- 신경망은 training set에 대한 전체 "loss"를 최소화하도록 학습된다.

[그림] Weight W로 **Forward Propagation** → Predicted Output을 Ground-truth와 비교 → **Loss Function: L**

## 슬라이드 23. Loss Function (손실 함수)

- 모델의 예측이 올바른 정답(ground-truth)에서 얼마나 벗어났는지를 계산해 **모델 성능을 측정**한다.
- 모델을 최적화한다는 것은 loss function의 출력을 최소화하도록 model parameter를 조정하는 것이다.
- 모델의 예측이 정확하면 loss가 작고, 예측이 부정확하면 loss가 크다.
- **error function** 또는 **cost function**이라고도 부른다.

## 슬라이드 24. Loss Function (cont.)

| Regression (회귀)                       | Classification (분류)                                |
|-----------------------------------------|------------------------------------------------------|
| Mean squared error (MSE)                | Binary/Categorical cross-entropy (one-hot 벡터용)    |
| Root mean squared error (RMSE)          | Sparse categorical cross-entropy (정수 레이블용)     |
| Mean squared logarithmic error (MSLE)   | Hinge loss                                           |
| Mean absolute error (MAE)               | Kullback-Leibler Divergence Loss (KL Divergence)     |
| Huber loss                              |                                                      |

- **단순한 평가 지표가 아니다. loss를 최소화하도록 model parameter를 최적화하는 알고리즘의 입력으로 쓰인다.**

## 슬라이드 25. Neural Network Training Process (신경망 학습 과정)

1. parameter를 초기화한다 (랜덤 값 또는 0으로)
   - 때로는... '**pretrained parameters**'(사전 학습된 파라미터)를 사용할 수도 있다.
2. 반복:
   - 2-1) 출력을 계산한다 (**forward propagation**으로)
   - 2-2) 오차 L을 계산한다 (**loss function**으로부터)
   - 2-3) gradient를 계산한다 (**backpropagation**으로)
   - 2-4) loss를 최소화하도록 parameter를 업데이트한다 (**gradient descent** 같은 최적화 기법으로)

## 슬라이드 26. Propagation (전파)

η (eta): learning rate

- **Forward Propagation**: Weight W로 계산 → Predicted Output과 Ground-truth로 **Loss Function: L** 계산
- **Backward Propagation**: **Gradient: ∂L/∂W** 계산 (출력에서 입력 방향)
- **Weight Update: ΔW** = −η · ∂L/∂W
- **W⁽ᵗ⁺¹⁾ = W⁽ᵗ⁾ + ΔW**

## 슬라이드 27. Backpropagation (역전파)

- **뒤쪽 layer부터** gradient를 계산한다.
- [그림] Forward Propagation(→)으로 loss L을 구한 뒤, Backward Propagation(= Backpropagation, ←)으로 Gradient ∂L/∂W를 출력층부터 입력층 방향으로 계산

## 슬라이드 28. Optimizer (gradient descent 알고리즘은 다루지 않음)

- parameter를 **어떻게 업데이트할지** 정하는 방법
- 예: **Gradient Descent (GD)**
  - **W := W − η · ∂L/∂W**
  - W: parameter
  - L: loss
  - η: learning rate
- 최적화 알고리즘: GD, SGD, AdaGrad, RMSProp, Adam 등
- [그림] 가로축 Parameter(W), 세로축 Loss(L)인 곡선. 현재 점의 접선 기울기가 Gradient = ∂L/∂W

## 슬라이드 29. Learning Rate (학습률)

- 최적화 알고리즘의 각 단계에서 모델이 parameter를 **얼마나 조정할지** (**step size**라고도 부름)
- 다양한 learning rate schedule: step decay, exponential decay 등
- [그림 왼쪽] learning rate가 너무 크면 → 최솟값을 계속 지나치며 이리저리 튄다.
- [그림 오른쪽] learning rate가 너무 작으면 → 아주 조금씩 움직여 가까운 local minimum에 머문다.

## 슬라이드 30. Example (예제)

- hidden layer가 하나인 얕은(shallow) 신경망
- 입력: x₀ = 0.35, x₁ = 0.7
- 입력 → 은닉: w₁,₀,₀ = 0.2, w₁,₀,₁ = 0.3, w₁,₁,₀ = 0.2, w₁,₁,₁ = 0.3
- 은닉 → 출력: w₂,₀,₀ = 0.3, w₂,₁,₀ = 0.9

## 슬라이드 31. Example (cont.)

- activation function이 sigmoid라고 하자.
  - z₁,₀ = 0.2 × 0.35 + 0.2 × 0.7 = 0.21 → o₁,₀ = sigmoid(z₁,₀) = 0.5522
  - z₁,₁ = 0.3 × 0.35 + 0.3 × 0.7 = 0.315 → o₁,₁ = sigmoid(z₁,₁) = 0.5781
  - z₂,₀ = 0.3 × 0.5522 + 0.9 × 0.5781 = 0.686 → o₂,₀ = sigmoid(z₂,₀) = 0.665

## 슬라이드 32. Example (cont.) (gradient 계산법은 다루지 않음)

- loss function이 L = (ŷ − y)²이라고 하자.
  - y = 0.5, o₂,₀ = 0.665 = ŷ
  - L = (ŷ − y)² = (0.5 − 0.665)²
- δ₂,₀ = 2(o₂,₀ − y) × o₂,₀(1 − o₂,₀)
  = 2(0.665 − 0.5) × 0.665(1 − 0.665)
  = **0.0735**

## 슬라이드 33. Example (cont.) (gradient 계산법은 다루지 않음)

η (eta): learning rate, δ (delta): error

- **Backpropagation은 gradient를 계산하는 것이다.**
- δ₁,₀ = o₁,₀(1 − o₁,₀)(w₂,₀,₀ × δ₂,₀)
  = 0.5522 × (1 − 0.5522) × (0.3 × 0.0735)
  = **0.0055**

## 슬라이드 34. Example (cont.) (gradient 계산법은 다루지 않음)

- δ₁,₁ = o₁,₁(1 − o₁,₁)(w₂,₁,₀ × δ₂,₀)
  = 0.5781 × (1 − 0.5781) × (0.9 × 0.0735)
  = **0.0161**

## 슬라이드 35. Example (cont.) (parameter 업데이트 방법은 다루지 않음)

- learning rate 1.0으로 gradient descent 수행 (**Δw_{l,i,j} = −η · δ_{l,j} · o_{l−1,i}**)
- Δw₂,₀,₀ = −η · δ₂,₀ · o₁,₀ = −1.0 × 0.0735 × 0.5522 = −0.0406
- w₂,₀,₀ = w₂,₀,₀ + Δw₂,₀,₀ = 0.3 + (−0.0406) = **0.2594**

## 슬라이드 36. Example (cont.) (parameter 업데이트 방법은 다루지 않음)

- Δw₂,₁,₀ = −η · δ₂,₀ · o₁,₁ = −1.0 × 0.0735 × 0.5781 = −0.0425
- w₂,₁,₀ = w₂,₁,₀ + Δw₂,₁,₀ = 0.9 + (−0.0425) = **0.8575**

## 슬라이드 37. Example (cont.) (parameter 업데이트 방법은 다루지 않음)

- Δw₁,₁,₀ = −η · δ₁,₀ · o₀,₁ = −1.0 × 0.0055 × 0.7 = −0.0039
- w₁,₁,₀ = w₁,₁,₀ + Δw₁,₁,₀ = 0.2 + (−0.0039) = **0.1961**
- (o₀,₁ = x₁ = 0.7, 즉 입력층의 출력은 입력값 그대로)

## 슬라이드 38. Neural Network Training Process (revisit, 다시 보기)

1. parameter를 초기화한다 (랜덤 값 또는 0으로)
   - 때로는... 'pretrained parameters'를 사용할 수도 있다.
2. 반복:
   - 2-1) 출력을 계산한다 (forward propagation으로)
   - 2-2) 오차 L을 계산한다 (loss function으로부터)
   - 2-3) gradient를 계산한다 (backpropagation으로)
   - 2-4) loss를 최소화하도록 parameter를 업데이트한다 (gradient descent 같은 최적화 기법으로)
- **특정 조건(예: 정해진 횟수만큼 반복)을 만족할 때까지...**

## 슬라이드 39. MNIST Dataset

- 손글씨 숫자 이미지
- 클래스 수 = 10 (0~9)
- training data 수 = 60,000
- test data 수 = 10,000

## 슬라이드 40. MNIST Dataset (cont.)

- 전체 28×28 pixel
- 각 pixel은 값을 하나만 가진다.
  - 범위: [0, 255]
  - 정규화(regularized)한 범위: [0, 1]
  - 참고) RGB 컬러 이미지는 pixel마다 여러 개의 값을 가진다.
- 그렇다면...
  - input neuron은 몇 개?
  - output neuron은 몇 개?
- [그림] 숫자 7 이미지의 Pixel Intensity Matrix (28 × 28)

## 슬라이드 41. Fashion-MNIST Dataset

[그림] 10개 클래스 예시: T-shirt/top, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag, Ankle boot

## 슬라이드 42. Fashion-MNIST Dataset (cont.)

[그림] Label 9(Ankle boot) 이미지와 그 Pixel Intensity Matrix (28 × 28)

## 슬라이드 43. Implementation (구현)

```python
class our_first_nn(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.hidden_layer = nn.Linear(784, 128)
        self.sigmoid = nn.Sigmoid()
        self.output_layer = nn.Linear(128, 10)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.flatten(x)
        x = self.sigmoid(self.hidden_layer(x))
        x = self.output_layer(x)
        return x

model = our_first_nn().to(device)
```

## 슬라이드 44. Implementation (cont.) — 학습

```python
for epoch in range(epochs):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    indices = torch.randperm(len(train_dataset))
    for index in indices:
        image, label = train_dataset[index.item()]

        image = image.unsqueeze(0).to(device)
        label = torch.tensor([label], device=device)

        # Forward propagation
        logits = model(image)
        loss = criterion(logits, label)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()

        # weight와 bias 업데이트
        optimizer.step()

        total_loss += loss.item()
        prediction = logits.argmax(dim=1)
        correct += (prediction == label).sum().item()
        total += 1
```

## 슬라이드 45. Implementation (cont.) — 평가

```python
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for i in range(len(test_dataset)):
        image, label = test_dataset[i]
        image = image.unsqueeze(0).to(device)

        logits = model(image)
        probabilities = model.softmax(logits)
        prediction = probabilities.argmax(dim=1).item()

        if prediction == label:
            correct += 1

        total += 1
```

## 슬라이드 46. Batch

- training data를 하나씩(one by one) → **batch 단위로**(데이터의 묶음)
- 샘플 1개: **XW + b** = [x₁ ⋯ xₙ] (1×n) · W (n×m) + [b₁ … bₘ] (1×m) = **1×m**
- 샘플 s개: **XW + b** = X (s×n) · W (n×m) + b (s×m) = **s×m**
  - b의 각 행은 모두 **같다(Same)**.

## 슬라이드 47. Mini-batch

- **Full-batch**: training data 전체로 한 번에 학습
  - XW + b: (s×n)(n×m) + (s×m), b의 각 행은 같음
  - (장점) 계산이 더 빠르다
  - (단점) 메모리를 더 많이 쓴다
- **Mini-batch**: 더 작은 batch로 학습 (예: 16, 32)

## 슬라이드 48. Epoch

- **Epoch**: training set 전체를 한 번 학습하는 것
- 예: training data 1,000개, (mini-)batch size 100
  - 각 epoch마다,
    - training data를 (mini-)batch들로 나눈다 (100개 × 10 batch)
    - 각 batch마다 반복: 모델을 학습한다 = parameter를 업데이트한다
- [그림] 전체 training data(Whole training data)를 10개의 Mini-batch로 나눈 모습

## 슬라이드 49. Implementation (구현) — batching

```python
# batching
batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
```

## 슬라이드 50. Implementation (cont.) — batch 학습

```python
for epoch in range(epochs):
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        # Forward propagation
        logits = model(images)
        loss = criterion(logits, labels)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()

        # weight와 bias 업데이트
        optimizer.step()

        total_loss += loss.item() * labels.size(0)
        predictions = logits.argmax(dim=1)
        correct += (predictions == labels).sum().item()
        total += labels.size(0)
```

## 슬라이드 51. Implementation (cont.) — batch 평가

```python
model.eval()
correct = 0
total = 0

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        labels = labels.to(device)

        logits = model(images)
        probabilities = model.softmax(logits)
        predictions = probabilities.argmax(dim=1)

        correct += (predictions == labels).sum().item()
        total += labels.size(0)
```

## 슬라이드 53. Next Time... (다음 시간에는...)

8주차: 중간고사 (10월 20일 화요일 오후 6시 30분~7시 30분)

## 슬라이드 54~55. 중간고사 (원문이 한국어)

- 일시: 10월 20일 화요일 오후 6시 30분~7시 30분 (6시 20분까지 입실)
- 장소: 지하 대강당 (수업 강의실 아님)
- 준비물: 신분증/학생증, 계산기 (공학용 계산기가 필요한 문제 없음)
- 힌트노트: A4 단면 한 페이지 수기 작성 허용
- 시험 범위: Problem Solving (week 2) ~ Neural Networks (week 7)
- 문제 유형: T/F, 객관식, 단답형 주관식, 빈칸 채우는 손코딩 등 (코드는 python만)
- 자세한 내용은 `lecture_summary.md`의 "8부: 중간고사 안내" 참고

## 슬라이드 56. Reference (참고 자료)

- https://en.wikipedia.org/wiki/Backpropagation
- https://en.wikipedia.org/wiki/MNIST_database
