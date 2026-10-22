# 인공지능개론 퀴즈 2

- 범위: week1 ~ week7 강의 PDF + week5 실습 코드
- 문제 유형: T/F, 객관식, 단답형 주관식, 빈칸 채우는 손코딩 (순서 무작위)
- 코드는 모두 Python
- 정답과 해설: `quiz_2_explanation.md`

---

### Q1. [단답형]
다음 방향 그래프에서 S에서 G까지 **Uniform-Cost Search**를 수행한다. (비용이 같으면 알파벳 순서로 먼저 꺼낸다.)

| 간선  | 비용 | 간선  | 비용 | 간선  | 비용 |
|-------|------|-------|------|-------|------|
| S → A | 1    | A → D | 6    | C → G | 7    |
| S → B | 4    | B → D | 2    | D → G | 3    |
| A → C | 2    | B → E | 6    | E → G | 1    |

- (1) 노드가 우선순위 큐에서 꺼내지는(확장되는) 순서와, 꺼낼 때의 누적 비용 $g$를 쓰시오.
- (2) 탐색 도중 **비용이 더 작은 값으로 갱신되는** 노드 두 개와, 각각 어떤 값에서 어떤 값으로 바뀌는지 쓰시오.
- (3) 찾은 경로와 총 비용을 쓰시오.

### Q2. [T/F]
Softmax의 입력 $\mathbf{z}$의 모든 원소에 같은 상수 $c$를 더해도($z_i \to z_i + c$) 출력 확률 분포는 변하지 않는다.

답: ☐ T ☐ F

### Q3. [빈칸 손코딩]
입력 2개, 출력 뉴런 3개인 단층 퍼셉트론을 NumPy로 구현했다(열 벡터 방식, 활성 함수 Heaviside: 1 if $z \ge 0$). 빈칸을 채우시오.

```python
import numpy as np

x = np.array([[0.5], [2.0]])           # Shape: (2, 1)
W = np.array([[ 1.0, -0.5],
              [-1.0,  0.5],
              [ 0.2,  0.3]])           # Shape: ( (a) )
b = np.array([[0.1], [0.2], [-0.8]])   # Shape: ( (b) )

z = np.____(c)____(W, x) + b           # Shape: ( (d) )
y = np.____(e)____(z >= 0, 1, 0)
pred = np.argmax(y, axis=0)
```

- (f) `z`의 세 값, `y`, `pred`를 각각 쓰시오.

### Q4. [단답형]
어떤 이진 분류 데이터의 테스트 샘플은 1,000개이고, 그중 실제 Positive는 200개이다. 모델의 recall은 0.8, precision은 0.5였다.

- (1) TP, FN, FP, TN을 구하시오.
- (2) 이 모델의 accuracy를 구하시오.
- (3) 모든 샘플을 Negative로 예측하는 모델의 accuracy를 구하고, (2)와 비교해 accuracy만 볼 때의 문제점을 한 문장으로 쓰시오.

### Q5. [객관식]
다음 중 $P \to Q$와 논리적으로 동치가 **아닌** 것은?

① $\lnot P \lor Q$  ② $\lnot Q \to \lnot P$  ③ $\lnot (P \land \lnot Q)$  ④ $Q \to P$  ⑤ $(\lnot P \lor Q) \land (P \lor \lnot P)$

### Q6. [단답형]
우산 HMM에서 숨은 상태는 $R_t \in \{T, F\}$(비가 옴/안 옴), 관측은 $U_t$(우산을 가져옴)이다.

| 전이 모델         | 값  | 관측 모델         | 값  |
|-------------------|-----|-------------------|-----|
| $P(R_t=T \mid T)$ | 0.7 | $P(U=T \mid R=T)$ | 0.9 |
| $P(R_t=F \mid T)$ | 0.3 | $P(U=T \mid R=F)$ | 0.2 |
| $P(R_t=T \mid F)$ | 0.3 | $P(U=F \mid R=T)$ | 0.1 |
| $P(R_t=F \mid F)$ | 0.7 | $P(U=F \mid R=F)$ | 0.8 |

$P_0(T) = P_0(F) = 0.5$이고, 관측 순서는 $U_1 = F,\ U_2 = T,\ U_3 = T$이다. Viterbi 알고리즘

$$P_t(j) = \max_i \big[ P_{t-1}(i) \cdot P(R_t = j \mid R_{t-1} = i) \big] \cdot P(U_t \mid R_t = j)$$

으로 다음을 구하시오.

- (1) $P_1(T)$, $P_1(F)$
- (2) $P_2(T)$, $P_2(F)$ 와 각각 max를 준 이전 상태
- (3) $P_3(T)$, $P_3(F)$
- (4) backtracking으로 구한 가장 가능성 높은 날씨 순서 $(R_1, R_2, R_3)$

### Q7. [T/F]
Local search(예: hill climbing)는 시작 노드부터의 경로와 방문한/방문하지 않은 노드 집합을 모두 기록하므로, local optimum에서 벗어날 수 있다.

답: ☐ T ☐ F

### Q8. [단답형]
결정 트리의 한 노드에 Class1 20개, Class2 20개가 있다. 후보 분할 규칙이 두 개 있다.

| 규칙   | 왼쪽 (C1, C2) | 오른쪽 (C1, C2) |
|--------|---------------|-----------------|
| 규칙 1 | (13, 0)       | (7, 20)         |
| 규칙 2 | (10, 10)      | (10, 10)        |

Gini impurity는 $G = 1 - \sum_k p_k^2$이고, 분할 후 불순도는 각 자식 노드의 $G$를 **샘플 수 비율로 가중 평균**한 값이다.

- (1) 분할 전 노드의 Gini impurity는?
- (2) 규칙 1, 규칙 2 각각의 분할 후 불순도는? (소수 넷째 자리에서 반올림)
- (3) 결정 트리 학습은 어느 규칙을 고르는가? 이 선택 방식을 무엇이라고 부르는가?

### Q9. [단답형]
다음 트리에서 루트는 MAX, 둘째 층은 MIN, 셋째 층은 MAX 노드이다. 단말 값은 왼쪽부터 주어진다.

```
                               MAX
            ┌───────────────────┼───────────────────┐
           MIN                 MIN                 MIN
       ┌────┴────┐         ┌────┴────┐         ┌────┴────┐
      MAX       MAX       MAX       MAX       MAX       MAX
     ┌─┴─┐     ┌─┴─┐     ┌─┴─┐     ┌─┴─┐     ┌─┴─┐     ┌─┴─┐
     4   6     7   9     1   2     0   8     5   3     9   1
```

- (1) 루트의 minimax 값과, 루트에서 선택하는 자식(왼쪽/가운데/오른쪽)은?
- (2) 왼쪽에서 오른쪽 순서로 alpha-beta pruning을 할 때 **방문하지 않는 단말 값**을 모두 쓰시오.
- (3) 실제로 방문하는 단말 노드는 모두 몇 개인가?

### Q10. [객관식 — 모두 고르기]
다음 중 신경망 **학습(training)을 통해 값이 정해지는 것**을 모두 고르시오.

① 가중치 $\mathbf{W}$  ② bias $\mathbf{b}$  ③ learning rate $\eta$  ④ batch size  ⑤ epoch 수
⑥ 은닉층 뉴런 수  ⑦ `DecisionTreeClassifier`의 `max_depth`

### Q11. [단답형]
Naïve Bayes로 뉴스 기사를 Sports / Business 중 하나로 분류한다. 단어 목록은 {game, stocks, team}이다.

| 확률                                  | Sports | Business |
|---------------------------------------|--------|----------|
| $P(\text{Category})$                  | 0.4    | 0.6      |
| $P(\text{HasWord}_{game}=T \mid C)$   | 0.5    | 0.1      |
| $P(\text{HasWord}_{stocks}=T \mid C)$ | 0.05   | 0.6      |
| $P(\text{HasWord}_{team}=T \mid C)$   | 0.4    | 0.2      |

기사: *"The game was delayed after stocks fell sharply."* (단어 목록 중 game, stocks만 등장)

- (1) Sports와 Business 각각에 대해 $P(C) \prod_i P(x_i \mid C)$를 구하시오.
- (2) 예측 카테고리는?
- (3) team이 기사에 없다는 정보를 무시하고 계산하면 두 값은 각각 얼마이며, 예측이 바뀌는가?

### Q12. [T/F]
PyTorch 학습 루프에서 `optimizer.zero_grad()`를 호출하지 않으면, 이전 batch에서 계산된 gradient가 현재 batch의 gradient에 누적(더해짐)된다.

답: ☐ T ☐ F

### Q13. [단답형]
Q1과 같은 그래프에서 휴리스틱이 다음과 같다. (같은 값이면 알파벳 순서)

| 노드   | S | A | B | C | D | E | G |
|--------|---|---|---|---|---|---|---|
| $h(n)$ | 8 | 5 | 3 | 7 | 2 | 1 | 0 |

- (1) **Greedy best-first search**의 확장 순서, 찾은 경로, 총 비용을 쓰시오.
- (2) **A\* search**의 확장 순서와 각 노드를 꺼낼 때의 $f(n) = g(n) + h(n)$, 찾은 경로, 총 비용을 쓰시오.
- (3) 두 결과가 다른 이유를 $f(n)$의 정의로 설명하시오.

### Q14. [빈칸 손코딩]
Iris 데이터(입력 feature 4개, 클래스 3개)를 분류하는 MLP이다. 빈칸을 채우시오.

```python
import torch
import torch.nn as nn

class IrisMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden_layer = nn.Linear(__(a)__, __(b)__)   # 입력 4 → 은닉 8
        self.output_layer = nn.Linear(__(c)__, __(d)__)   # 은닉 8 → 클래스 3
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=__(e)__)

    def forward(self, x):
        hidden_o = self.relu(self.hidden_layer(x))
        output_z = self.output_layer(hidden_o)
        return output_z

model = IrisMLP()
x = torch.tensor([[5.1, 3.5, 1.4, 0.2],
                  [6.3, 3.3, 6.0, 2.5]])   # shape: (f)
logits = model(x)                           # shape: (g)
probs = model.softmax(logits)
pred = probs.__(h)__(dim=1)                 # shape: (i)
```

### Q15. [단답형]
Heaviside(1 if $z \ge 0$) 퍼셉트론 3개로 다음 2층 네트워크를 만들었다.

- $h_1 = \text{step}(x_1 + x_2 - 0.5)$
- $h_2 = \text{step}(-x_1 - x_2 + 1.5)$
- $y = \text{step}(h_1 + h_2 - 1.5)$

- (1) $(x_1, x_2) = (0,0), (0,1), (1,0), (1,1)$ 각각에 대해 $h_1$, $h_2$, $y$를 쓰시오.
- (2) $h_1$, $h_2$, $y$(입력 $h_1, h_2$에 대해)는 각각 어떤 논리 게이트인가?
- (3) 전체 네트워크는 어떤 함수를 계산하는가? 이 함수를 단층 퍼셉트론 하나로 구현할 수 없는 이유는?

### Q16. [T/F]
HMM에서 Viterbi 알고리즘이 구하는 가장 가능성 높은 상태 순서는, 각 시점마다 관측만 보고 확률이 가장 큰 상태를 독립적으로 골라 이어 붙인 순서와 항상 같다.

답: ☐ T ☐ F

### Q17. [단답형]
전체 메일 중 30%가 스팸이다. 스팸 메일의 60%에 "lottery"라는 단어가 들어 있고, 정상 메일의 5%에도 이 단어가 들어 있다.

- (1) "lottery"가 들어 있는 메일의 비율 $P(\text{lottery})$는?
- (2) "lottery"가 들어 있는 메일이 스팸일 확률은? (소수 넷째 자리에서 반올림)
- (3) (2)에서 cause와 effect는 각각 무엇인가?

### Q18. [객관식]
세 모델의 훈련 오류율과 검증(validation) 오류율이 다음과 같다.

| 모델 | 훈련 오류율 | 검증 오류율 |
|------|-------------|-------------|
| A    | 1%          | 25%         |
| B    | 30%         | 31%         |
| C    | 6%          | 8%          |

옳은 것은?

① A는 과소적합, B는 과대적합이다.
② A는 과대적합, B는 과소적합이며, 셋 중 C를 고른다.
③ 훈련 오류율이 가장 낮은 A를 고르고, test set으로 A의 하이퍼파라미터를 다시 조정한다.
④ B는 훈련과 검증 오류율 차이가 가장 작으므로 가장 좋은 모델이다.
⑤ 셋 중 가장 좋은 모델을 고르는 데는 test set을 쓰고, validation set은 최종 평가에 쓴다.

### Q19. [단답형]
날씨 Markov chain의 상태는 [Sunny, Rainy]이고 전이 행렬(행: 오늘, 열: 내일)은

$$P = \begin{bmatrix} 0.7 & 0.3 \\ 0.4 & 0.6 \end{bmatrix}$$

이다. 오늘은 Rainy, 즉 $\mathbf{x}^{(0)} = [0\ \ 1]$이다.

- (1) $\mathbf{x}^{(1)}$, $\mathbf{x}^{(2)}$, $\mathbf{x}^{(3)}$을 구하시오.
- (2) 오늘이 Rainy일 때, 내일 Sunny이고 **모레도 Sunny일** 확률은?
- (3) (2)의 값이 $\mathbf{x}^{(2)}$의 Sunny 확률보다 작은 이유를 한 문장으로 쓰시오.

### Q20. [T/F]
Uniform-cost search는 간선 비용 중 음수가 있어도 시작 노드에서 각 노드까지의 최소 비용 경로를 항상 보장한다.

답: ☐ T ☐ F

### Q21. [단답형]
훈련 데이터 50,000개를 `DataLoader(train_dataset, batch_size=64, shuffle=True)`로 학습한다. (마지막에 남는 데이터도 하나의 batch로 학습한다.)

- (1) 1 epoch 동안 파라미터는 몇 번 갱신되는가?
- (2) 매 epoch 마지막 batch의 크기는?
- (3) 5 epoch 동안 파라미터는 몇 번 갱신되는가?
- (4) 강의의 첫 MNIST 코드처럼 데이터를 하나씩(one by one) 학습하면 1 epoch에 몇 번 갱신되는가?

### Q22. [단답형]
강의의 추론 기법 4가지 — (가) 논리, (나) Bayesian network, (다) Markov model, (라) 심층 신경망 — 중 각 상황에 가장 알맞은 것을 고르시오.

- (1) 기침과 발열이 있는 환자가 독감일 확률이 64%라고 추정한다.
- (2) "출입증이 없는 사람은 서버실에 들어갈 수 없다"는 규칙과 "Kim은 출입증이 없다"는 사실로 Kim의 출입을 거부한다.
- (3) 흉부 X-ray 이미지를 보고 폐렴인지 판별한다.
- (4) 카드 결제 기록을 시간 순으로 보면서 계정 상태가 정상 → 의심 → 도용으로 바뀌는 과정을 추적한다.

### Q23. [단답형]
batch 크기 2인 입력에 fully connected layer를 행 벡터 방식 $\mathbf{X}\mathbf{W} + \mathbf{b}$로 계산한다.

$$\mathbf{X} = \begin{bmatrix} 1 & 2 \\ 0 & -1 \end{bmatrix}, \quad \mathbf{W} = \begin{bmatrix} 1 & -1 & 0 \\ 2 & 0 & -3 \end{bmatrix}, \quad \mathbf{b} = \begin{bmatrix} 0.5 & -1 & 1 \end{bmatrix}$$

- (1) $\mathbf{X}\mathbf{W} + \mathbf{b}$의 shape과 값을 구하시오.
- (2) (1)에 ReLU를 적용한 결과를 쓰시오.
- (3) (1)의 결과에 `argmax(dim=1)`을 적용한 결과를 쓰시오.
- (4) $\mathbf{b}$는 shape이 $1 \times 3$인데 어떻게 더해지는가?

### Q24. [T/F]
이진 분류(binary classification) MLP는 클래스가 2개이므로 출력 뉴런이 반드시 2개 있어야 한다.

답: ☐ T ☐ F

### Q25. [단답형]
상태 1~8이 일렬로 놓여 있고, 각 상태의 이웃은 바로 옆 상태(±1)뿐이다. 비용은 다음과 같고, **비용을 최소화**하는 hill climbing을 한다. (이웃 중 비용이 가장 낮은 상태가 현재보다 **엄격히** 낮을 때만 이동)

| 상태 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|------|---|---|---|---|---|---|---|---|
| 비용 | 7 | 5 | 4 | 6 | 8 | 3 | 1 | 2 |

- (1) 상태 1에서 시작할 때 이동 경로와 멈추는 상태는?
- (2) 상태 5에서 시작할 때 이동 경로와 멈추는 상태는?
- (3) 상태 4에서 시작할 때 멈추는 상태는?
- (4) (1)~(3) 중 global optimum에 도달한 경우는? 도달하지 못한 경우는 무엇에 갇힌 것인가?

### Q26. [빈칸 손코딩]
Alpha-beta pruning을 적용한 minimax 함수이다. 트리는 중첩 리스트로 표현하고, 정수는 단말 노드이다. 빈칸을 채우시오.

```python
import math

def alphabeta(node, alpha, beta, is_max):
    if isinstance(node, int):                 # 단말 노드
        return node
    if is_max:
        value = __(a)__
        for child in node:
            value = max(value, alphabeta(child, alpha, beta, __(b)__))
            alpha = __(c)__
            if __(d)__:
                break                         # 가지치기
        return value
    else:
        value = math.inf
        for child in node:
            value = min(value, alphabeta(child, alpha, beta, True))
            beta = __(e)__
            if alpha >= beta:
                break
        return value

tree = [[3, 12], [2, 8], [14, 1]]             # MAX → MIN 3개 → 단말
print(alphabeta(tree, __(f)__, __(g)__, True))
```

- (h) 출력값과, 이 코드에서 방문하지 않는 단말 값을 쓰시오.

### Q27. [단답형]
Bayesian network: Rain(R) → Sprinkler(S), 그리고 R과 S → GrassWet(G)

| 확률              | 값   | 확률                   | 값   |
|-------------------|------|------------------------|------|
| $P(R=T)$          | 0.2  | $P(G=T \mid S=T, R=T)$ | 0.99 |
| $P(S=T \mid R=T)$ | 0.01 | $P(G=T \mid S=T, R=F)$ | 0.9  |
| $P(S=T \mid R=F)$ | 0.4  | $P(G=T \mid S=F, R=T)$ | 0.8  |
|                   |      | $P(G=T \mid S=F, R=F)$ | 0.0  |

- (1) $P(G=T, S=T, R=T)$, $P(G=T, S=T, R=F)$, $P(G=T, S=F, R=T)$, $P(G=T, S=F, R=F)$를 구하시오.
- (2) $P(G=T)$를 구하시오.
- (3) 잔디가 젖었을 때 스프링클러가 켜져 있었을 확률 $P(S=T \mid G=T)$는? (소수 넷째 자리에서 반올림)
- (4) 강의에서 구한 $P(R=T \mid G=T) \approx 0.3577$과 (3)의 합이 1이 아닌 이유는?

### Q28. [T/F]
결정 트리 학습은 가능한 모든 트리를 비교하여 전체 불순도가 가장 낮은 트리를 한 번에 찾는다.

답: ☐ T ☐ F

### Q29. [단답형]
지식 베이스(KB)가 다음과 같다.

- $\forall p\ \forall n\ [\text{Emergency}(p) \land \text{AssignedTo}(p, n) \to \text{Alert}(n)]$
- $\text{Emergency}(Alice)$, $\text{AssignedTo}(Alice, Bob)$, $\text{AssignedTo}(Carol, Bob)$, $\text{AssignedTo}(Carol, Dan)$

- (1) KB로부터 추론되는 새로운 사실을 모두 쓰시오.
- (2) $\text{Alert}(Dan)$과 $\lnot\text{Alert}(Dan)$ 중 KB로 추론할 수 있는 것은?
- (3) 이 KB의 constant symbol과 predicate symbol을 모두 쓰시오.
- (4) $\text{Emergency}(Carol)$이 KB에 추가되면 새로 추론되는 사실은?

### Q30. [객관식]
AI 역사에 대한 설명으로 **옳지 않은** 것은?

① 1956년 다트머스 워크숍에서 "Artificial Intelligence"라는 이름이 처음 쓰였다.
② 1969년 Minsky와 Papert는 *Perceptrons*에서 단순 퍼셉트론이 XOR을 학습할 수 없음을 보였고, 이후 제1차 AI 겨울이 왔다.
③ MYCIN은 약 450개의 if-then 규칙으로 혈액 감염을 진단한 전문가 시스템이다.
④ DENDRAL은 1997년 체스 세계 챔피언을 이긴 IBM의 시스템이다.
⑤ 1980년대 중반 backpropagation이 여러 연구 그룹에 의해 재발견되면서 신경망 연구가 다시 살아났다.

### Q31. [단답형]
틱택토에서 heuristic alpha-beta tree search의 평가 함수가 다음과 같다. (O = +1, X = −1)

$$\text{EVAL} = (+1) \times \frac{\text{O가 아직 완성할 수 있는 줄 수}}{8} + (-1) \times \frac{\text{X가 아직 완성할 수 있는 줄 수}}{8}$$

"아직 완성할 수 있는 줄"은 **상대 말이 하나도 없는** 줄이다(빈 줄 포함).

```
 O | X | .
---+---+---
 . | O | .
---+---+---
 . | . | X
```

- (1) O가 완성할 수 있는 줄 수와 그 줄들을 쓰시오.
- (2) X가 완성할 수 있는 줄 수와 그 줄들을 쓰시오.
- (3) EVAL 값은?
- (4) 분모가 8인 이유는?

### Q32. [T/F]
Boolean 노드 X의 부모가 Boolean 노드 2개이면 CPT의 conditioning case는 4개이고, 각 conditioning case에서 $P(X=T \mid \cdots) + P(X=F \mid \cdots) = 1$이다.

답: ☐ T ☐ F

### Q33. [단답형]
은닉층 1개인 신경망(bias 없음, 모든 활성 함수 sigmoid)이다. $w_{l,i,j}$는 $(l-1)$층 $i$번 뉴런 → $l$층 $j$번 뉴런 가중치이다.

| 가중치      | 값   | 가중치      | 값  | 가중치      | 값   |
|-------------|------|-------------|-----|-------------|------|
| $w_{1,0,0}$ | 0.5  | $w_{1,1,0}$ | 0.3 | $w_{2,0,0}$ | 1.0  |
| $w_{1,0,1}$ | -0.5 | $w_{1,1,1}$ | 0.8 | $w_{2,1,0}$ | -1.0 |

입력 $x_0 = 1.0$, $x_1 = 0.0$, 정답 $y = 0$, 손실 $L = (y - o_{2,0})^2$, 학습률 $\eta = 1.0$이다. ($\sigma(0.5) = 0.6225$, $\sigma(-0.5) = 0.3775$, $\sigma(0.245) = 0.5609$)

- (1) $z_{1,0}$, $o_{1,0}$, $z_{1,1}$, $o_{1,1}$
- (2) $z_{2,0}$, $\hat{y} = o_{2,0}$, $L$
- (3) $\delta_{2,0} = 2(o_{2,0} - y) \cdot o_{2,0}(1 - o_{2,0})$
- (4) $\Delta w_{l,i,j} = -\eta \cdot \delta_{l,j} \cdot o_{l-1,i}$로 갱신한 $w_{2,0,0}$, $w_{2,1,0}$
- (5) $\delta_{1,0} = o_{1,0}(1 - o_{1,0}) \cdot w_{2,0,0} \cdot \delta_{2,0}$ (갱신 **전** $w_{2,0,0}$ 사용)과, 갱신한 $w_{1,0,0}$, $w_{1,1,0}$

(소수 넷째 자리까지)

### Q34. [빈칸 손코딩]
MNIST를 mini-batch로 학습·평가하는 코드이다. 빈칸을 채우시오.

```python
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=__(a)__)
test_loader  = DataLoader(test_dataset,  batch_size=32, shuffle=__(b)__)

for epoch in range(epochs):
    model.__(c)__()                                  # 학습 모드
    total_loss, correct, total = 0.0, 0, 0
    for images, labels in train_loader:
        logits = model(images)
        loss = criterion(logits, labels)
        optimizer.__(d)__()
        loss.__(e)__()
        optimizer.__(f)__()
        total_loss += loss.__(g)__() * labels.size(0)
        correct += (logits.__(h)__(dim=1) == labels).sum().item()
        total += labels.size(0)
    print(total_loss / total, correct / total)

model.__(i)__()                                      # 평가 모드
with torch.__(j)__():                               # gradient 계산 끄기
    for images, labels in test_loader:
        ...
```

- (k) `total_loss`에 `labels.size(0)`을 곱하는 이유는?

### Q35. [단답형]
Monte Carlo Tree Search에서 루트의 자식 노드 세 개의 시뮬레이션 결과가 다음과 같다.

| 자식 | 승리 횟수 | 전체 시행 횟수 |
|------|-----------|----------------|
| A    | 7         | 10             |
| B    | 4         | 5              |
| C    | 30        | 50             |

- (1) 각 자식의 평균 효용값(avg_utility)을 구하고, 지금 가장 좋은 수를 고르시오.
- (2) B에서 시뮬레이션을 한 번 더 했더니 졌다. B의 평균 효용값과, 이때 가장 좋은 수는?
- (3) 시뮬레이션 중 무작위로 둔 수들은 트리에 노드로 추가되는가?

### Q36. [T/F]
John Searle의 구분에 따르면, 추천 시스템이나 이미지 분류기처럼 특정 작업에서만 지능적으로 행동하는 AI는 Strong AI에 해당한다.

답: ☐ T ☐ F

### Q37. [단답형]
명제 P: 시험 기간이다, Q: 도서관이 붐빈다, R: 도서관에 빈자리가 없다.

KB: $P \to Q$, $Q \to R$, $\lnot R$

- (1) KB에서 $\lnot Q$를 이끌어낼 때 쓰는 추론 규칙은?
- (2) 이어서 $\lnot P$를 이끌어내시오. (사용한 규칙 포함)
- (3) $Q \to R$을 implication elimination으로 $\to$ 없이 쓰시오.
- (4) KB에 $\lnot R$ 대신 $R$이 있었다면 $P$의 참/거짓을 결정할 수 있는가?

### Q38. [객관식]
상황과 손실 함수의 짝으로 **옳지 않은** 것은?

① 정답이 정수 레이블(0, 1, 2)인 3클래스 분류 → Sparse categorical cross-entropy
② 정답이 one-hot 벡터([0, 1, 0])인 3클래스 분류 → Categorical cross-entropy
③ 스팸/정상 이진 분류 → Binary cross-entropy
④ 이상치가 섞인 집값 예측 → Huber loss
⑤ 손글씨 숫자(0~9) 10클래스 분류 → MSLE

### Q39. [단답형]
데이터 200개(클래스 A 100개, B 60개, C 40개)를 다음과 같이 나눈다.

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
```

- (1) train과 test의 데이터 수는?
- (2) test set의 클래스별 개수는?
- (3) `stratify=y`를 빼면 (2)가 보장되지 않는 이유는?
- (4) `random_state=42`의 역할은?

### Q40. [T/F]
$\lnot(P \lor \lnot Q) \equiv \lnot P \land Q$ 이다.

답: ☐ T ☐ F

### Q41. [단답형]
$\mathbf{z} = [-2,\ 0,\ 3]$에 각 활성 함수를 원소별로 적용한 결과를 쓰시오. ($e^{2} \approx 7.389$, $e^{-3} \approx 0.0498$, 소수 넷째 자리까지)

- (1) Binary step (Heaviside)
- (2) ReLU
- (3) Sigmoid
- (4) $\tanh(0)$의 값과 tanh의 출력 범위
- (5) 회귀(regression) 모델의 출력층에 Binary step을 쓸 수 없는 이유

### Q42. [단답형]
Q14의 IrisMLP(4 → 8 → 3)에 batch 크기 16으로 입력을 넣는다. 행 벡터 방식($\mathbf{X}\mathbf{W} + \mathbf{b}$)으로 다음 shape을 쓰시오.

- (1) 입력 $\mathbf{X}$
- (2) 은닉층의 $\mathbf{W}^{(1)}$, $\mathbf{b}^{(1)}$, 은닉층 출력
- (3) 출력층의 $\mathbf{W}^{(2)}$, 출력
- (4) 샘플 1개를 열 벡터 방식($\mathbf{W}\mathbf{x} + \mathbf{b}$)으로 계산할 때의 $\mathbf{W}^{(1)}$, $\mathbf{x}$
- (5) 이 모델의 학습 파라미터 총 개수

### Q43. [T/F]
Markov 가정에 따르면 $X_t$는 $X_0, \dots, X_{t-1}$ 전체에 의존하므로, $P(X_t \mid X_{t-1})$ 하나만으로는 상태 전이를 표현할 수 없다.

답: ☐ T ☐ F

### Q44. [빈칸 손코딩]
이진 분류(1 = Positive) 결과로 precision, recall, accuracy를 구하는 코드이다. 빈칸을 채우시오.

```python
y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
y_pred = [1, 1, 0, 1, 0, 1, 0, 1, 1, 0]

tp = fp = fn = tn = 0
for actual, predicted in __(a)__(y_true, y_pred):
    if actual == 1 and predicted == 1:
        tp += 1
    elif actual == 0 and predicted == 1:
        __(b)__ += 1
    elif actual == 1 and predicted == 0:
        __(c)__ += 1
    else:
        tn += 1

precision = tp / (__(d)__)
recall    = tp / (__(e)__)
accuracy  = (__(f)__) / len(y_true)
```

- (g) tp, fp, fn, tn과 precision, recall, accuracy 값을 쓰시오.

### Q45. [단답형]
로봇 경로를 유전 알고리즘으로 찾는다. 경로는 F(전진), R(우회전), L(좌회전)의 나열이다.

- 부모 1: `F F R F L`
- 부모 2: `L F F R R`

- (1) **앞 2개 유전자 뒤**를 자르는 one-point crossover로 만든 자식 1(부모 1의 앞부분 + 부모 2의 뒷부분)과 자식 2(부모 2의 앞부분 + 부모 1의 뒷부분)를 쓰시오.
- (2) 자식 1의 4번째 유전자에 mutation이 일어나 `L`로 바뀌었다. 결과는?
- (3) 한 세대에서 다음 세대로 넘어가는 세 단계를 순서대로 쓰시오.
- (4) 부모 어디에도 없던 새로운 변화를 만드는 단계는?

### Q46. [단답형]
주사위 두 개를 던진다.

- (1) 두 눈의 합이 10 이상일 확률은?
- (2) 두 눈의 합이 10 이상일 때, 첫 번째 주사위가 5일 확률은?
- (3) 두 눈의 합이 10 이상일 때, 두 눈이 같을(double) 확률은?
- (4) (2)를 $P(a \mid b) = P(a \land b) / P(b)$ 식에 맞춰 쓰시오.

### Q47. [T/F]
같은 예측 결과에 대해 RMSE는 항상 MAE 이상이며, 두 값은 모든 오차의 절댓값이 같을 때만 같아진다.

답: ☐ T ☐ F

### Q48. [단답형]
도난 경보 Bayesian network: Burglary(B), Earthquake(E) → Alarm(A) → JohnCalls(J), MaryCalls(M). 모든 변수는 Boolean이다.

- (1) 각 노드의 CPT 행(conditioning case) 수를 쓰시오.
- (2) 이 네트워크를 정의하는 데 필요한 확률값은 모두 몇 개인가? (각 행에서 $P(X=T \mid \cdots)$만 저장)
- (3) 같은 5개 변수의 full joint distribution을 표로 저장하려면 독립적인 확률값이 몇 개 필요한가?
- (4) (2)가 (3)보다 작을 수 있는 이유를 쓰시오.

### Q49. [빈칸 손코딩]
Q1의 그래프에서 Uniform-cost search를 `heapq`로 구현했다. 빈칸을 채우시오.

```python
import heapq

graph = {
    'S': [('A', 1), ('B', 4)],
    'A': [('C', 2), ('D', 6)],
    'B': [('D', 2), ('E', 6)],
    'C': [('G', 7)],
    'D': [('G', 3)],
    'E': [('G', 1)],
    'G': [],
}

def uniform_cost_search(start, goal):
    pq = [(0, start, [start])]               # (누적 비용, 노드, 경로)
    visited = set()
    while pq:
        cost, node, path = heapq.__(a)__(pq)
        if node in visited:
            continue
        visited.add(node)
        if node == __(b)__:
            return cost, path
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.__(c)__(pq, (__(d)__, neighbor, path + [neighbor]))
    return None

print(uniform_cost_search('S', 'G'))
```

- (e) 출력 결과를 쓰시오.
- (f) 이 코드를 A\* search로 바꾸려면 큐에 넣는 우선순위를 어떻게 바꿔야 하는가? (휴리스틱은 딕셔너리 `h`)

### Q50. [단답형]
`nn.Flatten()` → `nn.Linear(784, 256)` → ReLU → `nn.Linear(256, 64)` → ReLU → `nn.Linear(64, 10)` 모델이 있다.

- (1) 각 `nn.Linear` 층의 파라미터 수(가중치 + bias)를 쓰시오.
- (2) 전체 학습 파라미터 수는?
- (3) 모든 층에서 bias를 없애면 전체 파라미터 수는?
- (4) 이 모델에 넣는 이미지 한 장의 원래 크기는? 출력 뉴런 10개는 무엇을 뜻하는가?
