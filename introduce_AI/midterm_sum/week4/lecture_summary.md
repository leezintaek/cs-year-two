# Week4 강의 요약

**과목**: 인공지능개론(CSE2302) · **주제**: 지식과 추론 (Knowledge and Reasoning) 2, 3부
**강의일**: 2026-09-22(Lecture 01), 2026-09-24(Lecture 02, 추석 연휴로 동영상 대체)

---

## 1부: 게임 탐색 기법 복습 (Lecture 01 앞부분)

이전 주차(문제해결)에서 다룬 게임 탐색 기법들을 정리하며 시작한다.

- **미니맥스(Minimax)**: MAX 노드는 값이 최대가 되는 상태로, MIN 노드는 값이 최소가 되는 상태로 이동하는 것을 선호하는 탐색 방식.
- **알파-베타 가지치기(Alpha-Beta Pruning)**: 미니맥스 탐색에서 불필요한 하위 트리를 탐색하지 않도록 가지치기하는 기법.
  - **알파(α)**: MAX 입장에서 지금까지 확보한 최선(최댓값)의 선택지 값.
  - **베타(β)**: MIN 입장에서 지금까지 확보한 최선(최솟값)의 선택지 값.
  - α ≥ β 조건이 되면 더 이상 그 하위 트리를 탐색할 필요가 없어 가지치기한다.
- **한계**: 그래도 탐색해야 할 상태(state)의 수가 여전히 너무 많다는 문제가 남는다.
- **경험적 알파-베타 트리 탐색 (Heuristic Alpha-Beta Tree Search)**:
  - 특정 깊이(depth)까지만 탐색하고 멈추는 방식(cutting off search).
  - 이때 남은 상태의 가치를 추정하기 위한 **평가 함수(evaluation function)**가 필요하다.
    - 좋은 평가 함수는 실제 승패와 강하게 연관되어야 하고(정확도), 계산이 빨라야 한다(속도).
  - 문제는 좋은 평가 함수를 정의하는 것 자체가 어렵다는 점이다.
- **몬테카를로 트리 탐색 (Monte Carlo Tree Search)**: 리프 노드가 게임의 끝(terminal)이 아니면 자식 노드를 추가해 트리를 확장하고, 게임이 끝날 때까지 무작위로 수를 두어(트리에는 기록하지 않음) 결과를 시뮬레이션하는 방식.
- **탐색 기법 총정리표**:
  - 정보 기반/비정보 기반 탐색: DFS/BFS, 균일 비용 탐색(Uniform cost search), 그리디 최우선 탐색(Greedy best-first search), (가중) A* 탐색
  - 적대적 탐색(Adversarial search): 미니맥스, 알파-베타 가지치기가 적용된 미니맥스, 경험적 알파-베타 트리 탐색, 몬테카를로 트리 탐색
  - 지역/전역 탐색: 등산 알고리즘(Hill climbing), 유전 알고리즘(Genetic algorithm)

---

## 2부: 지식 기반 AI 에이전트

### 지식 기반 에이전트란
"AI에서 지식 기반 에이전트는 지식을 내부적으로 표현하고, 그 위에서 추론(reasoning)하는 과정을 통해 어떤 행동을 할지 결정한다."

동작 순서:
1. 지각(percept)을 받는다.
2. 에이전트가 그 지각을 지식 베이스(knowledge base)에 추가한다.
3. 에이전트가 지식 베이스에 최선의 행동을 물어본다(추론).
4. 에이전트가 지식 베이스에게 실제로 그 행동을 취했다고 알려준다.

### 핵심 용어 정리
- **지식(Knowledge)**: AI 시스템이 가지고 있는 정보.
- **지식 표현(Knowledge representation)**: 지식을 구조화된 형태로 모델링하는 것.
- **지식 베이스(Knowledge base)**: 구조화된 정보들의 집합.
- **추론(Reasoning)**: 주어진 정보를 바탕으로 결론을 이끌어내고, 새로운 사실을 유추하며, 문제를 해결하는 과정.
- **추론 메커니즘(Inference)**: 지식 베이스로부터 새로운 사실을 도출해내는 구체적인 방법.

**예시**: "모든 인간은 죽는다"와 "소크라테스는 인간이다" → "소크라테스는 죽는다"
- 지식: 두 명제 자체
- 지식 표현: ∀x(모든) Human(x) → Mortal(x), Human(Socrates) (술어 논리 형태)
- 지식 베이스: 위 두 식의 집합
- 추론: Mortal(Socrates)라는 새로운 사실을 이끌어냄

### 추론 기법의 4가지 큰 갈래
같은 주차 전체를 관통하는 핵심 뼈대로, 이후 강의들이 이 네 가지를 하나씩 다룬다.

| 기법 | 용도 | 예시 |
|---|---|---|
| **논리(Logics)** | 사실이나 규칙에 대해 추론 | "모든 인간은 죽는다" → 소크라테스는 죽는다 |
| **베이지안 네트워크(Bayesian networks)** | 불확실성(uncertainty)을 가지고 추론 | 비(Rain), 스프링클러(Sprinkler) → 젖은 잔디(Wet Grass) |
| **마르코프 모델(Markov models)** | 시간에 따른 변화를 추론 | 맑음 → 흐림 → 비 |
| **심층 신경망(Deep neural networks)** | 이미지, 소리 등 비정형 데이터에 대해 추론 | 이미지 분류 |

**적용 예시 1 (병원 스마트 경보 시스템)**: 환자 침대에 환자가 있고 응급 상황이면 경보(논리) / 특정 생체 신호일 때 응급 상황일 확률 87%(베이지안 네트워크) / 정상이던 생체 신호가 위험 상태로 변화(마르코프 모델) / 침대에 있는 환자의 이미지(심층 신경망).

**적용 예시 2 (자율주행차)**: 신호가 빨간불이면 정지(논리) / 보행자가 인도 근처에 있을 때 길을 건널 확률 73%(베이지안 네트워크) / 서 있던 보행자가 걷기 시작하다가 길을 건넘(마르코프 모델) / 빨간불과 보행자가 있는 이미지(심층 신경망).

---

## 3부: 논리(Logics)

### 논리 연산자 (Logical Connectives)
| 기호 | 의미 |
|---|---|
| ¬ | not (부정) |
| ∧ | and (논리곱) |
| ∨ | or (논리합) |
| → | implication (함의) |
| ↔ | biconditional (쌍조건) |

**예시**: P="화요일이다", Q="비가 온다", R="해리가 달리기를 한다"
- 지식: "화요일이고 비가 오지 않으면, 해리는 달리기를 한다" / "화요일이다" / "비가 오지 않는다"
- 지식 베이스: (P ∧ ¬Q) → R, P, ¬Q
- 추론: R (해리는 달리기를 한다)

### 논리적 동치 (Logical Equivalences)
같은 의미를 다른 형태로 표현할 수 있는 규칙들이다.
- **교환 법칙(Commutativity)**: P∧Q ≡ Q∧P, P∨Q ≡ Q∨P
- **결합 법칙(Associativity)**: (P∧Q)∧R ≡ P∧(Q∧R)
- **분배 법칙(Distributivity)**: P∧(Q∨R) ≡ (P∧Q)∨(P∧R)
- **이중 부정 제거(Double-Negation Elimination)**: ¬(¬P) ≡ P
- **대우(Contraposition)**: P→Q ≡ ¬Q→¬P
- **함의 제거(Implication Elimination)**: P→Q ≡ ¬P∨Q
- **쌍조건 제거(Biconditional Elimination)**: P↔Q ≡ (P→Q)∧(Q→P)
- **드모르간의 법칙(De Morgan's Law)**: ¬(P∧Q) ≡ ¬P∨¬Q, ¬(P∨Q) ≡ ¬P∧¬Q

### 추론 규칙 (Inference Rules)
- **논리곱 제거(And Elimination)**: P∧Q → P (둘 다 참이면 그중 하나만도 참)
- **긍정 논법(Modus Ponens)**: P→Q, P ⟹ Q ("비가 오면 해리는 안에 있다", "비가 온다" ⟹ "해리는 안에 있다")
- **부정 논법(Modus Tollens)**: P→Q, ¬Q ⟹ ¬P ("비가 오면 해리는 안에 있다", "해리는 안에 없다" ⟹ "비가 오지 않는다")

이 규칙들을 조합하면 앞선 "화요일-비-달리기" 예시를 함의 제거와 드모르간의 법칙으로 재구성해 R을 유도할 수 있음을 보여준다.

### 1차 논리 (First-Order Logic)
명제 논리보다 더 표현력이 풍부한 논리로, 대상과 그들 사이의 관계를 다룰 수 있다.
- **상수 기호(Constant symbols)**: 객체를 나타냄 (예: Harry, Gryffindor)
- **술어 기호(Predicate symbols)**: 관계를 나타냄 (예: Person, House, BelongsTo)
  - Person(Hermione): "Hermione는 사람이다"
  - House(Gryffindor): "Gryffindor는 기숙사이다"
  - BelongsTo(Malfoy, Slytherin): "Malfoy는 Slytherin에 속한다"

**응용 예시**:
- 스마트 경보 시스템: ∀p∀n [Emergency(p) ∧ AssignedTo(p,n) → Alert(n)], Emergency(PatientAlice), AssignedTo(PatientAlice, NurseBob) ⟹ Alert(NurseBob)
- 이미지 분류: ∀x [TriangularEars(x) ∧ FourLegs(x) ∧ Fur(x) → Cat(x)] 형태로 규칙을 세우고, 이미지의 특징(귀 모양, 다리 수, 털)을 관찰해 고양이인지 추론.

---

## 4부: 확률적 추론(Probabilistic Reasoning)과 베이즈 규칙

### 논리 vs 확률적 추론
- **논리**: 참/거짓(True/False)만 표현. 예: P(Mortal(Socrates)|KnowledgeBase) = 1.0 (이진 진리값, 0 또는 1).
- **확률적 추론**: [0, 1] 사이의 값으로 불확실성을 반영.

### 조건부 확률(Conditional Probability)
- **무조건부 확률(Unconditional probability)**: 추가 정보 없이 어떤 명제를 믿는 정도. (예: 주사위 두 개를 던져 합이 11이 나올 확률)
- **조건부 확률(Conditional probability)**: 어떤 정보가 주어졌을 때 명제를 믿는 정도. (예: 첫 번째 주사위가 5일 때 두 주사위가 같은 숫자(더블)가 나올 확률)
- 공식: P(a|b) = P(a∧b) / P(b)
- **곱 규칙(Product Rule)**: P(a∧b) = P(a|b)P(b) = P(b|a)P(a)

### 베이즈 규칙(Bayes' Rule)
곱 규칙 두 형태를 정리하면 다음이 유도된다.

**P(Y|X) = P(X|Y)P(Y) / P(X)**

실무에서는 주로 "결과(effect)를 관찰했을 때 원인(cause)일 확률"을 구하는 데 쓰인다.

- P(cause|effect) = P(effect|cause)P(cause) / P(effect)
- 예: 증상(symptoms)을 보이는 환자가 특정 질병(disease)일 확률
  - P(disease|symptoms) = P(symptoms|disease)P(disease) / P(symptoms)
- 예: 특정 단어("Casino")가 등장했을 때 스팸일 확률도 같은 형태로 계산 가능.

**수치 예시 (수막염 진단)**:
- P(뻣뻣한 목|수막염) = 0.7, P(수막염) = 1/50,000, P(뻣뻣한 목) = 0.01
- P(수막염|뻣뻣한 목) = (0.7 × 1/50,000) / 0.01 ≈ 0.0014 (약 0.14%)

### 베이즈 규칙의 또 다른 형태 (전체 확률 공식 활용)
분모 P(effect)를 직접 모를 때는 원인의 여집합(¬cause)까지 고려해 展開한다.

P(cause|effect) = P(effect|cause)P(cause) / [P(effect|cause)P(cause) + P(effect|¬cause)P(¬cause)]

**수치 예시 (백신 예시)**: 백신 접종자의 회복률 0.95, 비접종자의 회복률 0.85, 접종률 0.80일 때, 회복한 사람이 접종자일 확률
= (0.95×0.80) / (0.95×0.80 + 0.85×0.20) ≈ 0.82 (약 82%)

---

## 5부: 나이브 베이즈 모델(Naïve Bayes Model)

### 개념
- **나이브 베이즈 모델(= 베이지안 분류기, Bayesian Classifier)**: 하나의 원인(cause)이 여러 결과(effect, 특징/feature)에 직접 영향을 주며, 그 특징들은 원인(=목표 클래스, target class)이 주어졌을 때 서로 조건부 독립(conditionally independent)이라고 가정하는 모델.

식: P(cause|effect₁,…,effectₙ) = P(cause) × Π P(effectᵢ|cause)

- 이 가정을 "나이브(순진한, naïve)"라고 부르는 이유는, 실제로는 특징들 사이에 상관관계가 있을 수도 있는데 이를 무시하고 독립이라 가정하기 때문이다.

### 분류기 구성
K개의 클래스 {C₁, …, C_K} 중 n개의 특징이 주어졌을 때 가장 그럴듯한 클래스를 고르는 것이 목표다.

**ŷ = argmax_k p(C_k) × Π p(xᵢ|C_k)**

### 예시: 골프를 칠지 예측하기
Outlook(날씨), Temperature(기온), Humidity(습도), Windy(바람) 4가지 특징으로 골프를 칠지(Yes/No) 예측하는 데이터셋을 이용한다.
- 입력 {Sunny, Hot, Normal, False}가 주어졌을 때
  - p(Yes|입력) ∝ p(Yes) × Π p(xᵢ|Yes) ≈ 9/14 × 2/9 × 2/9 × 6/9 × 6/9 ≈ 0.0141
  - p(No|입력) ∝ p(No) × Π p(xᵢ|No) ≈ 5/14 × 3/5 × 2/5 × 1/5 × 2/5 ≈ 0.0068
  - p(Yes|입력) > p(No|입력) 이므로 "골프를 친다(Yes)"로 예측한다.
- 체크인 퀴즈에서는 다른 데이터셋으로 {Rainy, Hot, High, True}가 주어졌을 때의 예측을 연습한다.

### 텍스트 분류(Text Classification)에 적용
글의 범주(예: 신문 기사의 world/sports/business/sci-tech)를 나이브 베이즈로 분류하는 것도 같은 원리다.
- 특징(feature)은 "어떤 단어가 등장했는가/안 했는가(HasWord)"가 된다.
- 예: P(Category=sports)=0.09, P(HasWord_stocks=true|Category=business)=0.37
- 기사 "The president will attend the NBA finals. Who's gonna win the game?"가 주어지면, 기사에 등장한 단어와 등장하지 않은 단어 각각의 조건부 확률을 모두 곱해 카테고리별 점수를 계산하고 가장 높은 카테고리로 분류한다.
- 실습에서는 AG-NEWS 데이터셋(뉴스 기사 분류 데이터셋)과 파이썬 코드 예제로 실제 구현 과정을 보여준다.

---

## 6부: 베이지안 네트워크(Bayesian Networks)

### 정의
**베이지안 네트워크**: 변수들 간의 인과관계(cause-and-effect relationship)를 방향성 비순환 그래프(DAG, Directed Acyclic Graph)와 확률을 이용해 표현하는 그래프 모델.
- 그래프에서 부모 노드(parent)는 원인, 자식 노드는 그 원인의 영향을 받는 결과를 나타낸다.
- 예: '비(Rain)'는 '잔디가 젖음(Grass Wet)'의 부모 노드이며, '잔디가 젖음' 노드는 부모의 영향을 정량화한 확률을 가진다.

### 조건부 독립과 연쇄 법칙
**치통 예시**: 충치(Cavity)가 원인이고, 치통(Toothache)과 의사가 충치를 발견함(Catch)이 그 결과다. 치통과 발견 여부는 충치가 주어졌을 때 조건부 독립이다.

- **곱 규칙(2개 사건)**: P(X∧Y) = P(Y|X)P(X)
- **연쇄 법칙(Chain Rule, 여러 사건 일반화)**:
  P(X₁∧X₂∧⋯∧Xₙ) = Π P(Xᵢ|X₁∧⋯∧Xᵢ₋₁)
- 조건부 독립을 이용하면 이 연쇄 법칙이 각 노드가 자신의 **부모 노드에만 의존**하는 형태로 단순화된다:
  **P(X₁=x₁,…,Xₙ=xₙ) = Π P(xᵢ|Parents(Xᵢ))**

### 조건부 확률표(CPT, Conditional Probability Table)
- 각 행은 부모 노드들의 특정 조건(conditioning case)에서 해당 노드가 가지는 조건부 확률을 담는다.
- 부모 노드가 k개면 가능한 조건은 2ᵏ가지이며, 각 행의 확률 합은 항상 1이 되어야 한다.

### 예시: 도난-지진-경보 네트워크
절도(Burglary), 지진(Earthquake) → 경보(Alarm) → John이 전화함(JohnCalls), Mary가 전화함(MaryCalls)로 이어지는 네트워크.
- P(j,m,a,¬b,¬e) = P(j|a)P(m|a)P(a|¬b∧¬e)P(¬b)P(¬e) = 0.90×0.70×0.001×0.999×0.998 ≈ 0.000628
- MaryCalls는 Alarm에만 의존하므로, JohnCalls·Earthquake·Burglary가 주어져도 P(MaryCalls|…) = P(MaryCalls|Alarm)로 간단해진다(조건부 독립).

### 베이지안 네트워크를 이용한 예측
**질문**: 잔디가 젖었다는 것을 관찰했을 때, 비가 왔을 확률은?
- 잔디가 젖는 원인은 비(Rain)와 스프링클러(Sprinkler) 두 가지가 있을 수 있다.
- 모든 가능한 조합(비X스프링클러의 참/거짓)에 대한 결합 확률을 계산한 뒤, 베이즈 규칙으로 정리하면:
  P(R=T|G=T) = [0.00198(TTT) + 0.1584(TFT)] / [0.00198(TTT)+0.288(TTF)+0.1584(TFT)+0.0(TFF)] = 891/2491 ≈ 35.77%
- 체크인 퀴즈: 반대로 "잔디가 젖었을 때 비가 오지 않았을 확률"도 같은 방식으로 계산해볼 수 있다.

---

## 7부: 마르코프 모델(시간에 따른 확률적 추론)

### 시간에 따른 확률적 추론
- 목적: 과거의 이력(history)으로부터 현재 상태를 판단하고, 앞으로의 결과(행동의 결과)를 예측하는 것.
- 세상을 일련의 시간 조각(time slice)들의 연속으로 본다.
- **핵심 가정**: 현재 상태는 오직 바로 이전 상태에만 의존한다. **P(X_t | X_(t-1))**

### 마르코프 체인 (Markov Chain = Markov Process)
- **전이 모델(Transition model)**: P(X_t | X_(t-1)) — 상태가 시간에 따라 어떻게 변하는지.
- **관측 모델(Observation model)**: P(E_t | X_t) — 실제로 관측되는 값이 숨겨진 상태와 어떤 관계인지.

### 은닉 마르코프 모델(Hidden Markov Model, HMM)
- 프로세스의 상태가 **하나의, 이산적인(discrete) 확률 변수** 하나로 기술되는 시간적 확률 모델.
  - 예: 상태 변수는 "비가 오는가(Rain_t)" 하나뿐.
- **예시**: 우산을 든 사람이 관측된 순서(observed umbrella sequence)가 주어졌을 때, 그 뒤에 숨겨진 날씨 상태(Rain/No Rain)의 가장 가능성 높은 순서를 추정하는 문제. (다음 주차 이후에 더 깊이 다룰 주제로 이어짐)

---

## 참고: 공지사항 (수업 운영 관련, 참고용)

- **강의 계획**: 1주 과목 소개 → 2주 문제해결 → 3~4주 지식과 추론 → 5주 기계학습 기초 → 6~7주 신경망 → 8주 중간고사(10월 20일 화 오후 6:30~7:30). (상황에 따라 변경될 수 있음)
- **9/24 수업**: 추석 연휴로 동영상 강의로 대체. 시청률 90% 이상이면 출석, 50~90%면 지각, 50% 미만이면 결석 처리. 시청 기한은 10월 1일(목) 오후 11시 55분까지.
- **과제 1 (Tic-Tac-Toe AI 봇)**:
  - 제출 기한: 10월 8일 오후 11시 55분 (24시간 지각당 -10%)
  - 제출물: 소스 코드(파일명 규칙: 학번-이름-code.py/c/cpp/java), 영상 녹화(학번-이름-video.mp4)
  - 미니맥스 탐색, 무작위(Random), 왼쪽-위 우선(Left-up first) 세 가지 전략 중 선택해 봇을 구현
  - 승/패/무승부의 세 가지 종료 상태와, 잘못된 입력(1~9 범위 밖, 이미 채워진 칸 선택) 예외 처리를 모두 시연해야 함
  - 코드는 Python/C/C++/Java 모두 허용되지만, 시험은 Python만 다룸
