# Week3 강의 요약

> 강의 자료: `CSE2302_003_week03_1 (1).pdf` (Problem-Solving 3, 2026-09-15), `CSE2302_003_week03_2.pdf` (Problem-Solving 4 & Knowledge and Reasoning 1, 2026-09-17)

## 1. 지난 주 복습: Uninformed vs. Informed Search

| 구분 | Uninformed (Blind) Search | Informed (Heuristic) Search |
|---|---|---|
| 특징 | 문제에 특화된 지식을 사용하지 않음 | 문제에 특화된 지식(휴리스틱)을 사용해 더 효율적으로 해를 찾음 |
| 대표 전략 | BFS, DFS, Uniform-cost search, Iterative deepening search | Greedy best-first search, A* search, Iterative-deepening A*, Recursive best-first search |

- **Best-First Search**: 지금까지 도달한 상태들 중에서 우선순위 큐(priority queue)로 비용이 가장 작은 노드를 꺼내(dequeue) 탐색을 이어가는 방식. Uniform-cost search, greedy best-first search, A* search, weighted A* search 등이 여기 속한다.
- **Weighted A\* Search**: 탐색 함수 f(n)을 어떻게 정의하는지에 따라 알고리즘이 달라진다.
  - Greedy best-first search: f(n) = h(n) (목표까지의 예상 비용만 사용)
  - Uniform-cost search: f(n) = g(n) (지금까지 든 비용만 사용)
  - A* search: f(n) = g(n) + h(n) (실제 비용 + 예상 비용)
  - Weighted A* search: f(n) = g(n) + W·h(n), W > 1 (예상 비용에 가중치를 더 크게 부여해 목표 방향으로 더 적극적으로 탐색)

## 2. 복잡한 환경에서의 탐색 (Search in Complex Environments)

- 체스판은 10^44개, 바둑은 10^120개가 넘는 상태를 가질 수 있어 실제 문제의 탐색 공간은 매우 크다.
- 메모리(공간)나 시간 제약 때문에 앞서 배운 global search 방식은 현실적으로 불가능해질 수 있다.
- 이런 경우 사용하는 것이 **지역 탐색(local search) 알고리즘**이다.
  - Hill climbing (언덕 오르기)
  - Genetic algorithm, GA (유전 알고리즘) — 교재에서는 지역 알고리즘으로 분류하지만, 전역 알고리즘으로 분류되는 경우도 있음

### Hill Climbing (= Greedy Local Search)
- 이웃 상태 중 비용이 더 낮은(나보다 나은) 상태로만 이동한다.
- 이웃보다 더 좋은 해가 존재하더라도, 국지적으로 더 좋아 보이는 지점(local optimum)에서 멈추면 목표 상태에 도달하지 못하고 탐색이 끝날 수 있다는 단점이 있다.

### Genetic Algorithm (유전 알고리즘)
생물의 진화(evolutionary biology)에서 아이디어를 얻은 알고리즘으로, 한 세대(generation)의 해집단에서 다음 세대를 만들어가는 과정을 반복한다.
- **선택 (Selection)**: 적합도 점수(fitness score, 비용과 관련된 점수)를 기준으로 상태들을 선택
- **교차/재조합 (Crossover/Recombination)**: 선택된 두 상태의 일부를 서로 교환해 새로운 상태를 생성
- **변이 (Mutation)**: 새로 만들어진 상태에 무작위 오류(변화)를 추가

#### 예시 1: 외판원 문제 (Traveling Salesman Problem, TSP)
- 주어진 도시들을 한 번씩만 방문하면서 전체 이동 거리(D)를 최소화하는 경로(투어)를 찾는 문제.
- 상태는 도시들을 방문하는 순서(경로)로 표현되며, 이 경로들의 집합이 한 세대(generation)를 이룬다.
- 세대 내에서 거리(D)가 작은 경로를 **선택**하고, 두 경로를 **교차**시켜 새 경로를 만들고, 일부 구간을 무작위로 바꾸는 **변이**를 적용해 다음 세대를 구성한다.

#### 예시 2: 로봇 내비게이션에서의 유전 알고리즘
- 행동(action)은 F(전진), R(우회전), L(좌회전)의 나열로 표현된다.
- **적합도 점수** = −거리(distance) − 10 × 충돌 횟수(collision)
  - 목표까지의 거리가 짧을수록, 충돌이 적을수록 적합도 점수가 높다(덜 음수).
- 초기 집단(population)에서 시작해 선택 → 교차 → 변이를 반복하면서, 매 세대마다 적합도가 더 높은(충돌이 적고 거리가 짧은) 경로가 살아남도록 진화시킨다.
- 이 과정을 개체가 충분히 적합해지거나, 정해진 시간이 지날 때까지 반복한다.

### Local Search vs. Global Search 비교

| 구분 | Local Search | Global Search |
|---|---|---|
| 방식 | 시작 상태에서 이웃 상태로만 이동 | 지금까지 도달한 상태들 중에서 탐색 |
| 경로/상태 기록 | 경로나 탐색된/미탐색 상태 집합을 기록하지 않음 | 시작 노드부터의 경로와 탐색된/미탐색 노드 집합을 모두 기록해야 함 |
| 장점 | 메모리 사용이 적고 빠름 | 지역 최적(local minima)에서 벗어날 수 있음 |
| 예시 | Hill climbing (이웃 중 비용이 더 작은 상태로 이동) | Greedy best-first search (미방문 이웃 노드 중 비용이 더 작은 노드로 이동) |

## 3. 적대적 탐색 (Adversarial Search)

- 두 개 이상의 에이전트가 서로 충돌하는 목표를 가지는 경쟁적 환경(competitive environment)에서의 탐색을 의미한다.
- 예: 오목/틱택토처럼 한쪽이 이기면 다른 쪽은 지는 게임.

### 2인 제로섬 게임 (Two-player Zero-sum Games)
- "내가 이기면 = 상대가 진다"는 관계.
- 두 플레이어 **MAX**(점수를 최대화하려는 쪽)와 **MIN**(점수를 최소화하려는 쪽)이 번갈아 게임이 끝날 때까지 움직인다.
- 예: 틱택토, 체스, 체커, 바둑.

게임을 형식적으로 정의하는 요소:
- **InitialState**: 게임이 시작될 때의 초기 상태
- **ToMove(s)**: 상태 s에서 누구의 차례인지
- **Actions(s)**: 상태 s에서 가능한 합법적인 수(move)들의 집합
- **Result(s, a)**: 상태 전이 모델 (상태 s에서 행동 a를 했을 때의 다음 상태)
- **IsTerminal(s)**: 게임이 끝났는지를 판정하는 종료 검사
- **Utility(s, p)**: 종료 상태 s에서 플레이어 p가 얻는 최종 점수를 정의하는 효용 함수

### Minimax 알고리즘
2인 제로섬 적대적 게임을 푸는 방법으로, 다음 5단계로 진행된다.
1. 게임 트리(game tree)를 생성한다.
2. 종료 상태(terminal state)에 도달한다.
3. 종료 상태에 효용 값(utility value)을 부여한다.
4. 값을 트리의 위쪽으로 전파(propagate)한다. 이때 **MAX 노드**는 자식 노드 중 최댓값을, **MIN 노드**는 자식 노드 중 최솟값을 가져간다.
5. 루트에서 가장 좋은 값을 주는 수를 선택한다.

- 틱택토를 예로 들면, 'X' 차례에서는 승리(+1)/무승부(0)/패배(-1) 값을 부여하고 이를 위로 전파해서 각 상태에서 최선의 수를 결정한다.

**Minimax 의사코드(pseudo code) 요지**
- `BOT`은 점수를 최대화하려 하고, `PLAYER`는 점수를 최소화하려 한다.
- 각 빈 위치에 대해 재귀적으로 `MINIMAX(board, turn)`을 호출해, 종료 상태이면 승/패/무에 따라 +1/-1/0을 반환한다.
- `BOT` 차례면 자식들 중 최댓값을, `PLAYER` 차례면 자식들 중 최솟값을 반환한다.

### HW #1 공지: Tic-Tac-Toe with AI Bot
- **제출 기한**: 10월 8일 오후 11시 55분 (24시간 지각마다 -10% 감점, 1초~24시간 단위)
- **제출물**
  1. Source code (파일명: `학번-이름-code.py/c/cpp/java`) — C/C++, Java, Python 모두 허용하지만 시험은 Python만 다룸. 각 줄에 주석을 작성해야 함.
  2. Video recording (파일명: `학번-이름-video.mp4`)
- **과제 내용**: 틱택토를 플레이하는 AI 봇을 구현한다.
  - Option 1: Minimax search 사용
  - Option 2: Random(무작위) 선택
  - Option 3: 왼쪽 위부터 순서대로(Left-up first) 선택
  - 사용자가 먼저 시작하며 사용자는 'X', 봇은 'O'.
  - 종료 상태: 사용자 승리(-1), 봇 승리(+1), 무승부(0)
  - 예외 처리: 1~9 사이의 값만 선택 가능해야 하고, 이미 채워진 위치는 선택할 수 없어야 함.
  - 영상에는 세 가지 전략, 모든 예외 처리, 모든 결과(승/패/무)를 반드시 보여줘야 함.

### Minimax의 문제점과 알파-베타 가지치기 (Alpha-Beta Pruning)
- 게임 상태의 수는 트리의 깊이에 대해 지수적으로 증가한다 (체스 > 10^44, 바둑 > 10^120).
- "모든 상태를 다 탐색해야 할까?"라는 질문에서 나온 답이 **알파-베타 가지치기**다.
- 루트 노드의 최종 선택에 영향을 주지 않는 상태/노드는 가지치기(prune, 제거)해서 계산량을 줄인다.
- **α(알파)**: MAX 입장에서 지금까지 발견한 가장 좋은(가장 큰) 선택의 값
- **β(베타)**: MIN 입장에서 지금까지 발견한 가장 좋은(가장 작은) 선택의 값
- 탐색 도중 어떤 노드의 값이 α ≥ β 조건을 만족하면, 그 아래의 나머지 자식 노드들은 결과에 영향을 줄 수 없으므로 더 이상 탐색하지 않고 가지치기한다.

## 4. 휴리스틱 알파-베타 트리 탐색 (Heuristic Alpha-Beta Tree Search)

- 알파-베타 가지치기를 적용해도 게임 상태 수가 여전히 많을 수 있다.
- 이를 해결하기 위해 **Utility 함수 → EVAL 함수(평가 함수)**로, **종료 검사(terminal test) → 컷오프 검사(cutoff test)**로 바꿔서 사용한다.
  - 종료 상태에서는 EVAL(s, p) = UTILITY(s, p)를 그대로 사용
  - 종료 상태가 아니어도, 정해진 깊이(예: depth=2)에 도달하면 탐색을 중단(cutoff)하고 EVAL 함수로 그 상태의 가치를 추정한다.
- **좋은 평가 함수(evaluation function)의 조건**
  - 실제 승패 가능성과 강한 상관관계를 가져야 더 좋은 해를 찾기 쉬움
  - 계산이 오래 걸리면 안 됨 (탐색 속도를 빠르게 유지해야 함)
- 예시 (틱택토, O=+1, X=−1): EVAL = (+1)×(O가 아직 완성 가능한 줄 수/8) + (−1)×(X가 아직 완성 가능한 줄 수/8). 8은 틱택토의 전체 줄 수(가로3+세로3+대각2). 예: (+1)×(5/8) + (−1)×(6/8) = −0.125. (자세한 풀이는 `qna.md` Q1 참고)
- 다만, 좋은 평가 함수를 정의하는 것 자체가 여전히 어려운 문제로 남는다.

## 5. 몬테카를로 트리 탐색 (Monte Carlo Tree Search, MCTS)

- 현대의 바둑 프로그램들이 사용하는 방법.
- 휴리스틱 함수로 **여러 번의 시뮬레이션에 대한 평균 효용값**을 사용한다.
  - 평균 효용값(avg_utility) = 승리 횟수(# wins) / 전체 시행 횟수(# runs)
  - 즉, 평균 효용값 = 승률(win percentage)
- 동작 방식
  1. 리프 노드가 종료 상태가 아니면, 자식 노드를 하나 이상 추가해 트리를 확장한다.
  2. 확장된 노드에서 게임이 끝날 때까지 무작위로 수를 두어(random moves) 시뮬레이션한다. 단, 이 무작위 시뮬레이션 과정 자체는 트리에 기록되지 않는다.
  3. 시뮬레이션 결과(승/패)를 바탕으로 평균 효용값을 갱신하며 반복한다.

### 3~4주차 요약 정리
- Informed vs. uninformed search: DFS/BFS, Uniform-cost search, Greedy best-first search, (Weighted) A* search
- Local vs. global search: Hill climbing, Genetic algorithm
- Adversarial search: Minimax, 알파-베타 가지치기를 적용한 Minimax, Heuristic alpha-beta tree search, Monte Carlo Tree Search

## 6. 지식과 추론 (Knowledge and Reasoning) 시작

> "AI에서 지식 기반 에이전트(knowledge-based agent)는 지식의 내부 표현에 대한 추론 과정을 통해 어떤 행동을 취할지 결정한다."

- 지식 기반 에이전트의 동작 흐름: (1) 지각(percept)을 받으면 → (2) 그 지각을 지식 베이스(knowledge base)에 추가하고 → (3) 지식 베이스에 가장 좋은 행동이 무엇인지 물어보고 → (4) 그 행동을 실제로 수행했음을 다시 지식 베이스에 알려준다.

### 핵심 용어 정리
- **지식(Knowledge)**: AI 시스템이 가지고 있는 정보
- **지식 표현(Knowledge representation)**: 지식을 구조화된 형태로 모델링하는 것. (신경망을 포함한 머신러닝 모델들도 지식 표현 기법의 하나로 볼 수 있다)
- **지식 베이스(Knowledge base)**: 구조화된 정보들의 집합
- **추론(Reasoning)**: 정보를 바탕으로 결론을 도출하고, 추리하고, 문제를 해결하는 과정
- **인퍼런스(Inference)**: 지식 베이스로부터 새로운 사실을 이끌어내는 추론 메커니즘

### 예시 1: 삼단논법
"모든 인간은 죽는다"와 "소크라테스는 인간이다" ⇒ "소크라테스는 죽는다"
- 지식표현: ∀x Human(x) → Mortal(x), Human(Socrates)
- 지식 베이스: {Human(Socrates), ∀x Human(x) → Mortal(x)}
- 추론 결과: Mortal(Socrates) ⇒ "소크라테스는 죽는다"

### 예시 2: 이미지 분류(고양이 판별)로 다시 보기
- 지식: "고양이는 삼각형 귀를 가진다" & "고양이는 다리가 네 개다" & "고양이는 털이 있다"
- 지식표현: TriangularEars(x) ∧ FourLegs(x) ∧ Fur(x) → Cat(x)
- 지식 베이스: {TriangularEars(CatImg1), FourLegs(CatImg1), Fur(CatImg1)}
- 추론 결과: Cat(CatImg1) ⇒ "CatImg1은 고양이다"

### 지식 표현 기법 (Knowledge Representation Techniques)
- **논리적 표현 (Logical representation)**
- **의미망 (Semantic networks)**
- 신경망을 포함한 머신러닝 모델들도 지식 표현 기법의 하나로 볼 수 있다.
  - 논리적 표현이나 의미망 ⇒ **명시적(explicit)** 지식 표현
  - 머신러닝/딥러닝 ⇒ **암시적(implicit)** 지식 표현

> 다음 주(4주차)에는 "지식과 추론 (2)"가 이어지며, HW #1(틱택토 AI 봇) 마감은 10월 8일이다. 중간고사는 10월 20일(화) 오후 6시30분~7시30분이다.
