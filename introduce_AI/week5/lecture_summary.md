# Week5 강의 요약

**과목**: 인공지능개론(CSE2302) · **주제**: 지식과 추론 (4) 마무리 → 기계학습 기초 (Machine Learning)
**강의일**: 2026-09-29(Lecture 01), 2026-10-01(Lecture 02)

---

## 1부: 지난 주차 복습 (Lecture 01 앞부분)

### 추론 기법 4가지 갈래 (다시 보기)
논리(Logics) / 베이지안 네트워크(Bayesian networks) / 마르코프 모델(Markov models) / 심층 신경망(Deep neural networks). 이번 주에는 마르코프 모델을 마무리하고 기계학습으로 넘어간다.

### 나이브 베이즈를 이용한 텍스트 분류 (복습)
- 하나의 원인(카테고리)이 여러 결과(단어 등장 여부)에 영향을 주고, 결과들은 원인이 주어졌을 때 서로 조건부 독립이라고 가정.
- **ŷ = argmax_k p(C_k) × Π p(xᵢ|C_k)**
- 예: 단어 목록 {"president", …, "game", "team"}, P(Category=Sports)=0.25, P(HasWord_president=False|Sports)=0.99, P(HasWord_game=True|Sports)=0.12, P(HasWord_team=True|Sports)=0.10
- 기사 "The president will attend the NBA finals. Who's gonna win the game?"가 주어지면
  - 기사에 있고 단어 목록에도 있는 단어(president, game 등) → HasWord=True 확률을 곱함
  - 기사에 없지만 단어 목록에 있는 단어(team 등) → HasWord=False 확률을 곱함
  - P(Sports|article) ∝ P(Sports) × P(HasWord_president=True|Sports) × P(HasWord_game=True|Sports) × ⋯ × P(HasWord_team=False|Sports)

### 베이지안 네트워크 (복습)
- DAG로 변수 간 인과관계를 표현. **P(X₁=x₁,…,Xₙ=xₙ) = Π P(xᵢ|Parents(Xᵢ))**
- 도난-지진-경보 예시: P(j,m,a,¬b,¬e) = 0.90×0.70×0.001×0.999×0.998 ≈ 0.000628

### 지난 체크인 퀴즈 풀이: 잔디가 젖었을 때 비가 오지 않았을 확률
- P(R=F|G=T) = [P(G=T,S=T,R=F) + P(G=T,S=F,R=F)] / P(G=T)
  = (0.288 + 0.0) / (0.00198 + 0.288 + 0.1584 + 0.0) **≈ 64.23%**
- 예: P(G=T,S=T,R=F) = P(G=T|S=T,R=F) × P(S=T|R=F) × P(R=F) = 0.9 × 0.4 × 0.8 = 0.288
- 참고로 P(R=T|G=T) ≈ 35.77%이므로 두 값의 합은 1이 된다.

---

## 2부: 시간에 따른 확률적 추론 — 마르코프 모델

### 기본 아이디어
- 과거 이력으로부터 현재 상태를 판단하고, 행동의 결과를 예측하는 것이 목적.
- 세상을 시간 조각(time slice)들의 연속으로 본다.
- 현재 상태는 바로 이전 상태에만 의존한다: **P(X_t | X_(t-1))** ⇒ **마르코프 과정(Markov Process)**

### 마르코프 체인(Markov Chain) 예시: 간단한 날씨 모델
"오늘이 맑다면 내일 날씨는?"
- **전이 모델(Transition model)** P (행: 오늘, 열: 내일, 순서는 [맑음, 비]):
  ```
  [0.9  0.1]   ← 맑음 → 맑음 0.9, 맑음 → 비 0.1
  [0.5  0.5]   ← 비 → 맑음 0.5,  비 → 비 0.5
  ```
- 초기 상태 x⁽⁰⁾ = [1, 0] (오늘 맑음)
- x⁽¹⁾ = x⁽⁰⁾P = [0.9, 0.1] (내일 맑을 확률 90%)
- x⁽²⁾ = x⁽¹⁾P = [0.9×0.9 + 0.1×0.5, 0.9×0.1 + 0.1×0.5] = [0.86, 0.14] (모레)

### 두 가지 모델
- **전이 모델(Transition model)**: P(X_t | X_(t-1)) — 숨겨진 상태가 시간에 따라 어떻게 변하는지
- **관측 모델(Observation model)**: P(E_t | X_t) — 숨겨진 상태에서 어떤 관측(증거, evidence)이 나오는지

### 은닉 마르코프 모델 (Hidden Markov Model, HMM)
- 프로세스의 상태가 **하나의 이산적인(single, discrete) 확률 변수**로 기술되는 시간적 확률 모델.
  - 상태 변수: Rain_t (비가 오는가)
- 실제 날씨(상태)는 직접 보이지 않고(hidden), 사람이 **우산을 들고 왔는지(Umbrella)**만 관측된다.
- 질문: "관측된 우산 순서가 주어졌을 때, 가장 그럴듯한 숨겨진 날씨 순서는?"

### 비터비 알고리즘 (Viterbi Algorithm)
**가장 가능성 높은 숨겨진 상태 순서(most likely sequence of hidden events)**를 찾는 알고리즘.

**Pₜ(j) = maxᵢ [ Pₜ₋₁(i) · P(Rₜ=j | Rₜ₋₁=i) ] · P(Uₜ | Rₜ=j)**
(앞쪽 P(Rₜ|Rₜ₋₁)는 전이 모델, 뒤쪽 P(Uₜ|Rₜ)는 관측 모델)

**예시에서 사용한 확률값**
| 전이 모델    | 값  | 관측 모델     | 값  |
| ------------ | --- | ------------- | --- |
| P(R=T → R=T) | 0.7 | P(U=T \| R=T) | 0.9 |
| P(R=T → R=F) | 0.3 | P(U=T \| R=F) | 0.2 |
| P(R=F → R=T) | 0.3 | P(U=F \| R=T) | 0.1 |
| P(R=F → R=F) | 0.7 | P(U=F \| R=F) | 0.8 |

**관측 순서**: U₁=T, U₂=T, U₃=F, U₄=T, U₅=T (초기 P₀(T)=P₀(F)=0.5)

| t   | 관측 | Pₜ(T) (비 옴)                                   | Pₜ(F) (비 안 옴)                                |
| --- | ---- | ----------------------------------------------- | ----------------------------------------------- |
| 0   | –    | 0.500                                           | 0.500                                           |
| 1   | U=T  | max(0.5·0.7, 0.5·0.3)·0.9 = **0.315**           | max(0.5·0.3, 0.5·0.7)·0.2 = **0.07**            |
| 2   | U=T  | max(0.315·0.7, 0.07·0.3)·0.9 = **0.19845**      | max(0.315·0.3, 0.07·0.7)·0.2 = **0.0189**       |
| 3   | U=F  | max(0.19845·0.7, 0.0189·0.3)·0.1 = **0.01389**  | max(0.19845·0.3, 0.0189·0.7)·0.8 = **0.04762**  |
| 4   | U=T  | max(0.01389·0.7, 0.04762·0.3)·0.9 = **0.01286** | max(0.01389·0.3, 0.04762·0.7)·0.2 = **0.00667** |
| 5   | U=T  | max(0.01286·0.7, 0.00667·0.3)·0.9 = **0.0081**  | max(0.01286·0.3, 0.00667·0.7)·0.2 = **0.00093** |

- Lecture 01에서는 t=3까지 진행: P₃(F) > P₃(T) → 3일째는 비가 오지 않았을 가능성이 높다.
- Lecture 02에서는 t=5까지 진행: P₅(T) > P₅(F) → 마지막 날은 비가 왔을 가능성이 높다.
- (보충) 각 단계에서 max를 준 이전 상태를 거꾸로 따라가면(backtracking) 전체 최적 순서는 **비-비-안 옴-비-비 (T, T, F, T, T)**가 된다.

---

## 3부: 기계학습(Machine Learning) 소개

### 왜 기계학습이 필요한가
- 설계자(프로그래머)가 미래에 일어날 모든 상황을 예측할 수 없다.
- 때로는 설계자가 해결책을 어떻게 프로그래밍해야 할지조차 모른다.

### AI ⊃ ML ⊃ DL
- **인공지능(AI)**: 인간의 지능과 관련된 작업을 수행할 수 있는 컴퓨터/기계를 만드는 것
- **기계학습(ML)**: 데이터로부터 학습하고, 보지 못한 데이터(unseen data)에 일반화(generalize)하여, 명시적으로 프로그래밍하지 않고도 작업을 수행하는 것
- **딥러닝(DL)**: (깊은) 인공 신경망을 사용하는 기계학습

### 학습(Learning)이란
- **학습**: 에이전트가 관측(observation)을 한 뒤 성능이 향상되는 것
- **기계학습**: 컴퓨터가 데이터를 관찰하고, 그 데이터로 **모델(model)**을 만들고, 그 모델로 문제를 해결하는 것

### 피드백 방식에 따른 학습의 종류
| 종류                          | 학습 방식                                                     | 예시                   |
| ----------------------------- | ------------------------------------------------------------- | ---------------------- |
| **지도학습 (Supervised)**     | 입력-출력 쌍으로 입력→출력 함수를 학습, 새 입력의 레이블 예측 | 이미지 → "bus"         |
| **비지도학습 (Unsupervised)** | 피드백 없이 입력 속 패턴 학습 (대표: **군집화, clustering**)  | 비슷한 이미지끼리 묶기 |
| **강화학습 (Reinforcement)**  | 보상·벌을 보고 보상이 커지도록 행동을 바꿈                    | 체스 승(보상)/패(벌)   |

---

## 4부: 지도학습(Supervised Learning)

### 정의
- N개의 입력-출력 쌍으로 된 훈련 집합 (x₁,y₁), (x₂,y₂), …, (x_N,y_N)이 주어짐. 각 쌍은 알 수 없는 함수 **y = f(x)**로 생성됨.
- 목표: 참 함수 f를 근사하는 함수(모델) **h**를 찾는 것.
- 예: 나이(입력) → 키(출력)의 관계를 표현하는 모델.
- 같은 참 함수 f에서 나온 데이터라도, **훈련 데이터가 다르면 학습된 모델 h도 달라진다.**

### 분류(Classification) vs 회귀(Regression)
- **분류**: 클래스를 예측. (예: 픽셀 RGB 값 → "사과"일 확률 → 확률이 가장 높은 클래스 선택)
- **회귀**: 연속적인 값(value)을 예측. (예: 집값)
- 둘 다 레이블(정답)이 있으므로 지도학습이다.

### 모델 성능(Model Performance)
- 모델의 진짜 실력은 **훈련 집합에서 얼마나 잘하느냐가 아니라, 아직 보지 못한 데이터를 얼마나 잘 처리하느냐**로 측정한다.
- **테스트 집합(Test set)**: 보지 못한 (xᵢ, yᵢ)들의 집합
  - 입력 xᵢ로부터 출력 ŷᵢ를 예측
  - **정답(Ground-truth)**: 모델이 맞혀야 하는 실제 답 yᵢ
  - **오류율(Error rate)**: 예측값 ≠ 정답인 비율, 즉 h(xᵢ) = ŷᵢ ≠ yᵢ인 비율
- 반면 훈련 집합은 모델 h를 **만드는** 데 쓰인다.

### 과소적합(Underfitting) vs 과대적합(Overfitting)
| 과소적합 (Underfitting)                | 과대적합 (Overfitting)                   |
| -------------------------------------- | ---------------------------------------- |
| 훈련 데이터로부터 충분히 학습하지 못함 | 훈련 데이터에 지나치게 집중함            |
| 데이터의 패턴을 찾지 못함              | 그 결과 보지 못한 데이터에서 성능이 나쁨 |

- 목표: 훈련 데이터를 이용해 오류율을 줄이는 **균형 잡힌 모델(balanced model)**을 만드는 것. (너무 단순하면 과소적합, 너무 복잡하면 과대적합 가능성↑)

### 훈련 / 검증 / 테스트 집합
| 집합                           | 역할                                                               |
| ------------------------------ | ------------------------------------------------------------------ |
| **훈련 집합 (Training set)**   | 모델을 학습시키고 만드는 데 사용 (seen/known data)                 |
| **검증 집합 (Validation set)** | 모델을 평가해 **가장 좋은 모델을 고르는 데** 사용                  |
| **테스트 집합 (Test set)**     | 고른 최선의 모델을 **최종 평가**하는 데 사용 (unseen/unknown data) |

- 데이터 하나하나를 **Example = Instance = Sample = Data point**라고 부른다(모두 같은 의미).

---

## 5부: 기계학습의 주요 과제와 데이터셋 (Lecture 02)

### 기계학습의 주요 과제 (Main Challenges)
- 훈련 데이터의 **양이 부족함**
- **품질이 낮은** 데이터
- 훈련 데이터에 대한 **과대적합/과소적합**
- **대표성이 없는** 훈련 데이터 (이상치(Outlier): 다른 관측값들과 크게 다른 데이터 포인트)
- **관련 없는 특징(Irrelevant features)** → 특징 선택(feature selection)을 포함한 **특징 공학(Feature engineering)** 필요

### 분류 데이터셋: Iris (붓꽃)
- 입력 특징 4개: SepalLengthCm(꽃받침 길이), SepalWidthCm(꽃받침 너비), PetalLengthCm(꽃잎 길이), PetalWidthCm(꽃잎 너비)
- 출력: Species(꽃 종류) — Iris-setosa / Iris-versicolor / Iris-virginica (3개 클래스)
- **Hugging Face**: 기계학습 커뮤니티가 모델, 데이터셋, 애플리케이션을 공유·협업하는 플랫폼. 여기서 Iris 데이터셋을 받아온다.

```python
import pandas as pd
from datasets import load_dataset
dataset = load_dataset("scikit-learn/iris", split="train")
df = dataset.to_pandas()
print(df.head(10).to_string(index=False))
```

### 특징(Feature)과 레이블(Label)
- **특징(Feature)**: 데이터셋의 개별적으로 측정 가능한 속성 → 패턴을 찾거나 예측하기 위한 **입력 변수**
  - 예: SepalLengthCm 등 4개 / **특징 벡터(Feature vector)**: [5.1, 3.5, 1.4, 0.2]
- **레이블(Label, = target)**: 모델이 예측하도록 학습하는 정답 → **출력 변수**
  - 예: Species
  - 표현 방법
    - **클래스 ID**: 0(setosa), 1(versicolor), 2(virginica)
    - **원-핫 인코딩(One-hot encoding)**: [1,0,0](setosa), [0,1,0](versicolor), [0,0,1](virginica)
- **특징 공간(Feature space)**: 특징 벡터들이 놓이는 벡터 공간. (Iris를 그려보면 setosa가 다른 두 종과 뚜렷이 분리됨)

### 입력 X / 출력 y 분리
```python
X = df[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]]  # 4개 input features
y = df["Species"]  # 3개의 class (setosa, versicolor, virginica)
```

### 훈련/테스트 데이터 분할
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 전체 데이터의 20%를 test set으로 사용
    random_state=42,    # 돌릴 때마다 같게 분할되도록 시드 고정
    stratify=y          # y(클래스 비율) 기준으로 균일하게 분할
)
```

### 학습과 테스트
- X_train, y_train으로 모델을 **학습(fit)** → 학습된 모델에 X_test를 넣어 **예측(predict)** → 예측 결과를 y_test(정답)와 비교.

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

### 성능 지표 1: 정확도와 오류율 (주로 분류)
- **accuracy = (ŷ = y인 샘플 수) / (테스트 샘플 수)**
- **errorRate = (ŷ ≠ y인 샘플 수) / (테스트 샘플 수) = 1 − accuracy**

```python
correct = 0
for actual, predicted in zip(y_test, y_pred):
    if actual == predicted:
        correct += 1
accuracy = correct / len(y_test)
error_rate = (len(y_test) - correct) / len(y_test)
```

### 회귀 데이터셋: California Housing
- 입력 특징 8개: MedInc(블록 그룹 중위 소득), HouseAge(주택 중위 연식), AveRooms(가구당 평균 방 수), AveBedrms(가구당 평균 침실 수), Population(인구), AveOccup(평균 가구원 수), Latitude(위도), Longitude(경도)
- 출력: MedHouseVal(주택 가격 중앙값)

```python
from sklearn.datasets import fetch_california_housing
housing = fetch_california_housing(as_frame=True)
X = housing.data
y = housing.target
# train_test_split은 동일 (회귀이므로 stratify 없음)

from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor(criterion="squared_error", max_depth=5, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

### 성능 지표 2: MAE, MSE, RMSE (주로 회귀)
- **MAE (Mean Absolute Error)** = Σ|ŷᵢ − yᵢ| / m
- **MSE (Mean Squared Error)** = Σ(ŷᵢ − yᵢ)² / m
- **RMSE (Root MSE)** = √MSE
- (ŷ: 예측값, y: 정답, m: 테스트 샘플 수)

**수치 예시**: 예측 (4,3,4,5,11), 정답 (3,5,1,1,6) → 오차 ŷ−y = (1, −2, 3, 4, 5)
- MAE = (1+2+3+4+5)/5 = **3**
- RMSE = √((1+4+9+16+25)/5) = √11 ≈ **3.3**

**MSE/RMSE는 큰 오차에 MAE보다 더 큰 벌점을 준다**
| 오차                   | MAE | RMSE   |
| ---------------------- | --- | ------ |
| {1, −2, 3, 4, 5}       | 3   | ≈ 3.3  |
| {1, −2, 3, 4, **100**} | 22  | ≈ 44.8 |

```python
total_error = 0
for actual, predicted in zip(y_test, y_pred):
    total_error += abs(actual - predicted)
mae = total_error / len(y_test)

total_squared_error = 0
for actual, predicted in zip(y_test, y_pred):
    total_squared_error += (actual - predicted) ** 2.0
rmse = (total_squared_error / len(y_test)) ** 0.5
```

---

## 6부: 결정 트리(Decision Tree)

### 결정 트리란
- 속성값 벡터(입력)를 하나의 출력값, 즉 **"결정(decision)"**으로 매핑하는 함수.
- 일련의 테스트를 수행하여 결정에 도달한다.
- **루트(root)**에서 시작해 조건에 맞는 가지(branch)를 따라 내려가다 **리프(leaf)**에 도착하면 결정이 나온다.
- 예: 식당에서 자리를 기다릴지(Wait) 말지(Do not wait) 결정하는 트리.

### 결정 트리 학습(Decision Tree Learning)
- 규칙(어떤 특징을, 어떤 임곗값(threshold)으로 나눌지)을 사람이 직접 쓰지 않고, 데이터로부터 학습해 목표 변수를 예측.
- 예: Class1 20개, Class2 20개 → 규칙1 x₁ ≤ T₁로 나누면
  - 한쪽: Class1 13개, Class2 0개 → Class 1 (순수)
  - 다른 쪽: Class1 7개, Class2 20개 → 규칙2 x₂ ≤ T₂로 다시 분할 → (7, 4) / (0, 16)
- **불순도(impurity)**: 한 노드에 여러 클래스가 섞여 있는 정도. 한 클래스만 있으면 불순도 0(zero impurity).
  - 분할 규칙 선택에는 **지니 불순도(Gini impurity)**나 **정보 이득(Information gain)** 같은 지표가 널리 쓰인다.
- 규칙은 **탐욕적(greedy)** 방식으로 찾는다: 매 단계마다 지금 당장 불순도를 가장 많이 줄이는 분할을 선택.

### Iris 데이터로 학습한 결정 트리 예시
```
|--- PetalLengthCm <= 2.45
|   |--- class: Iris-setosa
|--- PetalLengthCm >  2.45
|   |--- PetalWidthCm <= 1.65
|   |   |--- PetalLengthCm <= 4.95 → Iris-versicolor
|   |   |--- PetalLengthCm >  4.95 → Iris-virginica
|   |--- PetalWidthCm >  1.65
|   |   |--- PetalLengthCm <= 4.85 → Iris-virginica
|   |   |--- PetalLengthCm >  4.85 → Iris-virginica
```
- 시각화된 각 노드에는 **결정 규칙, 샘플 수, 불순도, 다수 클래스(majority class)**가 표시된다.
- 꽃잎 길이 하나만으로 setosa는 완벽히 분리된다(특징 공간에서 본 것과 일치).

### 하이퍼파라미터와 시각화
- 분류: `DecisionTreeClassifier(criterion="gini", max_depth=3)`
- 회귀: `DecisionTreeRegressor(criterion="squared_error", max_depth=5)`
  - `criterion`: 어떤 feature와 threshold로 나눌지 선택하는 기준
  - `max_depth`: 트리의 최대 깊이 제한 (너무 깊으면 과대적합 위험)
- 시각화: `sklearn.tree.plot_tree(model, feature_names=..., class_names=model.classes_, filled=True, rounded=True)`
- 텍스트 규칙 출력: `sklearn.tree.export_text(model, feature_names=list(X.columns))`

---
 
## 참고: 공지사항 (수업 운영 관련, 참고용)

- **강의 계획**: 5주 기계학습 기초 → 6주 신경망(1) (과제 1 마감) → 7주 신경망(2) → 8주 중간고사. (상황에 따라 변경될 수 있음)
- **과제 1 (Tic-Tac-Toe AI 봇)**:
  - 제출 기한: 10월 8일 오후 11시 55분 (24시간 지각당 -10%)
  - 제출물: 소스 코드(학번-이름-code.py/c/cpp/java), 영상(학번-이름-video.mp4)
  - 미니맥스 / 무작위(Random) / 왼쪽-위 우선(Left-up first) 세 전략 모두, 예외 처리(1~9 범위, 이미 채워진 칸) 모두, 결과(승/패/무) 모두 영상에서 시연
  - 주석은 의미 있는 단위마다 남기면 됨. 코드는 C/C++/Java/Python 모두 가능하지만 시험은 Python만 다룸.
- **중간고사** (시험 전 재공지 예정):
  - 일시: 10월 20일(화) 오후 6:30~7:30, **6:20까지 입실**
  - 장소: **지하 대강당** (수업 강의실 아님)
  - 준비물: 신분증/학생증, 계산기(공학용 계산기 불필요)
  - 힌트노트: A4 단면 1장 **수기 작성** 허용 (부적합 시 사용 제한될 수 있음)
  - 범위: Problem Solving(2주차) ~ Neural Networks(7주차)
  - 유형: T/F, 객관식, 단답형, 빈칸 채우기 손코딩 (코드는 Python만, 사소한 문법 오류는 허용)
  - 오피스아워: 10/19(월) 13~21시 @하-1412, 10/20(화) 수업 시간 @하-1412. 10/15(목) 마지막 수업 꼭 참석.
