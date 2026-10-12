# 인공지능개론 전체 흐름 정리 (1~6주차)

> 주차별 자세한 내용은 각 `weekN/lecture_summary.md` 참고.
> 이 파일은 **전체 흐름**과 **큰 덩어리별 공부 방법**만 정리한다. (7주차 이후 내용이 나오면 이어서 추가)

---

## 0. 한 줄 흐름

**AI란 무엇인가 → 문제를 "탐색"으로 푼다 → 지식을 표현하고 "추론"한다 (논리 → 확률 → 시간) → 규칙을 직접 쓰는 대신 데이터로 "학습"한다 (ML) → 그 학습 모델로 "신경망"을 쓴다**

핵심 질문이 이렇게 바뀌어 간다.
1. 목표까지 **어떻게 찾아갈까?** (탐색)
2. 아는 것으로 **무엇을 결론 낼까?** (추론)
3. 규칙을 모를 때 **데이터에서 어떻게 배울까?** (학습)

---

## 1. 주차별 흐름 (간단히)

| 주차 | 주제 | 핵심 키워드 |
|---|---|---|
| 1 | AI 소개 | AI ⊃ ML ⊃ DL, Turing Test, Weak/Strong AI, AI 역사(AI 겨울: XOR 문제) |
| 2 | 문제해결 (1) | 탐색 문제 정의, BFS/DFS, Uniform-Cost(=Dijkstra), Greedy Best-First, A*, Weighted A*, Hill Climbing, Genetic Algorithm |
| 3 | 문제해결 (2) + 지식과 추론 시작 | Local vs Global search, 적대적 탐색: Minimax, Alpha-Beta Pruning, Heuristic Alpha-Beta, MCTS / 지식 기반 에이전트 |
| 4 | 지식과 추론 | 추론 4갈래, 논리(동치·추론 규칙·1차 논리), 베이즈 규칙, Naive Bayes, Bayesian Network, Markov Chain |
| 5 | 추론 마무리 + ML 기초 | HMM, Viterbi / 지도·비지도·강화학습, 분류 vs 회귀, 과대·과소적합, train/val/test, Iris, MAE·MSE·RMSE, Decision Tree |
| 6 | ML 평가 + 신경망 (1) | Feature/Label, 결정 경계, 임베딩 공간, Confusion Matrix, Accuracy·Recall·Precision(Macro/Micro), K-Fold / 퍼셉트론, 활성 함수, Bias, 단층·다층 퍼셉트론, Backpropagation |

---

## 2. 큰 덩어리 5개로 나눠 공부하기

### 덩어리 A. AI 개관 (1주차) — 가볍게
- **외울 것**: AI ⊃ ML ⊃ DL 관계, Turing Test의 의미, Weak vs Strong AI(John Searle), AGI
- **역사 흐름**: 다트머스 회의(1956) → **Perceptrons(1969)가 XOR을 못 푼다고 증명 → AI 겨울** → 역전파 재발견으로 신경망 부활 → Big Data(3V) → Deep Learning(AlexNet, Transformer, GPT …)
- **연결고리**: "XOR은 선형 분리 불가능" → **6주차 MLP(은닉층)**에서 해결. 시험에서 1주차와 6주차를 엮어 물을 수 있다.

### 덩어리 B. 탐색 (2~3주차) — 알고리즘 비교와 손으로 따라가기
세 갈래로 묶어서 외운다.

| 갈래 | 알고리즘 | 한 줄 핵심 |
|---|---|---|
| **비정보 탐색** | BFS, DFS, Uniform-Cost | 목표까지의 거리 정보 없음. UCS는 f(n)=g(n), 최소 비용 보장 |
| **정보 탐색** | Greedy Best-First, A*, Weighted A* | 휴리스틱 h(n) 사용. f(n)=h(n) / g(n)+h(n) / g(n)+W·h(n) |
| **지역 탐색** | Hill Climbing, Genetic Algorithm | 경로를 기억하지 않음 → 메모리 적음, local optimum 위험 |
| **적대적 탐색** | Minimax, Alpha-Beta, Heuristic Alpha-Beta, MCTS | MAX/MIN 번갈아, 불필요한 가지 쳐내기, 평가 함수·시뮬레이션으로 근사 |

- **꼭 연습할 것**
  - f(n) 공식 4개 구분 (UCS / Greedy / A* / Weighted A*)
  - 그래프에서 UCS·A*로 노드 방문 순서 따라가기
  - Minimax 트리 값 위로 올리기, Alpha-Beta에서 **어디가 잘리는지** (α ≥ β)
  - GA 3단계: Selection → Crossover → Mutation
  - Local vs Global 비교표
- **손코딩 후보**: Minimax (과제 1 틱택토 코드와 연결)

### 덩어리 C. 지식과 추론 (3~5주차) — 계산 문제가 가장 많은 구간
**추론 4갈래**를 뼈대로 잡고 하나씩 채운다.

| 갈래 | 다루는 것 | 핵심 도구 |
|---|---|---|
| 논리 | 참/거짓 사실과 규칙 | 연산자, 논리적 동치, Modus Ponens/Tollens, 1차 논리 |
| 베이지안 네트워크 | 불확실성 | 베이즈 규칙, Naive Bayes, DAG + CPT |
| 마르코프 모델 | 시간에 따른 변화 | Markov Chain, HMM, Viterbi |
| 심층 신경망 | 이미지·소리 같은 비정형 데이터 | → 덩어리 E로 이어짐 |

- **꼭 연습할 것 (계산형)**
  - 논리: 동치 변환(함의 제거, 드모르간), 추론 규칙으로 결론 끌어내기
  - 베이즈 규칙: 수막염, 백신(전체 확률 공식) 예제
  - Naive Bayes: 골프 예제 — 클래스별로 p(C)·Πp(xᵢ|C) 계산 후 큰 쪽 선택
  - Bayesian Network: 도난-지진-경보 결합 확률, 잔디-비-스프링클러 P(R|G) 계산
  - Markov Chain: 전이 행렬로 x⁽ᵗ⁾ = x⁽ᵗ⁻¹⁾P 계산
  - Viterbi: 표 채우기 + backtracking으로 최적 순서 찾기
- **연결고리**: 지식 표현은 논리·의미망 같은 **명시적(explicit)** 표현과 ML/DL 같은 **암시적(implicit)** 표현으로 나뉜다 → 그래서 ML로 넘어간다. Naive Bayes는 그 자체로 **분류기**이기도 하다.

### 덩어리 D. 기계학습 기초와 평가 (5~6주차) — 개념 + 지표 계산
- **개념 흐름**: 왜 ML이 필요한가 → 학습 종류(지도/비지도/강화) → 지도학습(분류 vs 회귀) → 데이터(Feature/Label, X/y, train/val/test) → 모델(Decision Tree) → 평가(지표, Cross Validation)
- **꼭 외울 것**
  - 과대적합 vs 과소적합, train / validation / test 역할 차이
  - Feature space, Decision boundary(선형/비선형), Embedding(=Latent) space
  - 이진 / 다중 클래스 / 다중 레이블 분류, one-hot encoding
  - 결정 트리: 불순도(Gini)가 낮아지게 greedy하게 분할
  - K-Fold: K번 학습해서 평균, 대신 시간이 K배
- **꼭 연습할 것 (계산형)**
  - 회귀: MAE, MSE, RMSE
  - 분류: 혼동 행렬 그리기 → Accuracy, **Recall(행 기준)**, **Precision(열 기준)**
  - 다중 클래스: Macro(클래스별로 구해서 평균) vs Micro(TP·FP·FN을 합쳐서 계산)
  - 코로나 check-in quiz 같은 문장형 문제 → 혼동 행렬로 바꾸기
- **손코딩 후보**: `model = DecisionTreeClassifier(...)`, `model.fit(X_train, y_train)`, `model.predict(X_test)`

### 덩어리 E. 신경망 (6~7주차) — 식과 행렬 크기
- **흐름**: 생물학적 뉴런 → ANN → 퍼셉트론(TLU) → 활성 함수 → Bias → 단층 퍼셉트론(여러 출력) → MLP(은닉층) → 학습(순전파·손실·역전파·가중치 갱신)
- **꼭 외울 것**
  - z = xᵀw + b, h = φ(z)
  - 활성 함수 6개: 식과 출력 범위 (Identity, Step, Sigmoid, tanh, ReLU, Softmax)
  - 퍼셉트론 vs 뉴런, MLP vs 신경망 차이
  - 출력 뉴런 개수: 이진 분류는 1개, 다중 클래스는 클래스 수만큼
  - 학습 절차: 초기화 → (출력 계산 → 손실 계산 → 파라미터 갱신) 반복
  - **ΔW = −η·∂L/∂W, W(t) = W(t−1) + ΔW**
- **꼭 연습할 것**
  - 주어진 w, b로 AND/OR 게이트 진리표 계산하기
  - **행렬 크기 맞추기**: φ(WX+b)는 W가 m×n, φ(XW+b)는 W가 n×m
  - NumPy 단층 퍼셉트론 코드로 z, h 손계산
- **손코딩 후보**: `np.matmul(W, x) + b`, `np.where(z >= 0, 1, 0)`

---

## 3. 덩어리 간 연결 지도

```
[A. AI 개관] ── XOR/AI 겨울 ──────────────────────────────┐
     │                                                     ▼
[B. 탐색] ── 휴리스틱·평가 함수 ──▶ "좋은 함수를 사람이 직접 만들기 어렵다"
     │                                                     │
[C. 추론] ── 명시적 지식(논리/확률) ──▶ 암시적 지식 ──▶ [D. ML] ──▶ [E. 신경망]
              Naive Bayes = 확률 기반 분류기 ──────────────▲     (MLP로 XOR 해결)
```

- **탐색 → ML**: 탐색에서는 휴리스틱과 평가 함수를 **사람이 설계**했다. ML에서는 그 함수를 **데이터로 학습**한다.
- **추론 → ML**: Naive Bayes, 베이지안 네트워크도 분류·예측 모델이다. "명시적 규칙이냐, 데이터로 학습한 암시적 표현이냐"의 차이.
- **ML → 신경망**: 결정 트리 같은 여러 ML 모델 중 이 수업은 신경망만 깊게 다룬다. 평가 지표(덩어리 D)는 신경망에도 그대로 쓰인다.

---

## 4. 추천 공부 순서 (중간고사: 10/20, 범위 2~7주차)

1. **뼈대 먼저**: 이 파일의 표 4개(탐색 갈래, 추론 4갈래, 학습 종류, 신경망 흐름)를 백지에 다시 그려 본다.
2. **계산 문제 반복**: 점수 비중이 큰 쪽부터 — Bayes/Naive Bayes/BN → Viterbi → 혼동 행렬 지표 → MAE/RMSE → A*/Minimax/Alpha-Beta → 퍼셉트론 계산
3. **비교형 개념 정리** (T/F·객관식 대비): Local vs Global, Weak vs Strong AI, 과대 vs 과소적합, Recall vs Precision, Macro vs Micro, 퍼셉트론 vs 뉴런, MLP vs NN, Feature vs Embedding space
4. **손코딩 대비** (Python만): Minimax 함수, sklearn `fit/predict` 흐름, NumPy 퍼셉트론
5. **힌트노트(A4 단면 수기)**: 공식 위주로 채운다 — f(n) 4종, 베이즈 규칙 2형태, BN 결합 확률식, Viterbi 점화식, 지표 공식, 활성 함수 식, 가중치 갱신식
