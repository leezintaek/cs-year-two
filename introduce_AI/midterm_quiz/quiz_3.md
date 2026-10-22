# 인공지능개론 퀴즈 3

- 범위: week1 ~ week7 강의 PDF + week5 실습 코드
- 문제 유형: T/F, 객관식, 단답형 주관식, 빈칸 채우는 손코딩 (순서 무작위)
- 코드는 모두 Python
- 정답과 해설: `quiz_3_explanation.md`

---

### Q1. [단답형]
다음 방향 그래프에서 S에서 G까지 탐색한다. ($f$ 값이 같으면 알파벳 순서로 먼저 꺼낸다.)

| 간선  | 비용 | 간선  | 비용 | 노드 | $h(n)$ |
|-------|------|-------|------|------|--------|
| S → A | 1    | B → C | 1    | S    | 4      |
| S → B | 2    | B → G | 5    | A    | 3      |
| A → C | 3    | C → G | 2    | B    | 2      |
| A → G | 6    |       |      | C    | 1      |
|       |      |       |      | G    | 0      |

- (1) **A\* search**의 확장 순서와 각 노드를 꺼낼 때의 $f(n)$, 탐색 중 비용이 갱신되는 노드, 찾은 경로와 비용을 쓰시오.
- (2) **Greedy best-first search**의 확장 순서, 찾은 경로와 비용을 쓰시오.
- (3) **Weighted A\*** ($W = 2$)의 확장 순서와 각 노드를 꺼낼 때의 $f(n)$, 찾은 경로와 비용을 쓰시오.
- (4) (1)과 (3)에서 확장한 노드 수를 비교하시오.

### Q2. [T/F]
A\* search에서 모든 노드의 휴리스틱을 $h(n) = 0$으로 두면, A\*는 uniform-cost search와 같은 평가 함수로 노드를 고르게 된다.

답: ☐ T ☐ F

### Q3. [빈칸 손코딩]
강의의 2 → 4 → 3 MLP(활성 함수 Heaviside, 열 벡터 방식)에 새 입력을 넣는다. 빈칸을 채우시오.

```python
import numpy as np

x = np.array([[0.5], [1.0]])                       # Petal Width, Petal Length
hidden_layer_W = np.array([[ 0.5, -0.3],
                           [-0.2,  0.8],
                           [ 0.1,  0.4],
                           [-0.6, -0.1]])
hidden_layer_b = np.array([[0.1], [-0.2], [0.0], [0.3]])
hidden_z = np.____(a)____(hidden_layer_W, x) + hidden_layer_b
hidden_y = np.____(b)____(hidden_z >= 0, 1, 0)      # Shape: ( (c) )

output_layer_W = np.array([[-0.8, -1.2,  0.5, -0.2],    # Setosa
                           [ 0.1, -0.05, 0.3,  0.1],    # Versicolor
                           [ 0.7,  1.3, -0.4,  0.8]])   # Virginica
output_layer_b = np.array([[-0.4], [-0.01], [0.4]])
output_z = np.matmul(output_layer_W, ____(d)____) + output_layer_b
output_y = np.where(output_z >= 0, 1, 0)
pred = np.argmax(output_y, axis=____(e)____)
```

- (f) `hidden_z`, `hidden_y`, `output_z`, `output_y`, `pred`를 쓰시오.
- (g) 출력층에서만 Heaviside 대신 ReLU를 쓰면 예측 클래스는 무엇으로 바뀌는가?

### Q4. [단답형]
이진 분류 모델이 테스트 샘플 8개에 대해 Positive일 점수를 다음과 같이 냈다.

| 점수 | 0.9 | 0.8 | 0.7 | 0.6 | 0.45 | 0.4 | 0.35 | 0.1 |
|------|-----|-----|-----|-----|------|-----|------|-----|
| 정답 | 1   | 1   | 0   | 1   | 0    | 1   | 0    | 0   |

점수가 threshold **이상**이면 Positive로 예측한다.

- (1) threshold = 0.5일 때 TP, FP, FN, TN과 precision, recall, accuracy
- (2) threshold = 0.3일 때 TP, FP, FN, TN과 precision, recall, accuracy
- (3) 이 모델이 암 검진용이라면 어느 threshold가 더 적절한가? 강의의 기준으로 이유를 쓰시오.

### Q5. [객관식 — 모두 고르기]
$P$, $Q$의 참/거짓에 관계없이 **항상 참(tautology)** 인 것을 모두 고르시오.

① $(P \to Q) \lor (Q \to P)$  ② $(P \land Q) \to (P \lor \lnot Q)$  ③ $P \to (P \land Q)$
④ $(P \to Q) \to (\lnot P \to \lnot Q)$  ⑤ $((P \to Q) \land P) \to Q$

### Q6. [단답형]
HMM의 숨은 상태는 $R_t \in \{T, F\}$, 관측은 $U_t$이다. 강의 예제와 **확률값이 다르다**.

| 전이 모델         | 값  | 관측 모델         | 값  |
|-------------------|-----|-------------------|-----|
| $P(R_t=T \mid T)$ | 0.6 | $P(U=T \mid R=T)$ | 0.9 |
| $P(R_t=F \mid T)$ | 0.4 | $P(U=T \mid R=F)$ | 0.3 |
| $P(R_t=T \mid F)$ | 0.2 |                   |     |
| $P(R_t=F \mid F)$ | 0.8 |                   |     |

$P_0(T) = P_0(F) = 0.5$, 관측 순서 $U_1 = T,\ U_2 = T,\ U_3 = F$일 때 Viterbi 알고리즘으로

- (1) $P_1(T)$, $P_1(F)$와 각각 max를 준 이전 상태
- (2) $P_2(T)$, $P_2(F)$와 각각 max를 준 이전 상태
- (3) $P_3(T)$, $P_3(F)$와 각각 max를 준 이전 상태
- (4) backtracking으로 구한 가장 가능성 높은 순서 $(R_1, R_2, R_3)$

를 구하시오.

### Q7. [T/F]
Softmax의 입력 $\mathbf{z}$의 모든 원소에 같은 양수 $c$를 **곱해도**($z_i \to c \cdot z_i$) 출력 확률 분포는 변하지 않는다.

답: ☐ T ☐ F

### Q8. [단답형]
Iris 훈련 데이터 120개(setosa, versicolor, virginica 각 40개)로 결정 트리를 만든다. Gini impurity는 $G = 1 - \sum_k p_k^2$이고, 분할 후 불순도는 자식 노드 $G$의 샘플 수 가중 평균이다.

- 규칙 1 `PetalLengthCm <= 2.45`: 왼쪽 (40, 0, 0), 오른쪽 (0, 40, 40)
- 규칙 2 (규칙 1의 오른쪽 노드에서) `PetalWidthCm <= 1.65`: 왼쪽 (0, 38, 4), 오른쪽 (0, 2, 36)

- (1) 루트 노드의 Gini impurity
- (2) 규칙 1 분할 후 불순도와, 불순도가 얼마나 줄었는지
- (3) 규칙 2의 두 자식 노드 각각의 Gini와, 규칙 2 분할 후 불순도(80개 기준)
- (4) 두 번 분할한 뒤 leaf 3개 전체(120개 기준)의 가중 평균 Gini
- (5) 규칙 2의 왼쪽·오른쪽 leaf가 예측하는 클래스(다수 클래스)

(소수 넷째 자리에서 반올림)

### Q9. [단답형]
다음 트리는 **루트가 MIN**, 둘째 층이 MAX 노드이다. 단말 값은 왼쪽부터 주어진다.

```
                    MIN
        ┌────────────┼────────────┐
       MAX          MAX          MAX
     ┌──┼──┐      ┌──┼──┐      ┌──┼──┐
     3  9  2      4 10  1      8  2  5
```

- (1) 각 MAX 노드의 값과 루트의 값, 루트가 고르는 자식은?
- (2) 왼쪽에서 오른쪽 순서로 alpha-beta pruning을 할 때 방문하지 않는 단말 값과, 잘린 시점의 $\alpha$, $\beta$를 쓰시오.
- (3) 루트의 자식을 **오른쪽 → 왼쪽 → 가운데** 순서로 방문하면(각 MAX 안의 단말은 그대로 왼쪽부터) 방문하지 않는 단말 값은? 루트 값은 바뀌는가?

### Q10. [단답형]
다음 문제는 각각 binary classification, multi-class classification, multi-label classification, regression 중 무엇인가? 그리고 출력 뉴런은 몇 개가 필요한가?

- (a) 사진 한 장에 "개", "고양이", "자동차" 태그(총 3종) 중 해당하는 것을 **모두** 붙인다.
- (b) 종양이 악성인지 아닌지 판별한다.
- (c) MNIST 손글씨 숫자를 인식한다.
- (d) 내일 최고 기온(℃)을 예측한다.

### Q11. [단답형]
강의의 백신 예시: 백신 접종률은 0.80, 접종자의 회복률은 0.95, 비접종자의 회복률은 0.85이다.

- (1) 전체 인구 중 회복하지 **못한** 사람의 비율 $P(\lnot \text{recover})$는?
- (2) 회복하지 못한 사람이 접종자일 확률은? (소수 넷째 자리에서 반올림)
- (3) 강의에서 구한 "회복한 사람이 접종자일 확률 ≈ 0.82"와 (2)를 비교하여, (2)가 접종률 0.80보다 낮은 이유를 한 문장으로 쓰시오.

### Q12. [T/F]
`np.argmax(np.array([0, 1, 1]))`의 결과는 1이다.

답: ☐ T ☐ F

### Q13. [단답형]
다음 **무방향** 그래프에서 A를 시작으로 강의의 Uniform-cost search(Dijkstra) 의사코드를 수행한다.

| 간선  | 비용 | 간선  | 비용 |
|-------|------|-------|------|
| A – B | 4    | C – D | 5    |
| A – C | 1    | C – E | 8    |
| B – C | 2    | D – E | 3    |
| B – D | 1    |       |      |

- (1) 방문(선택)되는 정점 순서를 쓰시오.
- (2) 각 정점을 선택한 직후의 `distance` 배열 [A, B, C, D, E]를 단계별로 쓰시오.
- (3) 탐색 중 `distance`가 더 작은 값으로 갱신되는 정점과, 어떤 값에서 어떤 값으로 바뀌는지 모두 쓰시오.
- (4) A에서 E까지의 최단 경로와 비용은?

### Q14. [빈칸 손코딩]
강의의 우산 HMM(전이 0.7/0.3, 관측 0.9/0.2, $P_0 = 0.5$)을 Viterbi로 푸는 코드이다. 빈칸을 채우시오.

```python
states = ['T', 'F']
trans = {'T': {'T': 0.7, 'F': 0.3},              # trans[i][j] = P(R_t=j | R_{t-1}=i)
         'F': {'T': 0.3, 'F': 0.7}}
emit = {'T': {True: 0.9, False: 0.1},            # emit[j][u] = P(U_t=u | R_t=j)
        'F': {True: 0.2, False: 0.8}}

def viterbi(observations):
    P = {'T': 0.5, 'F': 0.5}
    back = []
    for u in observations:
        new_P, ptr = {}, {}
        for j in states:
            best_i = max(states, key=lambda i: ____(a)____)
            new_P[j] = P[best_i] * trans[best_i][j] * ____(b)____
            ptr[j] = best_i
        P = new_P
        back.append(ptr)

    last = max(states, key=lambda s: ____(c)____)
    path = [last]
    for ptr in reversed(back[1:]):
        path.append(ptr[path[-1]])
    return P, ____(d)____

print(viterbi([True, True, False]))
```

- (e) 출력 결과를 쓰시오. (확률은 소수 다섯째 자리까지)
- (f) `back[1:]`에서 `back[0]`을 빼는 이유는?

### Q15. [단답형]
입력 2개 퍼셉트론에서 $w_1 = w_2 = -1$로 고정하고 bias $b$만 바꾼다. 활성 함수는 Heaviside(1 if $z \ge 0$)이다.

- (1) 이 퍼셉트론이 **NAND**가 되는 $b$의 범위는?
- (2) **NOR**가 되는 $b$의 범위는?
- (3) $b = 1$이면 어떤 게이트인가? $b = 2$이면 어떤 출력이 나오는가?

### Q16. [T/F]
Turing test는 기계 내부의 추론 과정이 사람의 사고 과정과 같은지를 직접 검사하는 테스트이다.

답: ☐ T ☐ F

### Q17. [단답형]
도난 경보 Bayesian network에서 다음 값을 사용한다.

| 확률                         | 값    | 확률                | 값   |
|------------------------------|-------|---------------------|------|
| $P(b)$                       | 0.001 | $P(j \mid a)$       | 0.90 |
| $P(e)$                       | 0.002 | $P(m \mid a)$       | 0.70 |
| $P(a \mid \lnot b, \lnot e)$ | 0.001 | $P(j \mid \lnot a)$ | 0.05 |
|                              |       | $P(m \mid \lnot a)$ | 0.01 |

- (1) 강의에서 구한 $P(j, m, a, \lnot b, \lnot e)$의 식과 값
- (2) $P(j, m, \lnot a, \lnot b, \lnot e)$의 식과 값
- (3) 도둑도 지진도 없고 John과 Mary가 모두 전화했을 때, 경보가 실제로 울렸을 확률 $P(a \mid j, m, \lnot b, \lnot e)$ (소수 넷째 자리에서 반올림)

### Q18. [객관식]
AI 역사에 대한 설명으로 **옳지 않은** 것은?

① 1952년 Arthur Samuel은 체커(Checkers) 프로그램을 만들었다.
② 1958년 John McCarthy는 AI를 위한 고급 언어 Lisp를 개발했다.
③ Herbert Simon은 1957년 "10년 안에 컴퓨터가 체스 챔피언이 된다"고 예측했지만, 실제로는 약 40년 뒤 Deep Blue가 세계 챔피언을 이겼다.
④ DENDRAL은 혈액 감염을 진단하는 전문가 시스템이고, MYCIN은 분자 구조를 추론하는 최초의 전문가 시스템이다.
⑤ Rumelhart와 McClelland의 *Parallel Distributed Processing*에서 은닉층과 sigmoid 활성 함수가 쓰였다.

- 추가 질문: Big Data의 3V를 모두 쓰시오.

### Q19. [단답형]
파라미터가 하나인 손실 함수 $L(w) = (w - 3)^2$를 gradient descent $w := w - \eta \cdot \dfrac{dL}{dw}$로 최소화한다. 시작값은 $w_0 = 0$이다.

- (1) $\eta = 0.1$일 때 $w_1$, $w_2$, $w_3$
- (2) $\eta = 1.0$일 때 $w_1$, $w_2$, $w_3$
- (3) $\eta = 1.1$일 때 $w_1$, $w_2$, $w_3$
- (4) (1)~(3)의 결과를 learning rate의 크기와 연결해 설명하시오.

### Q20. [T/F]
하나의 샘플이 하나의 클래스만 갖는 다중 클래스 분류에서, micro 평균 precision과 micro 평균 recall은 항상 서로 같고, accuracy와도 같다.

답: ☐ T ☐ F

### Q21. [단답형]
상태가 [Sunny, Cloudy, Rainy]인 Markov chain의 전이 행렬(행: 오늘, 열: 내일)이 다음과 같다.

$$P = \begin{bmatrix} 0.6 & 0.3 & 0.1 \\ 0.3 & 0.4 & 0.3 \\ 0.2 & 0.3 & 0.5 \end{bmatrix}$$

오늘은 Cloudy, 즉 $\mathbf{x}^{(0)} = [0\ \ 1\ \ 0]$이다.

- (1) $\mathbf{x}^{(1)}$, $\mathbf{x}^{(2)}$, $\mathbf{x}^{(3)}$
- (2) 내일 Rainy이고 모레도 Rainy일 확률
- (3) 전이 행렬의 각 **행**의 합이 1이어야 하는 이유

### Q22. [빈칸 손코딩]
Gini impurity와 분할 후 불순도를 구하는 함수이다. 빈칸을 채우시오.

```python
def gini(counts):                     # counts: 클래스별 샘플 수 리스트
    total = ____(a)____
    impurity = 1.0
    for c in counts:
        impurity -= ____(b)____
    return impurity

def split_gini(left, right):
    n_l, n_r = sum(left), sum(right)
    n = n_l + n_r
    return ____(c)____ * gini(left) + ____(d)____ * gini(right)

print(round(gini([10, 10, 20]), 4))                    # (e)
print(round(split_gini([10, 0, 0], [0, 10, 20]), 4))   # (f)
```

- (g) `gini([40, 0, 0])`과 `gini([20, 20])`의 값은? 클래스가 $K$개일 때 Gini가 가장 커지는 경우와 그 값은?

### Q23. [단답형]
불균형한 3클래스 데이터의 혼동 행렬이다. (행: 실제, 열: 예측)

| 실제 \ 예측 | A   | B   | C   |
|-------------|-----|-----|-----|
| A           | 90  | 5   | 5   |
| B           | 4   | 4   | 2   |
| C           | 1   | 1   | 8   |

- (1) accuracy
- (2) 클래스별 recall과 macro recall
- (3) 클래스별 precision과 macro precision
- (4) micro precision
- (5) macro와 micro 중 소수 클래스 B의 낮은 성능이 더 잘 드러나는 쪽은? 이유는?

(소수 넷째 자리에서 반올림)

### Q24. [T/F]
`DecisionTreeClassifier`의 `max_depth`를 키우면 트리가 훈련 데이터를 더 잘 맞히므로 test accuracy도 항상 올라간다.

답: ☐ T ☐ F

### Q25. [단답형]
batch 크기 2인 입력을 2층 신경망(행 벡터 방식 $\mathbf{X}\mathbf{W} + \mathbf{b}$)에 넣는다. 은닉층 활성 함수는 ReLU, 출력층은 identity이다.

$$\mathbf{X} = \begin{bmatrix} 1 & 0 \\ 2 & 1 \end{bmatrix}, \quad \mathbf{W}^{(1)} = \begin{bmatrix} 1 & -1 & 0.5 \\ -2 & 1 & 1 \end{bmatrix}, \quad \mathbf{b}^{(1)} = \begin{bmatrix} 0 & 0.5 & -1 \end{bmatrix}$$

$$\mathbf{W}^{(2)} = \begin{bmatrix} 2 \\ 1 \\ -1 \end{bmatrix}, \quad \mathbf{b}^{(2)} = \begin{bmatrix} 0.5 \end{bmatrix}, \quad \mathbf{y} = \begin{bmatrix} 3 \\ 0 \end{bmatrix}$$

- (1) $\mathbf{X}\mathbf{W}^{(1)} + \mathbf{b}^{(1)}$과 ReLU 적용 결과 (shape 포함)
- (2) 출력 $\hat{\mathbf{y}}$ (shape 포함)
- (3) 이 batch의 MSE와 MAE
- (4) 이 문제는 분류와 회귀 중 무엇에 가까운가? 출력층에 Heaviside를 쓰면 안 되는 이유는?

### Q26. [빈칸 손코딩]
BFS로 A에서 F까지의 경로를 찾는 코드이다. 빈칸을 채우시오.

```python
from collections import deque

graph = {'A': ['B', 'C'], 'B': ['F'], 'C': ['D'],
         'D': ['E'], 'E': ['F'], 'F': []}

def bfs(start, goal):
    frontier = deque([(start, [start])])
    visited = {start}
    order = []
    while frontier:
        node, path = frontier.____(a)____()
        order.append(node)
        if node == goal:
            return path, order
        for nb in graph[node]:
            if nb not in visited:
                visited.____(b)____(nb)
                frontier.____(c)____((nb, path + [nb]))
    return None, order

print(bfs('A', 'F'))
```

- (d) 출력 결과(경로와 꺼낸 순서)를 쓰시오.
- (e) (a)를 `pop`으로 바꾸면 어떤 탐색이 되며, 출력은 어떻게 바뀌는가?
- (f) 모든 간선 비용이 같을 때 (d)와 (e) 중 최적해를 보장하는 것은?

### Q27. [단답형]
강의의 잔디 Bayesian network(Rain → Sprinkler, Rain·Sprinkler → GrassWet)에서 구한 결합 확률은 다음과 같다.

| $(G, S, R)$ | $P$     |
|-------------|---------|
| (T, T, T)   | 0.00198 |
| (T, T, F)   | 0.288   |
| (T, F, T)   | 0.1584  |
| (T, F, F)   | 0.0     |

- (1) 잔디가 젖었고 스프링클러가 **켜져 있었을 때** 비가 왔을 확률 $P(R=T \mid G=T, S=T)$ (소수 넷째 자리에서 반올림)
- (2) 잔디가 젖었고 스프링클러가 **꺼져 있었을 때** 비가 왔을 확률 $P(R=T \mid G=T, S=F)$
- (3) 강의의 $P(R=T \mid G=T) \approx 0.3577$과 (1), (2)를 비교하여, 스프링클러 정보가 비에 대한 믿음을 어떻게 바꾸는지 쓰시오.

### Q28. [T/F]
강의의 hill climbing 의사코드(`if value[next] <= value[current]: return current`)에서, 가장 좋은 이웃의 값이 현재 상태의 값과 **같으면** 이동하지 않고 현재 상태를 반환한다.

답: ☐ T ☐ F

### Q29. [단답형]
KB:
- $\forall x\ [\text{Cat}(x) \to \text{Mammal}(x)]$
- $\forall x\ [\text{Mammal}(x) \to \text{Animal}(x)]$
- $\text{Cat}(Tom)$, $\lnot\text{Animal}(Jerry)$

- (1) Tom에 대해 추론되는 새 사실을 모두 쓰고, 사용한 추론 규칙을 쓰시오.
- (2) Jerry에 대해 추론되는 새 사실을 모두 쓰고, 사용한 추론 규칙을 쓰시오.
- (3) $\text{Animal}(Max)$가 KB에 추가되면 $\text{Cat}(Max)$를 추론할 수 있는가? 이유는?
- (4) 이 KB의 constant symbol과 predicate symbol을 모두 쓰시오.

### Q30. [객관식]
기계학습의 주요 과제(main challenges)와 상황의 짝으로 **옳지 않은** 것은?

① 서울 아파트 데이터만으로 학습한 모델이 시골 주택 가격을 엉뚱하게 예측한다 → 대표성 없는 훈련 데이터
② 고객 이탈 예측 모델에 의미 없는 고객 ID 번호를 feature로 넣었다 → 관련 없는 특징 (feature selection 필요)
③ 훈련 정확도는 100%인데 테스트 정확도는 60%이다 → 과소적합
④ 센서 고장으로 측정값에 잡음과 누락이 많다 → 낮은 품질의 데이터
⑤ 희귀 질환 사진 20장만으로 분류기를 학습한다 → 훈련 데이터 양 부족

### Q31. [단답형]
두 회귀 모델의 테스트 샘플 4개에 대한 오차 $\hat{y} - y$가 다음과 같다.

| 모델 | 오차 1 | 오차 2 | 오차 3 | 오차 4 |
|------|--------|--------|--------|--------|
| A    | 2      | -2     | 2      | -2     |
| B    | 0      | 0      | 0      | 6      |

- (1) 각 모델의 MAE, MSE, RMSE
- (2) MAE로 고르면 어느 모델인가? RMSE로 고르면?
- (3) 두 지표의 선택이 갈리는 이유를 한 문장으로 쓰시오.

### Q32. [빈칸 손코딩]
Naïve Bayes 점수 $p(C) \prod_i p(x_i \mid C)$를 데이터에서 직접 세어 계산하는 코드이다. 빈칸을 채우시오.

```python
data = [("Sunny",  "Weak",   "No"),
        ("Sunny",  "Strong", "No"),
        ("Rainy",  "Weak",   "Yes"),
        ("Rainy",  "Strong", "No"),
        ("Sunny",  "Weak",   "Yes"),
        ("Cloudy", "Weak",   "Yes"),
        ("Cloudy", "Strong", "Yes"),
        ("Rainy",  "Weak",   "Yes")]            # (Outlook, Wind, Play)

def nb_score(x, label):
    rows = [r for r in data if r[-1] == label]
    score = ____(a)____ / len(data)              # prior p(C)
    for i, value in enumerate(x):
        match = sum(1 for r in rows if ____(b)____)
        score *= ____(c)____                     # likelihood p(x_i | C)
    return score

x = ("Sunny", "Strong")
scores = {c: nb_score(x, c) for c in ["Yes", "No"]}
pred = max(scores, key=____(d)____)
```

- (e) `scores`의 두 값(분수와 소수)과 `pred`를 쓰시오.
- (f) `x = ("Cloudy", "Strong")`이면 두 점수는? 여기서 드러나는 문제점은?

### Q33. [T/F]
Sigmoid $\sigma(z)$의 미분값 $\sigma(z)(1 - \sigma(z))$는 $z = 0$에서 최댓값 0.25를 가진다.

답: ☐ T ☐ F

### Q34. [단답형]
강의의 계산 예제(입력 $x_0 = 0.35$, $x_1 = 0.7$, sigmoid, bias 없음, $\eta = 1.0$)에서 backpropagation 결과는 $\delta_{1,0} = 0.0055$, $\delta_{1,1} = 0.0161$이었다. 초기 가중치는 $w_{1,0,0} = 0.2$, $w_{1,0,1} = 0.3$, $w_{1,1,0} = 0.2$, $w_{1,1,1} = 0.3$이다.

- (1) $\Delta w_{l,i,j} = -\eta \cdot \delta_{l,j} \cdot o_{l-1,i}$로 갱신한 $w_{1,0,0}$, $w_{1,0,1}$, $w_{1,1,1}$ (소수 넷째 자리까지)
- (2) $\eta = 0.5$였다면 갱신한 $w_{1,0,1}$은?
- (3) $\delta_{1,j}$를 계산할 때 출력층 가중치 $w_{2,j,0}$은 갱신 **전** 값과 **후** 값 중 무엇을 써야 하는가? 이유는?
- (4) 은닉층의 $\delta$를 구하는 데 출력층의 $\delta_{2,0}$이 필요한 이유를 "backpropagation"이라는 이름과 연결해 쓰시오.

### Q35. [단답형]
- (1) `nn.Flatten()` → `nn.Linear(784, h)` → Sigmoid → `nn.Linear(h, 10)` 모델의 학습 파라미터가 총 101,770개이다. $h$는?
- (2) 입력 3 → 은닉 5 → 은닉 4 → 출력 2인 fully connected MLP의 파라미터 수는?
- (3) MNIST용 `784 → 64 → 64 → 10` MLP의 파라미터 수는?

### Q36. [T/F]
$\lnot(P \to Q) \equiv \lnot P \to \lnot Q$ 이다.

답: ☐ T ☐ F

### Q37. [단답형]
강의의 골프 데이터셋(14개, Yes 9개, No 5개)에서 각 feature 값의 개수는 다음과 같다.

| feature 값        | Yes 중 개수 | No 중 개수 |
|-------------------|-------------|------------|
| Outlook = Rainy   | 3           | 2          |
| Temperature = Hot | 2           | 2          |
| Humidity = High   | 3           | 4          |
| Windy = True      | 3           | 3          |

체크인 퀴즈의 입력 {Rainy, Hot, High, True}에 대해

- (1) $p(\text{Yes}) \prod_i p(x_i \mid \text{Yes})$ (식과 소수)
- (2) $p(\text{No}) \prod_i p(x_i \mid \text{No})$ (식과 소수)
- (3) 예측 결과와, 두 값을 정규화한 $p(\text{Yes} \mid \text{입력})$

를 구하시오. (소수 다섯째 자리에서 반올림)

### Q38. [빈칸 손코딩]
PyTorch에서 batch 출력에 softmax를 적용한다. 물음에 답하시오.

```python
import torch
import torch.nn.functional as F

logits = torch.tensor([[1., 2., 3.],
                       [1., 1., 1.]])      # batch 2개, 클래스 3개

p0 = F.softmax(logits, dim=0)
p1 = F.softmax(logits, dim=1)
pred = logits.argmax(dim=____(a)____)      # 샘플별 예측 클래스
```

($e^1 \approx 2.718$, $e^2 \approx 7.389$, $e^3 \approx 20.086$)

- (b) `p1`의 값을 쓰시오. (소수 넷째 자리까지)
- (c) `p0`의 값을 쓰시오. (소수 넷째 자리까지)
- (d) `p0`과 `p1` 중 각 **샘플**의 클래스 확률 분포는 어느 것인가? 합이 1이 되는 방향은 각각 어디인가?
- (e) (a)를 채웠을 때 `pred`의 값은?
- (f) 예측 클래스만 필요할 때 softmax를 거치지 않고 logits에 바로 argmax를 해도 되는 이유는?

### Q39. [단답형]
결정 트리의 `max_depth`를 바꿔 가며 얻은 결과이다.

| max_depth | train acc | validation acc |
|-----------|-----------|----------------|
| 1         | 0.67      | 0.65           |
| 2         | 0.95      | 0.93           |
| 3         | 0.98      | 0.95           |
| 4         | 1.00      | 0.93           |
| 5         | 1.00      | 0.90           |

- (1) 어떤 `max_depth`를 골라야 하는가? 근거가 되는 집합은?
- (2) `max_depth = 1`과 `max_depth = 5`는 각각 어떤 상태인가?
- (3) 선택 후 test set은 어떻게 쓰는가? test accuracy를 보고 `max_depth`를 다시 고르면 무엇이 문제인가?

### Q40. [T/F]
Heuristic alpha-beta tree search에서 평가 함수(EVAL)는 실제 승패와 상관관계가 높을수록 좋으므로, 계산 시간이 오래 걸리더라도 가장 정확한 함수를 쓰는 것이 바람직하다.

답: ☐ T ☐ F

### Q41. [단답형]
도시 A, B, C, D의 거리가 다음과 같다. 투어는 A에서 출발해 모든 도시를 한 번씩 방문하고 A로 돌아온다.

| 구간 | A–B | A–C | A–D | B–C | B–D | C–D |
|------|-----|-----|-----|-----|-----|-----|
| 거리 | 2   | 5   | 4   | 3   | 6   | 1   |

한 세대(generation)의 투어 4개: T1 = A-B-C-D, T2 = A-C-B-D, T3 = A-B-D-C, T4 = A-D-B-C

- (1) 각 투어의 총 거리 D를 구하고, selection으로 2개를 고르시오.
- (2) T1의 앞 2개(A-B)와 T2의 뒤 2개(B-D)를 이어 붙이는 one-point crossover를 하면 어떤 결과가 나오며, 무엇이 문제인가?
- (3) T3에서 3번째와 4번째 도시를 서로 바꾸는 mutation을 하면 결과 투어와 총 거리는?
- (4) (3)처럼 두 도시의 위치를 바꾸는 mutation은 (2)의 문제가 생기지 않는다. 이유는?

### Q42. [빈칸 손코딩]
로봇 경로(F/R/L 문자열)에 유전 알고리즘의 crossover, mutation, 적합도를 구현했다. 빈칸을 채우시오.

```python
def crossover(p1, p2, k):                 # k번째 유전자 뒤를 자르는 one-point crossover
    return p1[:k] + p2[k:], ____(a)____

def mutate(route, idx, new_gene):
    route = list(route)
    route[idx] = new_gene
    return ____(b)____                    # 다시 문자열로

def fitness(distance, collision):
    return ____(c)____                    # 강의의 적합도 점수

p1, p2 = "FRFFL", "LLFRF"
c1, c2 = crossover(p1, p2, 3)
c1 = mutate(c1, 0, "L")
print(c1, c2)                             # (d)
print(fitness(12, 0), fitness(5, 1), fitness(3, 2))   # (e)
```

- (f) (e)의 세 경로 중 selection에서 가장 먼저 고르는 경로는? 충돌 가중치가 10이 아니라 2라면?

### Q43. [단답형]
- (1) 데이터 10,000개를 `test_size=0.2`로 나눈 뒤 훈련 데이터를 `batch_size=64`로 20 epoch 학습하면 파라미터 갱신 횟수는?
- (2) 같은 훈련 데이터를 `batch_size=48`로 학습하면 1 epoch의 갱신 횟수와 마지막 batch 크기는? (남는 데이터도 하나의 batch로 학습)
- (3) Iris 150개를 `test_size=0.2`로 나누고 `batch_size=16`으로 학습하면 1 epoch의 갱신 횟수와 마지막 batch 크기는?
- (4) Full-batch 학습이면 (1)의 갱신 횟수는?

### Q44. [단답형]
어떤 질병의 유병률은 2%이다. 검사는 환자의 95%를 양성으로, 환자가 아닌 사람의 10%를 양성으로 판정한다.

- (1) 첫 검사에서 양성인 사람이 환자일 확률 (소수 넷째 자리에서 반올림)
- (2) 같은 사람이 같은 종류의 검사를 한 번 더 받아 또 양성이었다. (1)의 결과를 새 사전확률로 써서 환자일 확률을 다시 구하시오. (두 검사 결과는 질병 여부가 주어지면 조건부 독립)
- (3) (2)를 한 번에 계산하는 식을 Naïve Bayes 형태 $P(C) \prod_i P(x_i \mid C)$로 쓰고, 결과가 같은지 확인하시오.

### Q45. [T/F]
논리적 표현과 의미망(semantic network)은 명시적(explicit) 지식 표현이고, 신경망을 포함한 머신러닝 모델은 암시적(implicit) 지식 표현으로 볼 수 있다.

답: ☐ T ☐ F

### Q46. [빈칸 손코딩]
데이터 10개로 5-fold cross validation의 fold를 직접 나누는 코드이다. 빈칸을 채우시오.

```python
data = list(range(10))         # 샘플 인덱스 0~9
k = 5
fold_size = len(data) // k
scores = []

for i in range(k):
    test_idx = data[____(a)____ : ____(b)____]
    train_idx = data[:i * fold_size] + data[____(c)____:]
    acc = train_and_evaluate(train_idx, test_idx)   # 정의되어 있다고 가정
    scores.append(acc)

print(sum(scores) / ____(d)____)
```

- (e) `i = 2`일 때 `test_idx`와 `train_idx`는?
- (f) `scores = [0.9, 0.8, 0.85, 0.95, 0.9]`이면 출력값은?
- (g) 모델은 몇 번 학습되는가?
- (h) Iris처럼 데이터가 클래스 순서대로 정렬되어 있으면 이 코드에는 어떤 문제가 생기는가? 강의의 K-fold 절차 중 이 코드에서 빠진 것은?

### Q47. [단답형]
칸이 두 개(Left, Right)인 로봇 청소기 세계가 있다. 로봇은 둘 중 한 칸에 있고, 각 칸은 더럽거나(Dirty) 깨끗하다(Clean). 행동은 Left, Right, Suck이고 각 비용은 1이다.

- (1) state space의 상태 수는?
- (2) $result((\text{Left}, \text{Dirty}, \text{Dirty}), \text{Suck})$은? (순서: 로봇 위치, 왼쪽 칸, 오른쪽 칸)
- (3) goal state(두 칸 모두 깨끗함)의 개수는?
- (4) $(\text{Left}, \text{Dirty}, \text{Dirty})$에서 시작할 때의 optimal solution과 그 비용은?

### Q48. [객관식]
Bayesian network의 간선이 A → B, A → C, B → D, C → D, D → E이다. 모든 변수는 Boolean이다. 옳은 것은?

① $P(A, B, C, D, E) = P(A)\,P(B \mid A)\,P(C \mid A)\,P(D \mid B, C)\,P(E \mid D)$
② $P(E \mid A, B, C, D) = P(E \mid A)$
③ D의 CPT는 conditioning case가 2개이다.
④ 간선 E → A를 추가해도 여전히 올바른 Bayesian network이다.
⑤ 각 행에서 $P(X=T \mid \cdots)$만 저장하면 네트워크 전체에 필요한 확률값은 10개이다.

- 추가 질문: ⑤의 올바른 개수와, 같은 5개 변수의 full joint distribution에 필요한 독립 확률값 개수를 쓰시오.

### Q49. [빈칸 손코딩]
상태 0~7이 일렬로 놓인 hill climbing(비용 최소화)이다. 이웃은 바로 옆(±1) 상태이고, 이웃 중 비용이 가장 낮은 상태가 현재보다 **엄격히** 낮을 때만 이동한다. 빈칸을 채우시오.

```python
cost = [6, 4, 5, 3, 2, 7, 1, 0]

def hill_climbing(start):
    current = start
    path = [current]
    while True:
        neighbors = [n for n in (current - 1, current + 1) if ____(a)____]
        best = min(neighbors, key=lambda n: ____(b)____)
        if ____(c)____:
            return path
        current = best
        path.append(current)

print(hill_climbing(0))   # (d)
print(hill_climbing(3))   # (e)
print(hill_climbing(5))   # (f)
```

- (g) (d)~(f) 중 global optimum에 도달한 것은? 나머지는 무엇에 갇혔는가?

### Q50. [단답형]
다음 학습 코드에는 순서 오류가 있다. (`optimizer = torch.optim.SGD(model.parameters(), lr=0.01)`, momentum 없음)

```python
for epoch in range(epochs):
    model.train()
    for images, labels in train_loader:
        logits = model(images)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.zero_grad()
        optimizer.step()
```

- (1) 이 코드로 학습하면 파라미터는 어떻게 되는가? 이유는?
- (2) 올바른 순서로 고쳐 쓰시오.
- (3) 평가 단계에서 `model.eval()`과 `with torch.no_grad():`를 쓰는 목적을 각각 쓰시오.
