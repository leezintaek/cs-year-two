# 중간고사 대비 모의문제 — Set 5

> 범위: Problem Solving(2주차) ~ Neural Networks(7주차)
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (코드는 모두 Python)
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** DFS는 항상 최적해를 보장한다.

**2.** 교재에서는 Genetic Algorithm을 local search 알고리즘으로 분류한다.

**3.** 베이지안 네트워크에서 이진 변수 노드의 부모가 k개이면, 그 노드의 CPT에는 2ᵏ개의 조건(행)이 있다.

**4.** 테스트 집합은 여러 후보 모델 중 가장 좋은 모델을 고르는 데 사용한다.

**5.** `np.argmax([0, 1, 1])`의 결과는 1이다.

---

## Part B. 객관식

**6.** John Searle(1980)의 구분에서 Weak AI에 대한 설명으로 옳은 것은?
① 사람처럼 실제로 의식적으로 사고한다
② 지능이 있는 것처럼 행동하며, 특정 작업에 한정된다
③ 사람의 개입 없이 모든 영역의 문제를 푼다
④ 아직 이론적 연구 단계에 있다

**7.** 탐색 문제(search problem)를 정의하는 요소가 **아닌** 것은?
① Initial state  ② Transition model `result(s, a)`  ③ Action cost `c(s, a, s')`  ④ Loss function

**8.** "비가 오면 해리는 안에 있다", "비가 온다" ⟹ "해리는 안에 있다"에 쓰인 추론 규칙은?
① Modus Ponens  ② Modus Tollens  ③ And Elimination  ④ Contraposition

**9.** 출력 범위가 (−1, 1)인 활성 함수는?
① Sigmoid  ② ReLU  ③ tanh  ④ Heaviside

**10.** Mini-batch와 비교한 Full-batch 학습의 단점은?
① 계산이 느리다
② 메모리를 많이 쓴다
③ 훈련 데이터의 일부만 쓴다
④ 역전파를 할 수 없다

**11.** 오차 {1, −2, 3, 4, 100}처럼 **큰 오차 하나**가 있을 때, 그 오차에 더 큰 벌점을 주는 지표는?
① MAE  ② RMSE  ③ Accuracy  ④ Recall

---

## Part C. 단답형

**12.** 틱택토 평가 함수 EVAL = (+1)×(O가 아직 완성할 수 있는 줄 수 / 8) + (−1)×(X가 아직 완성할 수 있는 줄 수 / 8) 이다. O가 완성할 수 있는 줄이 4개, X가 완성할 수 있는 줄이 6개일 때 EVAL 값은?

**13.** MCTS에서 루트의 자식 노드 세 개의 시뮬레이션 결과가 다음과 같다.
- A: 20번 중 12번 승리
- B: 12번 중 9번 승리
- C: 40번 중 20번 승리

각 노드의 평균 효용값(avg_utility)을 구하고, 가장 좋은 노드를 고르시오.

**14.** 잔디 젖음 베이지안 네트워크 (Rain → Sprinkler, Rain·Sprinkler → GrassWet)
- P(R=T) = 0.2
- P(S=T | R=T) = 0.01
- P(G=T | S=T, R=T) = 0.99, P(G=T | S=F, R=T) = 0.8

(a) P(G=T, S=T, R=T)는?
(b) P(G=T, S=F, R=T)는?

**15.** 은닉 뉴런 h의 출력 o_h = 0.6이고, h → 출력 뉴런 가중치 w = 0.5이다. 출력 뉴런의 출력은 o = 0.8, 정답 y = 1이다. 활성 함수는 sigmoid, 손실 함수는 L = (y − o)², η = 0.5이다.
(a) 출력층 δ = 2(o − y) · o(1 − o)는?
(b) Δw = −η · δ · o_h와 업데이트된 w는?

**16.** 입력 2개 → 은닉 뉴런 4개 → 출력 3개인 완전 연결 MLP의 학습 파라미터(가중치 + bias) 총 개수는?

---

## Part D. 빈칸 채우기 손코딩

**17.** heapq로 A* search의 frontier를 관리하는 코드를 완성하시오. (heapq는 첫 번째 값이 가장 작은 원소를 먼저 꺼낸다)
```python
import heapq
frontier = []
heapq.heappush(frontier, (h(start), 0, start))      # (f, g, node)
while frontier:
    f, g, node = heapq.____(a)____(frontier)
    if node == goal:
        return g
    for neighbor, cost in graph[node]:
        new_g = g + cost
        heapq.heappush(frontier, (____(b)____, new_g, neighbor))
```

**18.** Iris 데이터로 결정 트리 분류기를 학습하고 예측하시오. (지니 불순도, 최대 깊이 3)
```python
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(criterion=____(a)____, max_depth=____(b)____, random_state=42)
model.____(c)____(X_train, y_train)
y_pred = model.____(d)____(X_test)
```

**19.** PyTorch로 여러 활성 함수를 적용하시오.
```python
import torch
import torch.nn.functional as F
x = torch.tensor([-1.0, 0.34, 2.1])

relu_output    = F.____(a)____(x)
sigmoid_output = torch.____(b)____(x)
softmax_output = F.softmax(x, dim=____(c)____)
```

**20.** batch 단위 학습 루프에서 loss 합과 맞힌 개수를 누적하시오.
```python
for images, labels in train_loader:
    logits = model(images)
    loss = criterion(logits, labels)          # batch 평균 loss
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    total_loss += loss.item() * ____(a)____                  # batch 크기만큼 곱해서 합계로
    predictions = logits.____(b)____(dim=1)
    correct += (predictions == labels).____(c)____().item()
    total += labels.size(0)
```

---
---

## 정답 및 해설

**1. X** — DFS는 최적해를 보장하지 않는다.

**2. O** — 교재는 local로 분류하지만 global로 분류되기도 한다.

**3. O** — 부모 k개의 참/거짓 조합이 2ᵏ개이고, 각 행의 확률 합은 1이다.

**4. X** — 모델 선택은 검증 집합, 테스트 집합은 최종 평가에 쓴다.

**5. O** — 최댓값이 여러 개면 argmax는 첫 번째 인덱스를 반환한다. (7주차 MLP 예제의 출력 [0, 1, 1]이 Versicolor로 예측된 이유)

**6. ②** — ①은 Strong AI, ③·④는 AGI에 대한 설명이다.

**7. ④** — Loss function은 기계학습 개념이다.

**8. ①** — P→Q, P ⟹ Q.

**9. ③** — Sigmoid (0, 1), ReLU [0, ∞), Heaviside {0, 1}.

**10. ②** — Full-batch는 계산은 빠르지만 메모리를 많이 쓴다.

**11. ②** — 오차를 제곱하므로 큰 오차가 크게 반영된다. (MAE 22, RMSE ≈ 44.8)

**12. −0.25**
(+1)×(4/8) + (−1)×(6/8) = 0.5 − 0.75 = −0.25

**13.** A = 12/20 = **0.6**, B = 9/12 = **0.75**, C = 20/40 = **0.5** → **B**
(평균 효용값 = 승리 횟수 / 전체 시행 횟수 = 승률)

**14.** (a) P(G=T|S=T,R=T) × P(S=T|R=T) × P(R=T) = 0.99 × 0.01 × 0.2 = **0.00198**
(b) P(G=T|S=F,R=T) × P(S=F|R=T) × P(R=T) = 0.8 × 0.99 × 0.2 = **0.1584**

**15.** (a) δ = 2(0.8 − 1) × 0.8 × 0.2 = **−0.064**
(b) Δw = −0.5 × (−0.064) × 0.6 = **0.0192**, w = 0.5 + 0.0192 = **0.5192**
(예측이 정답보다 작으니 이 가중치를 키우는 방향으로 업데이트된다)

**16. 27개**
은닉층: 2×4 + 4 = 12, 출력층: 4×3 + 3 = 15 → 12 + 15 = 27

**17.** (a) `heappop`  (b) `new_g + h(neighbor)`
— A*는 f(n) = g(n) + h(n)이 가장 작은 노드를 먼저 꺼낸다. (b)를 `new_g`로 바꾸면 Uniform-cost search, `h(neighbor)`로 바꾸면 Greedy best-first search가 된다.

**18.** (a) `"gini"`  (b) `3`  (c) `fit`  (d) `predict`

**19.** (a) `relu`  (b) `sigmoid`  (c) `0`
— x가 1차원이라 축은 dim=0이다. (batch 형태 (N, C)라면 dim=1)

**20.** (a) `labels.size(0)`  (b) `argmax`  (c) `sum`
