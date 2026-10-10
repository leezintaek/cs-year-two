# Chapter 09. 선형변환

> 원본: `chapters/ch09_linear_transformations.pdf` (책 462–499쪽)

- 9장 개요: 선형변환과 선형연산자를 정의하고, 선형변환이 되는지를 예제로 판별한다. 선형사상과 커널, 함수와 선형변환의 관계, 함수의 기본 개념을 배운다. 여러 가지 변환(사영, 확대, 축소, 반사, 회전)을 2차원 그림으로 살펴보고, 표준행렬에 따른 변환을 그림으로 나타낸다. 응용으로 산업적 응용, 그래픽 변환, 층밀림을 다룬다.

---

## 9.1 선형변환의 개념과 함수

### 9.1.1 선형변환의 정의

- **정의 9-1**: $V$와 $W$가 벡터공간이고 $\mathbf{u}, \mathbf{v} \in V$, $\alpha$가 실수일 때, $V$에서 $W$로 가는 함수 $L: V \to W$ 가 다음 **2가지 공리(axiom)** 를 만족하면 **선형변환(linear transformation)** 또는 **선형사상(linear mapping)** 이라 한다.
  1. $L(\mathbf{u} + \mathbf{v}) = L(\mathbf{u}) + L(\mathbf{v})$
  2. $L(\alpha\mathbf{u}) = \alpha L(\mathbf{u})$
  - 특히 $V = W$ 이면 $L$을 $V$에서의 **선형연산자(linear operator)** 라 한다.

[보충] 두 조건을 한 번에 $L(\alpha\mathbf{u} + \beta\mathbf{v}) = \alpha L(\mathbf{u}) + \beta L(\mathbf{v})$ 로 쓰기도 한다. 또 선형변환은 항상 $L(\mathbf{0}) = \mathbf{0}$ 을 만족한다($\alpha = 0$ 을 대입). 그래서 **$L(\mathbf{0}) \neq \mathbf{0}$ 이면 바로 선형변환이 아니다**. 예제 9-3, 9-4, 9-5처럼 상수를 더하는 변환은 이것만으로 빠르게 걸러낼 수 있다.

#### 선형변환 판별 예제

- **예제 9-1**: $L(\mathbf{x}) = 3\mathbf{x}$ → $L(\mathbf{x} + \mathbf{y}) = 3\mathbf{x} + 3\mathbf{y}$, $L(\alpha\mathbf{x}) = \alpha L(\mathbf{x})$ → **선형변환 O**
  - 기하학적으로 벡터의 길이를 3배로 확대한다. 일반적으로 $\alpha > 0$ 이면 $L(\mathbf{x}) = \alpha\mathbf{x}$ 는 $\mathbf{x}$를 $\alpha$만큼 확대하거나 축소한다.
- **예제 9-2**: $L(x, y, z) = (x - y, 0, y + z)$ → 두 조건 모두 만족 → **선형변환 O**
- **예제 9-3**: $L(a_1, a_2) = (a_1 + 1, 2a_2)$ → $L(\mathbf{u} + \mathbf{v})$ 의 첫 성분은 $(a_1 + b_1) + 1$, $L(\mathbf{u}) + L(\mathbf{v})$ 의 첫 성분은 $(a_1 + b_1) + 2$ → **선형변환 X**
- **예제 9-4**: $L(x, y) = (x + a, y + b)$, $(a, b) \neq (0, 0)$ (평행이동) → $L(\mathbf{u}) + L(\mathbf{v})$ 에 $2a, 2b$ 가 생긴다 → **선형변환 X**
- **예제 9-5**: $L(a_1, a_2, a_3) = (a_1 + 2, 3a_2, a_3)$ → $a_1 + b_1 + 2 \neq a_1 + b_1 + 4$ → **선형변환 X**

#### 행렬과 선형변환

- $m \times n$ 행렬 $A$와 $\mathbf{x} \in R^n$ 의 곱은 $R^m$의 원소다.

$$
\begin{bmatrix} a_{11} & \cdots & a_{1n} \\ \vdots & \ddots & \vdots \\ a_{m1} & \cdots & a_{mn} \end{bmatrix}\begin{bmatrix} x_1 \\ \vdots \\ x_n \end{bmatrix} = \begin{bmatrix} a_{11}x_1 + \cdots + a_{1n}x_n \\ \vdots \\ a_{m1}x_1 + \cdots + a_{mn}x_n \end{bmatrix} \in R^m
$$

- 그러므로 변환함수 $L: R^n \to R^m$, $L(\mathbf{x}) = A\mathbf{x}$ 는 **선형변환**이다.

### 9.1.2 함수와 선형변환

#### (1) 함수의 개념

- **정의 9-2**: 집합 $X$에서 $Y$로의 관계의 부분집합으로서, $X$의 **모든 원소 $x$가 $Y$의 원소 중 한 개와** 관계가 있으면 $f$를 **함수(function)** 라 하고 $f: X \to Y$ 로 쓴다.
  - $X$: **정의역(domain)**, $Y$: **공변역(codomain)**
  - $(x, y) \in f$ 이면 $f(x) = y$. $y$를 $x$의 **상(image)**, **이미지** 또는 **함수값**이라 한다.
  - $y$들의 집합을 **치역(range)** 이라 한다.
- **예제 9-6**: (1) $b \in A$ 에서 $B$로의 사상이 없음 → 함수 X / (2) $c$가 $x$와 $z$에 동시에 대응 → 함수 X / (3) $A$의 모든 원소에서 $B$로 가는 사상이 하나씩 존재 → 함수 O

#### (2) 단사함수, 전사함수, 전단사함수

- **정의 9-3**
  - **단사함수(injective function)**: $f(a_i) = f(a_j)$ 이면 $a_i = a_j$. 즉 $A$의 서로 다른 원소는 $B$의 서로 다른 원소에 대응한다.
  - **전사함수(surjective function, onto function)**: $B$의 모든 원소 $b$에 대해 $f(a) = b$ 인 $a \in A$ 가 적어도 하나 존재한다. 즉 $B$의 모든 원소가 대응된다.
  - **전단사함수(bijective function)**: 단사이면서 전사인 함수. $A$의 모든 원소가 $B$의 모든 원소와 하나씩 대응되므로 **1대1 대응함수(one-to-one correspondence)** 라고도 한다.
- 화살표 도표(arrow diagram)로 그리면 특징을 쉽게 알 수 있다.
- **정의 9-4 (합성함수, composition function)**: $f: A \to B$, $g: B \to C$ 의 합성함수 $g \circ f: A \to C$ 는

$$
g \circ f = \{(a, c) \mid a \in A,\ b \in B,\ c \in C,\ f(a) = b,\ g(b) = c\}
$$

  - $c = g(b) = g(f(a)) = (g \circ f)(a)$
  - $f$의 공변역이 $g$의 정의역이 된다.

#### 변환과 커널

- 입력값과 출력값이 모두 벡터인 함수를 **변환(transformation)** 이라 하고 보통 대문자 $L, T, F$ 로 쓴다. $L(\mathbf{x}) = \mathbf{w}$
- 합성함수의 선형변환은 $(L_1 \circ L_2)(\mathbf{a})$ 처럼 쓴다. 순서에 따라 사영, 확대, 반사, 회전 등의 선형연산이 진행된다.
  - **합성변환의 순서는 매우 중요하다**: 변환의 순서에 따라 결과가 완전히 달라질 수 있다.
- 선형변환은 연산을 보존하므로 매우 중요하다. 예: 사진을 선형변환해 위치를 옮기거나 회전시켜 새 이미지를 얻는다.
  - $T(x, y) = (kx, y)$: x좌표를 $k$배 조정 / $T(x, y) = (x, ky)$: y좌표를 $k$배 조정
  - $k > 1$ 이면 확대, $k < 1$ 이면 축소
- **정의 9-5 (커널)**: $L: V \to W$ 가 선형변환일 때, $L(\mathbf{v}) = \mathbf{0}$ 을 만족하는 $V$의 부분집합을 $L$의 **커널(kernel)** 이라 하고 $\ker(L)$ 로 쓴다.
- 함수와 선형변환의 관계: 선형변환은 함수에 속하지만, 함수의 조건에 더해 두 가지 조건($L(\mathbf{u} + \mathbf{v}) = L(\mathbf{u}) + L(\mathbf{v})$, $L(\alpha\mathbf{u}) = \alpha L(\mathbf{u})$)을 추가로 만족해야 한다. 덕분에 일반 함수보다 응용 범위가 넓다.

[보충] 행렬 변환 $L(\mathbf{x}) = A\mathbf{x}$ 에서 $\ker(L)$ 은 동차시스템 $A\mathbf{x} = \mathbf{0}$ 의 해집합(**영공간, null space**)과 같다. $\ker(L) = \{\mathbf{0}\}$ 이면 $L$은 단사다. 예: $L(a_1, a_2) = (a_1, 0)$ 이면 $\ker(L) = \{(0, a_2)\}$, 즉 y축 전체가 0으로 보내진다.

### 9.1.3 여러 가지 선형변환

#### (1) 사영변환

- **예제 9-7**: $L: R^3 \to R^2$, $L(a_1, a_2, a_3) = (a_1, a_2)$ → 선형변환 O
  - 이런 경우를 **사영변환(projection transformation)** 이라 한다. $R^3$의 벡터를 $xy$평면($R^2$)에 수직으로 사영한다.

#### (2) 확대변환과 축소변환

- **예제 9-8**: $L: R^3 \to R^3$, $L(\mathbf{a}) = r\mathbf{a}$ ($r$은 실수) → 선형변환 O
  - $R^3 \to R^3$ 이므로 **선형연산자**다.
  - $r > 1$: **확대변환(dilation transformation)**, 벡터의 길이가 늘어난다.
  - $0 < r < 1$: **축소변환(contraction transformation)**, 벡터의 길이가 줄어든다.

#### (3) 반사변환

- **예제 9-9**: $L(a_1, a_2) = (a_1, -a_2)$ → 선형변환 O. **x축에 대한 반사변환(reflection transformation)**
- y축에 대한 반사변환: $L(a_1, a_2) = (-a_1, a_2)$

#### (4) 회전변환

- **예제 9-10**: $L: R^2 \to R^2$

$$
L\left(\begin{bmatrix} x \\ y \end{bmatrix}\right) = \begin{bmatrix} \cos\phi & -\sin\phi \\ \sin\phi & \cos\phi \end{bmatrix}\begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} x\cos\phi - y\sin\phi \\ x\sin\phi + y\cos\phi \end{bmatrix}
$$

  - 이를 **회전변환(rotation transformation)** 이라 한다. 점 $P(x, y)$ 를 원점 O를 중심축으로 $\phi$ 각도만큼(**시계 반대 방향**) 회전시켜 $P'(x', y')$ 로 보낸다.

### 9.1.4 변환의 표준행렬

- **정의 9-6**: $L: R^n \to R^m$ 이 선형변환이고 $\{\mathbf{e}_1, \dots, \mathbf{e}_n\}$ 이 $R^n$의 표준기저라 하자. **$j$번째 열이 $L(\mathbf{e}_j)$ 인 $m \times n$ 행렬 $A$** 는 모든 $\mathbf{x} \in R^n$ 에 대해

$$
L(\mathbf{x}) = A\mathbf{x}
$$

  를 만족한다. $A$가 이 식을 만족하는 유일한 행렬일 때, $A$를 $L$을 나타내는 **표준행렬(standard matrix)** 이라 한다.

$$
A = [L(\mathbf{e}_1)\ \ L(\mathbf{e}_2)\ \ \cdots\ \ L(\mathbf{e}_n)]
$$

- **예제 9-11**: $L(x_1, x_2, x_3) = (x_1 + 2x_2,\ 3x_2 - 2x_3)$
  - $L(\mathbf{e}_1) = (1, 0)$, $L(\mathbf{e}_2) = (2, 3)$, $L(\mathbf{e}_3) = (0, -2)$
  - 표준행렬 $A = \begin{bmatrix} 1 & 2 & 0 \\ 0 & 3 & -2 \end{bmatrix}$

#### 표준행렬과 여러 가지 변환 (단위 정사각형에 적용)

| 변환 | 표준행렬 | 효과 |
|---|---|---|
| x축으로의 사영 | $\begin{bmatrix} 1 & 0 \\ 0 & 0 \end{bmatrix}$ | y성분을 0으로 |
| x축으로의 반사 | $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$ | 위아래 뒤집기 |
| y축으로의 반사 | $\begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$ | 좌우 뒤집기 |
| 원점 대칭 | $\begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$ | x, y 모두 반전 |
| $y = -x$ 에 대한 반사 | $\begin{bmatrix} 0 & -1 \\ -1 & 0 \end{bmatrix}$ | $(x, y) \to (-y, -x)$ |
| 수평방향 축소/확대 | $\begin{bmatrix} k & 0 \\ 0 & 1 \end{bmatrix}$ | $0 < k < 1$ 축소, $k > 1$ 확대 |
| 수평방향 층밀림 | $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$ | $(x, y) \to (x + ky, y)$ |
| 회전 ($\phi$, 반시계) | $\begin{bmatrix} \cos\phi & -\sin\phi \\ \sin\phi & \cos\phi \end{bmatrix}$ | 원점 중심 회전 |

[보충] 표준행렬을 찾는 요령: "$\mathbf{e}_1 = (1, 0)$ 이 어디로 가는가"가 첫째 열, "$\mathbf{e}_2 = (0, 1)$ 이 어디로 가는가"가 둘째 열이다. 예: 90° 반시계 회전이면 $(1, 0) \to (0, 1)$, $(0, 1) \to (-1, 0)$ 이므로 $A = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$. 또 합성변환 "$L_1$을 먼저, 그다음 $L_2$"의 표준행렬은 $A_2A_1$ 이다(**오른쪽부터** 적용).

- 선형변환은 보통 **표준행렬을 곱해서** 이루어진다. 사영, 확대·축소, 반사, 회전 등이 있다.
- 고유값을 구할 때의 $A\mathbf{x} = \lambda\mathbf{x}$ 도 일종의 선형변환이다. 다만 고유값을 구할 때는 $\mathbf{x}$가 $A\mathbf{x}$ 의 곱 연산을 하더라도 원래의 $\mathbf{x}$가 $\lambda$배만큼만 변하는 성질을 활용한다.
- 행렬, 선형시스템, 행렬식, 벡터, 벡터공간, 고유값, 선형변환 등은 모두 유기적인 관계를 가진다.

---

## 9.2 선형변환의 응용

### 9.2.1 산업적 응용

- **예제 9-12**: 1만 원짜리 제품 A: 재료비 4,000원, 인건비 3,000원, 기타 1,500원 / 제품 B: 3,500원, 3,500원, 2,000원
  - 단가행렬 $P = [\mathbf{u}\ \mathbf{v}] = \begin{bmatrix} 4000 & 3500 \\ 3000 & 3500 \\ 1500 & 2000 \end{bmatrix}$ (행: 재료비, 인건비, 기타 경비 / 열: A, B)
  - 생산벡터 $\mathbf{x} = (x_1, x_2)$ → $T(\mathbf{x}) = P\mathbf{x}$ = (총 재료비, 총 인건비, 총 기타 경비)
  - 선형성의 의미: ① 생산량이 $4\mathbf{x}$로 늘면 비용도 $4T(\mathbf{x})$ 로 늘어난다. ② 생산벡터 $\mathbf{x} + \mathbf{y}$ 의 총 비용은 $T(\mathbf{x}) + T(\mathbf{y})$ 다.
  - 생산량과 제조 원가를 연동시키는 좋은 응용이다.

### 9.2.2 그래픽 변환으로의 응용

- 2차원 그래픽에서 $L: R^2 \to R^2$ 선형연산자의 결과를 보여 준다. 행렬 표현을 얻기 위해 **표준기저(standard basis)** 를 쓴다.
- **예제 9-13 (x축 반사)**: $L(x, y) = (x, -y)$ → $L(\mathbf{e}_1) = (1, 0)$, $L(\mathbf{e}_2) = (0, -1)$ → $A = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$
  - 삼각형 꼭짓점 $(-1, 4), (3, 1), (2, 6)$ → $A[\mathbf{v}_1\ \mathbf{v}_2\ \mathbf{v}_3] = \begin{bmatrix} -1 & 3 & 2 \\ -4 & -1 & -6 \end{bmatrix}$ → $(-1, -4), (3, -1), (2, -6)$
- **예제 9-14 ($y = -x$ 반사)**: $L(x, y) = (-y, -x)$ → $A = \begin{bmatrix} 0 & -1 \\ -1 & 0 \end{bmatrix}$
  - 같은 삼각형 → $(-4, 1), (-1, -3), (-6, -2)$
- **예제 9-15 (회전)**: $A = \begin{bmatrix} \cos\phi & -\sin\phi \\ \sin\phi & \cos\phi \end{bmatrix}$ 로 포물선 $y = x^2$ 을 시계 반대 방향으로 50° 회전
  - 점 $(-2, 4), (-1, 1), (0, 0), (\frac{1}{2}, \frac{1}{4}), (3, 9)$ → $(-4.3498, 1.0391), (-1.4088, -0.1233), (0, 0), (0.1299, 0.5437), (-4.9660, 8.0832)$
- **예제 9-16**: $T(\mathbf{x}) = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}\mathbf{x} = (-x_2, x_1)$, $\mathbf{u} = (4, 1)$, $\mathbf{v} = (2, 3)$
  - $T(\mathbf{u}) = (-1, 4)$, $T(\mathbf{v}) = (-3, 2)$, $T(\mathbf{u} + \mathbf{v}) = (-4, 6) = T(\mathbf{u}) + T(\mathbf{v})$
  - $T$는 원점을 축으로 **시계 반대 방향 90°** 회전이다. $\mathbf{u}, \mathbf{v}$ 로 만든 평행사변형을 $T(\mathbf{u}), T(\mathbf{v})$ 로 만든 평행사변형으로 바꾼다.

### 9.2.3 컴퓨터 그래픽에서 층밀림의 응용

- **예제 9-17**: $A = \begin{bmatrix} 1 & 3 \\ 0 & 1 \end{bmatrix}$ 일 때 $T(\mathbf{x}) = A\mathbf{x}$ 는 **층밀림변환(shear transformation)** 이다.
  - 길이 2인 정사각형 → 평행사변형. 예: $(0, 2) \to (6, 2)$, $(2, 2) \to (8, 2)$
  - 바닥은 고정된 채 **윗부분을 옆으로 미는** 작용을 한다. 물리학, 지질학, 결정학 등에 많이 응용된다.
- **예제 9-18**: x축 방향의 층밀림 $L(x, y) = (x + ky, y)$ → 표준행렬 $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$
  - 점 $(x, y)$ 를 x축 방향으로 $ky$만큼 평행이동한다.
  - 꼭짓점 $(0,0), (0,2), (4,0), (4,2)$ 인 직사각형 → $k = 2$: $(0,0), (4,2), (4,0), (8,2)$ / $k = -3$: $(0,0), (-6,2), (4,0), (-2,2)$
  - 개 그림에 층밀림을 적용한 예도 있다.
- **예제 9-19 (글씨 N)**: 8개의 점으로 이루어진 N의 좌표를 행렬 $D$로 나타낸다.
  - $D = \begin{bmatrix} 0 & .5 & .5 & 6 & 6 & 5.5 & 5.5 & 0 \\ 0 & 0 & 6.42 & 0 & 8 & 8 & 1.58 & 8 \end{bmatrix}$
  - 층밀림 $A = \begin{bmatrix} 1 & .25 \\ 0 & 1 \end{bmatrix}$ → $AD$ 로 **기울어진 N**
  - 추가로 x축 방향으로 0.75배(25% 축소): $S = \begin{bmatrix} .75 & 0 \\ 0 & 1 \end{bmatrix}$
  - 합성변환 $SA = \begin{bmatrix} .75 & .1875 \\ 0 & 1 \end{bmatrix}$ → 기울어진 N을 다시 25% 축소한 결과

---

## 선형변환의 생활 속 응용 (책 498쪽)

- 선형 관계에 있는 다양한 데이터의 변화를 원활하게 처리하고, 빠르고 정확한 계산을 가능하게 한다.
- 데이터의 단순화로 통계적 처리를 간편하게 한다.
- 높은 차원의 벡터를 **사영**으로 낮은 차원의 벡터로 변환한다.
- 행렬의 선형변환으로 수학, 물리학, 공학 등에 활용한다.
- 컴퓨터 그래픽에서 점이나 도형의 영상을 변환해 처리한다.

---

## 핵심 정리

- 선형변환의 2조건: $L(\mathbf{u} + \mathbf{v}) = L(\mathbf{u}) + L(\mathbf{v})$, $L(\alpha\mathbf{u}) = \alpha L(\mathbf{u})$
- 상수를 더하는 변환(평행이동)은 선형변환이 **아니다** ($L(\mathbf{0}) \neq \mathbf{0}$)
- $L(\mathbf{x}) = A\mathbf{x}$ 는 항상 선형변환이다. $V = W$ 이면 선형연산자라 부른다.
- 단사(서로 다른 원소 → 서로 다른 상), 전사(공변역 전체가 치역), 전단사(1대1 대응)
- 커널: $\ker(L) = \{\mathbf{v} \mid L(\mathbf{v}) = \mathbf{0}\}$
- 표준행렬: $A = [L(\mathbf{e}_1)\ \cdots\ L(\mathbf{e}_n)]$
- 사영, 확대($r > 1$)/축소($0 < r < 1$), 반사, 회전, 층밀림 $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$
- 합성변환의 순서가 중요하다 ($SA \neq AS$ 일 수 있음)
