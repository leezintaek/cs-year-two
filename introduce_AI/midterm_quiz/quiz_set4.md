# 중간고사 대비 모의문제 — Set 4

> 범위: Problem Solving(2주차) ~ Neural Networks(7주차)
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (코드는 모두 Python)
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** Strong AI는 추천 시스템처럼 특정 작업에서만 지능이 있는 것처럼 행동하는 AI를 말한다.

**2.** Big Data의 3V는 Volume, Variety, Velocity이다.

**3.** P ↔ Q 는 (P → Q) ∧ (Q → P)와 동치이다.

**4.** 결정 트리 학습은 분할 규칙을 탐욕적(greedy)으로 하나씩 찾는다.

**5.** 하나의 샘플이 하나의 레이블만 갖는 다중 클래스 분류에서, micro-averaged precision은 accuracy와 같다.

---

## Part B. 객관식

**6.** Uniform-cost search가 우선순위 큐에서 다음 노드를 꺼내는 기준은?
① h(n)이 가장 작은 노드
② g(n)이 가장 작은 노드
③ 깊이가 가장 깊은 노드
④ 가장 먼저 들어온 노드

**7.** 게임을 형식적으로 정의하는 요소 중, **종료 상태에서 플레이어가 얻는 최종 점수**를 정의하는 것은?
① ToMove(s)  ② Actions(s)  ③ IsTerminal(s)  ④ Utility(s, p)

**8.** 다음 중 **암시적(implicit)** 지식 표현에 해당하는 것은?
① 1차 논리  ② 의미망(semantic network)  ③ 심층 신경망  ④ 명제 논리

**9.** 추론 기법 4가지 중 "정상이던 생체 신호가 시간이 지나며 위험 상태로 변함"처럼 **시간에 따른 변화**를 추론하는 데 쓰는 것은?
① 논리  ② 베이지안 네트워크  ③ 마르코프 모델  ④ 심층 신경망

**10.** bias(편향)에 대한 설명으로 옳지 **않은** 것은?
① 입력과 무관한 상수 오프셋이다
② 값이 항상 1인 입력 x₀와 그 가중치 w₀로 표현할 수 있다
③ 학습되는 파라미터가 아니다
④ 입력 특징만으로 표현할 수 없는 패턴을 잡기 위해 쓴다

**11.** 신경망 학습에서 한 번의 반복(iteration) 순서로 옳은 것은?
① 역전파 → 순전파 → loss 계산 → 업데이트
② 순전파 → loss 계산 → 역전파 → 업데이트
③ loss 계산 → 순전파 → 업데이트 → 역전파
④ 순전파 → 업데이트 → loss 계산 → 역전파

---

## Part C. 단답형

**12.** 루트는 MAX, 그 아래 세 노드는 MIN이다. 리프는 왼쪽부터 탐색한다.
```
              MAX
          /    |    \
       MIN1   MIN2   MIN3
       /  \   /  \   /  \
      3    5 2    9 6    1
```
(a) 루트의 값은?
(b) 알파-베타 가지치기로 탐색하지 않아도 되는 리프는?

**13.** 비터비 알고리즘 첫 단계를 계산하시오.
- 초기: P₀(T) = P₀(F) = 0.5 (T: 비 옴, F: 비 안 옴)
- 전이: P(T→T) = 0.7, P(T→F) = 0.3, P(F→T) = 0.3, P(F→F) = 0.7
- 관측: P(U=F | R=T) = 0.1, P(U=F | R=F) = 0.8
- 첫날 관측: 우산 없음 (U₁ = F)

P₁(T)와 P₁(F)를 구하고, 첫날 날씨로 더 그럴듯한 것을 쓰시오.

**14.** 공장 A가 제품의 60%를, 공장 B가 40%를 만든다. 불량률은 A가 2%, B가 5%이다. 불량품 하나를 골랐을 때 그것이 공장 A에서 만들어졌을 확률은?

**15.** MNIST 이미지 32장을 한 batch로 784 → 128 은닉층에 넣는다. (행벡터 방식 XW + b)
X, W, 결과의 크기를 각각 쓰시오.

**16.** 단층 퍼셉트론(활성 함수 Heaviside, z ≥ 0이면 1)이 있다.
```
W = [[ 1.0, -1.0],     # 클래스 0
     [ 0.5,  0.5],     # 클래스 1
     [-1.0,  1.0]]     # 클래스 2
b = [0, -1, 0.5]
x = [0.5, 1.0]
```
z와 출력 y를 구하시오.

---

## Part D. 빈칸 채우기 손코딩

**17.** Uniform-cost search(Dijkstra)의 거리 갱신 부분을 완성하시오.
```python
for v, weight in graph[u]:
    new_distance = ____(a)____
    if new_distance ____(b)____ distance[v]:
        distance[v] = new_distance
```

**18.** 이진 분류의 혼동 행렬 값으로 지표를 계산하시오.
```python
TP, FN, FP, TN = 700, 100, 30, 170
accuracy  = ____(a)____
precision = ____(b)____
recall    = ____(c)____
```

**19.** MNIST용 신경망을 정의하시오. (784 → 128 → 10, 은닉층 sigmoid)
```python
class our_first_nn(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.____(a)____()
        self.hidden_layer = nn.Linear(____(b)____)
        self.sigmoid = nn.Sigmoid()
        self.output_layer = nn.Linear(____(c)____)

    def forward(self, x):
        x = self.flatten(x)
        x = self.sigmoid(self.hidden_layer(x))
        return self.output_layer(x)
```

**20.** 데이터를 하나씩 학습하는 루프를 완성하시오.
```python
for index in torch.randperm(len(train_dataset)):
    image, label = train_dataset[index.item()]
    image = image.____(a)____(0)                 # (1, 28, 28) → (1, 1, 28, 28): 배치 차원 추가
    label = torch.tensor([label])

    logits = model(image)
    loss = ____(b)____(logits, label)            # 손실 함수 객체
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

---
---

## 정답 및 해설

**1. X** — 설명은 Weak AI(Narrow AI)다. Strong AI는 실제로 의식적으로 사고하는, 사람 수준의 일반 지능이다.

**2. O** — Volume(양), Variety(정형/비정형 다양성), Velocity(생성·처리 속도).

**3. O** — 쌍조건 제거(Biconditional Elimination).

**4. O** — 매 단계마다 불순도를 가장 많이 줄이는 분할을 고른다.

**5. O** — 오분류 하나는 한 클래스의 FP이면서 동시에 다른 클래스의 FN이다. 그래서 FP 합 = FN 합이 되고, micro precision = micro recall = accuracy가 된다.

**6. ②** — f(n) = g(n). ①은 Greedy best-first, ④는 BFS.

**7. ④**

**8. ③** — 논리·의미망은 명시적(explicit), 머신러닝·딥러닝은 암시적(implicit) 지식 표현이다.

**9. ③**

**10. ③** — bias도 가중치와 함께 학습되는 파라미터다.

**11. ②**

**12.** (a) **3** — MIN1 = 3, MIN2 = 2, MIN3 = 1 → max = 3
(b) **9** — MIN1을 마치면 α = 3. MIN2의 첫 리프 2 ≤ α 이므로 9는 볼 필요가 없다. MIN3은 첫 리프 6 > 3이라 두 번째 리프 1까지 봐야 한다.

**13.**
- P₁(T) = max(0.5·0.7, 0.5·0.3) × 0.1 = 0.35 × 0.1 = **0.035**
- P₁(F) = max(0.5·0.3, 0.5·0.7) × 0.8 = 0.35 × 0.8 = **0.28**
- P₁(F) > P₁(T) → **비가 안 왔을** 가능성이 높다.

**14. 0.375**
P(A|불량) = (0.02 × 0.6) / (0.02 × 0.6 + 0.05 × 0.4) = 0.012 / 0.032 = 0.375

**15.** X: **32×784**, W: **784×128**, 결과: **32×128**
(b는 1×128이 32개 행에 똑같이 더해진다)

**16.**
- z₀ = 1.0·0.5 − 1.0·1.0 + 0 = −0.5 → 0
- z₁ = 0.5·0.5 + 0.5·1.0 − 1 = −0.25 → 0
- z₂ = −1.0·0.5 + 1.0·1.0 + 0.5 = 1.0 → 1
- z = **[−0.5, −0.25, 1.0]**, y = **[0, 0, 1]** → 클래스 2

**17.** (a) `distance[u] + weight`  (b) `<`

**18.** (a) `(TP + TN) / (TP + FN + FP + TN)` → 0.87
(b) `TP / (TP + FP)` → ≈ 0.959
(c) `TP / (TP + FN)` → 0.875

**19.** (a) `Flatten`  (b) `784, 128`  (c) `128, 10`

**20.** (a) `unsqueeze`  (b) `criterion`
