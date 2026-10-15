# 중간고사 대비 모의문제 — Set 2

> 범위: Problem Solving(2주차) ~ Neural Networks(7주차)
> 구성: T/F 5 · 객관식 6 · 단답형 5 · 빈칸 손코딩 4 (코드는 모두 Python)
> 정답과 해설은 맨 아래에 있다.

---

## Part A. T/F (O/X)

**1.** Uniform-cost search는 전산학에서 Dijkstra 알고리즘으로 불리는, 사실상 같은 알고리즘이다.

**2.** 알파-베타 가지치기를 적용하면 계산량은 줄지만, 루트에서 고르는 수가 Minimax와 달라질 수 있다.

**3.** Monte Carlo Tree Search에서 게임이 끝날 때까지 무작위로 수를 두는 시뮬레이션 과정은 트리에 기록된다.

**4.** 베이지안 네트워크는 변수 사이의 인과관계를 방향성 비순환 그래프(DAG)로 표현한다.

**5.** Softmax의 출력값들은 모두 0 이상이고, 합이 1이다.

---

## Part B. 객관식

**6.** Weighted A* search의 평가 함수는? (W > 1)
① f(n) = h(n)  ② f(n) = g(n)  ③ f(n) = g(n) + h(n)  ④ f(n) = g(n) + W·h(n)

**7.** Genetic Algorithm에서 한 세대가 다음 세대를 만드는 순서로 옳은 것은?
① Mutation → Crossover → Selection
② Selection → Crossover → Mutation
③ Crossover → Selection → Mutation
④ Selection → Mutation → Crossover

**8.** 함의 제거(Implication Elimination)에 따라 P → Q 와 동치인 것은?
① ¬P ∧ Q  ② P ∨ ¬Q  ③ ¬P ∨ Q  ④ ¬Q → P

**9.** 훈련/검증/테스트 집합 중 **검증 집합(validation set)** 의 역할은?
① 모델 파라미터를 학습시킨다
② 여러 모델 중 가장 좋은 모델을 고른다
③ 최종 선택된 모델을 마지막으로 평가한다
④ 이상치(outlier)를 제거한다

**10.** ReLU(−3)과 ReLU(2)의 값으로 옳은 것은?
① 0, 2  ② −3, 2  ③ 0, 1  ④ 0.05, 0.88

**11.** 샘플 s개를 한 번에 계산하는 batch 연산 XW + b 에서 X가 s×n, W가 n×m일 때 결과의 크기는?
① n×m  ② s×n  ③ s×m  ④ 1×m

---

## Part C. 단답형

**12.** 날씨의 전이 모델이 아래와 같다. (행: 오늘, 열: 내일, 순서는 [맑음, 비])
```
P = [[0.8, 0.2],
     [0.4, 0.6]]
```
오늘이 맑음일 때, **이틀 뒤** 맑을 확률은?

**13.** 나이브 베이즈로 골프를 칠지(Yes/No) 예측한다. 입력은 {Outlook = Sunny, Windy = True}이다.
- P(Yes) = 0.6, P(Sunny|Yes) = 0.2, P(Windy=True|Yes) = 0.3
- P(No) = 0.4, P(Sunny|No) = 0.5, P(Windy=True|No) = 0.6

각 클래스의 점수(비례값)를 구하고, 예측 결과를 쓰시오.

**14.** 퍼셉트론 w₁ = 1, w₂ = 1, b = −1.5, 활성 함수는 Heaviside이다. (x₁, x₂) = (0,0), (0,1), (1,0), (1,1)에 대한 출력을 쓰고, 이 퍼셉트론이 구현하는 논리 게이트를 쓰시오.

**15.** z = [2, 0, 0]에 softmax를 적용한 결과를 구하시오. (e² ≈ 7.389, 소수점 셋째 자리까지)

**16.** 훈련 데이터 60,000개를 batch size 32로 학습한다.
(a) 1 epoch 동안 파라미터는 몇 번 업데이트되는가?
(b) 5 epoch를 학습하면 총 몇 번 업데이트되는가?

---

## Part D. 빈칸 채우기 손코딩

**17.** Hill climbing을 완성하시오. (value가 클수록 좋은 상태)
```python
def hill_climbing(start):
    current = start
    while True:
        next_state = max(neighbors(current), key=value)
        if value(next_state) <= value(current):
            return ____(a)____
        current = ____(b)____
```

**18.** MAE와 RMSE를 계산하는 코드를 완성하시오.
```python
total_error = 0
total_squared_error = 0
for actual, predicted in zip(y_test, y_pred):
    total_error += ____(a)____(actual - predicted)
    total_squared_error += (actual - predicted) ____(b)____
mae = total_error / len(y_test)
rmse = (total_squared_error / len(y_test)) ____(c)____
```

**19.** 입력 2개 → 은닉 뉴런 4개 → 클래스 3개인 MLP를 PyTorch로 정의하시오.
```python
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden_layer = nn.Linear(____(a)____)
        self.output_layer = nn.Linear(____(b)____)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        h = self.sigmoid(self.____(c)____(x))
        return self.output_layer(h)
```

**20.** batch size 64로 DataLoader를 만드시오. 훈련 데이터만 섞는다.
```python
train_loader = DataLoader(train_dataset, batch_size=____(a)____, shuffle=____(b)____)
test_loader  = DataLoader(test_dataset,  batch_size=____(a)____, shuffle=____(c)____)
```

---
---

## 정답 및 해설

**1. O** — AI에서는 Uniform-cost search, CS에서는 Dijkstra라고 부른다.

**2. X** — 알파-베타 가지치기는 **결과에 영향을 주지 않는 노드만** 잘라내므로 Minimax와 같은 결과를 낸다.

**3. X** — 무작위 시뮬레이션 과정은 트리에 기록되지 않는다. 결과(승/패)만 평균 효용값 갱신에 쓰인다.

**4. O** — 부모 노드가 원인, 자식 노드가 결과다.

**5. O** — softmax는 실수 J개를 확률 분포로 바꾼다.

**6. ④** — h(n)에 가중치를 더 줘서 목표 방향으로 더 적극적으로 탐색한다. 대신 최적성을 일부 희생할 수 있다.

**7. ②** — 선택(적합도 기준) → 교차(일부 교환) → 변이(무작위 변화).

**8. ③** — P → Q ≡ ¬P ∨ Q. (④는 대우가 아니다. 대우는 ¬Q → ¬P)

**9. ②** — ①은 훈련 집합, ③은 테스트 집합의 역할이다.

**10. ①** — ReLU(x) = max(0, x).

**11. ③** — (s×n)(n×m) = s×m. b는 각 행에 같은 값이 복사되어 더해진다.

**12. 0.72**
x⁽¹⁾ = [1, 0]P = [0.8, 0.2]
x⁽²⁾의 맑음 = 0.8 × 0.8 + 0.2 × 0.4 = 0.64 + 0.08 = **0.72**

**13.** Yes: 0.6 × 0.2 × 0.3 = **0.036**, No: 0.4 × 0.5 × 0.6 = **0.12** → 0.12 > 0.036 이므로 **No**

**14.** z = x₁ + x₂ − 1.5
(0,0) → −1.5 → 0, (0,1) → −0.5 → 0, (1,0) → −0.5 → 0, (1,1) → 0.5 → 1 ⇒ **AND 게이트**
(b = −0.5이면 OR 게이트)

**15.** 분모 = e² + e⁰ + e⁰ = 7.389 + 1 + 1 = 9.389
→ [7.389/9.389, 1/9.389, 1/9.389] ≈ **[0.787, 0.107, 0.107]**

**16.** (a) 60,000 / 32 = **1,875번**  (b) 1,875 × 5 = **9,375번**
(epoch 1번 = 훈련 세트 전체를 한 번 학습, batch마다 1번 업데이트)

**17.** (a) `current`  (b) `next_state`
— 더 나은 이웃이 없으면 현재 상태를 반환하고 종료한다. (local optimum에 갇힐 수 있음)

**18.** (a) `abs`  (b) `** 2`  (c) `** 0.5`

**19.** (a) `2, 4`  (b) `4, 3`  (c) `hidden_layer`

**20.** (a) `64`  (b) `True`  (c) `False`
