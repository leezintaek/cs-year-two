# Week2 Q&A

---

## Q1. Informed Search에서는 모든 노드를 다 안 돌 수도 있는 거야?

**A.** 맞다. 오히려 **모든 노드를 돌지 않는 것**이 Informed Search의 핵심 목적이다.

- Informed Search는 휴리스틱 h(n)(목표까지의 예상 비용)을 이용해 **목표에 가까워 보이는 노드부터** 우선순위 큐에서 꺼내 확장한다.
- 목표 노드를 꺼내는(dequeue) 순간 탐색을 멈추므로, 우선순위가 낮은(목표에서 멀어 보이는) 노드들은 **한 번도 확장되지 않은 채 끝날 수 있다.**
- 강의의 Uniform-cost search vs. A* 비교 그림에서 A*의 탐색 범위가 목표 방향으로 좁게 퍼지는 것("Faster!")이 바로 이 의미다.

**알고리즘별 차이**

| 알고리즘 | 확장하지 않는 노드 | 주의할 점 |
|---|---|---|
| Greedy best-first (`f=h`) | 아주 많음 (목표 쪽으로 직진) | 최적해 보장 X, 엉뚱한 방향으로 빠지거나 (tree search면) 무한 루프 가능 |
| A* (`f=g+h`) | `f(n) > C*`(최적 비용)인 노드는 절대 확장하지 않음 | h가 admissible(실제 비용을 과대평가하지 않음)이면 최적해 보장 |
| Weighted A* (`f=g+W·h`) | A*보다 더 적게 확장 | 더 빠르지만 최적해 보장 X (최대 W배까지 나빠질 수 있음) |

**예외적인 경우**
- 휴리스틱이 쓸모없으면(예: 모든 노드에서 h(n)=0) A*는 Uniform-cost search와 같아져서 거의 모든 노드를 돌 수 있다.
- 목표가 존재하지 않는 문제라면 결국 도달 가능한 모든 노드를 확인해야 "해 없음"을 알 수 있다.
- 즉, **휴리스틱이 정확할수록 돌지 않는 노드가 많아지고**, 최악의 경우에는 uninformed search와 비슷해진다.

> 참고: "확장(expand)되지 않는다"와 "생성(generate)되지 않는다"는 다르다. 확장된 노드의 자식들은 큐에 들어가(생성) 있지만, 그중 상당수는 끝까지 꺼내지지 않고 남는다.

---

## Q2. Greedy best-first search에서는 Bucharest까지의 직선 거리만 보는 거야?

**A.** 맞다. 루마니아 지도 예제에서 Greedy best-first search는 `f(n) = h(n) = h_SLD(n)`, 즉 **각 도시에서 Bucharest까지의 직선 거리(Straight-Line Distance)만** 보고 다음 노드를 고른다.

- 지금까지 실제로 이동한 도로 거리 `g(n)`은 **전혀 고려하지 않는다.**
- 직선 거리는 지도에 있는 도로 거리가 아니라 미리 주어진 표(h_SLD 표)에서 가져오는 값이다.

**예시 (Arad → Bucharest)**

| 단계 | 후보(직선 거리) | 선택 |
|---|---|---|
| 1 | Sibiu 253, Timisoara 329, Zerind 374 | Sibiu |
| 2 | Fagaras 176, Rimnicu Vilcea 193, Arad 366, Oradea 380 | Fagaras |
| 3 | Bucharest 0, Sibiu 253 | Bucharest (도착) |

- 찾은 경로: Arad → Sibiu → Fagaras → Bucharest, 실제 도로 거리 = 140 + 99 + 211 = **450**
- 최적 경로: Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest = 140 + 80 + 97 + 101 = **418**

→ Fagaras가 직선 거리로는 더 가까워 보였지만, Fagaras → Bucharest 도로(211)가 길어서 결과적으로 손해를 봤다. 이것이 Greedy best-first search가 **최적해를 보장하지 못하는** 이유다.

**A\*와의 비교**: A*는 `f(n) = g(n) + h(n)`으로 실제 이동 거리까지 더하므로, 같은 예제에서 Rimnicu Vilcea(140+80+193=413)를 Fagaras(140+99+176=415)보다 먼저 확장하고 최적 경로(418)를 찾는다.
