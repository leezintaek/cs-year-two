# 중간고사 대비 모의문제 — Set 3

> 범위: Problem Solving(2주차) ~ Neural Networks(7주차)
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (코드는 모두 Python)
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** 튜링 테스트는 기계의 내부 작동 방식을 분석해서 지능이 있는지 판단한다.

**2.** Greedy best-first search의 평가 함수는 f(n) = h(n)이다.

**3.** Heuristic alpha-beta tree search에서는 Utility 함수 대신 EVAL 함수를, terminal test 대신 cutoff test를 사용한다.

**4.** 과대적합(overfitting)된 모델은 훈련 데이터에서 성능이 나쁘다.

**5.** K-fold cross validation은 모델을 K번 학습시키기 때문에 한 번만 나눠서 학습할 때보다 시간이 더 든다.

---

## Part B. 객관식

**6.** 1969년 민스키와 페퍼트의 책 *Perceptrons*가 보여준 것과, 그 결과로 옳은 것은?
① 퍼셉트론이 XOR를 학습할 수 없음 → 첫 번째 AI 겨울
② 역전파가 가능함 → 신경망 부활
③ 체스에서 인간을 이김 → AI 붐
④ 대규모 데이터가 필요함 → Big Data 시대

**7.** Global search와 비교한 Local search의 장점은?
① local optimum에 갇히지 않는다
② 메모리 사용이 적고 빠르다
③ 항상 최적해를 찾는다
④ 시작 노드부터의 경로를 모두 기록한다

**8.** 드모르간의 법칙에 따라 ¬(P ∧ Q)와 동치인 것은?
① ¬P ∧ ¬Q  ② ¬P ∨ ¬Q  ③ P ∨ Q  ④ ¬P → Q

**9.** 은닉 마르코프 모델에서 P(E_t | X_t)를 무엇이라 부르는가?
① 전이 모델(transition model)
② 관측 모델(observation model)
③ 사전 확률(prior)
④ 조건부 확률표(CPT)

**10.** 정답 레이블이 one-hot 벡터가 아니라 **정수(0, 1, 2, …)** 로 주어질 때 쓰는 분류 손실 함수는?
① MSE  ② Hinge loss  ③ Sparse categorical cross-entropy  ④ Huber loss

**11.** learning rate를 너무 크게 잡으면 생길 수 있는 문제는?
① 학습이 아주 느려진다
② 최솟값을 지나쳐 loss가 발산할 수 있다
③ 파라미터 수가 늘어난다
④ 과소적합이 반드시 일어난다

---

## Part C. 단답형

**12.** 아래 그래프에서 S에서 G로 가는 경로를 찾는다.
```
간선 비용: S→A = 1, A→G = 5, S→B = 3, B→G = 2
휴리스틱:  h(S) = 4, h(A) = 1, h(B) = 2, h(G) = 0
```
(a) Greedy best-first search가 찾는 경로와 그 비용은?
(b) A* search가 찾는 경로와 그 비용은?

**13.** 도난-지진-경보 베이지안 네트워크 (Burglary, Earthquake → Alarm → JohnCalls, MaryCalls)에서 다음 값이 주어졌다.
- P(¬b) = 0.99, P(¬e) = 0.95, P(a | ¬b, ¬e) = 0.002, P(j | a) = 0.8, P(m | a) = 0.5

P(j, m, a, ¬b, ¬e)를 구하시오.

**14.** 3-클래스 혼동 행렬이 아래와 같다. (행: 실제, 열: 예측)
```
        A   B   C
   A    5   3   2
   B    1   8   1
   C    0   4  16
```
(a) Accuracy는?
(b) 클래스별 recall과 macro-averaged recall은?

**15.** 입력 x = [1, 2]가 은닉층(뉴런 2개, ReLU) → 출력층(뉴런 1개, identity)을 지난다.
- 은닉 뉴런 1: 가중치 [1, −1], bias 0
- 은닉 뉴런 2: 가중치 [0.5, 0.5], bias −1
- 출력 뉴런: 가중치 [2, 4], bias 0.5

은닉층 출력과 최종 출력을 구하시오.

**16.** (a) Gradient descent에서 W = 0.8, ∂L/∂W = 0.5, η = 0.1일 때 업데이트된 W는?
(b) 역전파 예제의 공식 Δw = −η · δ · o 에서 η = 0.5, δ = 0.2, o = 0.6일 때 Δw는?

---

## Part D. 빈칸 채우기 손코딩

**17.** 틱택토 Minimax를 완성하시오. BOT은 MAX, PLAYER는 MIN이다.
```python
def minimax(board, turn):
    if is_terminal(board):
        return utility(board)             # BOT 승 +1, PLAYER 승 -1, 무승부 0
    if turn == BOT:
        best = -float("inf")
        for move in empty_cells(board):
            best = ____(a)____(best, minimax(result(board, move), PLAYER))
    else:
        best = float("inf")
        for move in empty_cells(board):
            best = ____(b)____(best, minimax(result(board, move), ____(c)____))
    return best
```

**18.** 마르코프 체인으로 내일 날씨 분포를 구하시오.
```python
import numpy as np
P  = np.array([[0.9, 0.1],
               [0.5, 0.5]])     # 행: 오늘, 열: 내일
x0 = np.array([1, 0])           # 오늘 맑음
x1 = ____(a)____                # 내일의 [맑음, 비] 확률
x2 = ____(b)____                # 모레의 [맑음, 비] 확률
```

**19.** softmax를 NumPy로 직접 구현하시오.
```python
def softmax(z):
    exp_z = ____(a)____(z)
    return exp_z / ____(b)____(exp_z)
```

**20.** 학습이 끝난 모델을 테스트 데이터로 평가하는 코드를 완성하시오.
```python
model.____(a)____()
correct, total = 0, 0
with torch.____(b)____():
    for images, labels in test_loader:
        logits = model(images)
        predictions = logits.argmax(dim=____(c)____)
        correct += (predictions == labels).sum().item()
        total += labels.size(0)
accuracy = correct / total
```

---
---

## 정답 및 해설

**1. X** — 튜링 테스트는 내부 작동이 아니라 겉으로 보이는 **행동(behavioral)** 만 평가한다.

**2. O** — 목표까지의 예상 비용만 본다.

**3. O** — 정해진 깊이에서 탐색을 멈추고(cutoff), 평가 함수 EVAL로 그 상태의 가치를 추정한다.

**4. X** — 과대적합은 훈련 데이터에 지나치게 맞춰져서 **보지 못한 데이터**에서 성능이 나쁜 것이다. 훈련 데이터에서도 성능이 나쁜 것은 과소적합이다.

**5. O** — K번 학습하고 K개 성능을 평균낸다.

**6. ①**

**7. ②** — ①, ④는 global search의 특징이다.

**8. ②** — ¬(P∧Q) ≡ ¬P ∨ ¬Q, ¬(P∨Q) ≡ ¬P ∧ ¬Q.

**9. ②** — P(X_t | X_{t−1})이 전이 모델이다.

**10. ③** — one-hot이면 (Categorical) cross-entropy, 정수 레이블이면 Sparse categorical cross-entropy.

**11. ②** — 너무 작으면 ①처럼 느려진다.

**12.** (a) **S → A → G, 비용 6**
— S를 펼치면 h(A) = 1 < h(B) = 2 이므로 A를 고르고, A에서 G로 간다. 실제 비용은 고려하지 않는다.
(b) **S → B → G, 비용 5**
— f(A) = 1 + 1 = 2, f(B) = 3 + 2 = 5 → A 확장, G(A 경유)의 f = 6 + 0 = 6
— 큐: B(5), G(6) → B 확장, G(B 경유)의 f = 5 + 0 = 5 → G(5)를 꺼내 종료
— Greedy는 더 빠르지만 최적해를 놓칠 수 있다.

**13. 약 0.000752**
P(j|a) × P(m|a) × P(a|¬b,¬e) × P(¬b) × P(¬e) = 0.8 × 0.5 × 0.002 × 0.99 × 0.95 ≈ 0.000752

**14.** (a) (5 + 8 + 16) / 40 = **0.725**
(b) recall_A = 5/10 = 0.5, recall_B = 8/10 = 0.8, recall_C = 16/20 = 0.8 → macro recall = (0.5 + 0.8 + 0.8) / 3 = **0.7**
(recall은 행 기준, precision은 열 기준)

**15.**
- 은닉 1: 1·1 + (−1)·2 + 0 = −1 → ReLU → 0
- 은닉 2: 0.5·1 + 0.5·2 − 1 = 0.5 → ReLU → 0.5
- 은닉층 출력 = **[0, 0.5]**
- 출력: 2·0 + 4·0.5 + 0.5 = **2.5**

**16.** (a) W := 0.8 − 0.1 × 0.5 = **0.75**
(b) Δw = −0.5 × 0.2 × 0.6 = **−0.06**

**17.** (a) `max`  (b) `min`  (c) `BOT`

**18.** (a) `np.matmul(x0, P)` (또는 `x0 @ P`) → [0.9, 0.1]
(b) `np.matmul(x1, P)` → [0.86, 0.14]

**19.** (a) `np.exp`  (b) `np.sum`

**20.** (a) `eval`  (b) `no_grad`  (c) `1`
— 출력이 (batch 크기, 클래스 수) 형태이므로 클래스 축은 dim=1. softmax는 단조 증가라 logits에 바로 argmax를 해도 결과가 같다.
