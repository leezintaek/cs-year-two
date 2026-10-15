# 인공지능개론 퀴즈 1

- 범위: week1 ~ week7 강의 PDF + week5 실습 코드
- 문제 유형: T/F, 객관식, 단답형 주관식, 빈칸 채우는 손코딩 (순서 무작위)
- 코드는 모두 Python
- 정답과 해설: `quiz_1_explanation.md`

---

### Q1. [단답형]
3개 클래스 분류 모델의 혼동 행렬(confusion matrix)이 다음과 같다. (행: 실제 클래스, 열: 예측 클래스)

| 실제 \ 예측 | A   | B   | C   |
|-------------|-----|-----|-----|
| A           | 40  | 5   | 5   |
| B           | 10  | 20  | 10  |
| C           | 0   | 10  | 50  |

- (1) accuracy
- (2) 클래스별 recall과 macro 평균 recall
- (3) 클래스별 precision과 macro 평균 precision
- (4) micro 평균 precision과 micro 평균 recall

(소수 셋째 자리에서 반올림)

### Q2. [단답형]
다음 방향 그래프에서 S에서 G까지 **Uniform-Cost Search**를 수행한다.

| 간선   | 비용 |
|--------|------|
| S → A  | 2    |
| S → B  | 5    |
| A → B  | 1    |
| A → C  | 6    |
| B → C  | 2    |
| B → G  | 7    |
| C → G  | 3    |

- (1) 노드가 **확장(dequeue)되는 순서**를 쓰시오.
- (2) 찾은 경로와 총 비용을 쓰시오.
- (3) 탐색 도중 경로 비용이 **더 작은 값으로 갱신**되는 노드와 그 시점을 모두 쓰시오.

### Q3. [T/F]
Naïve Bayes 모델은 모든 feature가 서로 (무조건적으로) 독립이라고 가정한다.

답: ☐ T ☐ F

### Q4. [빈칸 손코딩]
Iris 데이터(입력 feature 2개, 클래스 3개)를 분류하는 PyTorch MLP와 학습 루프이다. 빈칸을 채우시오.

```python
import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden_layer = nn.Linear(____(1)____, ____(2)____)   # 은닉 뉴런 4개
        self.output_layer = nn.Linear(4, ____(3)____)
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=____(4)____)

    def forward(self, x):
        hidden_o = self.sigmoid(self.hidden_layer(x))
        output_z = self.output_layer(hidden_o)
        return self.softmax(output_z)

model = MLP()
x = torch.tensor([[0.2, 1.4]])      # Petal Width, Petal Length

# 학습 루프 (criterion, optimizer, train_loader는 정의되어 있다고 가정)
for images, labels in train_loader:
    logits = model(images)
    loss = criterion(logits, labels)
    optimizer.____(5)____()   # 이전 gradient 초기화
    loss.____(6)____()        # backpropagation
    optimizer.____(7)____()   # 가중치와 bias 갱신
```

- (8) `x`의 shape은 무엇이며, Softmax의 `dim`을 (4)처럼 정한 이유는?

### Q5. [단답형]
다음 게임 트리에서 루트는 MAX, 둘째 층은 MIN 노드이다. 단말 값은 왼쪽부터 주어진다.

```
                 MAX
        ┌─────────┼─────────┐
       MIN       MIN       MIN
     ┌──┼──┐   ┌──┼──┐   ┌──┼──┐
     3  12 8   2  4  6   14 5  2
```

- (1) 각 MIN 노드의 값과 루트의 minimax 값을 쓰시오.
- (2) 왼쪽에서 오른쪽 순서로 alpha-beta pruning을 할 때 **방문하지 않는(가지치기되는) 단말 값**을 모두 쓰시오.

### Q6. [단답형]
회귀 모델의 예측값 $\hat{y}$와 실제값 $y$가 다음과 같다.

| $\hat{y}$ | 5   | 2   | 4   | 7   | 1   |
|-----------|-----|-----|-----|-----|-----|
| $y$       | 3   | 3   | 4   | 4   | 5   |

- (1) MAE와 RMSE를 구하시오.
- (2) 마지막 샘플의 실제값이 5가 아니라 15였다면 MAE와 RMSE는 각각 얼마가 되는가?
- (3) (1)과 (2)를 비교하여 두 지표의 차이를 한 문장으로 설명하시오.

(소수 셋째 자리에서 반올림)

### Q7. [T/F]
BFS(너비 우선 탐색)는 action마다 비용이 서로 달라도 항상 최소 비용 해(optimal solution)를 찾는다.

답: ☐ T ☐ F

### Q8. [단답형]
어떤 질병의 유병률은 1%이다. 검사는 환자의 90%를 양성으로 판정하고, 환자가 아닌 사람의 5%도 양성으로 판정한다. 검사 결과가 양성인 사람이 실제로 환자일 확률을 구하시오. (소수 넷째 자리에서 반올림, 풀이 과정 포함)

### Q9. [단답형]
입력 2개인 퍼셉트론이 $w_1 = 1$, $w_2 = 1$, $b = -1.5$이고 활성 함수는 Heaviside(1 if $z \ge 0$)이다.

- (1) 입력 $(x_1, x_2) = (0,0), (0,1), (1,0), (1,1)$에 대한 $z$와 출력을 쓰시오.
- (2) 이 퍼셉트론은 어떤 논리 연산을 수행하는가?
- (3) $b$만 바꿔서 OR 연산을 만들려면 $b$를 어떤 범위로 잡아야 하는가?
- (4) 단일 퍼셉트론으로 XOR를 만들 수 없는 이유와 해결 방법을 쓰시오.

### Q10. [객관식]
다음 사건을 **시간 순서대로** 바르게 나열한 것은?

- (가) AlphaGo가 이세돌 9단에게 승리
- (나) Dartmouth 워크숍에서 "Artificial Intelligence"라는 이름 탄생
- (다) Minsky와 Papert의 *Perceptrons* 출간 → 첫 번째 AI 겨울
- (라) ImageNet 데이터베이스 공개
- (마) 혈액 감염 진단 전문가 시스템 MYCIN
- (바) IBM Deep Blue가 체스 세계 챔피언에게 승리
- (사) IBM Watson이 퀴즈 쇼에서 인간 챔피언에게 승리

① 나 → 다 → 마 → 바 → 라 → 사 → 가
② 나 → 마 → 다 → 바 → 라 → 사 → 가
③ 나 → 다 → 마 → 라 → 바 → 사 → 가
④ 다 → 나 → 마 → 바 → 라 → 가 → 사

### Q11. [단답형]
우산(umbrella) HMM에서 숨은 상태는 $Rain_t \in \{T, F\}$이다.

- $P_0(T) = P_0(F) = 0.5$
- Transition: $P(R_t = T \mid R_{t-1} = T) = 0.7$, $P(R_t = T \mid R_{t-1} = F) = 0.3$
- Observation: $P(U_t = T \mid R_t = T) = 0.9$, $P(U_t = T \mid R_t = F) = 0.2$

관측 순서가 $U_1 = T$, $U_2 = F$일 때 Viterbi 알고리즘
$P_t(j) = \max_i \left[P_{t-1}(i) \cdot P(R_t = j \mid R_{t-1} = i)\right] \cdot P(U_t \mid R_t = j)$ 를 적용하시오.

- (1) $P_1(T)$, $P_1(F)$
- (2) $P_2(T)$, $P_2(F)$
- (3) 가장 가능성이 높은 숨은 상태 순서 $(R_1, R_2)$

### Q12. [단답형]
Q2와 같은 그래프에서 휴리스틱이 다음과 같을 때 **A\* search**를 수행한다.

| 노드   | S   | A   | B   | C   | G   |
|--------|-----|-----|-----|-----|-----|
| $h(n)$ | 6   | 4   | 2   | 1   | 0   |

- (1) 노드가 확장되는 순서와, 확장 시점의 $f(n) = g(n) + h(n)$ 값을 쓰시오.
- (2) 찾은 경로와 총 비용을 쓰시오.

### Q13. [T/F]
Alpha-beta pruning은 자식 노드를 방문하는 순서가 나쁘면 루트의 minimax 값이 원래 minimax와 달라질 수 있다.

답: ☐ T ☐ F

### Q14. [단답형]
- (1) 입력 2개 → 은닉 뉴런 4개 → 출력 3개인 fully connected MLP의 학습 파라미터(가중치 + bias) 개수는?
- (2) Fashion-MNIST용 `nn.Flatten()` → `nn.Linear(784, 128)` → `nn.Linear(128, 10)` 모델의 파라미터 개수는?

### Q15. [단답형]
명제 P: 화요일이다, Q: 비가 온다, R: Harry는 달리기를 한다.

- (1) $(P \land \lnot Q) \to R$ 을 implication elimination과 De Morgan's law로 $\to$ 없는 형태로 바꾸시오. (각 단계 표시)
- (2) $P = T$, $Q = F$, $R = F$일 때 원래 문장의 참/거짓은?

### Q16. [빈칸 손코딩]
Iris 데이터셋(150개, 클래스 3개, 클래스당 50개)으로 결정 트리를 학습·평가하는 코드이다.

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=____(1)____,       # 전체의 30%를 test set으로
    random_state=42,
    stratify=____(2)____         # 클래스 비율을 train/test에서 동일하게
)

model = DecisionTreeClassifier(criterion="gini", max_depth=3, random_state=42)
model.____(3)____(X_train, y_train)     # training
y_pred = model.____(4)____(X_test)      # testing

correct = 0
for actual, predicted in ____(5)____(y_test, y_pred):
    if actual == predicted:
        correct += 1

accuracy = ____(6)____
error_rate = ____(7)____
```

- (8) 이 코드에서 training data와 test data의 개수, 그리고 test data에 들어가는 클래스별 샘플 수는?

### Q17. [T/F]
False Positive가 치명적인 경우에는 recall을, False Negative가 치명적인 경우에는 precision을 우선적으로 보아야 한다.

답: ☐ T ☐ F

### Q18. [단답형]
로봇 경로를 유전 알고리즘으로 찾는다. 적합도 점수는 $-\text{distance} - 10 \times \text{collision}$ 이다.

| 경로 | distance | # collision |
|------|----------|-------------|
| R1   | 4        | 2           |
| R2   | 9        | 1           |
| R3   | 18       | 0           |

- (1) 각 경로의 적합도 점수를 구하고, selection에서 적합도가 높은 2개를 고르시오.
- (2) 충돌 가중치를 10이 아니라 1로 바꾸면 선택되는 2개는?
- (3) Selection, crossover, mutation 각각의 역할을 한 줄씩 쓰시오.

### Q19. [단답형]
출력층의 값이 $z = [2,\ 1,\ 0]$일 때 Softmax 출력을 구하시오. ($e^2 \approx 7.389$, $e^1 \approx 2.718$, $e^0 = 1$, 소수 넷째 자리에서 반올림) 그리고 `argmax`로 예측한 클래스 인덱스는?

### Q20. [단답형]
도난 경보 Bayesian network: Burglary(B), Earthquake(E) → Alarm(A) → JohnCalls(J), MaryCalls(M)

| 확률                         | 값    |
|------------------------------|-------|
| $P(b)$                       | 0.001 |
| $P(e)$                       | 0.002 |
| $P(a \mid b, e)$             | 0.95  |
| $P(a \mid b, \lnot e)$       | 0.94  |
| $P(a \mid \lnot b, e)$       | 0.29  |
| $P(a \mid \lnot b, \lnot e)$ | 0.001 |
| $P(j \mid a)$                | 0.90  |
| $P(m \mid a)$                | 0.70  |

- (1) $P(j, m, a, b, \lnot e)$를 구하시오. (식과 값)
- (2) $\mathbf{P}(M \mid J, A, E, B)$를 가장 간단히 쓰고, 그 이유를 쓰시오.

### Q21. [빈칸 손코딩]
Tic-Tac-Toe에서 BOT은 점수를 최대화, PLAYER는 최소화한다. Minimax 함수의 빈칸을 채우시오.

```python
def minimax(board, turn):
    if is_terminal(board):
        if winner(board) == 'BOT':
            return ____(1)____
        if winner(board) == 'PLAYER':
            return ____(2)____
        return 0                                  # Draw

    if turn == 'BOT':
        best = ____(3)____
        for p in empty_positions(board):
            board[p] = 'BOT'
            score = minimax(board, ____(4)____)
            board[p] = ' '
            best = ____(5)____(best, score)
        return best
    else:
        best = float('inf')
        for p in empty_positions(board):
            board[p] = 'PLAYER'
            score = minimax(board, 'BOT')
            board[p] = ' '
            best = ____(6)____(best, score)
        return best
```

- (7) `board[p] = ' '` 줄이 없으면 어떤 문제가 생기는가?

### Q22. [T/F]
Validation set은 학습이 끝난 최종 모델의 성능을 마지막에 한 번 평가하는 데 쓰고, test set은 여러 후보 모델 중 가장 좋은 모델을 고르는 데 쓴다.

답: ☐ T ☐ F

### Q23. [객관식]
Hill climbing(= greedy local search)에 대한 설명으로 옳은 것은?

① 지금까지 방문한 노드 집합과 경로를 우선순위 큐로 모두 기록한다.
② 이웃 중 가장 좋은 상태가 현재 상태보다 좋을 때만 이동하므로, 목표에 도달하지 못하고 멈출 수 있다.
③ Greedy best-first search와 달리 local minima를 항상 탈출할 수 있다.
④ 과거에 발견했던 이웃 노드로 되돌아가 다른 경로를 시도한다.

### Q24. [단답형]
메일 500통 중 실제 스팸은 120통이다. 모델은 100통을 스팸으로 분류했고, 그중 90통이 실제 스팸이었다. (스팸 = Positive)

- (1) TP, FP, FN, TN
- (2) accuracy, precision, recall

### Q25. [T/F]
PyTorch에서 `loss.backward()`는 gradient를 계산할 뿐 아니라 가중치까지 갱신한다.

답: ☐ T ☐ F

### Q26. [객관식]
"비가 오면 땅이 젖는다. 땅이 젖지 않았다. 따라서 비가 오지 않았다." 에 사용된 추론 규칙은?

① Modus Ponens  ② Modus Tollens  ③ And Elimination  ④ Double-Negation Elimination

### Q27. [단답형]
Iris 데이터로 학습한 결정 트리의 규칙이 다음과 같다.

```
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

- (1) 다음 샘플의 예측 클래스를 쓰시오. (PetalLength, PetalWidth) = (a) (1.9, 0.4) (b) (5.0, 1.5) (c) (4.7, 1.4) (d) (4.5, 1.7)
- (2) 마지막 분기(PetalLengthCm ≤ 4.85)는 두 leaf의 클래스가 같은데도 만들어졌다. 그 이유를 쓰시오.

### Q28. [단답형]
Q2의 그래프와 Q12의 휴리스틱으로 **weighted A\* search** ($W = 3$)를 수행한다.

- (1) 노드가 확장되는 순서와 확장 시점의 $f(n) = g(n) + W \cdot h(n)$ 값을 쓰시오.
- (2) 찾은 경로와 총 비용을 쓰고, A\*의 결과(Q12)와 비교하시오.

### Q29. [T/F]
Monte Carlo Tree Search에서 결과가 날 때까지 무작위로 두는 시뮬레이션(playout) 동안의 수들은 모두 트리에 노드로 추가된다.

답: ☐ T ☐ F

### Q30. [단답형]
단일층 퍼셉트론 $h = \text{heaviside}(\mathbf{W}\mathbf{x} + \mathbf{b})$ (1 if $z \ge 0$)로 Iris를 분류한다.

$$\mathbf{W} = \begin{bmatrix} -0.8 & -1.2 \\ 0.1 & -0.05 \\ 0.7 & 1.3 \end{bmatrix} \begin{matrix} \text{// Setosa} \\ \text{// Versicolor} \\ \text{// Virginica} \end{matrix}, \quad \mathbf{b} = \begin{bmatrix} -0.4 \\ -0.01 \\ 0.5 \end{bmatrix}, \quad \mathbf{x} = \begin{bmatrix} \text{Petal Width} \\ \text{Petal Length} \end{bmatrix} = \begin{bmatrix} 0.5 \\ 0.0 \end{bmatrix}$$

- (1) $\mathbf{z}$ 세 값과 출력 $\mathbf{h}$를 구하시오.
- (2) `np.argmax(h, axis=0)`의 결과(클래스 이름)는? 이 결과에서 생기는 문제점은?
- (3) Heaviside 대신 Softmax를 썼다면 예측 클래스는?

### Q31. [단답형]
다음 데이터로 Naïve Bayes 분류를 한다.

| #   | Weather | Temp | Wind   | Play |
|-----|---------|------|--------|------|
| 1   | Sunny   | Hot  | Weak   | No   |
| 2   | Sunny   | Hot  | Strong | No   |
| 3   | Rainy   | Hot  | Weak   | Yes  |
| 4   | Rainy   | Cool | Weak   | Yes  |
| 5   | Rainy   | Cool | Strong | No   |
| 6   | Sunny   | Cool | Strong | Yes  |
| 7   | Sunny   | Cool | Weak   | Yes  |
| 8   | Rainy   | Hot  | Strong | No   |
| 9   | Sunny   | Hot  | Weak   | Yes  |
| 10  | Rainy   | Cool | Weak   | Yes  |

입력이 {Sunny, Cool, Strong}일 때 $p(\text{Yes}) \prod p(x_i \mid \text{Yes})$ 와 $p(\text{No}) \prod p(x_i \mid \text{No})$ 를 각각 분수와 소수로 구하고, 예측 결과를 쓰시오.

### Q32. [단답형]
MNIST 훈련 데이터 60,000개를 mini-batch 크기 32로 학습한다.

- (1) 입력층 뉴런 수와 출력층 뉴런 수는?
- (2) 1 epoch 동안 파라미터는 몇 번 갱신되는가?
- (3) 10 epoch 동안은 몇 번 갱신되는가?
- (4) Full-batch로 학습할 때의 장점과 단점을 하나씩 쓰시오.

### Q33. [객관식 — 모두 고르기]
다음 중 **uninformed (blind) search**에 해당하는 것을 모두 고르시오.

① Breadth-first search  ② Greedy best-first search  ③ Uniform-cost search  ④ Iterative deepening search
⑤ A\* search  ⑥ Dijkstra's algorithm  ⑦ Weighted A\* search

### Q34. [단답형]
날씨 Markov chain의 상태는 [Sunny, Rainy]이고 전이 행렬은

$$P = \begin{bmatrix} 0.9 & 0.1 \\ 0.5 & 0.5 \end{bmatrix}$$

이다. 오늘이 Sunny, 즉 $\mathbf{x}^{(0)} = [1\ \ 0]$일 때 $\mathbf{x}^{(1)}$, $\mathbf{x}^{(2)}$, $\mathbf{x}^{(3)}$을 구하시오.

### Q35. [T/F]
$P \to Q$는 $\lnot P \to \lnot Q$와 논리적으로 동치이다.

답: ☐ T ☐ F

### Q36. [단답형]
다음 트리에서 루트는 MAX, 그 아래는 MIN, 그 아래는 MAX 노드이다. 단말 값은 왼쪽부터 주어진다.

```
                       MAX
            ┌───────────┴───────────┐
           MIN                     MIN
       ┌────┴────┐             ┌────┴────┐
      MAX       MAX           MAX       MAX
     ┌─┴─┐     ┌─┴─┐         ┌─┴─┐     ┌─┴─┐
     3   5     6   9         1   2     0   -1
```

- (1) 루트의 minimax 값은?
- (2) 왼쪽에서 오른쪽 순서로 alpha-beta pruning을 할 때 가지치기되어 방문하지 않는 단말 값을 모두 쓰고, 각각 어떤 조건($\alpha \ge \beta$)에서 잘렸는지 쓰시오.

### Q37. [객관식]
다음 중 **분류(classification)** 문제에 쓰는 손실 함수로 강의에서 소개되지 **않은** 것은?

① Categorical cross-entropy  ② Hinge loss  ③ Huber loss  ④ KL divergence  ⑤ Sparse categorical cross-entropy

- 추가 질문: 레이블이 정수(class ID)로 주어질 때 쓰는 것과, one-hot 벡터로 주어질 때 쓰는 것을 위 보기에서 각각 고르시오.

### Q38. [단답형]
데이터 1,000개로 5-fold cross validation을 한다.

- (1) 한 번의 평가에서 training에 쓰이는 데이터 수와 testing에 쓰이는 데이터 수는?
- (2) 모델은 총 몇 번 학습되며, 최종 성능은 어떻게 정하는가?
- (3) Training/test를 한 번만 나눠 평가하는 것보다 좋은 점과 단점을 각각 쓰시오.

### Q39. [T/F]
California Housing 회귀 실습에서도 `train_test_split`에 `stratify=y`를 지정해 train/test의 클래스 비율을 맞춘다.

답: ☐ T ☐ F

### Q40. [단답형]
Q2의 그래프와 Q12의 휴리스틱으로 **greedy best-first search**를 수행한다.

- (1) 확장 순서와 찾은 경로, 총 비용을 쓰시오.
- (2) Q2(UCS)의 결과와 비교하여 greedy best-first search의 특징을 쓰시오.

### Q41. [단답형]
- (1) "모든 학생 x에 대해, x가 시험을 통과하지 못하면 x는 재수강한다"를 1차 논리(first-order logic)로 쓰시오. (술어: Student, Pass, Retake)
- (2) 지식 베이스에 Student(Tom), ¬Pass(Tom)이 추가되었을 때 추론되는 새 사실은?
- (3) (1)에서 constant symbol과 predicate symbol의 예를 각각 하나씩 쓰시오.

### Q42. [단답형]
은닉층 1개인 신경망(bias 없음, 모든 활성 함수 sigmoid)이다. $w_{l,i,j}$는 $(l-1)$층의 $i$번 뉴런에서 $l$층의 $j$번 뉴런으로 가는 가중치이다.

| 가중치      | 값   | 가중치      | 값   |
|-------------|------|-------------|------|
| $w_{1,0,0}$ | 0.4  | $w_{1,0,1}$ | -0.3 |
| $w_{1,1,0}$ | 0.2  | $w_{1,1,1}$ | 0.6  |
| $w_{2,0,0}$ | 0.5  | $w_{2,1,0}$ | -0.4 |

입력 $x_0 = 1.0$, $x_1 = 0.5$, 정답 $y = 1$, 손실 $L = (\hat{y} - y)^2$ 이다.

- (1) $z_{1,0}$, $o_{1,0}$, $z_{1,1}$, $o_{1,1}$
- (2) $z_{2,0}$, $\hat{y} = o_{2,0}$, 손실 $L$
- (3) Backpropagation 결과 $\partial L / \partial w_{2,0,0} = -0.1465$였다. 학습률 $\eta = 0.5$인 gradient descent로 갱신한 $w_{2,0,0}$은?

(sigmoid 값은 소수 넷째 자리까지)

### Q43. [객관식]
Two-player zero-sum game의 형식적 정의로 **옳지 않은** 것은?

① $ToMove(s)$: 상태 $s$에서 둘 차례인 플레이어
② $Actions(s)$: 상태 $s$에서 가능한 합법적인 수의 집합
③ $Result(s, a)$: transition model
④ $IsTerminal(s)$: 게임이 끝났을 때 참이 되는 terminal test
⑤ $Utility(s, p)$: 모든 상태 $s$에서 플레이어 $p$의 승리 확률을 추정하는 함수

### Q44. [단답형]
다음 상황에 맞는 학습 유형(지도/비지도/강화 학습)을 쓰고, 지도 학습이면 분류인지 회귀인지도 쓰시오.

- (a) 체스 게임이 끝난 뒤 이겼는지 졌는지만 알려 주고, 에이전트가 이를 바탕으로 수를 고치도록 한다.
- (b) 레이블 없는 고객 구매 기록 100만 건에서 비슷한 고객끼리 묶는다.
- (c) "spam/ham" 레이블이 붙은 메일로 새 메일이 스팸인지 판단한다.
- (d) 지역 소득, 방 수, 위치로 집값 중앙값을 예측한다.

### Q45. [T/F]
Weighted A\* ($f(n) = g(n) + W \cdot h(n)$, $W > 1$)는 A\*보다 휴리스틱의 비중을 키워 해를 더 빨리 찾는 경향이 있지만, 찾은 해가 최소 비용 해라는 보장은 없다.

답: ☐ T ☐ F

### Q46. [단답형]
Fashion-MNIST 이미지(28×28)를 batch 크기 32로 `nn.Flatten()` → 은닉층(128) → 출력층(10)에 넣는다. 강의의 $\mathbf{X}\mathbf{W} + \mathbf{b}$ 형식(입력이 행 벡터)으로 계산할 때 다음 행렬의 shape을 쓰시오.

- (1) Flatten 후 입력 $\mathbf{X}$
- (2) 은닉층의 $\mathbf{W}$
- (3) 은닉층 출력
- (4) 출력층의 $\mathbf{W}$와 출력층 출력

### Q47. [T/F]
Bayesian network에서 부모가 3개인 Boolean 노드의 CPT(conditional probability table)는 conditioning case가 3개이다.

답: ☐ T ☐ F

### Q48. [빈칸 손코딩]
California Housing 회귀 모델의 MAE와 RMSE를 구하는 코드이다. 빈칸을 채우시오.

```python
total_error = 0
for actual, predicted in zip(y_test, y_pred):
    total_error += ____(1)____
mae = total_error / ____(2)____

total_squared_error = 0
for actual, predicted in zip(y_test, y_pred):
    total_squared_error += ____(3)____
rmse = ____(4)____
```

### Q49. [T/F]
Heuristic alpha-beta tree search는 terminal test 대신 cutoff test를, UTILITY 대신 EVAL 함수를 사용하며, EVAL은 terminal 상태에서는 UTILITY와 같은 값을 가져야 한다.

답: ☐ T ☐ F

### Q50. [단답형]
다음 설명에 해당하는 탐색 문제의 용어를 쓰시오.

- (1) 환경을 인지하고 그 환경에 대해 행동하는 개체
- (2) 상태 $s$에서 행동 $a$를 했을 때 도달하는 상태를 돌려주는 함수
- (3) 초기 상태에서 어떤 행동의 연속으로든 도달할 수 있는 모든 상태의 집합
- (4) 초기 상태에서 목표 상태로 이끄는 행동의 순서
- (5) (4) 중 비용이 가장 작은 것
