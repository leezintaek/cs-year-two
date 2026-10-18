# 중간고사 힌트노트 — 코드 중심판 (A4 단면 1장, 손글씨)

> - `midterm_cheatsheet.md`(개념판)의 코드 중심 버전. 개념은 맨 위 띠에 **공식만** 압축하고, 나머지 공간은 **빈칸 손코딩 대비 코드**로 채운다.
> - 시험 코드 문제는 Python만 나오고, 사소한 문법 오류는 허용된다. 그래서 import나 print는 빼고 **빈칸으로 뚫릴 만한 줄**만 남겼다.
> - ★ = 강의 슬라이드에 실제로 나온 코드(출제 1순위), ☆ = 강의 pseudocode를 Python으로 옮긴 것(공간이 남으면)
> - ☆ 코드는 전부 직접 실행해서 결과를 확인했다.

---

## 0. 종이 배치 (A4 세로)

```
┌─────────────────────────────────────────────┐
│ ⓪ 공식 띠 (2~3줄): f(n), Bayes, Viterbi,    │
│    Gini, 지표, shape, δ                      │
├──────────────────────┬──────────────────────┤
│ ① sklearn            │ ④ nn.Module          │
│   split, DT, 지표    │   MLP / MNIST 모델   │
├──────────────────────┼──────────────────────┤
│ ② numpy 퍼셉트론/MLP │ ⑤ 학습·평가 루프     │
│ ③ 활성 함수          │   1개씩 vs batch     │
├──────────────────────┴──────────────────────┤
│ ⑥ 알고리즘 코드: minimax/α-β, UCS·A*,       │
│    Gini, precision/recall, Markov           │
├─────────────────────────────────────────────┤
│ ⑦ 코드 함정 체크리스트                       │
└─────────────────────────────────────────────┘
```

- 위쪽 ①~⑤는 강의 코드(★), 아래쪽 ⑥은 알고리즘(☆)이다. 공간이 모자라면 ⑥부터 줄인다.
- 코드는 줄바꿈을 아끼려고 `;`로 이어 써도 된다.

---

## ⓪ 공식 띠 (개념은 이것만)

```
탐색  UCS=g | Greedy=h | A*=g+h | WA*=g+W·h(W>1)   α-β: α=MAX최선 β=MIN최선, α≥β → prune
논리  P→Q ≡ ¬P∨Q ≡ ¬Q→¬P | MP: P→Q,P⊢Q | MT: P→Q,¬Q⊢¬P | ¬(P∧Q) ≡ ¬P∨¬Q
확률  P(C|E)=P(E|C)P(C)/P(E), P(E)=P(E|C)P(C)+P(E|¬C)P(¬C) | NB: argmax P(C)ΠP(xᵢ|C)
      BN: ΠP(xᵢ|Parents) | Markov: x(t+1)=x(t)·P | Viterbi: Pₜ(j)=maxᵢ[Pₜ₋₁(i)P(j|i)]·P(Uₜ|j)
ML    Gini=1−Σp² (가중평균) | Recall=TP/(TP+FN) 행 | Precision=TP/(TP+FP) 열 | RMSE=√(Σe²/m)
NN    Wx+b: W m×n | XW+b: W n×m, batch s×n→s×m | 파라미터=n·m+m
      δ출력=2(o−y)o(1−o), δ은닉=o(1−o)Σwδ, Δw=−η·δ·o(앞) | epoch당 update = N/batch
```

---

## ① sklearn — Decision Tree (★ week5)

```python
X = df[["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]]
y = df["Species"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)   # 회귀: stratify 없음
# Iris 150 → train 120 / test 30 (클래스별 10)

model = DecisionTreeClassifier(criterion="gini", max_depth=3, random_state=42)
# 회귀: DecisionTreeRegressor(criterion="squared_error", max_depth=5)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# accuracy / error rate
correct = 0
for actual, predicted in zip(y_test, y_pred):
    if actual == predicted: correct += 1
accuracy = correct / len(y_test)
error_rate = (len(y_test) - correct) / len(y_test)

# MAE / RMSE
total_error += abs(actual - predicted);          mae  = total_error / len(y_test)
total_squared_error += (actual - predicted)**2.0; rmse = (total_squared_error / len(y_test)) ** 0.5

# 시각화
plot_tree(model, feature_names=X.columns, class_names=model.classes_, filled=True, rounded=True)
export_text(model, feature_names=list(X.columns))
```

## ② NumPy 퍼셉트론 / MLP (★ week6~7)

```python
x = np.array([[0.2], [1.4]])               # (2,1)  열벡터
W = np.array([[-0.8, -1.2],                # (3,2)  = (출력, 입력)
              [ 0.1, -0.05],
              [ 0.7,  1.3]])
b = np.array([[-0.4], [-0.01], [0.4]])     # (3,1)
z = np.matmul(W, x) + b                    # (3,2)(2,1)+(3,1) = (3,1)
y = np.where(z >= 0, 1, 0)                 # Heaviside → [0,0,1]

# MLP: 은닉 출력이 다음 층 입력
hidden_y = np.where(np.matmul(hidden_W, x) + hidden_b >= 0, 1, 0)        # (4,2)(2,1)→(4,1)
output_y = np.where(np.matmul(output_W, hidden_y) + output_b >= 0, 1, 0) # (3,4)(4,1)→(3,1)
np.argmax(output_y, axis=0)                # 동점이면 첫 인덱스
```

## ③ 활성 함수 (★ week7)

```python
F.relu(x)             # max(0, x)
torch.sigmoid(x)      # 1 / (1 + exp(-x))
F.softmax(x, dim=0)   # exp(x) / sum(exp(x))   ← 열벡터(3,1)라 dim=0
nn.ReLU(), nn.Sigmoid(), nn.Softmax(dim=1)     # 모델 안: (샘플, 클래스)라 dim=1
```

## ④ nn.Module (★ week7)

```python
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden_layer = nn.Linear(2, 4)    # nn.Linear(in, out)
        self.output_layer = nn.Linear(4, 3)
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=1)
    def forward(self, x):
        hidden_o = self.sigmoid(self.hidden_layer(x))
        output_z = self.output_layer(hidden_o)
        return output_z                        # logits (softmax 전)

x = torch.tensor([[0.2, 1.4]])                 # (1,2) = (샘플, feature)
pred = model(x).argmax(dim=1).item()

# MNIST: 28×28 → Flatten → 784 → 128 → 10
self.flatten = nn.Flatten()
self.hidden_layer = nn.Linear(784, 128); self.output_layer = nn.Linear(128, 10)
model = our_first_nn().to(device)
```

## ⑤ 학습·평가 루프 (★ week7, 출제 1순위)

```python
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader  = DataLoader(test_dataset,  batch_size=32, shuffle=False)

for epoch in range(epochs):
    model.train()
    for images, labels in train_loader:
        logits = model(images)                  # 1. forward
        loss = criterion(logits, labels)        # 2. loss
        optimizer.zero_grad()                   # 3. gradient 초기화
        loss.backward()                         # 4. backprop
        optimizer.step()                        # 5. update
        total_loss += loss.item() * labels.size(0)   # batch 평균 → 합계
        correct += (logits.argmax(dim=1) == labels).sum().item()
        total += labels.size(0)

model.eval()
with torch.no_grad():                           # backward/step 없음
    for images, labels in test_loader:
        probabilities = model.softmax(model(images))
        predictions = probabilities.argmax(dim=1)
        correct += (predictions == labels).sum().item(); total += labels.size(0)

# 1개씩 학습 버전에서 다른 줄
indices = torch.randperm(len(train_dataset))    # shuffle 대신
image = image.unsqueeze(0).to(device)           # batch 차원 추가 (1,28,28)→(1,1,28,28)
label = torch.tensor([label], device=device)
total_loss += loss.item(); total += 1
```

## ⑥ 알고리즘 코드 (☆ 강의 pseudocode → Python)

```python
# Minimax (BOT=MAX, PLAYER=MIN)
def minimax(board, turn):
    if is_terminal(board):                              # BOT승 +1 / PLAYER승 -1 / 무 0
        return 1 if winner(board) == 'BOT' else (-1 if winner(board) == 'PLAYER' else 0)
    best = -inf if turn == 'BOT' else inf
    for p in empty_positions(board):
        board[p] = turn
        score = minimax(board, 'PLAYER' if turn == 'BOT' else 'BOT')
        board[p] = ' '                                  # 되돌리기
        best = max(best, score) if turn == 'BOT' else min(best, score)
    return best

# Alpha-beta
def alphabeta(node, alpha, beta, is_max):
    if isinstance(node, int): return node
    v = -math.inf if is_max else math.inf
    for child in node:
        if is_max: v = max(v, alphabeta(child, alpha, beta, False)); alpha = max(alpha, v)
        else:      v = min(v, alphabeta(child, alpha, beta, True));  beta  = min(beta, v)
        if alpha >= beta: break
    return v
alphabeta([[3,12],[2,8],[14,1]], -math.inf, math.inf, True)   # → 3

# UCS (heapq)  — A*: 우선순위를 g+w+h[nb]로
pq = [(0, start, [start])]; visited = set()
while pq:
    g, node, path = heapq.heappop(pq)
    if node in visited: continue
    visited.add(node)
    if node == goal: return g, path                     # 꺼낼 때 종료
    for nb, w in graph[node]:
        if nb not in visited: heapq.heappush(pq, (g + w, nb, path + [nb]))

# Hill climbing
while True:
    nxt = max(neighbors(cur), key=value)
    if value(nxt) <= value(cur): return cur             # 더 나은 이웃 없음 → 멈춤
    cur = nxt

# Gini
def gini(c): n = sum(c); return 1 - sum((k / n) ** 2 for k in c)
def split_gini(groups):
    N = sum(sum(g) for g in groups)
    return sum(sum(g) / N * gini(g) for g in groups)    # (13,0),(7,20) → 0.2593

# Confusion matrix (1 = Positive)
if a == 1 and p == 1: tp += 1
elif a == 0 and p == 1: fp += 1
elif a == 1 and p == 0: fn += 1
else: tn += 1
precision = tp / (tp + fp); recall = tp / (tp + fn); accuracy = (tp + tn) / len(y_true)

# Markov chain (행 = 오늘)
x = [sum(x[i] * P[i][j] for i in range(n)) for j in range(n)]   # [1,0]→[.9,.1]→[.86,.14]
```

## ⑦ 코드 함정 체크리스트

| 함정                   | 정답                                     |
|------------------------|------------------------------------------|
| 학습 3줄 순서          | zero_grad → backward → step              |
| softmax dim            | 모델(샘플, 클래스) = 1 / 열벡터 = 0      |
| forward 반환값         | logits (CrossEntropyLoss가 softmax 포함) |
| 평가 모드              | eval() + no_grad(), backward·step 없음   |
| shuffle                | train True / test False                  |
| loss 누적              | loss.item() × labels.size(0)             |
| stratify               | 분류만, 회귀는 없음                      |
| criterion              | 분류 "gini" / 회귀 "squared_error"       |
| np.matmul(W, x)        | W(m×n) · x(n×1), 순서 바꾸면 에러        |
| argmax 동점            | 첫 번째 인덱스                           |
| unsqueeze(0)           | 샘플 1개일 때 batch 차원 추가            |
| nn.Linear(in, out)     | 내부 weight는 (out, in)                  |
| minimax `board[p]=' '` | 없으면 다음 탐색에 이전 수가 남음        |
| UCS 종료 시점          | push할 때가 아니라 pop할 때              |
