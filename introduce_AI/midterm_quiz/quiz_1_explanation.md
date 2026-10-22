# 인공지능개론 퀴즈 1 — 정답과 해설

- 문제: `quiz_1.md`
- 각 문항: **정답** → 풀이 → 함정 순서
- 괄호 안의 week는 근거가 되는 강의

---

## 정답 한눈에 보기

| 번호 | 정답 요약                             | 번호 | 정답 요약                                |
|------|---------------------------------------|------|------------------------------------------|
| Q1   | 0.733 / 0.711 / 0.714 / 0.733         | Q26  | ②                                        |
| Q2   | S→A→B→C→G, 비용 8                     | Q27  | setosa, virginica, versicolor, virginica |
| Q3   | F                                     | Q28  | S-B-C-G, 비용 10                         |
| Q4   | 2, 4, 3, 1, zero_grad, backward, step | Q29  | F                                        |
| Q5   | 루트 3, 가지치기 4·6                  | Q30  | Versicolor (argmax 동점 문제)            |
| Q6   | 2.0/2.449 → 4.0/6.481                 | Q31  | No (1/30 < 3/80)                         |
| Q7   | F                                     | Q32  | 784·10 / 1875 / 18750                    |
| Q8   | 0.1538                                | Q33  | ①③④⑥                                     |
| Q9   | AND, $-1 \le b < 0$                   | Q34  | [0.844, 0.156]                           |
| Q10  | ①                                     | Q35  | F                                        |
| Q11  | (T, F)                                | Q36  | 루트 5, 가지치기 9·0·-1                  |
| Q12  | S→A→B→C→G, 비용 8                     | Q37  | ③ / ⑤ / ①                                |
| Q13  | F                                     | Q38  | 800·200 / 5번 / 평균                     |
| Q14  | 27 / 101,770                          | Q39  | F                                        |
| Q15  | $\lnot P \lor Q \lor R$ / 거짓        | Q40  | S-B-G, 비용 12                           |
| Q16  | 0.3, y, fit, predict, zip, …          | Q41  | ∀x (Student ∧ ¬Pass → Retake)            |
| Q17  | F                                     | Q42  | ŷ = 0.5278, L = 0.2230, w = 0.5733       |
| Q18  | R3·R2 / R1·R2                         | Q43  | ⑤                                        |
| Q19  | [0.6652, 0.2447, 0.0900], 0           | Q44  | 강화 / 비지도 / 분류 / 회귀              |
| Q20  | 0.000591 / $\mathbf{P}(M \mid A)$     | Q45  | T                                        |
| Q21  | 1, -1, -inf, 'PLAYER', max, min       | Q46  | 32×784, 784×128, 32×128, …               |
| Q22  | F                                     | Q47  | F                                        |
| Q23  | ②                                     | Q48  | abs, len, 제곱, ** 0.5                   |
| Q24  | 90/10/30/370, 0.92/0.9/0.75           | Q49  | T                                        |
| Q25  | F                                     | Q50  | agent, result, state space, …            |

---

## Q1. 다중 클래스 혼동 행렬 (week6)

**정답:** (1) 0.733 (2) 0.8, 0.5, 0.833 → 0.711 (3) 0.8, 0.571, 0.769 → 0.714 (4) 둘 다 0.733

**(1) accuracy** = 대각선 합 / 전체 = $(40 + 20 + 50) / 150 = 110/150 \approx 0.733$

**(2) recall** = 대각선 / **행** 합 (실제 그 클래스인 것 중 맞힌 비율)

| 클래스 | 계산    | recall |
|--------|---------|--------|
| A      | 40 / 50 | 0.8    |
| B      | 20 / 40 | 0.5    |
| C      | 50 / 60 | 0.833  |

- macro recall = $(0.8 + 0.5 + 0.833) / 3 \approx 0.711$

**(3) precision** = 대각선 / **열** 합 (그 클래스로 예측한 것 중 맞힌 비율)

| 클래스 | 열 합            | precision |
|--------|------------------|-----------|
| A      | 40 + 10 + 0 = 50 | 0.8       |
| B      | 5 + 20 + 10 = 35 | 0.571     |
| C      | 5 + 10 + 50 = 65 | 0.769     |

- macro precision = $(0.8 + 0.571 + 0.769) / 3 \approx 0.714$

**(4) micro 평균:** 클래스마다 "그 클래스 vs 나머지" 이진 혼동 행렬을 만든 뒤 TP, FP, FN을 **모두 더해서** 계산한다.
- TP 합 = 40 + 20 + 50 = 110
- FP 합 = 열에서 대각선을 뺀 것 = 10 + 15 + 15 = 40
- FN 합 = 행에서 대각선을 뺀 것 = 10 + 20 + 10 = 40
- micro precision = 110 / (110 + 40) ≈ 0.733, micro recall = 110 / (110 + 40) ≈ 0.733

**함정**
- recall은 **행**, precision은 **열**이다. 표의 행/열 정의(행 = 실제)를 먼저 확인한다.
- 샘플마다 레이블이 하나인 다중 클래스 분류에서는, 잘못 분류된 샘플 하나가 어떤 클래스의 FP 1개이면서 동시에 다른 클래스의 FN 1개가 된다. 그래서 FP 합 = FN 합이고, **micro precision = micro recall = accuracy**가 된다(강의 예시도 셋 다 0.73).

---

## Q2. Uniform-Cost Search (week2)

**정답:** (1) S → A → B → C → G (2) S-A-B-C-G, 비용 8 (3) B: 5 → 3 (A 확장 시), C: 8 → 5 (B 확장 시), G: 10 → 8 (C 확장 시)

| 단계 | 확장 노드 (g) | 이웃 갱신                       | 우선순위 큐 (g) |
|------|---------------|---------------------------------|-----------------|
| 1    | S (0)         | A = 2, B = 5                    | A2, B5          |
| 2    | A (2)         | B: 2+1 = **3** < 5 갱신, C = 8  | B3, C8          |
| 3    | B (3)         | C: 3+2 = **5** < 8 갱신, G = 10 | C5, G10         |
| 4    | C (5)         | G: 5+3 = **8** < 10 갱신        | G8              |
| 5    | G (8)         | 목표가 dequeue됨 → 종료         |                 |

- 경로는 각 노드를 마지막으로 갱신한 부모를 따라간다: G ← C ← B ← A ← S

**함정**
- UCS는 목표 노드가 큐에 **들어갈 때**가 아니라 **꺼내질(dequeue) 때** 종료한다(강의: "until the destination node is dequeued"). G가 처음 큐에 들어갈 때의 비용 10은 최적이 아니다.
- UCS = Dijkstra's algorithm. 모든 비용이 음수가 아니면 최소 비용 경로를 보장한다.

---

## Q3. Naïve Bayes의 가정 (week4)

**정답:** F

- Naïve Bayes는 feature들이 **cause(클래스)가 주어졌을 때 조건부 독립**(conditionally independent, given the cause)이라고 가정한다.
- 클래스를 모를 때도 feature끼리 독립이라는 뜻(무조건 독립)이 아니다.
- 그래서 $\mathbf{P}(\text{cause} \mid e_1, \dots, e_n) \propto \mathbf{P}(\text{cause}) \prod_i \mathbf{P}(e_i \mid \text{cause})$ 처럼 **클래스별로** 곱한다.

---

## Q4. PyTorch MLP 코드 (week7)

**정답:** (1) 2 (2) 4 (3) 3 (4) 1 (5) `zero_grad` (6) `backward` (7) `step`

**(1)~(3)** `nn.Linear(in_features, out_features)` → 입력 2개 → 은닉 4개 → 출력 3개(클래스 수)

**(4)(8)** `x = torch.tensor([[0.2, 1.4]])`의 shape은 **(1, 2)** = (batch 크기, feature 수)
- 출력 `output_z`도 (batch, 3)이므로 클래스 방향은 **dim=1**이다.
- dim=0으로 하면 batch 방향으로 softmax가 되어, 샘플끼리 확률을 나누는 엉뚱한 결과가 된다.

**(5)~(7)** 학습 순서
1. `optimizer.zero_grad()`: 이전 단계 gradient를 0으로 초기화 (PyTorch는 gradient를 누적하므로)
2. `loss.backward()`: backpropagation으로 gradient 계산
3. `optimizer.step()`: gradient로 파라미터 갱신

---

## Q5. Minimax와 alpha-beta pruning (week3)

**정답:** (1) MIN 값 3, 2, 2 → 루트 3 (2) 4, 6

**(1)** MIN 노드는 자식 중 최솟값: min(3,12,8) = 3, min(2,4,6) = 2, min(14,5,2) = 2. 루트 MAX는 max(3,2,2) = **3**

**(2) 가지치기 과정**
- 첫째 MIN: 3, 12, 8을 모두 보고 3 → 루트 α = 3
- 둘째 MIN: 첫 단말 2를 보면 β = 2. α = 3 ≥ β = 2 → 이 MIN은 2 이하가 확정되어 루트가 고르지 않는다. **4, 6 가지치기**
- 셋째 MIN: 14 → β = 14, 5 → β = 5, 2 → β = 2. 마지막 단말까지 와서야 β ≤ α가 되므로 잘리는 단말이 없다.

**함정:** 셋째 MIN은 결과적으로 2지만, 2가 **마지막**에 나와서 아무것도 자르지 못한다. 순서가 (2, 14, 5)였다면 14, 5가 잘렸을 것이다 → 방문 순서는 가지치기 양에 영향을 준다(Q13).

---

## Q6. MAE와 RMSE (week5)

**정답:** (1) MAE = 2.0, RMSE ≈ 2.449 (2) MAE = 4.0, RMSE ≈ 6.481

**(1)** 오차 $\hat{y} - y$ = 2, −1, 0, 3, −4
- MAE = (2 + 1 + 0 + 3 + 4) / 5 = **2.0**
- MSE = (4 + 1 + 0 + 9 + 16) / 5 = 6 → RMSE = $\sqrt{6} \approx$ **2.449**

**(2)** 마지막 오차가 −14가 된다.
- MAE = (2 + 1 + 0 + 3 + 14) / 5 = **4.0** (2배)
- MSE = (4 + 1 + 0 + 9 + 196) / 5 = 42 → RMSE = $\sqrt{42} \approx$ **6.481** (약 2.6배)

**(3)** 오차를 제곱하는 RMSE(MSE)는 **큰 오차(이상치)에 더 큰 벌점**을 주므로, 이상치 하나에 MAE보다 훨씬 크게 반응한다(강의: {1,−2,3,4,5} → {1,−2,3,4,100}에서 MAE 3 → 22, RMSE 3.3 → 44.8).

---

## Q7. BFS의 최적성 (week2)

**정답:** F

- BFS는 **간선 개수(깊이)가 가장 적은** 경로를 먼저 찾는다. 모든 action 비용이 같을 때만 최소 비용 해를 보장한다(강의의 격자 예시는 모든 비용이 1).
- 비용이 다르면 깊이가 얕아도 비용이 큰 경로를 먼저 찾을 수 있다. Q2에서 BFS는 깊이 2인 S-B-G(비용 12)를 찾지만 최적은 S-A-B-C-G(비용 8)이다.
- 비용이 다를 때는 "weighted BFS"인 **uniform-cost search**를 쓴다.

---

## Q8. Bayes' rule (week4)

**정답:** ≈ 0.1538

$$P(d \mid +) = \frac{P(+ \mid d)\,P(d)}{P(+ \mid d)\,P(d) + P(+ \mid \lnot d)\,P(\lnot d)} = \frac{0.9 \times 0.01}{0.9 \times 0.01 + 0.05 \times 0.99} = \frac{0.009}{0.0585} \approx 0.1538$$

- 분모 $P(+)$는 강의의 "Another form of Bayes' rule"처럼 **환자인 경우 + 환자가 아닌 경우**로 나눠 구한다.

**함정:** 검사 정확도가 90%라서 양성이면 90%쯤 환자라고 생각하기 쉽다. 유병률이 1%로 낮아서, 건강한 99% 중 5%가 양성(0.0495)인 경우가 진짜 환자 양성(0.009)보다 훨씬 많다.

---

## Q9. 퍼셉트론과 논리 연산 (week6~7)

**정답:** (1) z = −1.5, −0.5, −0.5, 0.5 → 0, 0, 0, 1 (2) AND (3) $-1 \le b < 0$ (4) 아래 참고

| $x_1$ | $x_2$ | $z = x_1 + x_2 - 1.5$ | 출력 |
|-------|-------|-----------------------|------|
| 0     | 0     | −1.5                  | 0    |
| 0     | 1     | −0.5                  | 0    |
| 1     | 0     | −0.5                  | 0    |
| 1     | 1     | 0.5                   | 1    |

**(3) OR 조건:** $z = x_1 + x_2 + b$
- (0,0) → 0 이어야 함: $b < 0$
- (0,1), (1,0) → 1 이어야 함: $1 + b \ge 0$ → $b \ge -1$
- (1,1) → 1: $2 + b \ge 0$ (위 조건에 포함)
- 그래서 $-1 \le b < 0$ 이다. 강의 예시 $b = -0.5$가 여기에 해당한다.
- 참고: 같은 방식으로 AND가 되는 범위는 $-2 < b \le -1$ 이다. 문제의 $b = -1.5$가 여기에 해당한다.

**(4) XOR:** (0,1), (1,0)은 1, (0,0), (1,1)은 0이어서 **직선 하나로 나눌 수 없다(non-linearly separable)**. 단일 퍼셉트론의 결정 경계는 직선이라 불가능하다. 1969년 Minsky와 Papert가 이 한계를 보여 첫 번째 AI 겨울이 왔다. **은닉층을 둔 multi-layer perceptron**으로 해결한다.

---

## Q10. AI 역사 (week1~2)

**정답:** ①

| 사건                  | 연도        |
|-----------------------|-------------|
| (나) Dartmouth 워크숍 | 1956        |
| (다) *Perceptrons*    | 1969        |
| (마) MYCIN            | 1970년대 초 |
| (바) Deep Blue        | 1997        |
| (라) ImageNet         | 2009        |
| (사) IBM Watson       | 2011        |
| (가) AlphaGo          | 2016        |

**함정:** ③은 ImageNet(2009)과 Deep Blue(1997)의 순서가 바뀌었다. ②는 MYCIN과 *Perceptrons*가 바뀌었다(1969년 첫 겨울 → 1970년대 전문가 시스템).

---

## Q11. Viterbi 알고리즘 (week5)

**정답:** (1) 0.315, 0.07 (2) 0.02205, 0.0756 (3) (T, F)

**t = 1** ($U_1 = T$)
- $P_1(T) = \max(0.5 \times 0.7,\ 0.5 \times 0.3) \times 0.9 = 0.35 \times 0.9 = 0.315$ (이전 T에서 옴)
- $P_1(F) = \max(0.5 \times 0.3,\ 0.5 \times 0.7) \times 0.2 = 0.35 \times 0.2 = 0.07$ (이전 F에서 옴)

**t = 2** ($U_2 = F$ → 관측 확률은 $P(U = F \mid R = T) = 0.1$, $P(U = F \mid R = F) = 0.8$)
- $P_2(T) = \max(0.315 \times 0.7,\ 0.07 \times 0.3) \times 0.1 = 0.2205 \times 0.1 = 0.02205$
- $P_2(F) = \max(0.315 \times 0.3,\ 0.07 \times 0.7) \times 0.8 = \max(0.0945,\ 0.049) \times 0.8 = 0.0756$ ← **$R_1 = T$에서 옴**

**(3)** 마지막 시점에서 $P_2(F) > P_2(T)$ → $R_2 = F$. $P_2(F)$의 max를 만든 이전 상태가 T이므로 $R_1 = T$ → **(T, F)**

**함정**
- 관측이 F일 때는 $1 - P(U = T \mid R)$를 써야 한다: 비가 오는데 우산이 없을 확률 0.1, 비가 안 오는데 우산이 없을 확률 0.8.
- 경로는 각 시점에서 따로 큰 값을 고르는 것이 아니라, **마지막 최댓값에서 max를 만든 이전 상태를 거꾸로 따라가서(backtracking)** 정한다.

---

## Q12. A\* search (week2)

**정답:** (1) S(6) → A(6) → B(5) → C(6) → G(8) (2) S-A-B-C-G, 비용 8

| 단계 | 확장 (g, f) | 이웃 갱신 (g, f = g + h)          | 큐 (f)  |
|------|-------------|-----------------------------------|---------|
| 1    | S (0, 6)    | A (2, 6), B (5, 7)                | A6, B7  |
| 2    | A (2, 6)    | B: g 3 < 5 갱신 → f 5, C (8, 9)   | B5, C9  |
| 3    | B (3, 5)    | C: g 5 < 8 갱신 → f 6, G (10, 10) | C6, G10 |
| 4    | C (5, 6)    | G: g 8 < 10 갱신 → f 8            | G8      |
| 5    | G (8, 8)    | 목표 dequeue → 종료               |         |

- 이 휴리스틱은 모든 노드에서 실제 남은 비용 이하(S 6 ≤ 8, A 4 ≤ 6, B 2 ≤ 5, C 1 ≤ 3)라서 A\*가 UCS와 같은 최적 경로를 찾는다.

**함정:** $f$ 값이 단조 증가하지 않는다(6 → 6 → 5 → 6). 큐에서 꺼낼 때마다 그 시점의 최소 $f$를 고르면 된다.

---

## Q13. Alpha-beta pruning과 결과 (week3)

**정답:** F

- Alpha-beta pruning은 **루트의 선택에 영향을 주지 않는** 노드만 잘라낸다(강의: "Prune the states/nodes that do not affect the root's selection").
- 방문 순서가 나쁘면 **잘리는 양이 줄어들 뿐**, 루트의 minimax 값은 항상 같다(Q5 함정 참고).

---

## Q14. 파라미터 개수 (week7)

**정답:** (1) 27 (2) 101,770

- fully connected 층 하나의 파라미터 = (입력 수 × 출력 수) + 출력 수(bias)
- **(1)** 은닉층: 2 × 4 + 4 = 12, 출력층: 4 × 3 + 3 = 15 → **27**
- **(2)** 은닉층: 784 × 128 + 128 = 100,480, 출력층: 128 × 10 + 10 = 1,290 → **101,770**
- Flatten, Sigmoid, Softmax 같은 층은 학습 파라미터가 없다.

---

## Q15. 논리 동치 변환 (week4)

**정답:** (1) $\lnot P \lor Q \lor R$ (2) 거짓

1. Implication elimination ($\alpha \to \beta \equiv \lnot\alpha \lor \beta$): $\lnot(P \land \lnot Q) \lor R$
2. De Morgan's law ($\lnot(\alpha \land \beta) \equiv \lnot\alpha \lor \lnot\beta$): $(\lnot P \lor \lnot\lnot Q) \lor R$
3. Double-negation elimination: $\lnot P \lor Q \lor R$

**(2)** $\lnot T \lor F \lor F = F \lor F \lor F = F$
- 원래 문장으로 확인: 전건 $P \land \lnot Q = T$, 후건 $R = F$ → "참 → 거짓"인 유일한 경우라 거짓

---

## Q16. Iris 결정 트리 코드 (week5 실습)

**정답:** (1) `0.3` (2) `y` (3) `fit` (4) `predict` (5) `zip` (6) `correct / len(y_test)` (7) `(len(y_test) - correct) / len(y_test)` 또는 `1 - accuracy` (8) training 105개, test 45개, test에 클래스별 15개

- **(2)** `stratify=y`는 레이블 y의 비율대로 나눈다. Iris는 50:50:50이므로 test 45개에도 15:15:15로 들어간다.
- **(5)** `zip(y_test, y_pred)`는 정답과 예측을 한 쌍씩 묶는다.
- **(8)** 150 × 0.3 = 45 (test), 나머지 105 (training)

---

## Q17. Precision과 recall의 선택 (week6)

**정답:** F (반대로 되어 있다)

| 지표      | 식               | 분모에 들어가는 오류 | 중요할 때              |
|-----------|------------------|----------------------|------------------------|
| Precision | $TP / (TP + FP)$ | FP                   | FP가 치명적일 때       |
| Recall    | $TP / (TP + FN)$ | FN                   | FN이 치명적일 때(질병) |

- 질병 검사에서 환자를 놓치는(FN) 것이 치명적 → recall (강의 예시)
- 스팸 필터에서 정상 메일을 스팸으로 버리는(FP) 것이 치명적 → precision

---

## Q18. 유전 알고리즘 적합도 (week3)

**정답:** (1) R1 −24, R2 −19, R3 −18 → R3, R2 선택 (2) R1 −6, R2 −10, R3 −18 → R1, R2 선택

**(1)** $-4 - 10 \times 2 = -24$, $-9 - 10 \times 1 = -19$, $-18 - 10 \times 0 = -18$
- 적합도는 **클수록(0에 가까울수록)** 좋다 → R3(−18), R2(−19)

**(2)** $-4 - 2 = -6$, $-9 - 1 = -10$, $-18 - 0 = -18$ → R1, R2
- 충돌 벌점을 줄이면 거리가 짧은 경로가 유리해진다. 적합도 함수의 설계가 탐색 방향을 결정한다.

**(3)**
- Selection(선택): 적합도 점수에 따라 다음 세대에 쓸 상태(개체)를 고른다.
- Crossover(교차): 선택된 두 개체의 일부를 섞어 새 개체를 만든다.
- Mutation(변이): 새 개체 일부를 무작위로 바꿔(some errors) 다양성을 준다.

**함정:** 거리가 가장 먼 R3가 1등이다. 점수는 음수라서 "작은 값이 좋다"고 착각하면 R1을 고르게 된다.

---

## Q19. Softmax (week7)

**정답:** [0.6652, 0.2447, 0.0900], argmax = 0

- 합 = 7.389 + 2.718 + 1 = 11.107
- $7.389 / 11.107 \approx 0.6652$, $2.718 / 11.107 \approx 0.2447$, $1 / 11.107 \approx 0.0900$
- 출력은 모두 0 이상이고 합이 1 → 확률 분포(강의: non-negative & sum to 1)
- Softmax는 크기 순서를 바꾸지 않으므로 argmax는 z의 argmax와 같은 **0**

---

## Q20. Bayesian network 결합 확률 (week4)

**정답:** (1) ≈ 0.000591 (2) $\mathbf{P}(M \mid A)$

**(1)** 각 노드는 **부모만** 조건으로 둔다: $P(x_1, \dots, x_n) = \prod_i P(x_i \mid Parents(X_i))$

$$P(j, m, a, b, \lnot e) = P(j \mid a)\,P(m \mid a)\,P(a \mid b, \lnot e)\,P(b)\,P(\lnot e) = 0.90 \times 0.70 \times 0.94 \times 0.001 \times 0.998 \approx 0.000591$$

- $P(\lnot e) = 1 - 0.002 = 0.998$
- 강의 예시 $P(j, m, a, \lnot b, \lnot e) = 0.000628$과 비교: 이번에는 도둑이 들었고(b), 그래서 $P(a \mid b, \lnot e) = 0.94$를 쓴다.

**(2)** MaryCalls의 부모는 Alarm 하나뿐이다. 부모(Alarm)를 알면 나머지 변수(John, Earthquake, Burglary)는 추가 정보를 주지 않는다 → $\mathbf{P}(M \mid J, A, E, B) = \mathbf{P}(M \mid A)$

---

## Q21. Minimax 코드 (week3)

**정답:** (1) `1` (2) `-1` (3) `float('-inf')` (4) `'PLAYER'` (5) `max` (6) `min`

- **(1)(2)** 강의 pseudo code: BOT 승 +1, PLAYER 승 −1, 무승부 0
- **(3)** 최댓값을 찾을 때는 가장 작은 값에서 시작해야 어떤 점수든 갱신된다.
- **(4)** BOT이 둔 다음은 PLAYER 차례
- **(5)(6)** BOT(MAX)은 max, PLAYER(MIN)는 min

**(7)** 탐색이 끝난 뒤 둔 수를 되돌리지 않으면, 다음 후보 위치를 탐색할 때 이전에 놓은 말이 보드에 남아 있게 된다. 실제 게임과 다른 보드를 평가하게 되고, 결국 빈칸이 없어져 탐색이 틀어진다.

---

## Q22. Validation set과 test set (week5)

**정답:** F (역할이 바뀌어 있다)

| 집합           | 역할                                        |
|----------------|---------------------------------------------|
| Training set   | 모델을 학습(생성)                           |
| Validation set | 모델을 평가해 **가장 좋은 모델을 고름**     |
| Test set       | 고른 모델을 **마지막에 한 번** 평가(unseen) |

- Test set으로 모델을 고르면 test set에 맞춰진 모델이 되어, 처음 보는 데이터에서의 진짜 성능을 알 수 없다.

---

## Q23. Hill climbing (week2~3)

**정답:** ②

| 보기 | 판단 | 이유                                                                          |
|------|------|-------------------------------------------------------------------------------|
| ①    | X    | 경로와 방문 집합을 기록하지 않는다(local search). 기록하는 것은 global search |
| ②    | O    | 이웃이 현재보다 좋지 않으면 멈춤 → 목표에 못 갈 수 있음                       |
| ③    | X    | local minima 탈출은 global search(greedy best-first)의 장점                   |
| ④    | X    | 과거 이웃으로 돌아가지 않는다                                                 |

- Pseudo code: `if value[next] ≤ value[current] then return current`
- 장점은 메모리를 적게 쓰고 빠르다는 것이다.

---

## Q24. 이진 혼동 행렬 (week6)

**정답:** (1) TP 90, FP 10, FN 30, TN 370 (2) accuracy 0.92, precision 0.9, recall 0.75

| 실제 \ 예측 | 스팸  | 정상   |
|-------------|-------|--------|
| 스팸 (120)  | TP 90 | FN 30  |
| 정상 (380)  | FP 10 | TN 370 |

- FP = 스팸 예측 100 − TP 90 = 10, FN = 실제 스팸 120 − 90 = 30, TN = 500 − 90 − 10 − 30 = 370
- accuracy = (90 + 370) / 500 = 0.92
- precision = 90 / 100 = 0.9, recall = 90 / 120 = 0.75

**함정:** accuracy는 0.92로 높지만 스팸 4개 중 1개를 놓친다. 클래스 비율이 불균형할 때 accuracy만 보면 안 된다(강의: accuracy는 "when all classes are balanced").

---

## Q25. `loss.backward()` (week7)

**정답:** F

- `loss.backward()`: backpropagation으로 **gradient만 계산**
- `optimizer.step()`: 그 gradient로 **파라미터 갱신** (예: $W := W - \eta\,\partial L / \partial W$)
- 학습 과정: forward → loss → backward(gradient) → optimizer(update)

---

## Q26. 추론 규칙 (week4)

**정답:** ② Modus Tollens

- $P \to Q$ (비 → 땅 젖음), $\lnot Q$ (땅이 안 젖음) ⊢ $\lnot P$ (비 안 옴)
- Modus Ponens는 $P \to Q$, $P$ ⊢ $Q$ (전건 긍정)
- Modus Tollens는 대우($\lnot Q \to \lnot P$)에 Modus Ponens를 쓴 것과 같다.

---

## Q27. 결정 트리 해석 (week5)

**정답:** (1) (a) setosa (b) virginica (c) versicolor (d) virginica (2) 아래 참고

| 샘플 | Length ≤ 2.45 | Width ≤ 1.65 | 마지막 분기 | 결과       |
|------|---------------|--------------|-------------|------------|
| (a)  | 예            | -            | -           | setosa     |
| (b)  | 아니오        | 예           | 5.0 > 4.95  | virginica  |
| (c)  | 아니오        | 예           | 4.7 ≤ 4.95  | versicolor |
| (d)  | 아니오        | 아니오       | 4.5 ≤ 4.85  | virginica  |

**(2)** 결정 트리는 **불순도(Gini)를 가장 많이 줄이는** 규칙을 greedy하게 고른다. 분기 후 두 leaf의 **다수 클래스(majority class)는 같아도 불순도는 달라질 수 있다**. 예를 들어 한쪽에 versicolor가 일부 섞여 있고 다른 쪽은 순수 virginica처럼 나뉘면 불순도가 줄어들기 때문에 분기가 생긴다. 출력 클래스는 다수 클래스만 표시하므로 같아 보인다.

---

## Q28. Weighted A\* search (week2~3)

**정답:** (1) S(18) → B(11) → C(10) → G(10) (2) S-B-C-G, 비용 10 (A\*는 8)

| 단계 | 확장 (g, f) | 이웃 (g, f = g + 3h)     | 큐 (f)        |
|------|-------------|--------------------------|---------------|
| 1    | S (0, 18)   | A (2, 14), B (5, 11)     | B11, A14      |
| 2    | B (5, 11)   | C (7, 10), G (12, 12)    | C10, G12, A14 |
| 3    | C (7, 10)   | G: g 10 < 12 갱신 → f 10 | G10, A14      |
| 4    | G (10, 10)  | 목표 dequeue → 종료      |               |

- 확장한 노드 수: weighted A\* 4개, A\* 5개 → **더 적게 탐색**
- 비용: weighted A\* 10, A\* 8 → **최적이 아님**
- $h$에 가중치를 주면 목표 쪽으로 더 공격적으로 가서 빠르지만, A가 실제로 좋은 경로였는데도 $h$ 벌점 때문에 확장되지 않았다(Q45).

---

## Q29. MCTS의 playout (week3)

**정답:** F

- MCTS: leaf가 terminal이 아니면 자식 노드를 하나 이상 추가해 **트리를 확장**하고, 거기서부터 결과가 날 때까지 무작위로 둔다(playout).
- playout 중의 수는 **트리에 기록하지 않는다**(강의: "Do the random moves until the game is decided (but not recorded in the tree)"). 결과(승/패)만 위로 전달해 각 노드의 #wins / #runs를 갱신한다.
- 평균 utility = 승률 = $\#wins / \#runs$

---

## Q30. 단일층 퍼셉트론과 argmax (week6~7)

**정답:** (1) z = [−0.8, 0.04, 0.85], h = [0, 1, 1] (2) Versicolor, 동점 문제 (3) Virginica

**(1)**
- Setosa: $-0.8 \times 0.5 + (-1.2) \times 0 - 0.4 = -0.8$ → 0
- Versicolor: $0.1 \times 0.5 + (-0.05) \times 0 - 0.01 = 0.04$ → 1
- Virginica: $0.7 \times 0.5 + 1.3 \times 0 + 0.5 = 0.85$ → 1

**(2)** h = [0, 1, 1]에서 최댓값 1이 두 개다. `np.argmax`는 최댓값이 여러 개면 **처음 나온 인덱스**를 돌려주므로 1 → **Versicolor**
- 문제점: Heaviside는 0/1만 내므로 **얼마나 더 확신하는지(크기) 정보가 사라진다**. z는 Virginica(0.85)가 더 큰데도 순서 때문에 Versicolor가 선택된다.

**(3)** Softmax는 z의 크기를 유지한 확률로 바꾸므로 z가 가장 큰 **Virginica**를 고른다. 이것이 분류에 softmax를 쓰는 이유다.

---

## Q31. Naïve Bayes 계산 (week4)

**정답:** Yes ≈ 0.0333 (1/30), No = 0.0375 (3/80) → **No**

**클래스별 개수:** Yes 6개(3, 4, 6, 7, 9, 10), No 4개(1, 2, 5, 8)

| 확률             | Yes  | No   |
|------------------|------|------|
| $p(class)$       | 6/10 | 4/10 |
| $p(Sunny \mid)$  | 3/6  | 2/4  |
| $p(Cool \mid)$   | 4/6  | 1/4  |
| $p(Strong \mid)$ | 1/6  | 3/4  |

- Yes: $\frac{6}{10} \times \frac{3}{6} \times \frac{4}{6} \times \frac{1}{6} = \frac{72}{2160} = \frac{1}{30} \approx 0.0333$
- No: $\frac{4}{10} \times \frac{2}{4} \times \frac{1}{4} \times \frac{3}{4} = \frac{24}{640} = \frac{3}{80} = 0.0375$
- No가 더 크므로 **No**

**함정:** 조건부 확률의 분모는 **전체 10이 아니라 그 클래스의 개수**(Yes 6, No 4)다. 이 값들은 정규화하지 않은 점수라서 둘을 더해도 1이 되지 않는다. 비교만 하면 된다.

---

## Q32. Batch와 epoch (week7)

**정답:** (1) 784, 10 (2) 1,875번 (3) 18,750번 (4) 아래 참고

- **(1)** 28 × 28 = 784 픽셀 → 입력 784, 숫자 0~9 → 출력 10
- **(2)** 60,000 / 32 = 1,875 batch → batch마다 한 번 갱신
- **(3)** 1,875 × 10 = 18,750
- **(4)** Full-batch: (장점) 한 번에 계산해 계산이 빠르다 / (단점) 메모리를 많이 쓴다. 1 epoch에 갱신이 1번뿐이다.

---

## Q33. Uninformed search (week2)

**정답:** ① ③ ④ ⑥

| Uninformed (blind)         | Informed (heuristic)        |
|----------------------------|-----------------------------|
| BFS, DFS                   | Greedy best-first search    |
| Uniform-cost search        | A\* search                  |
| Iterative deepening search | Iterative-deepening A\*     |
|                            | Recursive best-first search |

- ⑥ Dijkstra's algorithm = uniform-cost search(CS 분야에서 부르는 이름)
- ⑦ Weighted A\*도 $h(n)$을 쓰므로 informed

**판단 기준:** "목표까지 얼마나 가까운지에 대한 단서($h(n)$)를 쓰는가?"

---

## Q34. Markov chain (week5)

**정답:** $\mathbf{x}^{(1)} = [0.9,\ 0.1]$, $\mathbf{x}^{(2)} = [0.86,\ 0.14]$, $\mathbf{x}^{(3)} = [0.844,\ 0.156]$

- $\mathbf{x}^{(t)} = \mathbf{x}^{(t-1)} P$ (행 벡터 × 행렬)
- $\mathbf{x}^{(3)}$: Sunny = $0.86 \times 0.9 + 0.14 \times 0.5 = 0.774 + 0.07 = 0.844$, Rainy = $0.86 \times 0.1 + 0.14 \times 0.5 = 0.086 + 0.07 = 0.156$
- 각 시점의 확률 합은 항상 1이다(검산).

---

## Q35. 이(inverse)는 동치가 아니다 (week4)

**정답:** F

- $P \to Q$와 동치인 것은 **대우(contraposition)** $\lnot Q \to \lnot P$다.
- $\lnot P \to \lnot Q$(이)는 동치가 아니다. 반례: $P = F$, $Q = T$이면 $P \to Q$는 참이지만 $\lnot P \to \lnot Q = T \to F$는 거짓이다.
- 예: "비가 오면 Harry는 안에 있다" ≢ "비가 안 오면 Harry는 밖에 있다"

---

## Q36. 3단 트리 alpha-beta pruning (week3)

**정답:** (1) 5 (2) 9, 0, −1

**왼쪽 MIN**
- 첫 MAX: 3, 5 → 5. MIN의 β = 5
- 둘째 MAX: 첫 단말 6 → 이 MAX의 α = 6 ≥ β = 5 → **9 가지치기** (MAX는 6 이상인데 MIN은 이미 5를 가졌으므로 이 MAX를 고르지 않음)
- 왼쪽 MIN = 5 → 루트 α = 5

**오른쪽 MIN**
- 첫 MAX: 1, 2 → 2. MIN의 β = 2
- α = 5 ≥ β = 2 → 오른쪽 MIN은 2 이하가 확정 → 루트는 5를 고를 것이므로 **둘째 MAX(0, −1) 전체 가지치기**

**루트** = max(5, ≤2) = **5**

---

## Q37. 손실 함수 (week7)

**정답:** ③ Huber loss / 정수 레이블 → ⑤, one-hot → ①

| 회귀                 | 분류                                       |
|----------------------|--------------------------------------------|
| MSE, RMSE, MSLE, MAE | Binary/Categorical cross-entropy (one-hot) |
| **Huber loss**       | Sparse categorical cross-entropy (정수)    |
|                      | Hinge loss, KL divergence                  |

- 손실 함수는 단순한 평가 지표가 아니라, 파라미터를 최적화하는 알고리즘의 입력이 된다.

---

## Q38. K-fold cross validation (week6)

**정답:** (1) training 800, testing 200 (2) 5번, 5개 성능의 평균

- 1,000개를 5개 fold(각 200개)로 무작위 분할 → 매번 4개 fold(800)로 학습, 1개 fold(200)로 평가
- **(3)** 장점: 한 번만 나누면 분할에 따라 성능이 너무 좋게/나쁘게 나올 수 있는데, 모든 데이터가 한 번씩 test에 쓰여 평가가 안정적이다. 단점: K번 학습하므로 시간이 K배 걸린다.

---

## Q39. 회귀와 stratify (week5 실습)

**정답:** F

- 회귀의 y(MedHouseVal)는 **연속적인 실수 값**이라 클래스가 없다. 그래서 실습 코드에서도 `stratify`를 쓰지 않는다("회귀는 클래스가 없으므로 stratify를 사용하지 않는다").
- `stratify`는 분류(Iris)에서 클래스 비율을 train/test에 똑같이 유지할 때 쓴다.

---

## Q40. Greedy best-first search (week2)

**정답:** (1) S → B → G, 경로 S-B-G, 비용 12 (2) 아래 참고

| 단계 | 확장 | 추가된 노드 (h) | 큐 (h)     |
|------|------|-----------------|------------|
| 1    | S    | A (4), B (2)    | B2, A4     |
| 2    | B    | C (1), G (0)    | G0, C1, A4 |
| 3    | G    | 목표 → 종료     |            |

**(2)** $f(n) = h(n)$만 보고 목표에 가까워 보이는 노드로 간다. 지금까지 쓴 비용 $g(n)$을 무시하므로 **빠르게 해를 찾지만 최적을 보장하지 않는다**(UCS 8 vs greedy 12).

---

## Q41. 1차 논리 (week4)

**정답:**
- (1) $\forall x\ \big(Student(x) \land \lnot Pass(x) \to Retake(x)\big)$
- (2) $Retake(Tom)$
- (3) constant symbol: Tom / predicate symbol: Student, Pass, Retake

- **(2)** x에 Tom을 대입하면 $Student(Tom) \land \lnot Pass(Tom) \to Retake(Tom)$. 전건이 지식 베이스에서 참이므로 Modus Ponens로 $Retake(Tom)$을 추론한다.
- 강의의 Socrates 예시($\forall x\ Human(x) \to Mortal(x)$, $Human(Socrates)$ ⊢ $Mortal(Socrates)$)와 같은 구조다.

---

## Q42. 순전파와 가중치 갱신 (week7)

**정답:** (1) 0.5, 0.6225, 0, 0.5 (2) 0.1112, 0.5278, 0.2230 (3) 0.5733

**(1)**
- $z_{1,0} = x_0 w_{1,0,0} + x_1 w_{1,1,0} = 1.0 \times 0.4 + 0.5 \times 0.2 = 0.5$ → $o_{1,0} = \frac{1}{1 + e^{-0.5}} \approx 0.6225$
- $z_{1,1} = x_0 w_{1,0,1} + x_1 w_{1,1,1} = 1.0 \times (-0.3) + 0.5 \times 0.6 = 0$ → $o_{1,1} = 0.5$

**(2)**
- $z_{2,0} = o_{1,0} w_{2,0,0} + o_{1,1} w_{2,1,0} = 0.6225 \times 0.5 + 0.5 \times (-0.4) \approx 0.1112$
- $\hat{y} = \text{sigmoid}(0.1112) \approx 0.5278$
- $L = (0.5278 - 1)^2 \approx 0.2230$

**(3)** Gradient descent: $W := W - \eta\,\dfrac{\partial L}{\partial W}$
- $w_{2,0,0} = 0.5 - 0.5 \times (-0.1465) = 0.5 + 0.0733 = 0.5733$
- gradient가 음수 → 이 가중치를 **키우면** 손실이 줄어든다는 뜻. 실제로 $\hat{y}$(0.53)가 정답(1)보다 작으므로 $o_{1,0}$에 곱해지는 가중치를 키워 출력을 올리는 방향이다.

**함정:** $w_{l,i,j}$의 인덱스는 (층, **출발** 뉴런, **도착** 뉴런)이다. $w_{1,1,0}$은 입력 1번 → 은닉 0번이다.

---

## Q43. 게임의 형식적 정의 (week3)

**정답:** ⑤

- $Utility(s, p)$는 **게임이 terminal 상태 s에서 끝났을 때** 플레이어 p에게 주는 **최종 점수**다(Tic-Tac-Toe: +1, 0, −1).
- 모든 상태에서 승리 가능성을 **추정**하는 것은 heuristic alpha-beta search의 **EVAL** 함수 역할이다(Q49).

---

## Q44. 학습 유형 (week5)

**정답:** (a) 강화 학습 (b) 비지도 학습(clustering) (c) 지도 학습 — 분류 (d) 지도 학습 — 회귀

| 상황 | 피드백                      | 유형             |
|------|-----------------------------|------------------|
| (a)  | 보상/처벌(승/패)만          | 강화 학습        |
| (b)  | 레이블 없음                 | 비지도 학습      |
| (c)  | 레이블(spam/ham) 있음, 범주 | 지도 학습 — 분류 |
| (d)  | 정답(집값) 있음, 연속 값    | 지도 학습 — 회귀 |

---

## Q45. Weighted A\* (week2~3)

**정답:** T

- $W > 1$이면 $h$가 커져 목표 쪽 노드를 더 강하게 선호 → 탐색 노드 수 감소(강의: "Faster!")
- 대신 실제 비용 $g$의 비중이 상대적으로 줄어 최적이 아닌 해를 찾을 수 있다. Q28에서 비용 10 경로를 찾았다(최적 8).

| 알고리즘          | $f(n)$                |
|-------------------|-----------------------|
| UCS               | $g(n)$                |
| Greedy best-first | $h(n)$                |
| A\*               | $g(n) + h(n)$         |
| Weighted A\*      | $g(n) + W \cdot h(n)$ |

---

## Q46. 행렬 shape (week7)

**정답:** (1) 32 × 784 (2) 784 × 128 (3) 32 × 128 (4) 128 × 10, 32 × 10

- $\mathbf{X}\mathbf{W} + \mathbf{b}$: $(s \times n)(n \times m) = s \times m$ ($s$: batch 크기)
- 은닉층: $(32 \times 784)(784 \times 128) = 32 \times 128$
- 출력층: $(32 \times 128)(128 \times 10) = 32 \times 10$
- $\mathbf{b}$는 같은 행을 batch 크기만큼 반복한 $32 \times m$으로 더해진다(강의: "Same").

---

## Q47. CPT의 conditioning case (week4)

**정답:** F

- conditioning case = 부모 값의 가능한 조합. Boolean 부모 $k$개 → $2^k$개
- 부모 3개 → $2^3 = 8$개 행
- 각 행의 확률(노드가 T일 확률 + F일 확률)은 합이 1이어야 한다.

---

## Q48. MAE / RMSE 코드 (week5 실습)

**정답:**
- (1) `abs(actual - predicted)`
- (2) `len(y_test)`
- (3) `(actual - predicted) ** 2.0`
- (4) `(total_squared_error / len(y_test)) ** 0.5`

- RMSE는 제곱 오차의 평균(MSE)에 제곱근을 씌운 것이다. `** 0.5`가 제곱근이다(`math.sqrt`도 가능).

---

## Q49. Heuristic alpha-beta tree search (week3)

**정답:** T

| Minimax       | Heuristic alpha-beta        |
|---------------|-----------------------------|
| Terminal test | Cutoff test (예: 고정 깊이) |
| UTILITY       | EVAL                        |

- $EVAL(s, p) = UTILITY(s, p)$ (terminal), 그 외에는 승리 가능성을 추정한 값
- 좋은 EVAL 조건: 실제 승리 가능성과 강하게 상관되어야 하고, 계산이 오래 걸리면 안 된다.

---

## Q50. 탐색 문제 용어 (week2)

**정답:** (1) agent (2) transition model, $result(s, a)$ (3) state space (4) solution (5) optimal solution

- 그 외 용어: state(환경이 있을 수 있는 상태), initial state(에이전트가 시작하는 상태), $actions(s)$(상태 s에서 할 수 있는 행동 집합), action cost $c(s, a, s')$
