# 인공지능개론 강의자료 Python 코드 모음

강의 PDF(week1 ~ week7)에 나온 Python 코드만 뽑아서 정리한 파일이다.

- 실제 Python 코드가 있는 강의: **week5_2, week6_1, week6_2, week7_1**
- week1 ~ week5_1에는 Python 코드가 없다. (week2의 탐색 알고리즘은 pseudocode)
- week6_1은 week5_2 코드(Decision Tree)를 복습용으로 다시 보여주므로 중복은 한 번만 적었다.
- PDF가 2단 레이아웃이라 텍스트가 섞여 있던 부분은 원래 코드 순서대로 재배열했다. 코드 내용 자체는 바꾸지 않았다.
- 각 섹션 제목 옆에 출처 슬라이드(`weekN_M, p.페이지`)를 적었다.

---

## 목차

1. Iris 분류 (Decision Tree Classifier) — week5_2 / week6_1
2. California Housing 회귀 (Decision Tree Regressor) — week5_2 / week6_1
3. Decision Tree 시각화 — week5_2 / week6_1
4. Single-Layer Perceptron (NumPy) — week6_2 / week7_1
5. Multi-Layer Perceptron (NumPy) — week7_1
6. 활성 함수 (PyTorch) — week7_1
7. MLP 구현 (PyTorch `nn.Module`) — week7_1
8. Fashion-MNIST 신경망 학습 (한 개씩 학습) — week7_1
9. Fashion-MNIST 신경망 학습 (Mini-batch) — week7_1

---

## 1. Iris 분류 (Decision Tree Classifier)

출처: week5_2 p.29 ~ 44 (week6_1 p.7 에서 복습)

### 1-1. Hugging Face에서 Iris 데이터셋 불러오기

```python
import pandas as pd
from datasets import load_dataset

dataset = load_dataset("scikit-learn/iris", split="train")
df = dataset.to_pandas()

print(df.head(10).to_string(index=False))
```

**설명**

- `datasets` 라이브러리(Hugging Face)의 `load_dataset`으로 Iris 데이터셋을 받아온다.
  - `"scikit-learn/iris"`: Hugging Face Hub에 올라온 데이터셋 이름
  - `split="train"`: train split을 가져온다 (Iris는 이 split 하나에 150개 전부 들어있음)
- `dataset.to_pandas()`: Hugging Face `Dataset` 객체를 pandas `DataFrame`으로 변환
- `df.head(10)`: 앞 10행만 출력. `to_string(index=False)`는 행 번호(index) 없이 출력한다는 뜻
- 컬럼: `Id`, `SepalLengthCm`(꽃받침 길이), `SepalWidthCm`(꽃받침 너비), `PetalLengthCm`(꽃잎 길이), `PetalWidthCm`(꽃잎 너비), `Species`(꽃 종류)

### 1-2. X (input)와 y (output) 나누기

```python
# 꽃받침의 길이/너비, 꽃잎의 길이/너비 (4개의 input features) -> 꽃종류 (1개의 output)
X = df[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]]
y = df["Species"]  # 3개의 class를 가지고 있음 (setosa, versicolor, virginica)

print("===================================================================")
print(X.head(10).to_string(index=False))
print("===================================================================")
print(y.head(10).to_string(index=False))
print("===================================================================")
```

**설명**

- `X`: **feature**(입력 변수) 4개를 고른 DataFrame. 대괄호 두 겹 `[[...]]` → 여러 컬럼을 고르면 DataFrame이 된다.
- `y`: **label(target)**, 즉 정답 컬럼. 대괄호 한 겹 `["Species"]` → Series가 된다.
- `Id` 컬럼은 단순 번호라서 feature에서 뺐다.
- class는 3개: Iris-setosa, Iris-versicolor, Iris-virginica

### 1-3. Training data / Test data 나누기

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,     # 전체 데이터의 20%를 test set으로 사용
    random_state=42,   # 돌릴 때마다 같게 분할되기 위하여 시드 고정
    stratify=y         # y 기준으로 균일하게 분할
)

print("# Training data:", len(X_train))
print("# Test data:", len(X_test))
```

**설명**

- `train_test_split`은 데이터를 섞은 뒤 training set과 test set으로 나눈다.
- 반환 순서가 `X_train, X_test, y_train, y_test`인 점 주의 (X 둘 먼저, y 둘 나중)
- `test_size=0.2`: 150개 중 20%인 30개를 test로, 120개를 training으로 사용
  - 출력: `# Training data: 120`, `# Test data: 30`
- `random_state=42`: 난수 시드를 고정해서 실행할 때마다 같은 결과로 나뉘게 함 (재현성)
- `stratify=y`: 각 class의 비율을 training/test에서 동일하게 유지
  - Iris는 class별 50개씩이므로 test set 30개 = class별 10개씩

### 1-4. 학습(Training)과 예측(Testing)

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    criterion="gini",   # 어떤 feature와 threshold로 나눌지 선택하는 기준
    max_depth=3,        # tree의 최대 depth를 3으로 제한
    random_state=42
)

model.fit(X_train, y_train)      # training
y_pred = model.predict(X_test)   # testing
```

**설명**

- `DecisionTreeClassifier`: 분류(classification)용 Decision Tree
- `criterion="gini"`: 분기 규칙(어떤 feature, 어떤 threshold)을 고를 때 **Gini impurity**가 가장 많이 줄어드는 쪽을 선택 (greedy 방식)
- `max_depth=3`: tree 깊이를 3으로 제한 → 너무 깊어져서 overfitting 되는 것을 막음
- `fit(X_train, y_train)`: training set으로 모델 학습 (decision rule을 찾음)
- `predict(X_test)`: 학습된 모델로 test set의 class를 예측 → `y_pred`
- sklearn 모델은 대부분 `모델 생성 → fit → predict` 3단계 패턴을 따른다.

### 1-5. 성능 측정: Accuracy, Error rate

```python
correct = 0
for actual, predicted in zip(y_test, y_pred):
    if actual == predicted:
        correct += 1

accuracy = correct / len(y_test)
error_rate = (len(y_test) - correct) / len(y_test)

print("Test Accuracy:", accuracy * 100.0)
print("Error Rate:", error_rate * 100.0)
```

**설명**

- `zip(y_test, y_pred)`: 정답(`actual`)과 예측(`predicted`)을 한 쌍씩 묶어서 순회
- 정답과 예측이 같으면 `correct`를 1 증가
- accuracy = (맞힌 개수) / (test 샘플 수)
- error rate = (틀린 개수) / (test 샘플 수) = 1 − accuracy
- `* 100.0`으로 퍼센트(%) 단위로 출력
- 분류(classification) 문제에서 주로 쓰는 지표

---

## 2. California Housing 회귀 (Decision Tree Regressor)

출처: week5_2 p.48 ~ 57

### 2-1. 데이터셋 다운로드 & X, y 나누기

```python
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing(as_frame=True)
print("===================================================================")
print(housing.frame.head(10).to_string(index=False))

X = housing.data
y = housing.target

print("===================================================================")
print(X.head(10).to_string(index=False))
print("===================================================================")
print(y.head(10).to_string(index=False))
print("===================================================================")
```

**설명**

- `fetch_california_housing`: sklearn에 내장된 캘리포니아 집값 데이터셋을 받아온다.
- `as_frame=True`: 결과를 pandas DataFrame/Series 형태로 받음
  - `housing.frame`: feature + target이 모두 들어있는 전체 표
  - `housing.data`: input feature 8개 (`MedInc`, `HouseAge`, `AveRooms`, `AveBedrms`, `Population`, `AveOccup`, `Latitude`, `Longitude`)
  - `housing.target`: output `MedHouseVal` (집값 중앙값, 연속값)
- Iris와 달리 output이 **연속적인 숫자** → regression 문제

### 2-2. Training data / Test data 나누기

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,     # 전체 데이터의 20%를 test set으로 사용
    random_state=42,   # 돌릴 때마다 같게 분할되기 위하여 시드 고정
)

print("# Training data:", len(X_train))
print("# Test data:", len(X_test))
```

**설명**

- Iris 버전과 거의 같지만 **`stratify`가 없다.**
  - `stratify`는 class 비율을 맞추는 옵션인데, regression의 y는 연속값이라 class가 없으므로 쓰지 않는다.

### 2-3. 학습과 예측

```python
from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor(
    criterion="squared_error",  # 어떤 feature와 threshold로 나눌지 선택하는 기준
    max_depth=5,                # tree의 최대 depth를 5로 제한
    random_state=42
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

**설명**

- `DecisionTreeRegressor`: 회귀(regression)용 Decision Tree
- `criterion="squared_error"`: 분기 후 각 노드 안의 값들의 **squared error(분산)** 가 가장 작아지도록 분기 규칙을 선택
  - 분류에서는 `"gini"`, 회귀에서는 `"squared_error"` — 이 대응을 기억할 것
- leaf에 도착하면 그 leaf에 속한 training 샘플들의 **평균값**을 예측값으로 출력
- `max_depth=5`: Iris보다 feature가 많고 복잡하므로 depth를 5로 설정

### 2-4. 성능 측정: MAE, RMSE

```python
total_error = 0
for actual, predicted in zip(y_test, y_pred):
    total_error += abs(actual - predicted)
mae = total_error / len(y_test)
print("MAE (Mean Absolute Error):", mae)

total_squared_error = 0
for actual, predicted in zip(y_test, y_pred):
    total_squared_error += (actual - predicted) ** 2.0
rmse = (total_squared_error / len(y_test)) ** 0.5
print("RMSE (Root Mean Squared Error):", rmse)
```

**설명**

- **MAE** = (1/m) Σ |ŷᵢ − yᵢ| : 오차 절댓값의 평균
- **MSE** = (1/m) Σ (ŷᵢ − yᵢ)² : 오차 제곱의 평균
- **RMSE** = √MSE : 코드에서는 `** 0.5`로 제곱근을 계산
- MSE/RMSE는 오차를 제곱하므로 **큰 오차에 더 큰 penalty**를 준다.
  - 예) 오차 {1, −2, 3, 4, 5} → MAE = 3, RMSE ≈ 3.3
  - 예) 오차 {1, −2, 3, 4, 100} → MAE = 22, RMSE ≈ 44.8
- 회귀(regression) 문제에서 주로 쓰는 지표

---

## 3. Decision Tree 시각화

출처: week5_2 p.65 ~ 66 (week6_1 p.20 ~ 21 에서 복습)

### 3-1. Classifier / Regressor 비교 (요약 슬라이드)

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    criterion="gini",   # 어떤 feature와 threshold로 나눌지 선택하는 기준
    max_depth=3,        # tree의 최대 depth를 3으로 제한
)
model.fit(X_train, y_train)

from sklearn.tree import DecisionTreeRegressor

model = DecisionTreeRegressor(
    criterion="squared_error",  # 어떤 feature와 threshold로 나눌지 선택하는 기준
    max_depth=5,                # tree의 최대 depth를 5로 제한
)
model.fit(X_train, y_train)
```

**설명**

- 1-4, 2-3의 코드를 나란히 놓고 비교한 슬라이드
- 차이점: 클래스 이름(`Classifier`/`Regressor`)과 `criterion`(`gini`/`squared_error`)

### 3-2. tree 그림 그리기 & decision rule 텍스트 출력

```python
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

plt.figure(figsize=(9, 5))
plot_tree(
    model,
    feature_names=X.columns,
    class_names=model.classes_,
    filled=True,
    rounded=True
)
plt.show()
```

```python
from sklearn.tree import export_text

decision_rules = export_text(
    model,
    feature_names=list(X.columns)
)
print(decision_rules)
```

**설명**

- `plot_tree`: 학습된 tree를 그림으로 그림 (Iris 분류 모델 기준)
  - `feature_names`: 분기 조건에 feature 이름을 표시
  - `class_names=model.classes_`: leaf에 class 이름 표시 (`classes_`는 학습 후 모델이 기억하는 class 목록)
  - `filled=True`: 다수 class에 따라 노드 색칠, `rounded=True`: 모서리 둥글게
  - 각 노드에는 decision rule, impurity(gini), samples 수, value(class별 개수), 다수 class가 표시된다.
- `export_text`: 같은 tree를 텍스트로 출력. Iris 결과 예시:

```text
|--- PetalLengthCm <= 2.45
|   |--- class: Iris-setosa
|--- PetalLengthCm >  2.45
|   |--- PetalWidthCm <= 1.65
|   |   |--- PetalLengthCm <= 4.95
|   |   |   |--- class: Iris-versicolor
|   |   |--- PetalLengthCm >  4.95
|   |   |   |--- class: Iris-virginica
|   |--- PetalWidthCm >  1.65
|   |   |--- PetalLengthCm <= 4.85
|   |   |   |--- class: Iris-virginica
|   |   |--- PetalLengthCm >  4.85
|   |   |   |--- class: Iris-virginica
```

- 첫 분기 `PetalLengthCm <= 2.45` 하나만으로 setosa가 완전히 분리된다 (impurity 0).
- `max_depth=3`이므로 root부터 최대 3번 분기한다.

---

## 4. Single-Layer Perceptron (NumPy)

출처: week6_2 p.38, week7_1 p.8

```python
import numpy as np

# Petal Width = 0.2, Petal Length = 1.4
x = np.array([[0.2], [1.4]])  # Shape: (2, 1)

W = np.array([
    [-0.8, -1.2],   # Weights for Setosa
    [ 0.1, -0.05],  # Weights for Versicolor
    [ 0.7,  1.3]    # Weights for Virginica
])  # Shape: (3, 2)

b = np.array([
    [-0.4],   # Bias for Setosa
    [-0.01],  # Bias for Versicolor
    [ 0.4]    # Bias for Virginica
])  # Shape: (3, 1)

# z = W * x + b
z = np.matmul(W, x) + b  # Shape: (3, 1)

# Heaviside (1 if z >= 0)
y = np.where(z >= 0, 1, 0)

print("z = \n", z)
print("h = \n", y)
```

**설명**

- 입력 2개(꽃잎 너비, 꽃잎 길이) → 출력 3개(class별 neuron)인 **single fully connected layer**
  - 식: h = φ(Wx + b), φ = Heaviside
- shape 계산: `W (3×2)` × `x (2×1)` = `(3×1)`, 여기에 `b (3×1)`를 더함
- `np.matmul(W, x)`: 행렬 곱
- `np.where(z >= 0, 1, 0)`: z가 0 이상이면 1, 아니면 0 → **Heaviside step function**
- 실행 결과:
  - z = [−2.24, −0.06, 2.36]ᵀ
  - h = [0, 0, 1]ᵀ → **Virginica** 로 예측
- 계산 예 (Setosa 행): (−0.8)(0.2) + (−1.2)(1.4) + (−0.4) = −0.16 − 1.68 − 0.4 = −2.24
- 참고: week7_1 p.7 퀴즈 슬라이드에는 Virginica bias가 `0.5`로 적혀 있지만 코드는 `0.4`다. 어느 쪽이든 z ≥ 0 이라 결과(Virginica)는 같다.

---

## 5. Multi-Layer Perceptron (NumPy)

출처: week7_1 p.10 ~ 11

### 5-1. Hidden layer

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
])  # Shape: (4, 2)

hidden_layer_b = np.array([
    [ 0.1],
    [-0.2],
    [ 0.0],
    [ 0.3]
])  # Shape: (4, 1)

# z = W * x + b
hidden_layer_z = np.matmul(hidden_layer_W, input_features) + hidden_layer_b  # Shape: (4, 1)

# Heaviside (1 if z >= 0)
hidden_layer_y = np.where(hidden_layer_z >= 0, 1, 0)  # Shape: (4, 1)
```

### 5-2. Output layer

```python
################
# Output Layer #
################

output_layer_W = np.array([
    [-0.8, -1.2,  0.5, -0.2],  # Setosa
    [ 0.1, -0.05, 0.3,  0.1],  # Versicolor
    [ 0.7,  1.3, -0.4,  0.8]   # Virginica
])  # Shape: (3, 4)

output_layer_b = np.array([
    [-0.4],   # Setosa
    [-0.01],  # Versicolor
    [ 0.4]    # Virginica
])  # Shape: (3, 1)

# z = W * x + b
output_layer_z = np.matmul(output_layer_W, hidden_layer_y) + output_layer_b  # Shape: (3, 1)

# Heaviside (1 if z >= 0)
output_layer_y = np.where(output_layer_z >= 0, 1, 0)  # Shape: (3, 1)

print("z = \n", output_layer_z)
print("y = \n", output_layer_y)
print("=> Predicted Class: ", np.argmax(output_layer_y, axis=0))
```

**설명**

- 구조: **입력 2개 → hidden layer 4개 neuron → output layer 3개 neuron** (2-4-3)
  - n₀ = 2, n₁ = 4, n₂ = 3
- Hidden layer
  - `W (4×2)` × `x (2×1)` + `b (4×1)` → `z (4×1)`
  - 결과: z = [−0.22, 0.88, 0.58, 0.04]ᵀ → Heaviside 후 o = [0, 1, 1, 1]ᵀ
- Output layer
  - **hidden layer의 출력(`hidden_layer_y`)이 output layer의 입력**이 된다.
  - `W (3×4)` × `o (4×1)` + `b (3×1)` → `z (3×1)`
  - 결과: z = [−1.30, 0.34, 2.10]ᵀ → Heaviside 후 y = [0, 1, 1]ᵀ
- `np.argmax(..., axis=0)`: 가장 큰 값의 **index**를 반환 (axis=0 → 세로 방향, 즉 3개 행 중에서 고름)
  - y = [0, 1, 1]처럼 최댓값이 여러 개면 **첫 번째 index**를 반환 → `[1]` (Versicolor)
  - Heaviside는 0/1만 출력해서 동점이 생기기 쉽다 → 이 문제 때문에 다음 슬라이드에서 다른 활성 함수(ReLU, Sigmoid, Softmax)를 써본다.
- 파라미터 수: hidden (4×2 + 4 = 12) + output (3×4 + 3 = 15) = 27개

---

## 6. 활성 함수 (PyTorch)

출처: week7_1 p.14 ~ 15

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

**설명**

- 5번 MLP의 output layer **z 값**(활성 함수 적용 전)에 Heaviside 대신 다른 활성 함수를 적용해본 코드
- `torch.tensor(...)`: NumPy 배열을 PyTorch tensor로 변환
- z = [−1.30, 0.34, 2.10]ᵀ 에 대한 결과:
  - **ReLU** `max(0, x)` → [0, 0.34, 2.10] → Virginica (index 2)
  - **Sigmoid** `1/(1+e^(−x))` → [0.214, 0.584, 0.891] → Virginica (index 2)
    - 각 값은 0~1이지만 **합이 1이 아님**
  - **Softmax** `e^(xᵢ) / Σe^(xⱼ)` → [0.028, 0.143, 0.830] → Virginica (index 2)
    - 각 값이 0 이상이고 **합이 1** → 확률 분포로 해석 가능 → 분류에 많이 사용
- `dim=0`: softmax를 계산할 축. z의 shape가 (3, 1)이라 세로 방향(3개 class)으로 정규화한다.
- 세 함수 모두 **단조 증가**라서 argmax 결과(z가 가장 큰 class)는 바뀌지 않는다. Heaviside처럼 값이 뭉개지지 않으므로 동점 문제가 사라진다.

---

## 7. MLP 구현 (PyTorch `nn.Module`)

출처: week7_1 p.17 ~ 18

### 7-1. 모델 정의

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MLP(nn.Module):
    def __init__(self):
        super().__init__()

        # random initialization
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

### 7-2. 모델 실행 (forward)

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

**설명**

- 5번에서 NumPy로 직접 짠 2-4-3 MLP를 PyTorch로 다시 만든 것
- `class MLP(nn.Module)`: PyTorch 신경망은 `nn.Module`을 상속해서 만든다.
  - `__init__`: 사용할 layer들을 정의. `super().__init__()`을 반드시 먼저 호출
  - `forward`: 입력이 layer를 통과하는 순서(forward propagation)를 정의
  - `model(x)`처럼 호출하면 내부적으로 `forward(x)`가 실행된다.
- `nn.Linear(2, 4)`: 입력 2개 → 출력 4개인 fully connected layer (z = xWᵀ + b)
  - weight와 bias는 **랜덤으로 초기화**된다 → 실행할 때마다 결과가 달라짐 (아직 학습 안 한 모델)
- 활성 함수: hidden layer는 **Sigmoid**, output layer는 **Softmax**
- **입력 shape이 NumPy 버전과 다르다**
  - NumPy 버전: `(2, 1)` 세로 벡터, `Wx + b`
  - PyTorch 버전: `[[0.2, 1.4]]` → `(1, 2)` 가로 벡터. 첫 번째 차원은 **batch** (샘플 개수)
  - 그래서 `Softmax(dim=1)`, `argmax(dim=1)`처럼 class 방향이 `dim=1`이 된다.
- `.item()`: 원소 1개짜리 tensor를 Python 숫자로 변환
- `output_z`(softmax 전)로 argmax를 해도 `output_o`(softmax 후)와 결과가 같다 (softmax는 단조 증가)

---

## 8. Fashion-MNIST 신경망 학습 (한 개씩 학습)

출처: week7_1 p.43 ~ 45

### 8-1. 모델 정의

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

**설명**

- Fashion-MNIST: 28×28 흑백 옷 이미지, 10개 class
- `nn.Flatten()`: 28×28 이미지를 784(=28×28)개 숫자의 1차원 벡터로 펼침
- 구조: **784 → 128 (Sigmoid) → 10**
- `forward`는 softmax를 적용하지 **않고** output layer의 z값(**logits**)을 그대로 반환한다.
  - 학습 때 쓰는 loss(`criterion`)가 내부에서 softmax를 계산해주기 때문 (보통 `nn.CrossEntropyLoss`)
  - `self.softmax`는 test 단계에서 확률을 보고 싶을 때 따로 호출한다 (8-3 참고)
- `.to(device)`: 모델을 GPU(`"cuda"`) 또는 CPU로 옮김
- 참고: `device`, `train_dataset`, `test_dataset`, `epochs`, `criterion`, `optimizer`는 슬라이드에 정의가 나오지 않는다. 전체 코드는 슬라이드의 Colab 링크에 있다.

### 8-2. 학습 루프 (샘플 1개씩)

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

        # Update weights and biases
        optimizer.step()

        total_loss += loss.item()
        prediction = logits.argmax(dim=1)
        correct += (prediction == label).sum().item()
        total += 1
```

**설명**

- `for epoch in range(epochs)`: 전체 training data를 `epochs`번 반복 학습
- `model.train()`: 모델을 학습 모드로 설정
- `torch.randperm(n)`: 0 ~ n−1을 **랜덤 순서로 섞은** index 목록 → 매 epoch마다 데이터 순서를 섞음
- `image.unsqueeze(0)`: 맨 앞에 batch 차원을 추가. (1, 28, 28) → (1, 1, 28, 28)
  - 모델은 항상 `(batch, ...)` 형태 입력을 기대하므로 샘플 1개라도 batch 차원이 필요
- 학습 1 step의 4단계 (반드시 기억):
  1. **Forward propagation**: `logits = model(image)` → `loss = criterion(logits, label)`
  2. `optimizer.zero_grad()`: 이전 step에서 쌓인 gradient를 0으로 초기화
  3. **Backpropagation**: `loss.backward()` → 각 parameter의 gradient 계산
  4. **Update**: `optimizer.step()` → gradient를 이용해 weight와 bias 갱신
- `loss.item()`: loss tensor를 Python 숫자로 바꿔서 누적
- `logits.argmax(dim=1)`: 10개 class 중 가장 큰 값의 index = 예측 class
- `correct / total`로 training accuracy를 구할 수 있다.

### 8-3. 테스트 (샘플 1개씩)

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

**설명**

- `model.eval()`: 모델을 평가 모드로 설정
- `torch.no_grad()`: 테스트에는 gradient가 필요 없으므로 계산을 끔 → 메모리/속도 절약
- test에서는 `optimizer`, `backward`, `step`이 **없다** (weight를 바꾸지 않음)
- `model.softmax(logits)`: logits를 확률로 바꾼 뒤 argmax로 예측 class 결정
- test accuracy = `correct / total`

---

## 9. Fashion-MNIST 신경망 학습 (Mini-batch)

출처: week7_1 p.49 ~ 51

### 9-1. DataLoader로 batch 만들기

```python
# batching
batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
```

**설명**

- `DataLoader` (`torch.utils.data`): dataset을 `batch_size`개씩 묶어서 꺼내준다.
- `batch_size = 32`: 한 번에 32개 샘플을 모델에 넣음 → **mini-batch**
- `shuffle=True`(train): 매 epoch마다 순서를 섞음. 8-2의 `torch.randperm` 역할을 대신한다.
- `shuffle=False`(test): 평가에는 섞을 필요 없음

### 9-2. 학습 루프 (mini-batch)

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

        # Update weights and biases
        optimizer.step()

        total_loss += loss.item() * labels.size(0)
        predictions = logits.argmax(dim=1)
        correct += (predictions == labels).sum().item()
        total += labels.size(0)
```

**설명**

- 8-2와 비교했을 때 달라진 점:
  - `train_loader`에서 이미 `(32, 1, 28, 28)` 형태로 batch가 나오므로 `unsqueeze(0)`가 필요 없다.
  - 한 step에 32개를 한꺼번에 처리 → **weight 갱신은 batch당 1번**
  - `loss`는 batch 평균이므로 `loss.item() * labels.size(0)`로 batch 크기를 곱해서 합계로 누적
  - `labels.size(0)`: 이번 batch의 샘플 수 (마지막 batch는 32보다 작을 수 있어서 32로 고정하지 않음)
  - `total += labels.size(0)`: 샘플 개수 단위로 누적
- 예) training data 60,000개, batch 32 → 1 epoch = 약 1,875번 update
- Mini-batch 장점: 1개씩보다 빠름, full-batch보다 메모리를 적게 씀

### 9-3. 테스트 (mini-batch)

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

**설명**

- 8-3과 같은 흐름인데 batch 단위로 처리
- `predictions == labels`: 원소별 비교 → True/False tensor
- `.sum().item()`: True 개수 = 이번 batch에서 맞힌 개수
- test accuracy = `correct / total`

---

## 부록: 코드 흐름 한눈에 보기

**sklearn (week5)**

```text
데이터 불러오기 → X, y 분리 → train_test_split → model 생성 → fit → predict → 성능 측정
```

**NumPy perceptron (week6 ~ 7)**

```text
x, W, b 정의 → z = np.matmul(W, x) + b → 활성 함수(np.where) → np.argmax
```

**PyTorch 학습 (week7)**

```text
for epoch:
    model.train()
    for batch:
        logits = model(x)            # forward
        loss = criterion(logits, y)
        optimizer.zero_grad()        # gradient 초기화
        loss.backward()              # backpropagation
        optimizer.step()             # parameter 갱신
model.eval()
with torch.no_grad():
    예측 → accuracy 계산
```
