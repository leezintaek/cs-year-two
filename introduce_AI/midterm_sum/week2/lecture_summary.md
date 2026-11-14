# Week2 강의 요약

- 강의: CSE2302 인공지능개론 (담당: 윤진이 교수)
- 자료: `CSE2302_003_week02_1 (1).pdf` (2026-09-08, Lecture 01), `CSE2302_003_week02_2.pdf` (2026-09-10, Lecture 02)
- 주제: 문제해결(Problem-Solving) — 탐색(Search) 알고리즘 전반

---

## 1. AI 개념 복습 (1주차 이어서)

### Turing Test
- 앨런 튜링이 던진 질문 "Can machines think?"를 검증하기 위한 **Imitation Game**.
- 텍스트 기반 대화만으로 사람인지 컴퓨터인지 질문자(interrogator)가 구별하지 못하면 통과(PASS).
- 열린 질문(open-ended)이 가능하고, 내부 작동 방식이 아니라 겉으로 관찰되는 행동(behavioral)만 평가하는 방식.

### Weak AI vs. Strong AI (John Searle, 1980)
| 구분 | Weak AI (Narrow AI) | Strong AI (Human-Level AI) |
|---|---|---|
| 정의 | 지능이 있는 것**처럼** 행동 | 실제로 **의식적으로 사고** |
| 범위 | 특정 작업에 한정(일반화 부족) | 사람처럼 일반적인 지능 |
| 예시 | 추천 시스템, 이미지 분류 | 아직 이론적 접근 단계 |

- **Artificial General Intelligence (AGI)**: 사람의 개입 없이 다양한 영역의 문제를 스스로 풀 수 있는 AI를 만드는 목표. 현재는 이론적 연구 단계.

### AI 역사 타임라인
1. **Inception (1943~1956)**: 1950년 튜링의 논문 *Computing Machinery and Intelligence*, 1956년 다트머스 대학 워크숍에서 "Artificial Intelligence"라는 이름 탄생 (2개월, 참가자 10명).
2. **A Dose of Reality / 첫 번째 AI 겨울 (1966~1973)**: 1957년 허버트 사이먼이 "10년 안에 컴퓨터가 체스 챔피언이 될 것"이라 예측했지만 실제로는 40년 걸림(1996년 IBM Deep Blue, 1997년 세계 챔피언 격파). 1969년 민스키·페퍼트의 *Perceptrons*에서 단순 퍼셉트론이 **선형 분리 불가능한 함수(예: XOR)**를 학습할 수 없음을 증명 → 연구비 급감, 첫 AI 겨울.
   - **비선형 분리 문제**: AND, OR는 하나의 직선으로 분리 가능(선형 분리)하지만 XOR는 불가능.
3. **Neural Networks Return (1987~현재)**: 역전파(back-propagation) 재발견으로 신경망 연구 부활.
4. **Big Data (2001~현재)**: World Wide Web의 확산으로 대규모 데이터셋 생성이 가능해짐.
   - Big Data의 3요소(3V): **Volume**(TB~PB급 방대한 양), **Variety**(정형 데이터인 CSV/엑셀과 비정형 데이터인 음성·PDF·이미지), **Velocity**(실시간에 가까운 빠른 생성·처리 속도).
5. **Deep Learning (2011~현재)**: 세상을 바꾸고 있는 현재 진행형 시대.
   - 대표 사건: AlexNet(2012, 이미지 분류), GANs(2014, 사실적 이미지 생성), ResNet(2015), AlphaGo(2016, 이세돌 격파), Transformer(2017, "Attention is all you need"), BERT & GPT(2018, 대규모 언어 모델), CLIP(2021, 멀티모달 AI), ChatGPT(2022), GPT/Claude/Gemini(2023, LLM 기반 멀티모달 AI).

### 머신러닝 기본 개념
- **Classification(분류)**: 클래스(범주)를 예측 — 예) 이미지가 "Bicycle"일 확률이 가장 높은 클래스를 선택.
- **Regression(회귀)**: 연속적인 값을 예측 — 예) 주택 정보로 가격 예측.
- 레이블(정답)이 있으면 **지도학습(Supervised Learning)**의 대상.
- **Supervised Learning(지도학습)**: 레이블이 있는 데이터로 학습 → 새로운 입력의 클래스를 예측.
- **Unsupervised Learning(비지도학습)**: 레이블 없이 데이터의 구조(군집 등)를 스스로 찾음.
- **AI ⊃ ML ⊃ (Supervised/Unsupervised/Reinforcement Learning) ⊃ Deep Learning** 관계도: 딥러닝은 지도·비지도·강화학습 모두에 적용될 수 있는 하위 기술.

---

## 2. 탐색 문제(Search Problem)의 정의

문제 해결 에이전트는 **초기 상태(initial state)**에서 **목표 상태(goal state)**로 가는 방법을 찾는다. 이를 구성하는 핵심 요소:

- **Agent**: 환경을 인식하고 그에 따라 행동하는 개체(문제 해결 프로그램).
- **State**: 환경이 가질 수 있는 상태.
- **Initial state**: 에이전트가 시작하는 상태.
- **Action**: 특정 상태에서 취할 수 있는 선택지. `actions(s)`는 상태 s에서 가능한 행동들의 집합을 반환.
- **Transition model**: 어떤 상태에서 특정 행동을 했을 때 결과 상태를 설명. `result(s, a)`는 상태 s에서 행동 a를 수행한 결과 상태를 반환.
- **State space**: 초기 상태에서 임의의 행동 순서로 도달 가능한 모든 상태의 집합.
- **Action cost**: 상태 s에서 행동 a를 하여 s'에 도달하는 비용 `c(s, a, s')`.
- **Solution**: 초기 상태에서 목표 상태로 이어지는 행동들의 순서(경로).
  - **Optimal solution(최적해)**: 모든 해 중 비용이 가장 낮은 해.

### 대표적인 탐색 응용 사례
- **퍼즐 풀기**: 특정 배열(configuration)에 도달하는 것이 목표. 행동은 회전·조각 이동.
- **로봇 경로 계획(motion planning)**: 가장 빠르거나, 에너지 효율적이거나, 안전한 경로를 찾음. 행동은 좌/우 이동, 흡입(suck) 등.
- **경로 탐색(route finding)**: 최단 거리, 최소 시간, 가장 경치 좋은 경로 등을 목표로 직진·좌회전·우회전 등의 행동을 사용.

---

## 3. 비정보 탐색(Uninformed Search)

목표까지 얼마나 가까운지에 대한 정보 없이, 지금까지의 비용만 알고 탐색하는 방식.

### DFS / BFS 복습
- **DFS(깊이 우선 탐색)**: 최적해를 보장하지 않음.
- **BFS(너비 우선 탐색)**: (행동 비용이 동일할 때) 최적해를 보장함.

### Uniform-Cost Search (균등 비용 탐색)
- "가중치가 있는(weighted) BFS" — 행동마다 비용이 다를 때 사용.
- 모든 비용이 음수가 아니면(non-negative) 시작 노드에서 다른 모든 노드까지의 **최소 비용 경로**를 보장.
- AI 분야에서는 Uniform-Cost Search, 전산학(CS) 분야에서는 **Dijkstra 알고리즘**으로 불림(사실상 동일한 알고리즘).
- **동작 절차**:
  1. 시작 노드를 방문하고 비용 0으로 큐(우선순위 큐)에 넣는다.
  2. 경로 비용이 가장 낮은 노드를 큐에서 꺼낸다(dequeue).
  3. 이웃 노드마다 시작 노드로부터의 총 비용을 계산해 큐에 추가한다.
  4. 목적지 노드가 꺼내질 때까지 2~3을 반복한다. 더 저렴한 경로가 발견되면 기존 비용을 갱신한다.
- **의사코드 (Dijkstra와 동일한 형태)**:
  ```
  UniformCostSearch(G, start):
      모든 정점 v에 대해 distance[v] ← ∞, visited[v] ← false
      distance[start] ← 0
      정점 수만큼 반복:
          방문하지 않은 정점 중 distance가 가장 작은 u 선택 → 방문 처리
          u의 각 이웃 v에 대해:
              new_distance ← distance[u] + weight(u, v)
              new_distance가 더 작으면 distance[v] 갱신
      return distance
  ```
- 강의에서는 루마니아 지도(Sibiu→Bucharest)와 별도의 그래프(B, J, O, M, P, D, A, S, L 노드) 예제로 단계별 계산 과정을 시연함.

---

## 4. 정보 탐색(Informed Search)

### 비정보 탐색 vs. 정보 탐색
| 구분 | Uninformed (Blind) Search | Informed (Heuristic) Search |
|---|---|---|
| 사용 정보 | 문제에 특화된 지식 없음 | 문제에 특화된 지식(휴리스틱) 사용 |
| 대표 전략 | BFS, DFS, Uniform-cost search, Iterative deepening search | Greedy best-first search, A* search, Iterative-deepening A*, Recursive best-first search |
| 특징 | — | 더 효율적으로 해를 찾음(일반적으로 더 빠름) |

- **휴리스틱(heuristic)**: "최적이나 완벽하지 않아도 충분히 쓸모 있는 실용적인 방법"(위키피디아 정의 인용).
- **휴리스틱 함수 h(n)**: 노드 n의 상태에서 목표까지 가는 **가장 저렴한 경로의 예상 비용**.
- 내비게이션 예시: 목적지까지의 직선거리(유클리드 거리)를 휴리스틱으로 사용(위도·경도·고도 정보 이용).

### Greedy Best-First Search
- 각 단계에서 가장 유망해 보이는(휴리스틱 값이 낮은) 경로를 선택.
- **절차**: 시작 노드에서 출발 → 이웃 노드들의 휴리스틱 값 평가 → 가장 낮은 값을 가진 노드 선택 → 목적지 도달까지 반복.
- 강의에서 맨해튼 거리(Manhattan Distance)를 휴리스틱으로 한 격자 미로 예제로 풀이함.

### Local Search vs. Global Search
| 구분 | Local Search | Global Search |
|---|---|---|
| 방식 | 현재 상태에서 이웃 상태로만 탐색, 경로나 방문 상태 집합을 기억하지 않음 | 지금까지 도달한 모든 상태 중에서 탐색, 경로와 방문/미방문 노드 집합을 계속 추적 |
| 장점 | 메모리 사용이 적고 빠름 | 지역 최적(local minima)에서 벗어날 수 있음 |
| 대표 알고리즘 | Hill Climbing(= Greedy Local Search) | Greedy Best-First Search |

- 즉, "경로(track)를 기록하며 탐색"하면 Greedy Best-First Search(global), "기록 없이" 현재 이웃만 보고 움직이면 Hill Climbing(local)이 된다.

### Hill Climbing (= Greedy Local Search)
- 현재보다 비용이 더 낮은 이웃 노드로만 이동(이웃 중 나보다 나은 것이 있어야 함).
- 더 나은 이웃이 없으면 탐색을 종료 → **지역 최적해(local optimum)에 갇혀 전역 최적해를 놓칠 수 있음**.
- **의사코드**:
  ```
  function HillClimbing:
      current ← 시작 상태
      반복:
          next ← current의 이웃 중 가장 값이 좋은 상태
          if value[next] ≤ value[current]: return current
          else: current ← next
  ```

### Best-First Search
- 지금까지 도달한 상태들 중에서 탐색을 진행(전역 탐색).
- 추적 방법: **우선순위 큐(priority queue)** — 이웃 노드를 큐에 넣고(enqueue), 비용이 최소인 노드를 꺼냄(dequeue).
- 예시 알고리즘: Uniform-cost search, Greedy best-first search, A* search, Weighted A* search 등.

### 평가 함수 f(n)
- **Greedy Best-First Search**: `f(n) = h(n)` — 목표까지의 예상 비용만 고려.
- **A\* Search**: `f(n) = g(n) + h(n)`
  - `g(n)`: 초기 상태에서 노드 n까지 실제로 이동한 비용.
  - `h(n)`: 노드 n에서 목표까지의 예상(휴리스틱) 비용.

### A* Search
- 정보 탐색 알고리즘으로, 목표 노드까지 가장 비용이 적은 경로를 찾는 것이 목표.
- 매 반복마다 평가 비용 `f(n) = g(n) + h(n)`이 가장 낮은 노드를 다음으로 선택.
- 루마니아 지도 예제와 맨해튼 거리 기반 격자 예제(Example 2)로 g(n)과 h(n)을 각각 더해가며 탐색 순서를 시연.

### Weighted A* Search
- 네 가지 평가 함수 비교:
  - Greedy best-first search: `f(n) = h(n)`
  - Uniform-cost search: `f(n) = g(n)`
  - A* search: `f(n) = g(n) + h(n)`
  - **Weighted A\* search**: `f(n) = g(n) + W·h(n)` (단, W > 1) — 휴리스틱에 가중치를 주어 속도를 높이되 최적성은 다소 희생할 수 있음.
- Uniform-cost search와 A* search의 탐색 범위를 시각적으로 비교하면, A*가 목표 방향으로 더 좁고 빠르게 탐색함(휴리스틱 덕분에 "Faster!").

---

## 5. 복잡한 환경에서의 탐색(Search in Complex Environments)

- 실제 문제들은 매우 큰 탐색 공간을 가짐 — 예) 체스판 상태 수 > 10⁴⁴, 바둑 상태 수 > 10¹²⁰.
- 메모리(공간)나 시간 제약으로 인해 모든 상태를 탐색하는 것이 사실상 불가능(infeasible).
- 이런 경우 사용하는 **지역 탐색(local search) 알고리즘**: Hill Climbing, **Genetic Algorithm(GA, 유전 알고리즘)**.
  - (참고: GA는 교재에서는 지역 탐색으로 분류되지만, 전역 탐색으로 분류되기도 함.)

### Genetic Algorithm (유전 알고리즘)
- 진화생물학(evolutionary biology)에서 영감을 얻은 알고리즘.
- 한 세대(Generation N)에서 다음 세대(N+1)로 넘어가는 과정:
  1. **Selection(선택)**: 적합도 점수(비용)에 따라 상태들을 선택.
  2. **Crossover/Recombination(교차)**: 선택된 상태들의 일부를 조합해 새로운 상태 생성.
  3. **Mutation(변이)**: 일부 값에 임의의 오류(변화)를 추가.

### 예시: 외판원 문제(Traveling Salesman Problem, TSP)
- 주어진 도시 집합을 한 번씩만 방문하면서 총 이동 거리를 최소화하는 경로(tour)를 찾는 문제.
- 상태: 방문 순서(예: 런던-서울-뉴욕).
- 강의에서 여러 개의 경로(각각 총 거리 D가 다름)에 대해 선택 → 교차 → 변이 과정을 숫자 배열 예시로 시연.

---

## 6. 다음 주제 예고: Adversarial Search (경쟁적 탐색)

- **경쟁 환경(competitive environments)**: 둘 이상의 에이전트가 서로 충돌하는 목표를 가질 때의 탐색 = **Adversarial Search**.
- 틱택토(tic-tac-toe) 게임 트리 예시로 소개.
- **Two-player Zero-sum Games(2인 제로섬 게임)**:
  - 두 플레이어 **MAX**와 **MIN**이 번갈아 가며 행동.
  - 한 쪽(MAX)의 이득은 다른 쪽(MIN)의 손실과 같음 → 전체 이득 + 전체 손실 = 0(제로섬).
  - 다음 주차(지식과 추론)로 이어지기 전, 3주차 이후 본격적으로 다룰 주제로 소개됨.

---

## 참고 (강의 슬라이드 기준 학기 일정)

| 주차 | 강의 내용 | 비고 |
|---|---|---|
| 1 | 과목 및 인공지능 소개 | |
| 2 | 문제해결 | |
| 3 | 지식과 추론 (1) | |
| 4 | 지식과 추론 (2) | 과제 1 공지 |
| 5 | 기계학습 기초 | |
| 6 | 신경망 (1) | 과제 1 마감 |
| 7 | 신경망 (2) | |
| 8 | 중간고사 (10월 20일 화요일 오후 6:30~7:30) | |
