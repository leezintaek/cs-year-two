# Week7 강의 요약

**과목**: 인공지능개론(CSE2302) · **주제**: 신경망 (3) 다층 퍼셉트론 구현, 활성 함수, 신경망 학습(손실 함수·역전파·옵티마이저), MNIST, Batch와 Epoch
**강의일**: 2026-10-13(Lecture 01)

> ⚠️ **중간고사: 10월 20일(화) 오후 6:30~7:30, 지하 대강당** → 맨 아래 "8부: 중간고사 안내" 참고

---

## 1부: 지난 주차 복습 (퍼셉트론)

> 자세한 내용은 `week6/lecture_summary.md` 참고.

### 인공 신경망 (ANN)
- 인공 뉴런(노드)들이 **edge**로 연결된 구조
- 각 뉴런은 연결된 뉴런들로부터 신호(실수값)를 받아 처리한 뒤 다른 뉴런으로 보냄
- 각 연결의 신호 세기는 **weight(가중치)** 가 결정

### 퍼셉트론 (TLU, Threshold Logic Unit)
1. 입력의 가중합을 계산: z = w₁x₁ + w₂x₂ + … + wₙxₙ = **xᵀw**
2. 그 합에 step 함수(활성 함수 φ)를 적용: ŷ = step(z)

### 이진 분류기 / 단층 퍼셉트론
- 이진 분류기: h(x) = φ(**xᵀw** + b)
  - x: n×1 입력, w: n×1 가중치, b: 1×1 bias, φ: 활성 함수
- 단층 퍼셉트론 (fully connected layer 하나): **h(x) = φ(Wx + b)**
  - x: n×1, **W: m×n**, b: m×1 (m = 출력 뉴런 수)
  - 학습 대상 **파라미터 = W와 b**

### Check-in Quiz: Iris 단층 퍼셉트론
- 입력: Petal Width = 0.2, Petal Length = 1.4 / 활성 함수: Heaviside

```
W = [[-0.8, -1.2 ],   # Setosa         b = [[-0.4 ],   # Setosa
     [ 0.1, -0.05],   # Versicolor          [-0.01],   # Versicolor
     [ 0.7,  1.3 ]]   # Virginica           [ 0.5 ]]   # Virginica
```

| 클래스     | z = Wx + b                         | 출력 |
|------------|------------------------------------|------|
| Setosa     | −0.16 − 1.68 − 0.4 = **−2.24**     | 0    |
| Versicolor | 0.02 − 0.07 − 0.01 = **−0.06**     | 0    |
| Virginica  | 0.14 + 1.82 + 0.5 = **2.46**       | 1    |

→ 출력 [0, 0, 1] → 예측 클래스: **Virginica**
(※ 코드 구현 슬라이드에서는 Virginica의 bias가 0.4로 되어 있지만 결과는 같다.)

```python
z = np.matmul(W, x) + b      # (3,2)×(2,1) + (3,1) = (3,1)
y = np.where(z >= 0, 1, 0)   # Heaviside
```

---

## 2부: 다층 퍼셉트론 (MLP) 구현

### 단층 vs 다층
| 구분                         | 구성                                 |
|------------------------------|--------------------------------------|
| Single-Layer (Original)      | input layer + output layer           |
| Multi-Layer (Modern)         | input + **hidden** + output layer    |

### NumPy 구현 예제 (2 입력 → 은닉 4 → 출력 3)
```python
x = np.array([[0.2], [1.4]])                    # (2, 1)
hidden_layer_W = np.array([[ 0.5, -0.3],
                           [-0.2,  0.8],
                           [ 0.1,  0.4],
                           [-0.6, -0.1]])       # (4, 2)
hidden_layer_b = np.array([[0.1], [-0.2], [0.0], [0.3]])   # (4, 1)
hidden_layer_y = np.where(np.matmul(hidden_layer_W, x) + hidden_layer_b >= 0, 1, 0)

output_layer_W = np.array([[-0.8, -1.2,  0.5, -0.2],   # Setosa
                           [ 0.1, -0.05, 0.3,  0.1],   # Versicolor
                           [ 0.7,  1.3, -0.4,  0.8]])  # Virginica  (3, 4)
output_layer_b = np.array([[-0.4], [-0.01], [0.4]])     # (3, 1)
output_layer_y = np.where(np.matmul(output_layer_W, hidden_layer_y) + output_layer_b >= 0, 1, 0)
np.argmax(output_layer_y, axis=0)
```

직접 계산해 보면 (참고용):
- 은닉층 z = [−0.22, 0.88, 0.58, 0.04] → Heaviside → h = [0, 1, 1, 1]
- 출력층 z = [−1.3, 0.34, 2.1] → Heaviside → y = [0, 1, 1]
- `argmax`는 최댓값이 여러 개면 **첫 번째 인덱스**를 반환 → 1 (Versicolor)
- 같은 z에 ReLU/Sigmoid/Softmax를 쓰면 최댓값이 2.1 하나로 갈려 → 2 (Virginica)
  → Heaviside는 0/1만 내므로 클래스 간 "얼마나 더 큰지"를 구분하지 못한다.

### 신경망 구조 표기법
- 예: 입력 2개, 은닉 뉴런 4개, 클래스 3개 → l = 0, 1, 2 / n₀ = 2, n₁ = 4, n₂ = 3
- **w_{l,i,j}**: (l−1)층의 i번 뉴런 → l층의 j번 뉴런을 잇는 가중치
  - l ∈ {0, …, L−1}, i ∈ {0, …, n_{l−1}−1}, j ∈ {0, …, n_l−1}
- **b_{l,j}**: l층 j번 뉴런의 bias
- L: 층 수, n_l: l번째 층의 뉴런 수
- 예: z₁,₃ = o₀,₀·w₁,₀,₃ + o₀,₁·w₁,₁,₃ + b₁,₃, o₁,₃ = heaviside(z₁,₃)
  - o_{l,j}: l층 j번 뉴런의 출력 (o₀,ᵢ = 입력 xᵢ)

---

## 3부: 활성 함수 (Activation Function, revisit)

| 이름                 | 식                                   |
|----------------------|--------------------------------------|
| Identity             | x                                    |
| Binary step          | 0 (x < 0), 1 (x ≥ 0)                 |
| Sigmoid (Logistic)   | 1 / (1 + e⁻ˣ)                        |
| tanh                 | (eˣ − e⁻ˣ) / (eˣ + e⁻ˣ)              |
| ReLU                 | 0 (x ≤ 0), x (x > 0) = max(0, x)     |
| Softmax              | e^{xᵢ} / Σⱼ e^{xⱼ}  (i = 1, …, J)    |

- Binary step = Heaviside, Logistic = Sigmoid

### Softmax (= Softargmax)
- **분류 문제에서 가장 많이 쓰임**
- J개의 실수를 J개 결과에 대한 **확률 분포**로 변환 → 모두 **음이 아니고 합이 1**
- 참고: **argmax**는 함수값이 최대가 되는 입력(인덱스)을 반환

### PyTorch에서의 활성 함수
```python
import torch.nn.functional as F
F.relu(x)              # max(0, x)
torch.sigmoid(x)       # 1 / (1 + exp(-x))
F.softmax(x, dim=0)    # exp(x) / sum(exp(x))
```

### PyTorch로 MLP 구현
```python
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden_layer = nn.Linear(2, 4)   # 랜덤 초기화
        self.output_layer = nn.Linear(4, 3)
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        hidden_z = self.hidden_layer(x)
        hidden_o = self.sigmoid(hidden_z)
        output_z = self.output_layer(hidden_o)
        output_o = self.softmax(output_z)
        return hidden_z, hidden_o, output_z, output_o

x = torch.tensor([[0.2, 1.4]])                # (1, 2): 행 = 샘플
predicted_class = output_z.argmax(dim=1).item()
```
- `nn.Linear(in, out)`: 가중치와 bias를 가진 fully connected layer
- PyTorch는 입력을 **(샘플 수, feature 수)** 형태로 받으므로 softmax/argmax를 `dim=1`로 계산

---

## 4부: 신경망 학습 (Neural Network Training)

### 학습의 목표
- 손실 함수로 계산한 **오차를 최소화하는 모델 파라미터를 찾는 것**
- 훈련 세트 전체의 "loss" 합을 최소화하도록 학습

### 손실 함수 (Loss Function)
- 모델의 예측이 정답(ground-truth)에서 얼마나 벗어났는지 측정
- 예측이 정확하면 loss가 작고, 부정확하면 loss가 크다
- 모델 최적화 = 손실 함수의 출력을 최소화하도록 파라미터를 조정하는 것
- 다른 이름: **error function**, **cost function**

| 회귀 (Regression)  | 분류 (Classification)                     |
|--------------------|-------------------------------------------|
| MSE                | Binary/Categorical cross-entropy          |
| RMSE               | Sparse categorical cross-entropy          |
| MSLE               | Hinge loss                                |
| MAE                | KL Divergence                             |
| Huber loss         |                                           |

- Categorical cross-entropy: 정답이 **one-hot 벡터**일 때
- Sparse categorical cross-entropy: 정답이 **정수 레이블**일 때
- 손실 함수는 단순한 평가 지표가 아니라, **파라미터를 최적화하는 알고리즘의 입력**으로 쓰인다.

### 학습 과정
1. 파라미터 초기화 (랜덤 또는 0). 경우에 따라 **pretrained parameters** 사용
2. 반복:
   1. **Forward propagation**으로 출력 계산
   2. **손실 함수**로 오차 L 계산
   3. **Backpropagation**으로 gradient 계산
   4. **Gradient descent** 같은 최적화 기법으로 파라미터 업데이트
3. 특정 조건(예: 일정 횟수 반복)을 만족할 때까지 반복

### Propagation
- **Forward propagation**: 입력 → 출력 방향으로 예측값 계산 → ground-truth와 비교해 loss L 계산
- **Backward propagation (= Backpropagation)**: gradient ∂L/∂W를 **뒤쪽 층부터** 계산
- **Weight update**: ΔW = −η·∂L/∂W, **W⁽ᵗ⁺¹⁾ = W⁽ᵗ⁾ + ΔW**
  - η (eta): learning rate

### Optimizer
- 파라미터를 어떻게 업데이트할지 정하는 방법 (gradient descent 알고리즘 자체는 다루지 않음)
- 예: Gradient Descent (GD): **W := W − η·∂L/∂W**
  - gradient(기울기)의 **반대 방향**으로 이동해 loss를 줄인다
- 최적화 알고리즘 종류: GD, SGD, AdaGrad, RMSProp, Adam 등

### Learning Rate (학습률)
- 최적화의 각 단계에서 파라미터를 얼마나 조정할지 (= **step size**)
- 너무 작으면 수렴이 느리고, 너무 크면 최솟값을 지나쳐 발산할 수 있다
- learning rate schedule: step decay, exponential decay 등

---

## 5부: 계산 예제 (은닉층 1개짜리 얕은 신경망)

> 슬라이드에 "gradient 계산법·업데이트 방법은 다루지 않음"이라고 되어 있다. 흐름 이해용으로 보면 된다.

### 구조와 초기값 (활성 함수: sigmoid, bias 없음)
- 입력: x₀ = 0.35, x₁ = 0.7
- 입력 → 은닉: w₁,₀,₀ = 0.2, w₁,₀,₁ = 0.3, w₁,₁,₀ = 0.2, w₁,₁,₁ = 0.3
- 은닉 → 출력: w₂,₀,₀ = 0.3, w₂,₁,₀ = 0.9
- 구조: 입력 2개 → 은닉 뉴런 2개 (1,0), (1,1) → 출력 뉴런 1개 (2,0)

### ① Forward propagation
| 뉴런  | z                                     | o = sigmoid(z) |
|-------|---------------------------------------|----------------|
| (1,0) | 0.2×0.35 + 0.2×0.7 = 0.21             | 0.5522         |
| (1,1) | 0.3×0.35 + 0.3×0.7 = 0.315            | 0.5781         |
| (2,0) | 0.3×0.5522 + 0.9×0.5781 = 0.686       | 0.665          |

### ② Loss
- 손실 함수 L = (y − o)², 정답 y = 0.5
- L = (0.5 − 0.665)² ≈ 0.027

### ③ Backpropagation (δ: error)
- 출력층: δ₂,₀ = 2(o₂,₀ − y) × o₂,₀(1 − o₂,₀) = 2 × 0.165 × 0.665 × 0.335 = **0.0735**
- 은닉층: δ₁,ⱼ = o₁,ⱼ(1 − o₁,ⱼ) × (w₂,ⱼ,₀ × δ₂,₀)
  - δ₁,₀ = 0.5522 × 0.4478 × (0.3 × 0.0735) = **0.0055**
  - δ₁,₁ = 0.5781 × 0.4219 × (0.9 × 0.0735) = **0.0161**
- 참고: o(1 − o)는 sigmoid의 미분값

### ④ Gradient descent로 업데이트 (η = 1.0)
- 공식: **Δw_{l,i,j} = −η · δ_{l,j} · o_{l−1,i}**, w ← w + Δw

| 가중치  | Δw                                 | 새 값  |
|---------|------------------------------------|--------|
| w₂,₀,₀  | −1.0 × 0.0735 × 0.5522 = −0.0406   | 0.2594 |
| w₂,₁,₀  | −1.0 × 0.0735 × 0.5781 = −0.0425   | 0.8575 |
| w₁,₁,₀  | −1.0 × 0.0055 × 0.7 = −0.0039      | 0.1961 |

- 나머지 가중치도 같은 방식으로 업데이트한다. 이 과정을 조건을 만족할 때까지 반복하는 것이 학습이다.

---

## 6부: MNIST 데이터셋과 PyTorch 학습 코드

### MNIST
- 손글씨 숫자 이미지 / 클래스 10개 (0~9)
- 훈련 데이터 60,000개, 테스트 데이터 10,000개
- 28×28 = 784 픽셀, 각 픽셀은 값 1개 (흑백)
  - 범위 [0, 255] → 정규화하면 [0, 1]
  - 참고: RGB 컬러 이미지는 픽셀마다 여러 값을 가짐
- **입력 뉴런 수 = 784, 출력 뉴런 수 = 10**
- **Fashion-MNIST**: 같은 형식(28×28 흑백, 10클래스)의 옷·신발 이미지 데이터셋

### 모델 정의 (784 → 128 → 10)
```python
class our_first_nn(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()               # 28×28 → 784
        self.hidden_layer = nn.Linear(784, 128)
        self.sigmoid = nn.Sigmoid()
        self.output_layer = nn.Linear(128, 10)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.flatten(x)
        x = self.sigmoid(self.hidden_layer(x))
        x = self.output_layer(x)
        return x                                  # logits (softmax 전 값)

model = our_first_nn().to(device)
```

### 학습 루프 (데이터 1개씩)
```python
for epoch in range(epochs):
    model.train()
    indices = torch.randperm(len(train_dataset))   # 매 epoch마다 순서 섞기
    for index in indices:
        image, label = train_dataset[index.item()]
        image = image.unsqueeze(0).to(device)      # 배치 차원 추가
        label = torch.tensor([label], device=device)

        logits = model(image)                      # Forward propagation
        loss = criterion(logits, label)            # Loss 계산

        optimizer.zero_grad()                      # 이전 gradient 초기화
        loss.backward()                            # Backpropagation
        optimizer.step()                           # 가중치·bias 업데이트
```

### 평가
```python
model.eval()
with torch.no_grad():                              # gradient 계산 안 함
    for i in range(len(test_dataset)):
        logits = model(image)
        probabilities = model.softmax(logits)
        prediction = probabilities.argmax(dim=1).item()
```

| 코드                    | 역할                              |
|-------------------------|-----------------------------------|
| `model.train()`         | 학습 모드                         |
| `model.eval()`          | 평가 모드                         |
| `optimizer.zero_grad()` | 누적된 gradient 초기화            |
| `loss.backward()`       | backpropagation (gradient 계산)   |
| `optimizer.step()`      | 파라미터 업데이트                 |
| `torch.no_grad()`       | 평가 시 gradient 계산 끄기        |

---

## 7부: Batch와 Epoch

### Batch
- 데이터를 하나씩(one by one) → **묶음(batch) 단위**로 학습
- 샘플 1개: **XW + b** → (1×n)(n×m) + (1×m) = **1×m**
- 샘플 s개: X를 s×n 행렬로 쌓으면 → (s×n)(n×m) + (s×m) = **s×m**
  - b는 모든 행에 **같은 값**이 복사되어 더해짐 (broadcasting)
  - 즉, 행렬곱 한 번으로 s개 샘플을 동시에 계산

| 방식        | 설명                         | 장단점                       |
|-------------|------------------------------|------------------------------|
| Full-batch  | 훈련 데이터 전체를 한 번에   | 계산 빠름 / 메모리 많이 씀   |
| Mini-batch  | 작은 묶음 (예: 16, 32)       | 둘 사이의 절충               |

### Epoch
- **훈련 세트 전체를 한 번 학습하는 것**
- 예: 훈련 데이터 1,000개, batch size 100
  - 매 epoch마다 데이터를 100개씩 10개의 batch로 나눔
  - batch마다 모델 학습(= 파라미터 업데이트) → **epoch 1번당 업데이트 10번**

### PyTorch에서 batch 적용
```python
batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader  = DataLoader(test_dataset,  batch_size=batch_size, shuffle=False)

for epoch in range(epochs):
    model.train()
    for images, labels in train_loader:          # 32개씩 꺼냄
        logits = model(images)
        loss = criterion(logits, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * labels.size(0)
        correct += (logits.argmax(dim=1) == labels).sum().item()
        total += labels.size(0)
```
- 훈련 데이터는 `shuffle=True`로 섞고, 테스트 데이터는 섞지 않음
- `loss.item()`은 batch 평균 loss이므로 `labels.size(0)`(batch 크기)를 곱해 합계로 누적

---

## 8부: 중간고사 안내

| 항목      | 내용                                         |
|-----------|----------------------------------------------|
| 일시      | **10/20(화) 오후 6:30~7:30**                 |
| 입실      | 오후 6:20까지 (10분 전)                      |
| 장소      | **지하 대강당** (수업 강의실 아님)           |
| 준비물    | 신분증/학생증, 계산기                        |
| 범위      | Problem Solving(2주차) ~ 신경망(7주차)       |

- 계산기: 공학용 계산기가 필요한 문제는 없음
- 힌트노트: 필요하면 **A4 한 장 단면, 손으로 쓴 것**만 허용 (시험 전 확인, 부적합하면 사용 제한)
- 영문 시험지: 10/16까지 inha.data@gmail.com으로 요청
- 문제 유형: T/F, 객관식, 단답형 주관식, 빈칸 채우는 손코딩 등
  - 코드 문제는 모두 **python**으로만 출제
  - 손코딩에서 약간의 문법 오류는 허용 (의도 전달이 중요)
- 오피스아워 (질의응답)
  - 10/19(월) 11:00~16:00 @하-1412 (윤진이 교수)
  - 10/19(월) 16:00~21:00 @하-1210 (강신우 조교)
  - 10/20(화) 수업 시간 @하-1412 (윤진이 교수)
  - 상시: inha.unilab@gmail.com
- 시험 전 마지막 수업 **10/15(목)** 꼭 참석
