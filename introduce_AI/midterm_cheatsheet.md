# 중간고사 힌트노트 (A4 단면 1장, 손글씨)

> - 범위: week2 Problem Solving ~ week7 Neural Networks (week1 AI 역사는 범위 밖이라 뺌)
> - 원칙: **이미 이해한 내용은 "떠올리는 열쇠"만** 적고, **헷갈리기 쉬운 공식·방향·크기·코드 순서**는 정확히 적는다.
> - ★ = 꼭 적기, ☆ = 공간이 남으면 적기
> - 손으로 옮기기 쉽도록 수식은 LaTeX 없이 일반 기호로 적었다.

---

## 0. 종이 배치 (A4 세로, 2단)

```
┌──────────────────────┬──────────────────────┐
│ ① 탐색               │ ⑤ ML 기초·평가지표   │
│   f(n) 표, UCS, GA   │   혼동행렬, MAE/RMSE │
├──────────────────────┤   Gini, K-fold       │
│ ② 게임 탐색          ├──────────────────────┤
│   minimax, α-β 절차  │ ⑥ 신경망             │
├──────────────────────┤   shape, 활성함수    │
│ ③ 논리               │   δ 역전파 공식      │
│   동치, MP/MT        │   batch/epoch        │
├──────────────────────┼──────────────────────┤
│ ④ 확률·시간          │ ⑦ 코드 골격          │
│   Bayes, NB, BN,     │   sklearn / numpy /  │
│   Markov, Viterbi    │   PyTorch 학습 루프  │
└──────────────────────┴──────────────────────┘
```

- 왼쪽 단 = 추론·탐색(week2~5), 오른쪽 단 = ML·신경망(week5~7)
- 블록 제목은 크게, 색 펜이나 박스로 구분하면 시험장에서 바로 찾는다.
- ④와 ⑥이 계산 문제가 가장 많이 나오는 곳이라 공간을 넉넉히 준다.
- 글씨는 2~3mm 정도면 아래 내용이 다 들어간다. 모자라면 ☆부터 뺀다.

---

## ① 탐색 (week2~3)

**★ f(n) 한 줄로 4개 구분**

| 알고리즘    | f(n)         | 메모                      |
|-------------|--------------|---------------------------|
| UCS         | g            | = Dijkstra, 비용 ≥ 0 최적 |
| Greedy BFS  | h            | 빠르지만 최적 보장 X      |
| A*          | g + h        | 목표 방향으로 좁게 탐색   |
| Weighted A* | g + W·h, W>1 | 더 빠름, 최적성 희생      |

- ★ UCS: 우선순위 큐에서 **최소 비용을 꺼냄** → 이웃 비용 계산 → **더 싸면 갱신** → 목표가 **꺼내질 때** 종료
- ★ BFS는 비용 같을 때만 최적, DFS는 최적 X
- ★ Uninformed: BFS, DFS, UCS, IDS / Informed: Greedy, A*, IDA*, RBFS
- ★ Local(hill climbing): 경로 기록 X, 메모리↓·빠름, **local optimum에 갇힘** (이웃이 나보다 안 좋으면 멈춤)
- ★ Global(best-first): PQ로 경로·방문 기록, local minima 탈출 가능
- ★ GA: **Selection → Crossover → Mutation** (TSP, 로봇)

## ② 게임 탐색 (week3~4)

- ★ Minimax: 아래 → 위로 올림. **MAX 노드 = max, MIN 노드 = min**
- ★ α = MAX가 확보한 최선(큰 값), β = MIN이 확보한 최선(작은 값)
  - 시작: α = −∞, β = +∞, **부모의 α, β를 자식에게 내려보냄**
  - MAX 노드는 α 갱신, MIN 노드는 β 갱신
  - **α ≥ β 이면 나머지 자식 prune**
- ★ Heuristic α-β: Utility → **EVAL**, terminal test → **cutoff test**(깊이 제한)
  - 좋은 EVAL = 실제 승률과 상관↑ + 계산 빠름
- ★ 틱택토 EVAL = (O가 아직 완성 가능한 줄 − X가 아직 완성 가능한 줄) / 8
- ★ MCTS: 트리 확장 → **랜덤 시뮬레이션(트리에 기록 X)** → 승률 = wins / runs

## ③ 논리 (week3~4)

- ★ 추론 4갈래: 논리(사실) / BN(불확실성) / Markov(시간) / DNN(비정형 데이터)
- ★ 동치
  - P→Q ≡ ¬P∨Q ≡ ¬Q→¬P(대우)
  - P↔Q ≡ (P→Q)∧(Q→P)
  - ¬(P∧Q) ≡ ¬P∨¬Q, ¬(P∨Q) ≡ ¬P∧¬Q
- ★ Modus Ponens: P→Q, P ⟹ Q / Modus Tollens: P→Q, ¬Q ⟹ ¬P
  - 함정: P→Q, Q ⟹ P (X), P→Q, ¬P ⟹ ¬Q (X)
- ★ FOL: 상수(Harry), 술어(Person(x), BelongsTo(x,y)), ∀x
- ☆ 지식 표현: 논리·의미망 = explicit, ML/DL = implicit
- ☆ KB 에이전트: percept를 KB에 추가 → 최선의 행동 질의 → 행동했다고 KB에 알림

## ④ 확률·시간 추론 (week4~5)

- ★ P(a|b) = P(a∧b) / P(b)
- ★ **Bayes**: P(C|E) = P(E|C)·P(C) / P(E)
  - P(E) = P(E|C)P(C) + P(E|¬C)P(¬C) ← 분모 경로 빠뜨리지 않기
  - cause = 원인(질병, 스팸), effect = 관측(증상, 단어)
- ★ **Naive Bayes**: ŷ = argmax_k P(C_k)·Π P(xᵢ|C_k)
  - 원인이 주어지면 특징끼리 조건부 독립이라고 가정
  - 텍스트: 기사에 **없는** 단어는 HasWord=**False** 확률을 곱한다
- ★ **BN**: P(x₁…xₙ) = Π P(xᵢ | Parents(Xᵢ)), DAG
  - CPT: 부모 k개면 행 2ᵏ개, 각 행 합 = 1
  - 질문 확률 = (조건 맞는 경우들의 결합확률 합) / (관측과 일치하는 모든 경우의 합)
- ★ **Markov chain**: x⁽ᵗ⁺¹⁾ = x⁽ᵗ⁾·P (P의 행 = 오늘, 열 = 내일)
- ★ Transition = P(Xₜ|Xₜ₋₁) (상태 → 상태), Observation = P(Eₜ|Xₜ) (상태 → 관측)
- ★ HMM: 상태는 **이산 확률변수 하나**, 숨어 있음(우산만 보임)
- ★ **Viterbi**: Pₜ(j) = maxᵢ[ Pₜ₋₁(i)·P(j|i) ] · P(Uₜ|j)
  - 관측확률은 **max 밖에서** 한 번 곱함
  - 끝에서 max를 준 이전 상태를 거꾸로 따라가면 전체 순서

## ⑤ ML 기초·평가 (week5~6)

- ★ 지도(레이블 O: 분류/회귀) / 비지도(clustering) / 강화(보상·벌)
- ★ train = 학습, **validation = 모델 선택**, test = 최종 평가(unseen)
- ★ Overfitting: train 좋음, test 나쁨 / Underfitting: 둘 다 나쁨
- ★ 혼동행렬: **행 = 실제, 열 = 예측**

| 지표      | 식             | 기준        |
|-----------|----------------|-------------|
| Accuracy  | (TP+TN) / 전체 | 균형 데이터 |
| Recall    | TP / (TP+FN)   | 행, FN 치명 |
| Precision | TP / (TP+FP)   | 열, FP 치명 |

- ★ 다중 클래스: Macro = 클래스별 값을 평균 / Micro = TP·FP·FN을 합친 뒤 계산 (= accuracy)
- ★ MAE = Σ|ŷ−y|/m, MSE = Σ(ŷ−y)²/m, RMSE = √MSE (큰 오차에 벌점↑)
- ★ K-fold: K개로 나눠 K번 학습(K−1개로 학습, 1개로 테스트) → 평균, 시간↑
- ★ **Gini** = 1 − Σpₖ² (2클래스 최대 0.5)
  - 분할 후 = **샘플 수 가중평균** (단순 평균 X)
  - 매 단계 불순도를 가장 많이 줄이는 규칙 = **greedy**
  - max_depth↑ → 과대적합 위험
- ☆ 결정 경계: 선형/비선형, 임베딩 공간 = latent space

## ⑥ 신경망 (week6~7)

- ★ 퍼셉트론(TLU): z = xᵀw + b → step(z)
  - OR: w = (1,1), b = −0.5 / AND: b = −1.5
  - **XOR는 선형 분리 불가** → 은닉층(MLP) 필요
- ★ **행렬 크기** (입력 n, 출력 m)

| 방식   | 식      | X   | W   | b   | 결과 |
|--------|---------|-----|-----|-----|------|
| 열벡터 | φ(Wx+b) | n×1 | m×n | m×1 | m×1  |
| 행벡터 | φ(XW+b) | 1×n | n×m | 1×m | 1×m  |
| 배치 s | φ(XW+b) | s×n | n×m | 1×m | s×m  |

- ★ 파라미터 수(한 층) = n×m + m (bias 포함)
- ★ 출력 뉴런: 이진 분류 1개, 다중 분류 = 클래스 수
- ★ 활성 함수 범위: sigmoid (0,1), tanh (−1,1), ReLU [0,∞) = max(0,x), softmax (0,1)·합 1
  - Heaviside(0/1)는 회귀 불가, argmax 동점이면 **첫 인덱스**
- ★ 손실: 회귀 = MSE·MAE·RMSE·Huber / 분류 = cross-entropy (categorical = one-hot, sparse = 정수 레이블)
- ★ 학습 순서: 초기화 → forward → loss → backward(gradient) → update
  - **ΔW = −η·∂L/∂W**, W ← W + ΔW (기울기 반대 방향)
  - η 작음 → 느림, η 큼 → 발산
- ★ **δ 공식** (sigmoid, L = (y−o)²)
  - 출력: δ = 2(o − y)·o(1 − o)
  - 은닉: δⱼ = oⱼ(1 − oⱼ)·Σ (w_다음 · δ_다음)
  - **Δw = −η · δ(받는 쪽) · o(보내는 쪽)**
- ★ Epoch = 훈련 세트 전체 1번 / epoch당 업데이트 수 = N / batch size
- ★ MNIST: 28×28 = **784** 입력, **10** 출력, train 60,000 / test 10,000
- ☆ w_{l,i,j} = (l−1)층 i번 → l층 j번

## ⑦ 코드 골격 (빈칸 대비)

```python
# sklearn
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)   # 회귀는 stratify 없음
model = DecisionTreeClassifier(criterion="gini", max_depth=3)
#       DecisionTreeRegressor(criterion="squared_error", max_depth=5)
model.fit(X_train, y_train); y_pred = model.predict(X_test)

# numpy 단층
z = np.matmul(W, x) + b          # (3,2)(2,1)+(3,1) = (3,1)
y = np.where(z >= 0, 1, 0)       # Heaviside

# PyTorch 모델
self.hidden = nn.Linear(784, 128)   # nn.Linear(in, out)
nn.Flatten(), nn.Sigmoid(), nn.Softmax(dim=1)   # dim=1: (샘플, 클래스)

# PyTorch 학습 루프
for epoch in range(epochs):
    model.train()
    for images, labels in train_loader:      # shuffle=True
        logits = model(images)               # forward
        loss = criterion(logits, labels)     # loss
        optimizer.zero_grad()                # gradient 초기화
        loss.backward()                      # backprop
        optimizer.step()                     # update
# 평가
model.eval()
with torch.no_grad():
    pred = logits.argmax(dim=1)
```

---

## 적지 않아도 되는 것 (이미 이해한 개념이라 키워드만 보면 떠오름)

- week1 AI 역사, Turing test, Weak/Strong AI (범위 밖)
- 강의 예제 숫자 전체(Iris 결정 트리 규칙, 루마니아 지도 등): 시험에서는 숫자가 바뀌어 나온다
- 특징·레이블, 원-핫 같은 용어 정의: ⑤의 키워드로 충분하다

## 마지막 점검

- 시험 전 공지대로 **A4 단면, 손글씨**인지 확인한다 (인쇄·복사본은 불허될 수 있음).
- 계산기를 챙긴다 (공학용은 필요 없음).
