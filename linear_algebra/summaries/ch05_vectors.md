# Chapter 05. 벡터

> 원본: `chapters/ch05_vectors.pdf` (책 308–349쪽)

---

## 5.1 벡터의 개념과 표현

- **스칼라(scalar)**: 크기(magnitude)만 있는 양. 압력, 속력(speed), 질량, 전하, 비열, 저항, 원의 지름, 면적, 체적 등. 보통 $r, s, t$ 같은 소문자 이탤릭체로 쓴다.
- **벡터(vector)**: **크기 + 방향**을 함께 가진 양. 속도(velocity), 힘(force), 가속도(acceleration) 등. 보통 $\mathbf{u}, \mathbf{v}, \mathbf{w}$ 같은 굵은 소문자로 쓴다.
  - 스칼라 → 크기 / 벡터 → 크기 + 방향
  - 예: 속력은 빠르기만, 속도는 방향과 빠르기를 모두 가진 양
  - 어원: 라틴어 'vehere'(어디로 이동시킨다)

### 5.1.1 벡터의 개념과 표기법

#### (1) 그래프에 의한 표기법

- 벡터는 **화살표(arrow)** 로 표기한다. 화살표의 방향이 벡터의 방향(direction), 길이가 크기(magnitude)다.
  - **시점(initial point, tail)**: 화살표의 시작점 P
  - **종점(terminal point, head)**: 화살표가 끝나는 점 Q
  - 표기: $\overrightarrow{PQ}$ 또는 $\mathbf{a}, \mathbf{b}, \mathbf{u}, \mathbf{v}$
- **유향선분(directed segment)**: 점 P에서 Q까지 방향을 가진 선분 $\overrightarrow{PQ}$. 모든 벡터는 유향선분으로 나타낼 수 있고 그 역도 성립하므로 사실상 같은 개념이다.
- 두 벡터 $\overrightarrow{PQ}$, $\overrightarrow{RS}$ 가 똑같은 크기와 방향을 가지면 위치와 관계없이 **동치(equivalent)** 다.
- 시점과 종점의 위치와 관계없이 크기와 방향만 생각하는 벡터를 **기하벡터(geometric vector)** 라 한다. $\mathbf{u} = \mathbf{v}$ 로 나타낸다.

#### (2) 좌표(coordinate)에 의한 표기법

- 원점 $(0, 0, 0)$ 에서 좌표 $(x, y, z)$ 로 향하는 벡터를 **위치벡터(position vector)** 라 한다. $\mathbf{u} = (x, y, z)$
  - $(\ )$ 는 정해진 순서대로만 쓰는 **순서쌍(ordered pair)** 이다.
  - $x, y, z$ 를 벡터의 **성분(component)** 이라 한다.
- $n$차원 공간 $R^n$ 으로 확장하면:
  - **행벡터(row vector) 표기**: $\mathbf{u} = (x_1, x_2, \dots, x_n)$
  - **열벡터(column vector) 표기**: $\mathbf{u} = \begin{bmatrix} x_1 \\ \vdots \\ x_n \end{bmatrix}$
- 3차원에서는 보통 **오른손 법칙**에 따른 **오른손 좌표계**를 쓴다.

### 5.1.2 평면상의 벡터

- 평면상의 벡터는 원점 O에서 $P(x, y)$ 로의 벡터 $\overrightarrow{OP}$ 다.
- **정의 5-1 (벡터의 상등)**: 평면상의 벡터 $\mathbf{u} = \begin{bmatrix} x \\ y \end{bmatrix}$ 는 $2 \times 1$ 행렬이다. 평행이동해서 완전히 겹쳐질 때, 즉 크기와 방향이 같을 때 두 벡터가 **같다(equal)** 라고 하고 $\mathbf{u} = \mathbf{v}$ 로 쓴다.
  - 성분으로 보면 $x_1 = x_2$, $y_1 = y_2$ 이면 같다.
  - 예: $\begin{bmatrix} a+b \\ 2 \end{bmatrix} = \begin{bmatrix} 4 \\ a-b \end{bmatrix}$ → $a = 3, b = 1$
- 예제 5-1: (1) $a - b = 4, a + b = 2$ → $a = 3, b = -1$ / (2) $x = y - 2, 2y + 1 = 3$ → $x = -1, y = 1$
- 시점이 원점이 아닌 $P(x, y)$, 종점이 $Q(x', y')$ 인 벡터 $\overrightarrow{PQ}$ 의 성분은 $(x' - x,\ y' - y)$ 다.
  - $\overrightarrow{PQ}$ 와 $\overrightarrow{QP}$ 는 **방향이 반대**다.
  - 예: $P_1(3,2) \to Q_1(5,5)$, $P_2(0,0) \to Q_2(2,3)$, $P_3(-3,1) \to Q_3(-1,4)$ 는 모두 같은 벡터 $(2, 3)$ 이다.
- 예제 5-3: 종점이 $(2, 1)$ 이고 벡터가 $(3, 4)$ → 시점 $= (2-3, 1-4) = (-1, -3)$

### 5.1.3 벡터의 크기와 기하학적 표현

#### (1) 벡터의 크기

- **정의 5-2**: $\mathbf{u} = (a, b)$ 의 **크기(magnitude)**, **길이(length)**, **노름(norm)**: 피타고라스 정리에 따라

$$
\|\mathbf{u}\| = \sqrt{a^2 + b^2}
$$

  - 항상 $\|\mathbf{u}\| \ge 0$, 영벡터일 때만 $\|\mathbf{u}\| = 0$
  - 예: $\mathbf{u} = (1, -2)$ → $\|\mathbf{u}\| = \sqrt{5}$
- 벡터 $\mathbf{u} = (a, b)$ 의 **방향**은 x축의 양의 방향에서 시계 반대 방향으로 잰 라디안(radian) 각 $\theta$ 다. $a \neq 0$ 이면 $\tan\theta = \frac{b}{a}$
- **정의 5-3 (영벡터, zero vector)**: 모든 성분이 0인 벡터 $\mathbf{0}$. 시점과 종점이 일치하는 특수한 벡터로 크기가 0이다.
  - $\mathbf{u} + \mathbf{0} = \mathbf{u}$, $\mathbf{u} + (-1)\mathbf{u} = \mathbf{0}$
  - $(-1)\mathbf{u} = -\mathbf{u}$ 는 $\mathbf{u}$와 반대 방향인 벡터다.

#### (2)~(4) 차원별 벡터

- **2차원**: 유클리드(Euclid) 공간 $R^2$. $\mathbf{v} = (v_1, v_2)$, $\|\mathbf{v}\| = \sqrt{v_1^2 + v_2^2}$. 예: $(3, -4)$ → 5
- **3차원**: $R^3$. $\|\mathbf{v}\| = \sqrt{v_1^2 + v_2^2 + v_3^2}$. 예: $(2, 3, 4)$ → $\sqrt{29}$
- **$n$차원**: $R^n$. $\|\mathbf{v}\| = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2}$. 예: $(-2, 1, 3, -1, 4, 2, 1)$ → $\sqrt{36} = 6$
- $R$은 실수를 뜻한다. $R^1$은 직선, $R^2$는 평면, $R^3$은 3차원 공간이다. $R^n$은 $n$개의 순서쌍으로 이루어진 벡터라고 보면 된다.

[보충] 두 벡터 $\mathbf{u}, \mathbf{v}$ 사이의 **거리**는 $\|\mathbf{u} - \mathbf{v}\|$ 로 구한다(연습문제 5.1의 주관식 3, 4번 유형). 예: $\mathbf{u} = (-1, 4, 2), \mathbf{v} = (0, 8, 1)$ → $\|\mathbf{u} - \mathbf{v}\| = \sqrt{1 + 16 + 1} = \sqrt{18} = 3\sqrt{2}$

### 5.1.4 단위벡터와 단위좌표벡터

#### (1) 단위벡터

- **정의 5-4**: $R^n$에서 **크기가 1인 벡터**를 **단위벡터(Unit vector)** $\mathbf{e}$ 라 한다.
  - $\mathbf{v}$와 방향이 같은 단위벡터:

$$
\mathbf{e} = \frac{1}{\|\mathbf{v}\|}\mathbf{v}
$$

  - 임의의 벡터를 그 크기로 나누면 항상 단위벡터가 된다(**정규화**).
- 예제 5-4: $\mathbf{u} = (2, -3)$ → $\mathbf{e} = \frac{1}{\sqrt{13}}(2, -3)$ / $\mathbf{v} = (2, 1, -3)$ → $\mathbf{e} = \frac{1}{\sqrt{14}}(2, 1, -3)$
- 예제 5-5: $\mathbf{v} = 3\mathbf{i} + 4\mathbf{j}$ → $\|\mathbf{v}\| = 5$ → $\mathbf{u} = \frac{3}{5}\mathbf{i} + \frac{4}{5}\mathbf{j}$
- $R^2$의 전형적인 단위벡터: 원점에서 단위원 $x^2 + y^2 = 1$ 까지의 벡터 / $R^3$: 원점에서 구(sphere)까지의 벡터

#### (2) 단위좌표벡터

- **단위좌표벡터(Unit coordinate vector)**: $R^2$에서 $\mathbf{i} = (1, 0)$, $\mathbf{j} = (0, 1)$
  - $\mathbf{v} = (a, b) = a(1, 0) + b(0, 1) = a\mathbf{i} + b\mathbf{j}$
  - $a$는 **수평성분**, $b$는 **수직성분**이다.
  - $\mathbf{i}, \mathbf{j}$ 를 벡터공간 $R^2$의 **기저벡터(basis vector)** 라 한다.
- $R^3$: $(a_1, a_2, a_3) = a_1\mathbf{i} + a_2\mathbf{j} + a_3\mathbf{k}$. 예: $(3, 2, -1) = 3\mathbf{i} + 2\mathbf{j} - \mathbf{k}$
- 정리
  - **단위벡터**: 크기가 1인 벡터
  - **단위좌표벡터**: 좌표상의 단위벡터임을 강조한 것
  - **기저벡터**: $\mathbf{i}, \mathbf{j}, \mathbf{k}$ 처럼 $x, y, z$축 역할을 하는 단위벡터
- 예제 5-6: $\mathbf{u} = (1, 2, 5)$ → $\frac{1}{\sqrt{30}}(1, 2, 5)$
- 예제 5-7: 시점 $P_1(-5, -3)$, $\overrightarrow{P_1P_2} = 4\mathbf{i} + 5\mathbf{j}$ → 종점 $P_2 = (-1, 2)$
- 벡터는 **신경망의 입력과 연결강도** 등을 표현하는 데 유용하다. 8장의 내적과 외적의 바탕이 된다.

---

## 5.2 벡터의 연산

### 5.2.1 벡터의 합과 차

#### (1) 벡터의 합

- **정의 5-5**: $R^n$에서 **벡터의 합(sum)** 은 대응하는 성분끼리 더한 것이다.

$$
\mathbf{v} + \mathbf{w} = (v_1 + w_1, v_2 + w_2, \dots, v_n + w_n)
$$

- 기하학적 의미
  - **평행사변형법**: 두 벡터로 만든 평행사변형의 **대각선**
  - **삼각형법**: $\mathbf{u}$의 종점에 $\mathbf{v}$의 시점이 오도록 평행이동한 뒤, $\mathbf{u}$의 시점에서 $\mathbf{v}$의 종점까지 잇는다.
- 예제 5-8: $(2, 3) + (3, -4) = (5, -1)$, $(2, 3, -1) + (3, -4, 2) = (5, -1, 1)$

#### (2) 벡터의 차

- **정의 5-7**: **벡터의 차(difference)** 또는 **뺄셈(subtraction)**:

$$
\mathbf{v} - \mathbf{w} = (v_1 - w_1, v_2 - w_2, \dots, v_n - w_n)
$$

- 벡터의 차는 합으로 바꾸어 쓰면 편리하다: $\mathbf{u} - \mathbf{v} = \mathbf{u} + (-\mathbf{v})$
- 기하학적으로 $\mathbf{v} - \mathbf{w}$ 는 **$\mathbf{w}$의 종점에서 $\mathbf{v}$의 종점으로** 향하는 벡터다.
- 예제 5-9: $(2, 3) - (3, -4) = (-1, 7)$, $(2, 3, -1) - (3, -4, 2) = (-1, 7, -3)$

### 5.2.2 벡터의 스칼라 곱

- **정의 5-8**: 벡터 $\mathbf{u}$와 스칼라 $\alpha$의 곱 $\alpha\mathbf{u} = \begin{bmatrix} \alpha u_1 \\ \alpha u_2 \end{bmatrix}$ 를 **스칼라 곱(scalar product)** 이라 한다.
  - $\alpha > 0$: $\mathbf{u}$와 **같은 방향**, $\alpha < 0$: **반대 방향**
  - 크기: $\|\alpha\mathbf{u}\| = |\alpha| \cdot \|\mathbf{u}\|$
  - $\alpha = 0$ 이거나 $\mathbf{u} = \mathbf{0}$ 이면 $\alpha\mathbf{u} = \mathbf{0}$. $(-1)\mathbf{u} = -\mathbf{u}$
- 예제 5-10: $\mathbf{u} = (2, -3)$, $\alpha = 2 \Rightarrow (4, -6)$, $\beta = -3 \Rightarrow (-6, 9)$
- 예제 5-11: $\mathbf{u} = (5, 3, -4), \mathbf{v} = (-1, 5, 2), \mathbf{w} = (3, -1, -2)$
  - $3\mathbf{u} = (15, 9, -12)$, $5\mathbf{u} - 2\mathbf{v} = (27, 5, -24)$, $-2\mathbf{u} + 4\mathbf{v} - 3\mathbf{w} = (-23, 17, 22)$

[보충] 이름이 비슷해서 헷갈리기 쉽다. **스칼라 곱(scalar product/scalar multiplication)** 은 "스칼라 × 벡터 = 벡터"다. 8장의 **내적(inner product, dot product)** 은 "벡터 · 벡터 = 스칼라"다. 일부 교재는 내적을 "scalar product"라고도 부르니 문맥으로 구분할 것.

### 5.2.3 벡터의 성질

**정리 5-1**: $R^2$나 $R^3$의 벡터 $\mathbf{u}, \mathbf{v}, \mathbf{w}$, 영벡터 $\mathbf{0}$, 스칼라 $\alpha, \beta$ 에 대해

| 식 | 이름 |
|---|---|
| $\mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u}$ | 덧셈에 대한 교환법칙 |
| $\mathbf{u} + (\mathbf{v} + \mathbf{w}) = (\mathbf{u} + \mathbf{v}) + \mathbf{w}$ | 덧셈에 대한 결합법칙 |
| $\mathbf{u} + \mathbf{0} = \mathbf{u}$ | 덧셈에 관한 항등원 |
| $\mathbf{u} + (-\mathbf{u}) = \mathbf{0}$ | 덧셈에 관한 역원 |
| $\alpha(\mathbf{u} + \mathbf{v}) = \alpha\mathbf{u} + \alpha\mathbf{v}$ | 분배 |
| $(\alpha + \beta)\mathbf{u} = \alpha\mathbf{u} + \beta\mathbf{u}$ | 분배 |
| $\alpha(\beta\mathbf{u}) = (\alpha\beta)\mathbf{u}$ | 결합 |
| $1\mathbf{u} = \mathbf{u}$ | 곱셈에 대한 항등원 |
| $0\mathbf{u} = \mathbf{0}$ | 영벡터 |

- 증명: 성분이 모두 실수이므로 $u_1 + v_1 = v_1 + u_1$ 등이 성립한다 → $\mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u}$

[보충] 이 성질들은 6장에서 **벡터공간의 공리**로 그대로 쓰인다. 즉 6장의 벡터공간은 "이 성질들을 만족하는 집합"으로 일반화한 것이다.

### 5.2.4 벡터의 응용

- **(1) 로봇의 위치**: $\mathbf{a}, \mathbf{b}, \mathbf{c}, \mathbf{d}$ 로 차례로 움직여 X에서 Y로 이동했다면 위치는 단 하나의 벡터 $\mathbf{p} = \mathbf{a} + \mathbf{b} + \mathbf{c} + \mathbf{d}$ 로 알 수 있다.
- **(2) 교량 건설**: 중앙 탑(tower)과 다리 옆 케이블 사이의 힘 벡터를 계산해 안전하게 설계한다.

---

## 5.3 MATLAB에 의한 연산

- 벡터 입력: `u=[2; 3]; v=[3; -4];`
- 합 `u+v`, 차 `u-v`, 스칼라 곱 `3*u`, 선형결합 `5*u-2*v`

---

## 벡터의 생활 속 응용 (책 348쪽)

- 물리학에서 두 물체 사이의 이동이나 상호작용을 나타내는 척도
- 일이나 에너지 같은 물리량을 벡터로 나타내 계산을 간편하게 함
- 자연법칙을 벡터와 스칼라로 표현
- 네트워크 분석, 경로 탐색
- 컴퓨터 그래픽
- 신경망의 입력과 연결강도 표현

---

## 핵심 정리

- 스칼라 = 크기 / 벡터 = 크기 + 방향
- 시점 $P(x, y)$, 종점 $Q(x', y')$ → $\overrightarrow{PQ} = (x' - x, y' - y)$
- 크기(노름): $\|\mathbf{v}\| = \sqrt{v_1^2 + \cdots + v_n^2}$
- 단위벡터: $\mathbf{e} = \mathbf{v} / \|\mathbf{v}\|$ (크기 1, 방향은 $\mathbf{v}$와 같음)
- 기저벡터: $\mathbf{i} = (1,0,0), \mathbf{j} = (0,1,0), \mathbf{k} = (0,0,1)$
- 합·차·스칼라 곱은 **성분별 계산**
- $\alpha > 0$ 이면 같은 방향, $\alpha < 0$ 이면 반대 방향, 크기는 $|\alpha|$배
