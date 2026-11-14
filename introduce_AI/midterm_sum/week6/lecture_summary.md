# Week6 강의 요약

**과목**: 인공지능개론(CSE2302) · **주제**: 기계학습 (3) 성능 평가 → 신경망 (1) 퍼셉트론과 다층 퍼셉트론
**강의일**: 2026-10-06(Lecture 01), 2026-10-08(Lecture 02)

---

## 1부: 지난 주차 복습 (Lecture 01 앞부분)

> 자세한 내용은 `week5/lecture_summary.md`의 5부·6부 참고. 여기서는 핵심만 다시 정리한다.

### 기계학습의 주요 과제 (Main Challenges)
- 훈련 데이터 양 부족 / 낮은 품질의 데이터
- 과대적합(Overfitting) / 과소적합(Underfitting)
- 대표성 없는 훈련 데이터 (Outlier: 다른 관측값과 크게 다른 데이터 포인트)
- 관련 없는 특징 (→ Feature engineering, Feature selection)

### 데이터 → 모델 흐름
- 데이터셋을 입력 **X**(features)와 출력 **y**(label)로 분리 → train/test로 분할
- `model.fit(X_train, y_train)` 으로 학습, `model.predict(X_test)` 로 예측 → 예측값 ŷ과 실제값 y_test 비교
- 분류 예: Iris (꽃받침/꽃잎 길이·너비 → Species)
- 회귀 예: California Housing (MedInc, HouseAge, AveRooms, … , Latitude, Longitude → MedHouseVal)

### 성능 지표
| 문제 | 지표 | 식 |
|---|---|---|
| 분류 | Accuracy | (ŷ = y인 샘플 수) / (테스트 샘플 수) |
| 분류 | Error rate | (ŷ ≠ y인 샘플 수) / (테스트 샘플 수) = 1 − accuracy |
| 회귀 | MAE | Σ\|ŷᵢ − yᵢ\| / m |
| 회귀 | MSE | Σ(ŷᵢ − yᵢ)² / m |
| 회귀 | RMSE | √MSE |

- 예시: ŷ = [4, 3, 4, 5, 11], y = [3, 5, 1, 1, 6] → 오차 = [1, −2, 3, 4, 5]
  - MAE = (1+2+3+4+5)/5 = **3**
  - MSE = (1+4+9+16+25)/5 = 11, RMSE = √11 ≈ **3.3**

### 결정 트리 (Decision Tree)
- 속성값 벡터(입력)를 하나의 출력값("결정")으로 매핑하는 함수. 루트에서 시작해 테스트를 차례로 수행하며 잎(leaf)에 도달하면 결정.
- **결정 트리 학습**: 규칙(어떤 feature를 어떤 threshold로 나눌지)을 직접 쓰지 않고 데이터에서 찾아낸다.
- 규칙 선택 기준: **Gini impurity**, **information gain** 등. 나눈 뒤의 각 그룹이 한 클래스로 순수할수록(불순도가 낮을수록) 좋은 분할.
- 규칙은 **탐욕적(greedy)**으로 하나씩 찾는다.
  - 예: 처음 (Class1 20, Class2 20) → 규칙1 x₁ ≤ T₁로 나누면 한쪽은 (13, 0)으로 불순도 0, 다른 쪽은 (7, 20) → 여기에 다시 규칙2 x₂ ≤ T₂ 적용 → (7, 4) / (0, 16)
- Iris 결정 트리: `PetalLengthCm <= 2.45`이면 setosa, 아니면 PetalWidthCm, PetalLengthCm로 versicolor/virginica를 추가 분리.
- 코드: `DecisionTreeClassifier(criterion="gini", max_depth=3)`, `DecisionTreeRegressor(criterion="squared_error", max_depth=5)`, 시각화는 `plot_tree`, 텍스트 규칙은 `export_text`.

### 기계학습 모델 종류
Decision tree, Random forest, XGBoost, Linear/Logistic regression, SVM, KNN, K-means Clustering, (Shallow) Neural Network, Deep Neural Networks(DNNs)
→ **이 수업에서는 신경망만 다룬다.** (딥러닝은 DNN 기반)

---

## 2부: 기계학습의 기본 개념 (Lecture 01)

### 학습 생애주기 (Learning Lifecycle)
**Data Collection → Model Training → Model Testing**

### 특징(Feature)과 레이블(Label)
- **Feature**: 데이터셋의 개별적으로 측정 가능한 속성 → 패턴을 찾거나 예측하기 위한 **입력 변수**
  - 예: SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm
  - **Feature vector**: [5.1, 3.5, 1.4, 0.2]
- **Label (= target)**: 모델이 예측하도록 학습되는 정답 → **출력 변수** (예: Species)
- 레이블 표현 방법
  - **Class ID**: 0 (setosa), 1 (versicolor), 2 (virginica)
  - **One-hot encoding**: [1,0,0] (setosa), [0,1,0] (versicolor), [0,0,1] (virginica)

### 특징 공간 (Feature Space)
- Feature vector들이 놓이는 벡터 공간. 예: 꽃잎 길이·너비를 두 축으로 그리면 setosa가 다른 두 종과 확연히 떨어져 있다.

### 결정 경계 (Decision Boundary)
- 특징 공간을 클래스별 영역으로 **나누는 경계**.
- **선형 분류기(linear classifier)**: 직선(평면)으로 나눔
- **비선형 분류기(non-linear classifier)**: 곡선 등으로 나눔

### 이진 분류 vs 다중 클래스 분류
- **Binary classification**: 클래스 2개 — Positive(1) / Negative(0)
- **Multi-class classification**: 클래스 3개 이상 — one-hot encoding 사용 ([1,0,0], [0,1,0], [0,0,1])
- (참고) **Multi-label classification**: 하나의 샘플이 여러 레이블을 동시에 가질 수 있음

### 선형 분리 가능성 (Linear Separation)
| x | y | AND | OR | XOR |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

- AND, OR → 직선 하나로 0과 1을 나눌 수 있음 (**선형 분리 가능**)
- **XOR → 직선 하나로는 나눌 수 없음** (선형 분리 불가능) ⇒ 이후 다층 퍼셉트론(MLP)이 필요한 이유

### 임베딩 공간 (Embedding Space)
- 입력 데이터의 근본적 구조를 알려주는 **핵심 특징만 보존한** 데이터 표현 공간.
- 일반적으로 **잠재 공간(Latent Space)**과 같은 의미로 쓰인다.
- 특징 공간에서 섞여 있던 점들이 모델을 거치면 임베딩 공간에서는 비슷한 것끼리 가깝게 재배치된다.

---

## 3부: 혼동 행렬과 분류 성능 지표

### 혼동 행렬 (Confusion Matrix)
클래스 A의 샘플이 클래스 B로 분류된 개수를 세는 표. (행: 실제 y, 열: 예측 ŷ)

|  | 예측 Positive | 예측 Negative |
|---|---|---|
| **실제 Positive** | TP (True Positive) | FN (False Negative) |
| **실제 Negative** | FP (False Positive) | TN (True Negative) |

- 이름 읽는 법: 앞(True/False) = 예측이 맞았나, 뒤(Positive/Negative) = 무엇으로 예측했나
- 예시 (실제/예측 쌍 8개): TP = 3, FN = 1, FP = 2, TN = 2

### Accuracy, Recall, Precision
| 지표 | 식 | 의미 | 언제 중요한가 | 예시 값 |
|---|---|---|---|---|
| **Accuracy (정확도)** | (TP+TN) / (TP+FN+FP+TN) | 전체 중 맞힌 비율 | 클래스가 **균형**일 때 | 5/8 = 0.625 |
| **Recall (재현율)** | TP / (TP+FN) | **실제 양성** 중 양성으로 맞힌 비율 | **FN이 치명적**일 때 (예: 질병 진단) | 3/4 = 0.75 |
| **Precision (정밀도)** | TP / (TP+FP) | **양성이라고 예측한 것** 중 실제 양성 비율 | 실제 양성 샘플 수가 제한적일 때 | 3/5 = 0.6 |

- 외우는 팁: Recall은 혼동 행렬의 **행(실제)** 기준, Precision은 **열(예측)** 기준.

### Check-in Quiz (Lecture 02): 코로나 검사
> 1000명 중 실제 코로나 환자 800명, 그 중 700명 양성 예측. 비환자 중 30명이 양성으로 잘못 예측됨.

|  | 예측 Positive | 예측 Negative |
|---|---|---|
| **실제 Positive (800)** | TP = 700 | FN = 100 |
| **실제 Negative (200)** | FP = 30 | TN = 170 |

- Accuracy = (700+170)/1000 = **0.87**
- Precision = 700/(700+30) = 700/730 ≈ **0.959**
- Recall = 700/(700+100) = 700/800 = **0.875**

### 다중 클래스에서의 지표
예시 혼동 행렬 (행: 실제, 열: 예측):

|  | A | B | C |
|---|---|---|---|
| **A** | 8 | 5 | 3 |
| **B** | 10 | 60 | 30 |
| **C** | 1 | 50 | 200 |

- **Accuracy** = 대각선 합 / 전체 = (8+60+200) / 367 ≈ **0.73**

#### Macro averaging: 클래스별로 지표를 구한 뒤 단순 평균
- Recall (행 기준)
  - recall_A = 8/(8+5+3) = 0.50
  - recall_B = 60/(10+60+30) = 0.60
  - recall_C = 200/(1+50+200) ≈ 0.80
  - recall = (0.50+0.60+0.80)/3 ≈ **0.63**
- Precision (열 기준)
  - precision_A = 8/(8+10+1) ≈ 0.42
  - precision_B = 60/(5+60+50) ≈ 0.52
  - precision_C = 200/(3+30+200) ≈ 0.86
  - precision = (0.42+0.52+0.86)/3 ≈ **0.60**

#### Micro averaging: 클래스별 이진 혼동 행렬(A vs Not A 등)을 **합친 뒤** 계산
| | TP | FN | FP | TN |
|---|---|---|---|---|
| A vs Not A | 8 | 8 | 11 | 340 |
| B vs Not B | 60 | 40 | 55 | 212 |
| C vs Not C | 200 | 51 | 33 | 83 |
| **합계** | **268** | **99** | **99** | **635** |

- precision = 268 / (268+99) ≈ **0.73**
- recall = 268 / (268+99) ≈ **0.73**
- (단일 레이블 다중 클래스에서는 micro precision = micro recall = accuracy가 된다. 각 오분류가 한 클래스의 FP이면서 동시에 다른 클래스의 FN이기 때문.)

---

## 4부: 교차 검증 (Cross Validation)

- 훈련/테스트를 수동으로 한 번만 나누면 결과가 우연히 **너무 좋거나 너무 나쁠** 수 있다.
- **K-Fold Cross Validation**
  1. 데이터를 무작위로 K개의 부분집합(**fold**)으로 나눈다.
  2. 모델을 K번 평가: 매번 (K−1)개 fold로 학습, 나머지 1개 fold로 테스트
  3. K번의 성능을 **평균**낸다.
- 예: K = 5 → Model 1~5가 각각 다른 fold를 테스트로 사용 → Performance 1~5의 평균
- 단점: 학습을 **K번** 해야 하므로 시간이 더 든다.

---

## 5부: 신경망 기초 — 뉴런과 퍼셉트론 (Lecture 01 후반 ~ Lecture 02)

### 생물학적 뉴런 (Biological Neuron)
- 개별 뉴런은 비교적 단순하게 동작하지만, 수십억 개가 거대한 네트워크로 조직되어 있다.
- 각 뉴런은 보통 수천 개의 다른 뉴런과 연결된다.
- 생물학적 신경망(BNN)은 여러 개의 연속된 층(layer)으로 구성된다.

### 인공 신경망 (Artificial Neural Network, ANN)
- **인공 뉴런**이라 불리는 노드들이 **엣지(edge)**로 연결된 구조.
- 각 인공 뉴런은 연결된 뉴런으로부터 신호를 받아 처리한 뒤, 연결된 다른 뉴런으로 신호를 보낸다.
- 신호는 **실수(real number)**이고, 각 연결에서 신호의 세기는 **가중치(weight)**로 결정된다.

### 퍼셉트론 (Perceptron)
- 가장 단순한 신경망 구조. 입력과 출력은 숫자.
  - 특징이 n개일 때 (n+1)개의 입력 노드 (+1은 bias용), 1개의 출력 노드
  - 각 입력 연결마다 가중치가 붙어 있다.
- 인공 뉴런 = **TLU (Threshold Logic Unit)**
  1. 입력의 **가중합**을 계산: **z = w₁x₁ + w₂x₂ + ⋯ + wₙxₙ = xᵀw**
     - x = [x₁ … xₙ]ᵀ, w = [w₁ … wₙ]ᵀ (둘 다 n×1) → xᵀw는 (1×n)(n×1) = 스칼라
  2. 가중합에 **step function(활성 함수)**을 적용해 출력: **h_w(x) = step(z) = step(xᵀw)**

### 퍼셉트론 vs 뉴런
| 퍼셉트론 | 뉴런 (더 일반화된 개념) |
|---|---|
| 출력이 0 또는 1 (이진) | 연속적인 값 출력 가능 |
| step function(예: Heaviside) 사용 | 다양한 활성 함수 사용 |
| 단순한 분류 문제용 | 더 복잡한 문제(회귀 등)에도 사용 |

---

## 6부: 활성 함수 (Activation Function)

- 생물학적 뉴런의 **활성화(activation)**를 흉내 낸 것.
- TLU 하나로 **간단한 선형 이진 분류**가 가능하다.
- **Heaviside**: z가 임계값 이상이면 양성 클래스(1), 아니면 음성 클래스(0)
  - heaviside(z) = 0 (z < 0), 1 (z ≥ 0)
  - 출력이 0/1뿐이므로 회귀(regression)에는 쓸 수 없다 → 다른 활성 함수 필요

| 활성 함수 | 식 | 출력 범위 |
|---|---|---|
| Identity | x | (−∞, ∞) |
| Binary step (= Heaviside) | 0 (x < 0), 1 (x ≥ 0) | {0, 1} |
| Logistic (= Sigmoid) | 1 / (1 + e^(−x)) | (0, 1) |
| Hyperbolic tangent (tanh) | (eˣ − e^(−x)) / (eˣ + e^(−x)) | (−1, 1) |
| ReLU (Rectified Linear Unit) | 0 (x ≤ 0), x (x > 0) = max(0, x) | [0, ∞) |
| Softmax (나중에 다룸) | e^(xᵢ) / Σⱼ e^(xⱼ), i = 1…J | (0, 1), 합 = 1 |

---

## 7부: 편향(Bias)과 퍼셉트론 이진 분류기

### 편향 (Bias)
- **상수 오프셋(shift)**. 가중치는 각 입력과 연결되지만, bias는 입력과 무관한 상수.
- 입력 특징만으로는 표현할 수 없는 패턴을 잡기 위해 사용.
- 추가 bias 특징 **x₀ = 1**과 그 가중치 w₀로 표현할 수 있다:
  - **z = w₁x₁ + ⋯ + wₙxₙ + w₀x₀ = xᵀw + w₀x₀ = xᵀw + b**

### 퍼셉트론 이진 분류기
**h_{w,b}(x) = φ(xᵀw + b)**
- x: 입력 특징 (n×1), w: 가중치 (n×1), b: bias (1×1), φ: 활성 함수

예: w₁ = 1, w₂ = 1, b = −0.5, φ = Heaviside

| x₁ | x₂ | z | h |
|---|---|---|---|
| 0 | 0 | 1·0 + 1·0 − 0.5 = −0.5 | 0 |
| 0 | 1 | 1·0 + 1·1 − 0.5 = 0.5 | 1 |
| 1 | 0 | 1·1 + 1·0 − 0.5 = 0.5 | 1 |
| 1 | 1 | 1·1 + 1·1 − 0.5 = 1.5 | 1 |

→ **OR 게이트**를 구현한 것. 결정 경계는 직선 x₁ + x₂ = 0.5.
(참고: b = −1.5로 바꾸면 (1,1)만 z ≥ 0이 되어 AND 게이트가 된다.)

---

## 8부: 단층 퍼셉트론 (Single-Layer Perceptron)

### 입력층·출력층과 완전 연결층
- 모든 입력 뉴런이 **입력층**, 모든 출력 뉴런이 **출력층**을 이룬다.
- **Fully connected layer**: 한 층의 모든 뉴런이 이전 층의 모든 뉴런과 연결된 층.
- 퍼셉트론은 단순히 **TLU 한 층**으로 구성된다.

### 행렬 표현 (입력 n개, 출력 m개)
두 가지 표기법이 있으니 **행렬 크기**에 주의할 것.

| 표기 | 식 | X | W | b | 결과 |
|---|---|---|---|---|---|
| 열벡터 방식 | **φ(WX + b)** | n×1 | m×n | m×1 | m×1 |
| 행벡터 방식 | **φ(XW + b)** | 1×n | n×m | 1×m | 1×m |

- W, b가 학습되는 **파라미터(parameters)**.
- **학습(training)이란 올바른 가중치와 편향 값을 찾는 것.**

### Iris 예시: 입력 2개 → 출력 3개
- 입력: Petal Width(x₁), Petal Length(x₂) / 출력: Setosa, Versicolor, Virginica
- 각 출력 뉴런 i는 φ(w_{i,1}x₁ + w_{i,2}x₂ + bᵢ) 를 계산 (i = 1, 2, 3)

### 구현 (NumPy)
```python
import numpy as np

# Petal Width = 0.2, Petal Length = 1.4
x = np.array([[0.2], [1.4]])          # Shape: (2, 1)

W = np.array([
    [-0.8, -1.2],    # Weights for Setosa
    [ 0.1, -0.05],   # Weights for Versicolor
    [ 0.7,  1.3]     # Weights for Virginica
])                                     # Shape: (3, 2)

b = np.array([
    [-0.4],   # Bias for Setosa
    [-0.01],  # Bias for Versicolor
    [ 0.4]    # Bias for Virginica
])                                     # Shape: (3, 1)

z = np.matmul(W, x) + b                # z = W * x + b, Shape: (3, 1)
y = np.where(z >= 0, 1, 0)             # Heaviside (1 if z >= 0)
```
- 직접 계산해 보면:
  - z₁ = −0.8·0.2 − 1.2·1.4 − 0.4 = −2.24 → 0
  - z₂ = 0.1·0.2 − 0.05·1.4 − 0.01 = −0.06 → 0
  - z₃ = 0.7·0.2 + 1.3·1.4 + 0.4 = 2.36 → 1
- 즉 h = [0, 0, 1]ᵀ. (입력은 setosa 값인데 virginica로 나온다 — 이 가중치는 학습된 값이 아니라 임의의 값이기 때문. 그래서 **학습**이 필요하다.)

---

## 9부: 다층 퍼셉트론 (Multi-Layer Perceptron, MLP)

### 단층 vs 다층
| Single-Layer Perceptron (원래 형태) | Multi-Layer Perceptron (현대) |
|---|---|
| 입력층 + 출력층 | 입력층 + **은닉층(hidden layer)** + 출력층 |

- MLP는 단순하고 얕은(shallow) 신경망이다.
- 은닉층을 더하면 XOR처럼 선형 분리가 불가능한 문제도 풀 수 있다.

### 층별 계산 예시 (입력 3 → 은닉 4 → 출력 2, 행벡터 방식)
- **은닉층**: [x₁⁽¹⁾ … x₃⁽¹⁾] · W⁽¹⁾(3×4) + [b₁⁽¹⁾ … b₄⁽¹⁾] = [x₁⁽²⁾ … x₄⁽²⁾]
- **출력층**: [x₁⁽²⁾ … x₄⁽²⁾] · W⁽²⁾(4×2) + [b₁⁽²⁾ b₂⁽²⁾] = [y₁ y₂]
- 앞 층의 출력이 다음 층의 입력이 된다. (위 첨자 (1), (2)는 층 번호)
- "그럼 딥러닝이란?" → 은닉층을 **여러 개 깊게** 쌓은 신경망(DNN)으로 학습하는 것.

### MLP vs 신경망 (Neural Network)
| MLP (또는 퍼셉트론) | Neural Network (더 일반화된 개념) |
|---|---|
| 완전 연결(Fully-connected) | 완전 연결일 필요 없음 |
| (원래 퍼셉트론에서는) step function 사용 | 다양한 활성 함수 사용 가능 |

- 현대의 MLP는 대부분 그냥 신경망으로 간주된다.

### 분류에서 출력 뉴런의 개수
- **이진 분류**: 출력 뉴런 **1개**로 충분. 출력이 임계값(threshold)보다 크면 True.
- **다중 클래스 분류**: 클래스마다 출력 뉴런 1개씩. 출력값들을 비교해 **가장 큰(가장 그럴듯한) 것**을 True로 (단일 레이블인 경우).

---

## 10부: 학습과 전파 (Learning and Propagation)

### 학습 (Learning)
손실 함수(loss function)로 계산한 **오차를 최소화하는 모델 파라미터를 찾는 것**.
1. 파라미터 초기화 (랜덤 값 또는 0) — 경우에 따라 **사전학습된 파라미터(pretrained parameters)** 사용
2. 반복:
   1. 출력 계산
   2. 오차 계산 (손실 함수로부터)
   3. 손실을 줄이도록 파라미터 갱신

### 전파 (Propagation)
- **순전파 (Forward Propagation)**: 가중치 W로 입력에서 출력 방향으로 계산 → 예측 출력 → 정답(ground-truth)과 비교해 **손실 L** 계산
- **역전파 (Backward Propagation = Backpropagation)**: 출력에서 입력 방향으로 **기울기(gradient) ∂L/∂W** 계산
- **가중치 갱신**:
  - **ΔW = −η · ∂L/∂W** (η: **학습률, learning rate**)
  - **W(t) = W(t−1) + ΔW**
  - 기울기의 **반대 방향**으로 조금씩 이동해 손실을 줄인다.

---

## 참고: 공지사항 (수업 운영 관련, 참고용)

- **강의 계획**: 6주 신경망(1) (과제 1 마감) → 7주 신경망(2) → 8주 중간고사. (상황에 따라 변경될 수 있음)
- **과제 1 (Tic-Tac-Toe AI 봇)**: 10월 8일 오후 11시 55분 마감 (24시간 지각당 −10%)
- **중간고사** (시험 전 재공지 예정):
  - 일시: 10월 20일(화) 오후 6:30~7:30, **6:20까지 입실**
  - 장소: **지하 대강당** (수업 강의실 아님)
  - 준비물: 신분증/학생증, 계산기(공학용 계산기 불필요)
  - 힌트노트: A4 단면 1장 **수기 작성** 허용 (부적합 시 사용 제한될 수 있음)
  - 범위: Problem Solving(2주차) ~ Neural Networks(7주차)
  - 유형: T/F, 객관식, 단답형, 빈칸 채우기 손코딩 (코드는 Python만, 사소한 문법 오류는 허용)
  - **오피스아워 (업데이트)**:
    - 10/19(월) 11~16시 @하-1412 (윤진이 교수)
    - 10/19(월) 16~21시 @하-1210 (강신우 조교)
    - 10/20(화) 수업 시간 @하-1412 (윤진이 교수)
    - 10/15(목) 마지막 수업 꼭 참석, 상시 inha.unilab@gmail.com 으로 질의 가능
