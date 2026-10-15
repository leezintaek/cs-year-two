# 중간고사 대비 모의문제 — Set 1

> 범위: Problem Solving(2주차) ~ Neural Networks(7주차)
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (코드는 모두 Python)
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** BFS는 모든 행동 비용이 같을 때 최적해를 보장한다.

**2.** Hill climbing은 방문한 상태 집합을 기록하기 때문에 local optimum에서 벗어날 수 있다.

**3.** P → Q 와 ¬Q 가 참이면 ¬P 를 추론할 수 있다. (Modus Tollens)

**4.** 나이브 베이즈 모델은 클래스가 주어졌을 때 특징(feature)들이 서로 조건부 독립이라고 가정한다.

**5.** Heaviside 활성 함수를 사용하는 퍼셉트론은 연속적인 값을 예측하는 회귀 문제에 적합하다.

---

## Part B. 객관식

**6.** A* search의 평가 함수 f(n)으로 옳은 것은?
① h(n)  ② g(n)  ③ g(n) + h(n)  ④ g(n) + W·h(n) (W > 1)

**7.** 다음 중 **지도학습(supervised learning)이 아닌** 것은?
① 사진 속 동물 종류 분류  ② 집 정보로 집값 예측  ③ 레이블 없는 고객 데이터 군집화(clustering)  ④ 메일의 스팸 여부 분류

**8.** 단층 퍼셉트론 h(x) = φ(Wx + b)에서 입력 특징이 4개, 출력 뉴런이 3개이다. (x는 열벡터) W의 크기는?
① 4×3  ② 3×4  ③ 3×1  ④ 4×1

**9.** 직선 하나로 0과 1을 분리할 수 **없는** 논리 연산은?
① AND  ② OR  ③ XOR  ④ NAND

**10.** 질병 진단처럼 **실제 환자를 놓치는 것(FN)이 치명적인** 상황에서 특히 중요하게 봐야 하는 지표는?
① Accuracy  ② Precision  ③ Recall  ④ Error rate

**11.** 다음 중 **분류(classification)용 손실 함수가 아닌** 것은?
① Categorical cross-entropy  ② Hinge loss  ③ Huber loss  ④ KL Divergence

---

## Part C. 단답형

**12.** 아래 게임 트리에서 루트는 MAX, 그 아래 두 노드는 MIN이다. 리프는 왼쪽부터 탐색한다.
```
            MAX
          /     \
       MIN1     MIN2
      / | \     / | \
     3 12  8   2  4  6
```
(a) Minimax로 구한 루트의 값은?
(b) 알파-베타 가지치기를 적용하면 탐색하지 않아도 되는(가지치기되는) 리프 값들은?

**13.** 어떤 질병의 유병률이 1%이다. 검사는 환자에게 90% 확률로 양성, 비환자에게 10% 확률로 (잘못) 양성이 나온다. 검사가 양성일 때 실제로 환자일 확률은? (소수점 셋째 자리까지)

**14.** 이진 분류 결과가 TP = 40, FN = 10, FP = 20, TN = 30 이다. Accuracy, Precision, Recall을 각각 구하시오.

**15.** 예측값 ŷ = [2, 4, 6], 정답 y = [3, 4, 8] 일 때 MAE와 RMSE를 구하시오. (RMSE는 소수점 둘째 자리까지)

**16.** MNIST(28×28 흑백, 클래스 10개)를 784 → 128 → 10 구조의 MLP로 분류한다.
(a) 입력 뉴런 수와 출력 뉴런 수는?
(b) 은닉층(784 → 128)의 학습 파라미터(가중치 + bias) 개수는?

---

## Part D. 빈칸 채우기 손코딩

**17.** 정확도(accuracy)를 계산하는 코드를 완성하시오.
```python
correct = 0
for actual, predicted in zip(y_test, y_pred):
    if ____(a)____:
        correct += 1
accuracy = ____(b)____
```

**18.** 단층 퍼셉트론의 순전파를 NumPy로 구현하시오. (Heaviside: z ≥ 0이면 1)
```python
import numpy as np
x = np.array([[0.2], [1.4]])                       # (2, 1)
W = np.array([[-0.8, -1.2], [0.1, -0.05], [0.7, 1.3]])   # (3, 2)
b = np.array([[-0.4], [-0.01], [0.4]])             # (3, 1)

z = np.____(a)____(W, x) + b                       # (3, 1)
y = np.____(b)____(z >= 0, 1, 0)
```

**19.** 전체 데이터의 20%를 테스트 세트로 쓰고, 클래스 비율이 유지되도록 분할하시오.
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=____(a)____,
    random_state=42,
    stratify=____(b)____
)
```

**20.** PyTorch 학습 루프에서 빈칸에 들어갈 코드를 순서대로 쓰시오.
```python
logits = model(images)                 # Forward propagation
loss = criterion(logits, labels)       # Loss 계산

____(a)____                            # 이전 gradient 초기화
____(b)____                            # Backpropagation
____(c)____                            # 가중치·bias 업데이트
```

---
---

## 정답 및 해설

**1. O** — BFS는 행동 비용이 동일할 때 최적해를 보장한다. (DFS는 보장하지 않음)

**2. X** — Hill climbing은 local search라 경로나 방문 상태를 **기록하지 않는다**. 그래서 local optimum에 갇힐 수 있다. 상태를 기록해 local minima에서 벗어날 수 있는 것은 global search다.

**3. O** — Modus Tollens: P→Q, ¬Q ⟹ ¬P.

**4. O** — 이 가정이 "나이브(naive)"라는 이름의 이유다.

**5. X** — Heaviside는 0 또는 1만 출력하므로 회귀에 쓸 수 없다.

**6. ③** — ① Greedy best-first, ② Uniform-cost, ④ Weighted A*.

**7. ③** — 군집화는 대표적인 비지도학습이다.

**8. ②** — 열벡터 방식 φ(Wx + b)에서 W는 (출력 수 × 입력 수) = 3×4.

**9. ③** — XOR은 선형 분리가 불가능하다. 그래서 은닉층이 있는 MLP가 필요하다.

**10. ③** — Recall = TP / (TP + FN). FN이 줄어야 Recall이 올라간다.

**11. ③** — Huber loss는 회귀용 손실 함수다.

**12.** (a) **3** — MIN1 = min(3, 12, 8) = 3, MIN2 = min(2, 4, 6) = 2, 루트 = max(3, 2) = 3
(b) **4, 6** — MIN1을 마치면 α = 3. MIN2에서 첫 리프 2를 보면 MIN2 ≤ 2 ≤ α 이므로 나머지 리프(4, 6)는 볼 필요가 없다.

**13. 약 0.083**
P(D|+) = (0.9 × 0.01) / (0.9 × 0.01 + 0.1 × 0.99) = 0.009 / 0.108 ≈ 0.083

**14.** Accuracy = (40+30)/100 = **0.7**, Precision = 40/(40+20) ≈ **0.667**, Recall = 40/(40+10) = **0.8**

**15.** 오차 = [−1, 0, −2]
MAE = (1+0+2)/3 = **1**, MSE = (1+0+4)/3 ≈ 1.667, RMSE = √1.667 ≈ **1.29**

**16.** (a) 입력 **784** (= 28×28), 출력 **10**
(b) 784 × 128 + 128 = **100,480**

**17.** (a) `actual == predicted`  (b) `correct / len(y_test)`

**18.** (a) `matmul`  (b) `where`

**19.** (a) `0.2`  (b) `y`

**20.** (a) `optimizer.zero_grad()`  (b) `loss.backward()`  (c) `optimizer.step()`
