# Week 06: Machine Learning (3) & Neural Networks (1)(2) — 한국어 번역

> 원본: `CSE2302_003_week06_1 (1).pdf` (Lecture 01, 2026-10-06), `CSE2302_003_week06_2 (1).pdf` (Lecture 02, 2026-10-08)
> 슬라이드 번호는 PDF 오른쪽 아래 번호와 같다. 전문 용어는 영어로 두었고, 그림은 "[그림]"으로 설명만 적었다.
> Lecture 02 앞부분(슬라이드 2~18)은 Lecture 01 복습이라 해당 슬라이드 번호만 적었다.
> 요약본은 `lecture_summary.md` 참고.

---

# Lecture 01 (2026-10-06)

## Part 1. Machine Learning (3)

### 슬라이드 2. Main Challenges in Machine Learning (기계학습의 주요 과제)

- training data의 양이 부족함
- 품질이 낮은 data
- training data에 대한 Overfitting/Underfitting
- 대표성이 없는(nonrepresentative) training data
  - (**Outlier**: 다른 관측값들과 크게 다른 data point)
- 관련 없는 feature(irrelevant features)
  - (feature selection을 포함한 **feature engineering**)
- [그림] 오른쪽 위 Outliers 점 그림 / data 양이 늘수록 여러 모델의 test accuracy가 함께 오르는 그래프 / GDP per capita와 Life satisfaction 그래프 (일부 국가만 쓰면 대표성이 없고, 지나치게 복잡한 곡선은 overfitting)

### 슬라이드 3. Classification Datasets – Iris (cont.) (분류 데이터셋 – 붓꽃)

[표] Id, SepalLengthCm(꽃받침 길이), SepalWidthCm(꽃받침 너비), PetalLengthCm(꽃잎 길이), PetalWidthCm(꽃잎 너비), Species(꽃 종류)
- 예: Id 1 → 5.1, 3.5, 1.4, 0.2, Iris-setosa / Id 51 → 7.0, 3.2, 4.7, 1.4, Iris-versicolor / Id 101 → 6.3, 3.3, 6.0, 2.5, Iris-virginica

### 슬라이드 4. Split X (input) and y (output) (입력 X와 출력 y 나누기)

[그림] 같은 Iris 표에서 feature 4개(빨간 박스)가 **X**, Species(파란 박스)가 **y**

### 슬라이드 5. Split X (input) and y (output) (cont.)

[그림] SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm → **Model** → Species

### 슬라이드 6. Training and Testing (학습과 테스트)

[그림]
- X_train(Training Set) → **Model** → y_train(Training Set): 모델 학습
- X_test(Test Set) → **Trained Model**(학습이 끝나 고정된 모델, 눈꽃 표시) → 예측값을 y_test(Test Set)와 비교

### 슬라이드 7. Training and Testing (cont.)

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(
    criterion="gini",
    max_depth=3,
    random_state=42
)

model.fit(X_train, y_train)      # training
y_pred = model.predict(X_test)   # testing
```
- 슬라이드 위 문구: "모델을 만드는 다양한 학습 방법은 앞으로 다룰 예정"

### 슬라이드 8. Performance Measure (성능 지표)

- Accuracy와 error rate (주로 classification에 사용)
  - **accuracy** = (ŷ = y인 sample 수) / (test sample 수)
  - **errorRate** = (ŷ ≠ y인 sample 수) / (test sample 수) = 1 − accuracy
  - ŷ: 예측 출력 (예: 예측한 class)
  - y: ground-truth (예: 실제 class)

### 슬라이드 9. Regression Datasets – California Housing (회귀 데이터셋 – 캘리포니아 주택)

- California housing dataset (https://inria.github.io/scikit-learn-mooc/python_scripts/datasets_california_housing.html)
  - 입력 feature: {MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude}
  - 출력: {MedHouseVal}

### 슬라이드 10. Split X (input) and y (output)

[그림] MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude → **Model** → MedHouseVal

### 슬라이드 11. Performance Measure (cont.) — MAE

- **Mean Absolute Error** (주로 regression에 사용)
  - MAE = Σᵢ₌₁ᵐ |ŷᵢ − yᵢ| / m
  - ŷ: 예측 출력 (예: 예측값), y: ground-truth (예: 실제값), m: test sample 수
- 예: 예측 (4, 3, 4, 5, 11), 정답 (3, 5, 1, 1, 6) → ŷ − y = (1, −2, 3, 4, 5)
  - MAE = (|1| + |−2| + |3| + |4| + |5|) / 5 = **3**

### 슬라이드 12. Performance Measure (cont.) — (R)MSE

- **(Root) Mean Squared Error** (주로 regression에 사용)
  - MSE = Σᵢ₌₁ᵐ (ŷᵢ − yᵢ)² / m
  - RMSE = √MSE
- 같은 예: RMSE = √((1² + (−2)² + 3² + 4² + 5²) / 5) = √11 ≈ **3.3**

### 슬라이드 13. Decision Tree (결정 트리)

- 속성값 벡터(입력)를 하나의 출력값, 즉 "**decision**(결정)"으로 매핑하는 함수
- 일련의 test를 수행해서 결정에 도달한다.
- **root**에서 시작해 알맞은 **branch**를 따라가다가 **leaf**에 도달한다.
- [그림] 식당에서 자리를 기다릴지 정하는 트리. (Yes) Wait / (No) Do not wait
  - Patrons? → None이면 No, Some이면 Yes, Full이면 WaitEstimate?로 이어서 판단 …

### 슬라이드 14. Decision Tree Learning (결정 트리 학습)

- 규칙(**어떤 feature와 threshold**로 나눌지)을 직접 쓰지 않고, 여러 입력 변수를 바탕으로 **target** 변수의 값을 예측하는 것
- [그림] Decision Rule 1: x₁ ≤ T₁ (N_class1 = 20, N_class2 = 20)
  - < Class 2 > 쪽: N_class1 = 7, N_class2 = 20
  - < Class 1 > 쪽: N_class1 = 13, N_class2 = 0

### 슬라이드 15. Decision Tree Learning (cont.)

- decision rule을 고를 때는 **Gini impurity**나 **information gain** 같은 지표가 널리 쓰인다.
- [그림 왼쪽] 위쪽은 Class 1만 있음 → **Zero impurity**(불순도 0), 아래쪽은 섞여 있음 → Low impurity
- [그림 오른쪽] 경계를 아래에 그으면 위쪽에 두 class가 많이 섞임 → **High impurity**

### 슬라이드 16~17. Decision Tree Learning (cont.)

- decision rule을 **greedy**하게(탐욕적으로) 찾아간다.
- [그림] Rule 1로 나눈 뒤, 섞여 있는 쪽(N_class1 = 7, N_class2 = 20)에 Decision Rule 2: x₂ ≤ T₂를 적용
  - < Class 1 >: N_class1 = 7, N_class2 = 4
  - < Class 2 >: N_class1 = 0, N_class2 = 16

### 슬라이드 18. Iris Dataset (revisit, 다시 보기)

[그림] Iris 표. feature(빨강)와 Species(파랑), 그리고 학습에 쓰는 일부 행(검은 점선)을 표시

### 슬라이드 19. Decision Tree Learning (cont.) — 결과 트리

- [그림] 학습된 트리의 각 node에 표시되는 것
  - **Decision rule** (예: PetalLengthCm <= 2.45)
  - **# samples** (sample 수, 예: 120)
  - **Impurity** (gini 값, 예: 0.5)
  - value = [setosa 수, versicolor 수, virginica 수] (예: [0, 40, 40])
  - **Majority class** (가장 많은 class)
- 텍스트로 출력한 규칙:
```
|--- PetalLengthCm <= 2.45
|   |--- class: Iris-setosa
|--- PetalLengthCm >  2.45
|   |--- PetalWidthCm <= 1.65
|   |   |--- PetalLengthCm <= 4.95  → class: Iris-versicolor
|   |   |--- PetalLengthCm >  4.95  → class: Iris-virginica
|   |--- PetalWidthCm >  1.65
|   |   |--- PetalLengthCm <= 4.85  → class: Iris-virginica
|   |   |--- PetalLengthCm >  4.85  → class: Iris-virginica
```

### 슬라이드 20. Decision Tree Learning (cont.) — 코드

```python
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(
    criterion="gini",            # 어떤 feature와 threshold로 나눌지 선택하는 기준
    max_depth=3,                 # tree의 최대 depth를 3으로 제한
)
model.fit(X_train, y_train)

from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor(
    criterion="squared_error",   # 어떤 feature와 threshold로 나눌지 선택하는 기준
    max_depth=5,                 # tree의 최대 depth를 5로 제한
)
model.fit(X_train, y_train)
```

### 슬라이드 21. Decision Tree Learning (cont.) — 시각화

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

from sklearn.tree import export_text
decision_rules = export_text(
    model,
    feature_names=list(X.columns)
)
print(decision_rules)
```

### 슬라이드 22. Machine Learning Models (기계학습 모델)

- Decision tree
- Random forest
- XGBoost
- Linear/Logistic regression
- Support Vector Machine (SVM)
- K-nearest Neighbor (KNN)
- K-means Clustering
- (Shallow) Neural Network ⇒ **이 수업에서는 neural network만 다룬다!**
- Deep Neural Networks (DNNs)
  - 딥러닝: neural network의 한 종류 (deep learning은 DNN에 기반한다)

### 슬라이드 23. Today... (오늘은...)

6주차 신경망 (1), 과제 1 마감 (강의 계획표는 `week7/lecture_ko.md` 슬라이드 20 참고)

### 슬라이드 24. Outline (목차)

- Learning Lifecycle (학습 생애주기)
- Feature and Label
- Feature and Embedding Spaces
- Decision Boundary (결정 경계)
- Confusion Matrix (혼동 행렬)
- Accuracy, Recall, and Precision
- Cross Validation (교차 검증)

### 슬라이드 25. Learning Lifecycle (학습 생애주기)

Data Collection (데이터 수집) → Model Training (모델 학습) → Model Testing (모델 테스트)

### 슬라이드 26. Feature and Label

- **Feature**: dataset에서 개별적으로 측정할 수 있는 속성이나 특성
  - ⇒ pattern을 찾거나 예측하기 위한 **입력 변수**
  - 예: SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm
  - **Feature vector**: [5.1, 3.5, 1.4, 0.2]
- **Label (= target)**: 모델이 예측하도록 학습되는 정답 또는 결과 ⇒ **출력 변수**
  - 예: Species
  - label은 어떻게 표현할까?
    - **Class ID**: 0 (Iris-setosa), 1 (Iris-versicolor), 2 (Iris-virginica)
    - **One-hot encoding**: Iris-setosa는 [1, 0, 0], Iris-versicolor는 [0, 1, 0], Iris-virginica는 [0, 0, 1]

### 슬라이드 27. Feature Space (특징 공간)

- **Feature space**: 이런 feature vector들이 놓이는 vector 공간
- [그림] 꽃잎 길이·너비 축으로 그린 산점도. Iris-setosa가 다른 두 종과 뚜렷이 떨어져 있다.

### 슬라이드 28. Decision Boundary (결정 경계)

- feature space를 **나누기** 위한 것
  - 예: **linear classifier** (직선으로 나눔)

### 슬라이드 29. Binary vs. Multi-class Classification (이진 분류 vs 다중 클래스 분류)

- **Binary classification**: class가 **두 개**
  - Positive (1)
  - Negative (0)
- **Multi-class classification**: class가 **두 개보다 많음**
  - class 3개의 one-hot encoding
    - class 0은 [1, 0, 0]
    - class 1은 [0, 1, 0]
    - class 2는 [0, 0, 1]
- \+ **Multi-label classification**: label이 두 개 이상 (한 sample이 여러 label을 가질 수 있음)

### 슬라이드 30. Decision Boundary (결정 경계) (cont.)

- feature space를 나누기 위한 것
  - 예: **non-linear classifier** (곡선으로 나눔)
- [그림] Petal length–Petal width 평면에서 setosa(노랑), versicolor(파랑), virginica(초록) 영역을 곡선 경계로 나눈 모습

### 슬라이드 31. (Non-)Linear Separation (선형 / 비선형 분리)

| x | y | AND | OR | XOR |
|---|---|-----|----|-----|
| 0 | 0 | 0   | 0  | 0   |
| 0 | 1 | 0   | 1  | 1   |
| 1 | 0 | 0   | 1  | 1   |
| 1 | 1 | 1   | 1  | 0   |

- AND: **Linear** (직선 하나로 분리 가능)
- OR: **Linear**
- XOR: **?** (직선 하나로는 분리 불가능, 곡선이 필요)

### 슬라이드 32. Embedding Space (임베딩 공간)

- 입력 data의 **근본적인 구조(underlying structure)** 를 알려주는 핵심 feature만 보존한 data point의 표현
- 일반적으로 **Latent Space**(잠재 공간)와 같은 뜻으로 쓰인다.
- [그림] Feature Space에서는 섞여 있던 a, b, c, d가 **Model**을 거친 Embedding Space에서는 같은 종류끼리(파랑 b, c / 빨강 a, d) 모인다.

### 슬라이드 33. Confusion Matrix (혼동 행렬)

- class A의 instance가 class B로 분류된 개수를 세는 것
- [그림] Ground-truth(y)와 Predicted(ŷ) 쌍 8개로 표를 채운 예

|                    | Predicted Positive  | Predicted Negative  |
|--------------------|---------------------|---------------------|
| Ground-truth Pos.  | 3                   | 1                   |
| Ground-truth Neg.  | 2                   | 2                   |

|                    | Predicted Positive  | Predicted Negative  |
|--------------------|---------------------|---------------------|
| Ground-truth Pos.  | (TP) True Positive  | (FN) False Negative |
| Ground-truth Neg.  | (FP) False Positive | (TN) True Negative  |

### 슬라이드 34. Accuracy, Recall, and Precision

- **Accuracy (정확도)**: 맞게 분류한 수 / 전체 분류 수 = **(TP + TN) / (TP + FN + FP + TN)**
  - 모든 class가 **균형**을 이룰 때 사용
  - 예: (3 + 2) / (3 + 1 + 2 + 2) = 5/8 = 0.625

### 슬라이드 35. Accuracy, Recall, and Precision (cont.)

- **Recall (재현율)**: 맞게 분류한 실제 positive / 모든 실제 positive = **TP / (TP + FN)**
  - **False Negative가 치명적일 때** 사용 (예: 질병)
  - 예: 3 / (3 + 1) = 3/4 = 0.75

### 슬라이드 36. Accuracy, Recall, and Precision (cont.)

- **Precision (정밀도)**: 맞게 분류한 실제 positive / positive로 분류한 모든 것 = **TP / (TP + FP)**
  - 실제 positive sample 수가 **제한적일 때** 사용
  - 예: 3 / (3 + 2) = 3/5 = 0.6

### 슬라이드 38. Accuracy, Recall, and Precision in Multi-class (다중 클래스에서의 지표)

|              | Pred. A | Pred. B | Pred. C |
|--------------|---------|---------|---------|
| Actual A     | 8       | 5       | 3       |
| Actual B     | 10      | 60      | 30      |
| Actual C     | 1       | 50      | 200     |

- accuracy = (8 + 60 + 200) / (8 + 5 + 3 + 10 + 60 + 30 + 1 + 50 + 200) ≈ **0.73**

### 슬라이드 39. Multi-class (cont.) — Macro averaging의 recall

- **Macro averaging** (class별로 구한 뒤 평균)
  - recall_A = 8 / (8 + 5 + 3) = 0.50
  - recall_B = 60 / (10 + 60 + 30) = 0.60
  - recall_C = 200 / (1 + 50 + 200) ≈ 0.80
  - recall = (0.50 + 0.60 + 0.80) / 3 ≈ **0.63**

### 슬라이드 40. Multi-class (cont.) — Macro averaging의 precision

- precision_A = 8 / (8 + 10 + 1) ≈ 0.42
- precision_B = 60 / (5 + 60 + 50) ≈ 0.52
- precision_C = 200 / (3 + 30 + 200) ≈ 0.86
- precision = (0.42 + 0.52 + 0.86) / 3 ≈ **0.60**

### 슬라이드 41. Multi-class (cont.) — Micro averaging

- **Micro averaging** (class별 이진 혼동 행렬을 합친 뒤 계산)
  - A vs Not A: TP 8, FN 8, FP 11, TN 340
  - B vs Not B: TP 60, FN 40, FP 55, TN 212
  - C vs Not C: TP 200, FN 51, FP 33, TN 83
  - 합치면: Positive 행 = (8+60+200, 8+40+51), Negative 행 = (11+55+33, 340+212+83)

### 슬라이드 42. Multi-class (cont.) — Micro averaging 계산

- 합친 행렬: TP = 268, FN = 99, FP = 99, TN = 635
- precision = (8+60+200) / ((8+60+200) + (11+55+33)) ≈ **0.73**
- recall = (8+60+200) / ((8+60+200) + (8+40+51)) ≈ **0.73**

### 슬라이드 43. Cross Validation (교차 검증)

- training set을 training set과 testing set으로 직접 나누면
  - ⇒ 결과가 때때로 너무 좋거나 너무 나쁠 수 있다.
- **K-Fold Cross Validation**
  - data를 K개의 부분집합(즉, **fold**)으로 무작위로 나눈다.
  - 모델을 K번 평가한다.
    - (K − 1)개 fold로 training
    - 1개 fold로 testing
  - K번 평가한 성능을 평균낸다.
- 하지만 training을 K번 해야 하므로 ⇒ 시간이 더 든다.

### 슬라이드 44. Cross Validation (cont.)

- K = 5인 경우
  - Model 1 ~ Model 5가 각각 다른 fold를 Testing으로, 나머지를 Training으로 사용 → Performance 1 ~ Performance 5

---

## Part 2. Neural Networks (1)

### 슬라이드 46. Outline (목차)

- Neurons (뉴런)
- Artificial Neural Network (ANN)
- Perceptron
- Activation Function
- Bias Neuron

### 슬라이드 47. Neurons (뉴런)

- **생물학적 neuron**
  - 개별 생물학적 neuron은 꽤 단순하게 동작하는 것처럼 보인다.
  - 이들은 수십억 개로 이루어진 거대한 network로 조직되어 있다.
  - 각 neuron은 보통 수천 개의 다른 neuron과 연결된다.
- 생물학적 신경망(**BNN**)은 여러 개의 연속된 **layer**로 이루어진다.

### 슬라이드 48. Artificial Neural Network (ANN, 인공신경망)

`week7/lecture_ko.md` 슬라이드 2와 같음.

### 슬라이드 49. Perceptron (퍼셉트론)

- 단순한 neural network 구조
- 입력과 출력은 숫자이다.
  - feature 수가 n일 때 **(n + 1)개의 input node** (+1은 bias용)
  - **1개의 output node**
- 각 입력 연결에는 **weight**가 붙어 있다.

### 슬라이드 50. Perceptron (cont.)

`week7/lecture_ko.md` 슬라이드 3과 같음. (TLU: weighted sum z = xᵀw를 계산하고 step function을 적용)

### 슬라이드 51. Activation Function (활성 함수)

- 생물학적 neuron의 **활성화(activation)** 를 흉내 낸다.
- TLU 하나로 단순한 **linear binary classification**을 할 수 있다.
- 예: **Heaviside** activation
  - 결과가 threshold를 넘으면 positive class를 출력한다.
  - 그렇지 않으면 negative class를 출력한다.
  - heaviside(z) = 0 (z < 0), 1 (z ≥ 0)

### 슬라이드 52. Activation Function (cont.)

`week7/lecture_ko.md` 슬라이드 13의 표와 같음. (이 시점에서는 "Softmax는 나중에 다룸"으로 표시)

### 슬라이드 53. Input and Output Layers (입력층과 출력층)

- 모든 input/output neuron이 **input/output layer**를 이룬다.
- **Fully connected layer**: 한 layer의 모든 neuron이 이전 layer의 모든 neuron(즉, 그 layer의 input neuron)과 연결된 layer
- perceptron은 단순히 **TLU 한 층**으로 이루어진다.

### 슬라이드 54. Bias Neuron

- 추가 bias feature: **x₀ = 1**
- **h_{W,b}(X) = φ(XW + b)**
  - **X**: 입력 feature 행렬
  - **W**: weight 행렬
  - **b**: bias 벡터
  - **φ**: activation function
- **Training(학습)이란 weight와 bias의 올바른 값을 찾는 것이다.**
- [그림] 입력 2개, 출력 3개인 perceptron. Bias neuron은 항상 1을 출력한다.

### 슬라이드 55. Next Time... (다음 시간에는...)

7주차 신경망 (2) (강의 계획표는 `week7/lecture_ko.md` 슬라이드 20 참고)

### 슬라이드 56~60. HW #1: Tic-Tac-Toe with AI Bot (과제 1)

- 제출 기한: 10월 8일 오후 11시 55분 (24시간 지각마다 −10%, 1초~24시간 단위)
- 제출물
  1. **Source code** (파일명: '학번-이름-code.py/c/cpp/java')
     - C/C++, Java, Python 코드 모두 허용 (단, **시험은 python만 다룸**)
     - 각 줄에 주석 달기 → **의미 있는 단위마다 남기면 됨**
  2. **Video recording** (파일명: '학번-이름-video.mp4')
     - 모든 전략(minimax search, random, left-up first)을 보여줘야 함
     - 모든 예외(1~9 범위, 빈 칸만 선택 가능)를 보여줘야 함
     - 모든 결과(You win, Bot wins, draw)를 보여줘야 함
- 'Tic-Tac-Toe'를 두는 AI bot 만들기
  - Option 1: Minimax search
  - Option 2: Random
  - Option 3: Left-up first (왼쪽 위부터, 즉 작은 번호부터)
- 게임 시작!
  - 사용자가 먼저 둔다: 위치를 선택한다.
  - 사용자는 'X', Bot은 'O'
- Bot은 선택된 전략에 따라 자동으로 위치를 고른다.
- **Terminal states (종료 상태)**: You Win! (−1), Bot Wins! (+1), Draw! (0)
- **Exceptions (예외)**
  - 1부터 9까지만 고를 수 있다. (예: 11 입력 → "Wrong number")
  - 이미 채워진 위치는 고를 수 없다. (→ "Unavailable")

### 슬라이드 61~62. 중간고사 (원문이 한국어)

`week7/lecture_ko.md` 슬라이드 54~55와 같음. (이 시점의 오피스아워는 10/19(월) 오후 1~9시 @하-1412, 이후 7주차에 변경됨)

### 슬라이드 63. Reference (참고 자료)

- https://en.wikipedia.org/wiki/Activation_function

---

# Lecture 02 (2026-10-08)

> 슬라이드 1의 제목은 "Week 06 - Lecture 01: Neural Networks (2)"로 되어 있지만 실제로는 Lecture 02다.

### 슬라이드 2~18. 복습

| Lecture 02 슬라이드 | 내용                        | 같은 내용                      |
|---------------------|-----------------------------|--------------------------------|
| 2                   | Machine Learning Models     | Lecture 01 슬라이드 22         |
| 3                   | Decision Boundary (linear)  | Lecture 01 슬라이드 28         |
| 4                   | Embedding Space             | Lecture 01 슬라이드 32         |
| 5~8                 | Confusion Matrix, 지표      | Lecture 01 슬라이드 33~36      |
| 10~14               | Multi-class 지표            | Lecture 01 슬라이드 38~42      |
| 15~16               | Cross Validation            | Lecture 01 슬라이드 43~44      |
| 17~18               | Neurons, ANN                | Lecture 01 슬라이드 47~48      |

### 슬라이드 9. Last Check-in Quiz (지난 시간 체크인 퀴즈, 원문이 한국어)

- 1000명을 대상으로 코로나 검사를 했다. 실제 환자 800명 중 700명을 양성으로 예측했다. 실제 환자가 아닌 사람 중 30명을 양성으로 잘못 예측했다.
- Confusion matrix(혼동 행렬)를 작성하고 accuracy(정확도), precision(정밀도), recall(재현율)을 구하시오.
- (풀이는 `lecture_summary.md` 3부 참고: TP 700, FN 100, FP 30, TN 170)

### 슬라이드 19. Today... (오늘은...)

6주차 신경망 (1)

### 슬라이드 20. Outline (목차)

- Perceptron
- Activation Function
- Bias
- Binary Classifier Using Perceptron (퍼셉트론을 이용한 이진 분류기)
- Single-Layer Perceptron (단층 퍼셉트론)
- Multi-Layer Perceptron (다층 퍼셉트론)
- Learning and Propagation (학습과 전파)

### 슬라이드 21. Perceptron (퍼셉트론)

Lecture 01 슬라이드 49와 같음.

### 슬라이드 22. Perceptron (cont.) — 행렬로 표현

- TLU는 입력의 weighted sum을 계산한다: z = w₁x₁ + w₂x₂ + ⋯ + wₙxₙ = **xᵀw**
- 행렬로 쓰면,
  - x = [x₁ ⋯ xₙ]ᵀ, w = [w₁ ⋯ wₙ]ᵀ (둘 다 n×1)
  - xᵀw = [x₁ ⋯ xₙ] · [w₁ ⋯ wₙ]ᵀ = x₁w₁ + ⋯ + xₙwₙ

### 슬라이드 23. Perceptron (cont.)

`week7/lecture_ko.md` 슬라이드 3과 같음.

### 슬라이드 24. Activation Function (활성 함수)

- Lecture 01 슬라이드 51과 같음.
- 추가 질문: **Regression?** (Heaviside는 0/1만 출력하는데 regression에 쓸 수 있을까?)

### 슬라이드 25. Perceptron vs. Neuron (퍼셉트론 vs 뉴런)

- neuron은 perceptron을 **더 일반화한** 것이다.
- **perceptron**은 0 또는 1(binary)을 출력한다.
  - activation function으로 step function(예: Heaviside)을 사용한다.
  - 단순한 classification 문제에 쓰인다.
- **neuron**은 연속적인 값을 출력할 수 있다.
  - 다양한 activation function을 사용한다.
  - 더 복잡한 문제에 쓰일 수 있다.

### 슬라이드 26. Activation Function (cont.)

`week7/lecture_ko.md` 슬라이드 13의 표와 같음.

### 슬라이드 27. Bias (편향)

- **상수 offset 또는 shift**
  - (반면 weight는 각 입력과 연결되어 있다)
- 입력 feature만으로는 표현할 수 없는 pattern을 잡아내기 위한 것
- bias를 포함한 weighted sum
  - z = w₁x₁ + w₂x₂ + ⋯ + wₙxₙ + w₀x₀ (x₀ = 1)
  - z = xᵀw + w₀x₀
  - z = **xᵀw + b**
  - = x₁w₁ + ⋯ + xₙwₙ + b

### 슬라이드 28. Binary Classifier Using Perceptron (퍼셉트론을 이용한 이진 분류기)

`week7/lecture_ko.md` 슬라이드 4와 같음.

### 슬라이드 29. Binary Classifier Using Perceptron — 예시

- 예: w₁ = 1, w₂ = 1, b = −0.5, activation function은 Heaviside (z ≥ 0이면 1)

| x₁ | x₂ | z                          | h |
|----|----|----------------------------|---|
| 0  | 0  | 1·0 + 1·0 − 0.5 = −0.5     | 0 |
| 0  | 1  | 1·0 + 1·1 − 0.5 = 0.5      | 1 |
| 1  | 0  | 1·1 + 1·0 − 0.5 = 0.5      | 1 |
| 1  | 1  | 1·1 + 1·1 − 0.5 = 1.5      | 1 |

- [그림] (x₁, x₂) 평면의 점 a(0,0), b(1,0), c(0,1), d(1,1)과 이를 가르는 직선 (OR 게이트)

### 슬라이드 30. Input and Output Layers (입력층과 출력층)

Lecture 01 슬라이드 53과 같음.

### 슬라이드 31. Single-Layer Perceptron (단층 퍼셉트론) — 열벡터 방식

`week7/lecture_ko.md` 슬라이드 5와 같음. (**φ(WX + b)**, X: n×1, W: m×n, b: m×1)

### 슬라이드 32. Single-Layer Perceptron (cont.) — 행벡터 방식

- 하나의 fully connected layer: **h_{W,b}(X) = φ(XW + b)**
  - **X**: 입력 feature (**1×n** 행렬)
  - **W**: weight (**n×m** 행렬)
  - **b**: bias (**1×m** 행렬)
  - **φ**: activation function
  - W와 b가 Parameters
- XW + b = [x₁ ⋯ xₙ] (1×n) · W (n×m) + [b₁ ⋯ bₘ] (1×m) = 1×m

### 슬라이드 33. Single-Layer Perceptron (cont.)

[그림] 입력: Petal Width(x₁), Petal Length(x₂) / 출력: Setosa, Versicolor, Virginica

### 슬라이드 34~36. Single-Layer Perceptron (cont.) — 출력 neuron별 계산

- Setosa 출력: φ(w₁,₁x₁ + w₁,₂x₂ + b₁)
- Versicolor 출력: φ(w₂,₁x₁ + w₂,₂x₂ + b₂)
- Virginica 출력: φ(w₃,₁x₁ + w₃,₂x₂ + b₃)

### 슬라이드 38. Implementation (다음 수업에서 같이 실행할 예정...)

`week7/lecture_ko.md` 슬라이드 8의 코드와 같음.

### 슬라이드 40. Multi-Layer Perceptron (다층 퍼셉트론)

`week7/lecture_ko.md` 슬라이드 9와 같음.

### 슬라이드 41. Multi-Layer Perceptron (cont.) — Hidden Layer

- input layer, output layer, hidden layer로 구성된다.
- 단순하고 얕은(shallow) neural network
- < Hidden Layer >
  - [x₁⁽¹⁾ ⋯ x₃⁽¹⁾] · W⁽¹⁾ (3×4) + [b₁⁽¹⁾ ⋯ b₄⁽¹⁾] = [x₁⁽²⁾ ⋯ x₄⁽²⁾]

### 슬라이드 42. Multi-Layer Perceptron (cont.) — Output Layer

- < Output Layer >
  - [x₁⁽²⁾ ⋯ x₄⁽²⁾] · W⁽²⁾ (4×2) + [b₁⁽²⁾ b₂⁽²⁾] = [y₁ y₂]
- "**자... 이제 deep learning이 무엇인지 설명할 수 있나요?**"

### 슬라이드 43. MLP vs. Neural Network (MLP vs 신경망)

- neural network는 multi-layer perceptron을 **더 일반화한** 것이다.
- MLP(또는 Perceptron)는
  - Fully-connected
  - (원래 perceptron에서는) step function 사용
- neural network(NN)는
  - fully-connected일 필요가 없다.
  - 다양한 activation function을 사용할 수 있다.
- 현대의 MLP는 대부분 그냥 neural network로 간주된다...

### 슬라이드 44. # of Output Neurons in Classification (분류에서 출력 neuron의 개수)

| Binary Classification                    | Multi-class Classification                       |
|------------------------------------------|--------------------------------------------------|
| neuron 하나면 충분하다                   | 각 출력 neuron이 값을 하나씩 가진다              |
| threshold를 기준으로 판단                | 출력값들을 비교해서                              |
| 출력이 threshold보다 크면 True           | 가장 그럴듯한 출력을 True로 (single label일 때)  |

### 슬라이드 45. Learning (학습)

- (loss function으로부터 나온) **오차를 최소화하는 model parameter를 찾는 것**
1. parameter를 초기화한다 (랜덤 값 또는 0으로)
   - 때로는... '**pretrained parameters**'를 사용할 수도 있다.
2. 반복:
   - 2-1) 출력을 계산한다.
   - 2-2) (loss function으로부터) 오차를 계산한다.
   - 2-3) loss를 최소화하도록 parameter를 업데이트한다.

### 슬라이드 46. Propagation (전파)

η: Learning rate

- **W(t) = W(t − 1) + ΔW**
- Weight W로 **Forward Propagation** → Predicted Output을 Ground-truth와 비교 → **Loss Function: L**
- **Backward Propagation** (= Backpropagation) → **Gradient: ∂L/∂W**
- **Weight Update: ΔW = −η · ∂L/∂W**

### 슬라이드 47. Next Time... (다음 시간에는...)

7주차 신경망 (2)

### 슬라이드 48~55. HW #1과 중간고사

- HW #1: Lecture 01 슬라이드 56~60과 같음.
- 중간고사: `week7/lecture_ko.md` 슬라이드 54~55와 같음. (오피스아워가 10/19(월) 11~16시 교수님 @하-1412, 16~21시 조교 @하-1210으로 바뀜)

### 슬라이드 56. Reference (참고 자료)

- https://en.wikipedia.org/wiki/Activation_function
