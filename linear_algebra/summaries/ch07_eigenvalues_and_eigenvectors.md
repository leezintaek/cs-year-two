# Chapter 07. 고유값과 고유벡터

> 원본: `chapters/ch07_eigenvalues_and_eigenvectors.pdf` (책 390–425쪽)

---

## 7.1 고유값과 고유벡터

### 7.1.1 특성다항식과 고유값

- **정의 7-1**: $A$가 $n \times n$ 행렬이고 $I$가 항등행렬일 때, 선형시스템

$$
A\mathbf{x} = \lambda\mathbf{x}
$$

  에서 **$\mathbf{x} \neq \mathbf{0}$ 인 해가 존재하기 위한 필요충분조건**은 $|A - \lambda I| = 0$ 이다.

[보충] 이유: $A\mathbf{x} = \lambda\mathbf{x}$ 를 $(A - \lambda I)\mathbf{x} = \mathbf{0}$ 으로 옮기면 동차선형시스템이 된다. 이 시스템이 자명해 $\mathbf{x} = \mathbf{0}$ 말고 다른 해(비자명해)를 가지려면 $A - \lambda I$ 가 **역행렬을 갖지 않아야** 한다. 즉 $\det(A - \lambda I) = 0$ 이어야 한다. 역행렬이 있으면 $\mathbf{x} = (A - \lambda I)^{-1}\mathbf{0} = \mathbf{0}$ 뿐이기 때문이다.

- **정의 7-2**: $n \times n$ 행렬 $A$에 대해

$$
\text{Det}(A - \lambda I) = \begin{vmatrix} a_{11} - \lambda & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} - \lambda & \cdots & a_{2n} \\ \vdots & & \ddots & \vdots \\ a_{n1} & a_{n2} & \cdots & a_{nn} - \lambda \end{vmatrix}
$$

  - 이를 $A$의 **특성다항식(characteristic polynomial)** 또는 **고유다항식**이라 한다.
  - $p(\lambda) = |A - \lambda I| = 0$ 을 **특성방정식(characteristic equation)** 또는 **고유방정식**이라 한다. $p(\lambda)$ 는 $\lambda$에 관한 $n$차 다항식이다.
  - 특성방정식의 근(root) $\lambda$ 를 **고유값(eigen value)** 이라 한다.
  - 고유값 $\lambda$에 대한 $\mathbf{x}$ ($n \times 1$ 행렬)를 **고유벡터(eigen vector)** 라 한다.
  - 한 고유값에 대한 고유벡터들의 집합을 **고유공간(eigen space)** 이라 한다.
  - 주어진 행렬에서 모든 고유값과 고유벡터를 구하는 것을 **고유값 문제(eigen value problem)** 라 한다.
- **예제 7-1**: $A = \begin{bmatrix} 1 & 2 \\ 4 & 3 \end{bmatrix}$, $\mathbf{x} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$ → $A\mathbf{x} = \begin{bmatrix} 5 \\ 10 \end{bmatrix} = 5\mathbf{x}$ → 고유값 5, 고유벡터 $(1, 2)$
- **예제 7-2**: $A = \begin{bmatrix} 3 & 0 \\ 8 & -1 \end{bmatrix}$, $\mathbf{x} = (1, 2)$ → $A\mathbf{x} = (3, 6) = 3\mathbf{x}$ → 고유값 3
- 고유값은 **정방행렬일 경우에만** 정의된다.
  - 항등행렬 $I$는 $I\mathbf{x} = 1\mathbf{x}$ 이므로 $\lambda = 1$ 이 유일한 고유값이다. 영벡터가 아닌 모든 벡터가 $I$의 고유벡터다.
  - 이 책에서는 **실수인 고유값**만 다룬다.
- **정의 7-3 (중복 해)**: 어느 고유값 $\lambda$가 특성다항식의 해로 $k$번($k \ge 2$) 나타나면 $\lambda$를 **중복 해(multiplicity solution)** 라 한다.
  - 예: $A = I_2$ → $(1 - \lambda)^2 = 0$ → $\lambda_1 = \lambda_2 = 1$ (중복 해)

#### 고유값과 고유벡터의 의미

- $A\mathbf{x} = \lambda\mathbf{x}$: 벡터 $\mathbf{x}$에 행렬 $A$를 곱한 결과가 **$\lambda$배 한 것과 같다**.
- **고유값의 의미**: 선형변환 후에 고유벡터의 **크기가 변하는 비율** $\lambda$
- **고유벡터의 의미**: 선형변환이 일어난 뒤 **크기만 $\lambda$만큼 변하고, 방향은 전혀 변하지 않는**(같은 직선 위에 있는) 영벡터가 아닌 벡터
- eigen: 독일어로 '고유한', '특징적인'이라는 뜻. 수학자 힐베르트가 처음 이 의미로 썼다.

### 7.1.2 고유값과 고유벡터 구하기

1. $\text{Det}(A - \lambda I)$ 를 구한다.
2. 특성다항식 $= 0$ 의 근을 구하면 **고유값**이 된다.
3. 각 고유값에 대해 $(A - \lambda I)\mathbf{x} = \mathbf{0}$ 을 풀어 **고유벡터**를 구한다.

- **예제 7-3**: $A = \begin{bmatrix} 2 & 3 \\ 3 & -6 \end{bmatrix}$
  - $\text{Det}(A - \lambda I) = (2 - \lambda)(-6 - \lambda) - 9 = \lambda^2 + 4\lambda - 21 = (\lambda - 3)(\lambda + 7)$ → 고유값 **3, −7**
- **예제 7-4**: $A = \begin{bmatrix} 3 & 2 \\ 3 & -2 \end{bmatrix}$
  - $\lambda^2 - \lambda - 12 = (\lambda - 4)(\lambda + 3) = 0$ → 고유값 4, −3
  - $\lambda = 4$: $(A - 4I)\mathbf{x} = \mathbf{0}$ → $-x_1 + 2x_2 = 0$ → $x_1 = 2x_2$ → 고유벡터 $\begin{bmatrix} 2 \\ 1 \end{bmatrix}$
  - $\lambda = -3$: $6x_1 + 2x_2 = 0$ → $x_2 = -3x_1$ → 고유벡터 $\begin{bmatrix} 1 \\ -3 \end{bmatrix}$
- **예제 7-5** ($3 \times 3$): $A = \begin{bmatrix} 3 & -1 & -1 \\ -12 & 0 & 5 \\ 4 & -2 & -1 \end{bmatrix}$
  - 1행에 대해 여인수 전개: $-\lambda^3 + 2\lambda^2 + \lambda - 2 = -(\lambda + 1)(\lambda - 1)(\lambda - 2) = 0$ → 고유값 −1, 1, 2
  - 각 $\lambda$에 대해 $A - \lambda I$ 를 기약 행 사다리꼴로 바꿔서 푼다.
  - $\lambda = -1$ → $(1, 2, 2)$, $\lambda = 1$ → $(-3, 1, -7)$, $\lambda = 2$ → $(-1, 1, -2)$
- 주의: 고유값을 구하기 위해 **미리 $A$에 행 연산을 하면 전혀 다른 고유값이 나온다.** 고유값을 구한 **후** 고유벡터를 구할 때는 행 연산을 하면 계산이 쉬워진다.

#### 고유벡터 구하기 팁 (만화 내용)

- $x_1 = -2x_2$ 같은 결과가 나오면 $x_2 = 1$ 로 놓고 $\begin{bmatrix} -2 \\ 1 \end{bmatrix}$ 을 고유벡터로 쓴다.
- 일반적으로 쓰면 $\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = x_2\begin{bmatrix} -2 \\ 1 \end{bmatrix}$ ($x_2 \neq 0$) 이므로 **$\begin{bmatrix} -2 \\ 1 \end{bmatrix}$ 의 배수**가 모두 고유벡터다.
- 분수가 나오면 적당한 수를 곱해 정수로 만든다: $\begin{bmatrix} -1 \\ \frac{1}{3} \end{bmatrix} \times 3 = \begin{bmatrix} -3 \\ 1 \end{bmatrix}$
- 고유벡터에 **0이 아닌 수를 곱하면 언제나 고유벡터**다.
- 고유값마다 선형독립인 고유벡터가 1개 이상 있다. 행렬의 크기만큼 구하면 된다.

---

## 7.2 고유값의 성질과 응용

### 7.2.1 고유값의 성질

- **정리 7-1**: 행렬 $A$의 고유값이 $\lambda_1, \lambda_2, \dots, \lambda_n$ 일 때
  1. **고유값의 합 = 대각합(trace)**: $\lambda_1 + \lambda_2 + \cdots + \lambda_n = \text{trace}(A)$
  2. **고유값의 곱 = 행렬식**: $\lambda_1 \cdot \lambda_2 \cdots \lambda_n = \text{Det}(A)$
  3. **$A^T$의 고유값**은 원래의 고유값과 같다: $\lambda_1, \dots, \lambda_n$
  4. **$A^{-1}$의 고유값**(역행렬이 존재할 때): $\frac{1}{\lambda_1}, \frac{1}{\lambda_2}, \dots, \frac{1}{\lambda_n}$
  5. **$kA$의 고유값**: $k\lambda_1, k\lambda_2, \dots, k\lambda_n$
  6. **$A^k$의 고유값** ($k$는 양의 정수): $\lambda_1^k, \lambda_2^k, \dots, \lambda_n^k$
- **정리 7-2 (삼각행렬)**: 삼각행렬의 특성방정식은 $p_A(\lambda) = (a_{11} - \lambda)(a_{22} - \lambda)\cdots(a_{nn} - \lambda) = 0$ 이다. 따라서 **대각원소 $a_{11}, a_{22}, \dots, a_{nn}$ 이 고유값**이다.
  - 예: $\begin{bmatrix} 4 & 1 \\ 0 & -5 \end{bmatrix}$ → 고유값 4, −5
- **예제 7-6**: $A = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 2 & 5 \\ 0 & 0 & -1 \end{bmatrix}$ (상부삼각) → 0, 2, −1 / $B = \begin{bmatrix} 4 & 0 & 0 \\ 0 & 0 & 0 \\ 1 & 0 & -3 \end{bmatrix}$ (하부삼각) → 4, 0, −3
- **정리 7-3 (고유벡터의 선형독립)**
  1. $\lambda$가 중복 해가 아니면, $\lambda$에 대응하는 선형독립인 고유벡터는 **유일**하다.
  2. $n \times n$ 행렬의 **서로 다른 고유값**에 대응하는 고유벡터들은 **선형독립**이다.
  3. $n \times n$ 행렬 $A$가 $n$개의 서로 다른 고유값을 가지면, $A$는 $n$개의 선형독립인 고유벡터를 가진다.
- **예제 7-7**: $A = \begin{bmatrix} 5 & 1 \\ 7 & -1 \end{bmatrix}$ → $\text{trace} = 4$, $\text{Det} = -12$
  - $\lambda^2 - 4\lambda - 12 = (\lambda + 2)(\lambda - 6) = 0$ → $\lambda = -2, 6$
  - $-2 + 6 = 4 = \text{trace}(A)$, $(-2)(6) = -12 = \text{Det}(A)$ ✓
- **정리 7-4 (동치 명제)**: $A$가 $n \times n$ 행렬이고 $\lambda$가 스칼라일 때 다음은 모두 동치다.
  1. $\lambda$가 $A$의 고유값이다.
  2. $(A - \lambda I)\mathbf{x} = \mathbf{0}$ 은 비자명해를 가진다.
  3. $A - \lambda I$ 는 비가역적이다.
  4. $\text{Det}(A - \lambda I) = 0$

[보충] $2 \times 2$ 행렬의 특성다항식은 trace와 Det만으로 바로 쓸 수 있다: $\lambda^2 - \text{trace}(A)\lambda + \text{Det}(A) = 0$. 연습문제 7.2의 "$\text{trace}(A) = 8, \text{Det}(A) = 12$ 일 때 고유값" 같은 문제는 $\lambda^2 - 8\lambda + 12 = 0$ → $\lambda = 2, 6$ 으로 바로 풀린다. 또 $\text{Det}(A) = 0$ 이면 고유값 중에 0이 있다는 뜻이므로 **"0이 고유값 ⟺ $A$가 비가역"** 도 함께 기억할 것.

### 7.2.2 닮은행렬과 고유값

- **정의 7-4**: 행렬 $A, B, C$가 모두 $n \times n$ 이고 $B = C^{-1}AC$ 가 성립하면 $A$와 $B$를 **닮은행렬(similar matrix)** 이라 한다.
- **예제 7-8**: $A = \begin{bmatrix} 2 & 1 \\ 0 & -1 \end{bmatrix}$, $B = \begin{bmatrix} 4 & -2 \\ 5 & -3 \end{bmatrix}$, $C = \begin{bmatrix} 2 & -1 \\ -1 & 1 \end{bmatrix}$
  - $CB = AC = \begin{bmatrix} 3 & -1 \\ 1 & -1 \end{bmatrix}$ 이고 $\text{Det}(C) = 1 \neq 0$ 이므로 $C$는 가역 → $B = C^{-1}AC$ → 닮은행렬
- **예제 7-9**: $3 \times 3$ 에서 $C$와 $C^{-1}$ 을 구해 $C^{-1}AC = B$ 를 직접 확인한다.
- **정리 7-5**: $A$와 $B$가 닮은행렬이면 **같은 고유값**을 가진다.
- **예제 7-10**: 예제 7-8의 $A, B$ → 둘 다 $(\lambda - 2)(\lambda + 1) = 0$ → 고유값 2, −1로 같다.

[보충] 닮은행렬은 같은 선형변환을 **다른 기저**로 표현한 것이다. 그래서 고유값뿐만 아니라 trace, 행렬식, rank도 같다. 특히 $C$의 열을 $A$의 고유벡터로 잡으면 $C^{-1}AC$ 가 고유값을 대각선에 가진 **대각행렬**이 된다. 이것이 **대각화(diagonalization)** 이며 $A^k$ 계산 등에 쓰인다.

### 7.2.3 고유값과 고유벡터의 응용

- $A\mathbf{x} = \lambda\mathbf{x}$ 의 의미: $\mathbf{x}$가 회전 같은 변환을 거치지 않고 **단지 스칼라 값을 곱한 결과**만 나타낸다. 즉 $\mathbf{x} \neq \mathbf{0}$ 일 때 $A\mathbf{x}$ 와 $\mathbf{x}$ 는 **같은 직선 위**에 있다.
  - $A\mathbf{x} = 2\mathbf{x}$: 같은 방향으로 2배
  - $A\mathbf{x} = -\frac{3}{2}\mathbf{x}$: 반대 방향으로 $\frac{3}{2}$배
- **예제 7-11**: $A = \begin{bmatrix} 1 & 6 \\ 5 & 2 \end{bmatrix}$, $\mathbf{u} = (6, -5)$, $\mathbf{v} = (3, -2)$
  - $A\mathbf{u} = (-24, 20) = -4\mathbf{u}$ → $\mathbf{u}$는 고유값 −4에 대응하는 고유벡터
  - $A\mathbf{v} = (-9, 11) \neq \lambda\mathbf{v}$ → $\mathbf{v}$는 고유벡터가 **아니다** ($A\mathbf{v}$ 가 $\mathbf{v}$와 같은 직선 위에 있지 않음)
- 응용 분야: 진동계, 양자역학, 전기계, 화학반응, 기계응력 등의 공학 분야와 새로운 물리학적 운동 방정식 모델 개발. 행렬의 복잡한 연산을 간단하게 하고, 선형 $n$차 연립 미분방정식의 일반해와 비선형 문제에도 쓰인다. 사회과학 등에서도 쓰인다.
  - 특히 **진동 문제**의 고유진동수나 $x, y, z$ 방향의 응력 등을 쉽게 구할 수 있다. 예: 양쪽 벽 사이에 걸린 3개의 스프링에 작용하는 힘과 늘어나는 길이
- 고유값과 고유벡터는 **인공지능 중 신경망**에도 쓰인다. 특히 **푸리에(Fourier) 행렬** 등은 수준 높은 선형대수학에서 다룬다.

---

## 7.3 MATLAB에 의한 연산

- 특성다항식: `poly(A)` → 예: `A=[2, 3; 3, -6]` → `1 4 -21` ($\lambda^2 + 4\lambda - 21$)
- 고유값: `eig(A)` → `-7, 3`
- 고유값과 고유벡터를 함께 구하기: `[X, landa] = eig(A)`
  - MATLAB은 고유벡터를 **크기 1로 정규화**해서 보여 준다. 성분의 비는 같다.
  - 예: $\lambda = 4$ 의 고유벡터 `[0.8944; 0.4472]` = 사실상 $(2, 1)$, $\lambda = -3$ 의 `[-0.3162; 0.9487]` = 사실상 $(1, -3)$ (부호 반전도 같은 고유벡터)
- 고유값의 **순서는 상관없다**. 다만 각 고유값과 그 고유벡터의 순서쌍이 대응되면 된다.

---

## 고유값과 고유벡터의 생활 속 응용 (책 424쪽)

- 선형변환의 **대각화**에 매우 중요한 개념
- 물리적 시스템의 특성을 표현하는 수학적 모델 개발
- **행렬의 거듭제곱** 계산을 편리하게 함
- 인구 증가 모델 분석, 동역학(Dynamic System) 분석
- 미분방정식의 풀이
- 선형대수학, 함수해석 등 응용 수학과 여러 비선형 분야

---

## [보충] 고유값은 왜 나왔고 어떻게 쓰나

> 이 섹션 전체가 강의 자료에 없는 보충 설명이다. 예제 7-4의 행렬 하나로 끝까지 설명한다.

$$
A = \begin{bmatrix} 3 & 2 \\ 3 & -2 \end{bmatrix}, \quad \lambda = 4 \to \begin{bmatrix} 2 \\ 1 \end{bmatrix}, \quad \lambda = -3 \to \begin{bmatrix} 1 \\ -3 \end{bmatrix}
$$

### 1. 왜 나왔나: 행렬은 "벡터를 움직이는 기계"

- 1~4장에서 행렬은 연립방정식 $A\mathbf{x} = \mathbf{b}$ 를 푸는 도구였다. 7장부터는 $A$를 곱하는 것을 **벡터를 다른 벡터로 바꾸는 변환**으로 본다.
- 아무 벡터나 넣으면 방향과 크기가 제멋대로 바뀐다: $A\begin{bmatrix} 3 \\ -2 \end{bmatrix} = \begin{bmatrix} 5 \\ 13 \end{bmatrix}$ (방향이 틀어짐)
- 그런데 특정 방향의 벡터는 방향이 그대로다: $A\begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 8 \\ 4 \end{bmatrix} = 4\begin{bmatrix} 2 \\ 1 \end{bmatrix}$ (같은 방향, 4배)
- 그래서 나오는 질문: **"방향이 안 틀어지고 늘어나기만 하는 방향이 있나? 있다면 몇 배인가?"**
  - 이를 식으로 쓴 것이 $A\mathbf{x} = \lambda\mathbf{x}$ 이다.
  - **고유벡터** $\mathbf{x}$ = 그 특별한 방향, **고유값** $\lambda$ = 그 방향의 배율
  - 이 방향과 배율은 그 행렬만의 **특징**이라서 eigen(고유한)이라는 이름이 붙었다.

### 2. $\det(A - \lambda I) = 0$ 은 왜 나오나

1. $A\mathbf{x} = \lambda\mathbf{x}$ → 이항하면 $(A - \lambda I)\mathbf{x} = \mathbf{0}$
2. $\mathbf{x} = \mathbf{0}$ 은 의미가 없으므로 **영벡터가 아닌 해**가 필요하다.
3. $A - \lambda I$ 가 가역이면 해는 $\mathbf{0}$ 뿐이다 (3장).
4. 따라서 $A - \lambda I$ 가 **비가역**, 즉 $\det(A - \lambda I) = 0$ 이어야 한다.

- 특성방정식 = "방향이 안 바뀌는 벡터가 존재하게 하는 $\lambda$"를 찾는 식
- 그래서 순서가 **고유값 먼저 → 고유벡터 나중**이다.

### 3. 어떻게 쓰나: 복잡한 변환을 단순하게 쪼개기

#### (1) 행렬 거듭제곱 $A^{100}$

- ① 벡터를 고유벡터의 조합으로 나눈다:

$$
\begin{bmatrix} 1 \\ 0 \end{bmatrix} = \frac{3}{7}\begin{bmatrix} 2 \\ 1 \end{bmatrix} + \frac{1}{7}\begin{bmatrix} 1 \\ -3 \end{bmatrix}
$$

- ② 각 고유벡터는 $A$를 곱할 때마다 자기 고유값만큼 곱해진다:

$$
A^{100}\begin{bmatrix} 1 \\ 0 \end{bmatrix} = \frac{3}{7} \cdot 4^{100}\begin{bmatrix} 2 \\ 1 \end{bmatrix} + \frac{1}{7} \cdot (-3)^{100}\begin{bmatrix} 1 \\ -3 \end{bmatrix}
$$

- 행렬 곱셈 100번이 숫자 거듭제곱 2번으로 줄었다. 정리 7-1의 "$A^k$의 고유값은 $\lambda^k$"가 이 원리다.

#### (2) 대각화: 위 계산을 행렬로 쓴 것

- 고유벡터를 열로 놓은 $C = \begin{bmatrix} 2 & 1 \\ 1 & -3 \end{bmatrix}$ 이면

$$
C^{-1}AC = \begin{bmatrix} 4 & 0 \\ 0 & -3 \end{bmatrix} = D, \qquad A^k = CD^kC^{-1}
$$

- 고유벡터를 기준축으로 보면 $A$는 **각 축 방향으로 늘이기만 하는 단순한 변환**이다.
- 닮은행렬이 같은 고유값을 갖는 이유(정리 7-5)도 같은 변환을 다른 축에서 본 것이기 때문이다.

#### (3) 장기적인 거동 예측

- (1)의 식에서 $4^{100} \gg 3^{100}$ 이므로, $A$를 계속 곱하면 결과는 **절댓값이 가장 큰 고유값의 고유벡터** $(2, 1)$ 방향으로 수렴한다.
- 인구 이동 모델: 수십 년 뒤 도시·농촌 인구 비율이 고유벡터로 정해진다.
- 구글 PageRank: 웹페이지 중요도가 거대한 행렬의 고유벡터다.
- 시스템 안정성: 모든 $|\lambda| < 1$ 이면 0으로 수렴(안정), 하나라도 $|\lambda| > 1$ 이면 발산한다.

#### (4) 공학과 AI

- **진동**: 구조물이 흔들리는 고유한 패턴(모드)은 고유벡터, 고유진동수는 고유값에서 나온다. 외부 진동이 고유진동수와 맞으면 공진이 일어난다.
- **PCA(주성분 분석)**: 데이터가 가장 넓게 퍼진 방향 = 공분산행렬의 고유벡터. 차원 축소에 쓴다.

### 4. 한눈에 보기

| 개념       | 의미                              |
|------------|-----------------------------------|
| 고유벡터   | 변환해도 방향이 안 바뀌는 축      |
| 고유값     | 그 축 방향의 배율                 |
| 특성방정식 | 그런 축이 존재하는 배율을 찾는 식 |
| 대각화     | 고유벡터를 축으로 다시 보는 것    |
| 쓰는 곳    | 거듭제곱, 장기 예측, 진동, PCA    |

- trace = 고유값의 합, det = 고유값의 곱, $A^k$의 고유값 = $\lambda^k$ 같은 성질도 변환을 "축별 배율"로 쪼갰기 때문에 성립한다.

---

## 핵심 정리

- $A\mathbf{x} = \lambda\mathbf{x}$ ($\mathbf{x} \neq \mathbf{0}$): $\lambda$는 고유값, $\mathbf{x}$는 고유벡터
- 순서: $\det(A - \lambda I) = 0$ → 고유값 $\lambda$ → $(A - \lambda I)\mathbf{x} = \mathbf{0}$ → 고유벡터
- 고유값을 구하기 **전에** $A$에 행 연산을 하면 안 된다.
- 고유벡터의 0이 아닌 배수도 고유벡터다.
- $\sum\lambda_i = \text{trace}(A)$, $\prod\lambda_i = \det(A)$
- $A^T$: 같은 고유값 / $A^{-1}$: $1/\lambda$ / $kA$: $k\lambda$ / $A^k$: $\lambda^k$
- 삼각행렬의 고유값 = 대각원소
- 서로 다른 고유값의 고유벡터는 선형독립이다.
- 닮은행렬 $B = C^{-1}AC$ → 같은 고유값
