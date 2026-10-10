# Chapter 02. 행렬

> 원본: `chapters/ch02_matrices.pdf` (책 60–151쪽)

- 현실의 문제는 방정식 개수가 너무 많아 전통적인 방법으로 풀기 어렵다. **행렬**은 선형방정식을 간단하게 표현하고, 연산을 쉽게 해 준다.
- 행렬은 수학, 물리학, 양자역학, 공학 등에서 매우 중요하다.
- 역사: 기원전 4세기 바빌로니아 점토판에 흔적이 있다. 19세기 영국의 **케일리(Arthur Cayley, 1821–1895)** 가 행렬 개념을 확립했다.

---

## 2.1 행렬과 행렬의 연산

### 2.1.1 행렬

- **행렬(matrix)**: 수나 문자를 직사각형 배열 형태로 나타낸 것. 어원은 라틴어 Mater(어머니) + -ix → "모체(母體)".
- $A = [a_{ij}]$, $i = 1, \dots, m$, $j = 1, \dots, n$ 이면 **$m \times n$ 행렬** 또는 **$(m, n)$ 행렬**이라 한다.
  - $m$개의 **행(row)**: 가로 방향
  - $n$개의 **열(column)**: 세로 방향

$$
A = \begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}
$$

- $a_{ij}$: **$ij$-항($ij$-entry)** 또는 **$ij$-성분($ij$-component)**. $i$번째 행과 $j$번째 열이 만나는 값이다.
- **행벡터(row vector)**: 가로의 $n$ 순서쌍 $[x_1, \dots, x_n]$, 즉 $1 \times n$ 행렬
- **열벡터(column vector)**: 세로의 $m$ 순서쌍, 즉 $m \times 1$ 행렬
- **정의 2-1 (정방행렬)**: $m = n$, 즉 행의 개수와 열의 개수가 같은 $A_{n \times n}$ 을 **정방행렬(square matrix)**, 또는 **$n$차 정방행렬(square matrix of order $n$)** 이라 한다.
- **주대각선(main diagonal)**: 정방행렬의 $a_{11}, a_{22}, \dots, a_{nn}$ 이 놓인 선

### 2.1.2 행렬의 합과 스칼라 곱

- **행렬의 합**: **같은 크기**의 행렬끼리만 정의된다. $A + B$ 의 $ij$-성분은 $a_{ij} + b_{ij}$ 이다(같은 위치끼리 더함).
  - 예: $\begin{bmatrix} 3 & -1 \\ 2 & 4 \end{bmatrix} + \begin{bmatrix} 2 & 1 \\ -3 & 2 \end{bmatrix} = \begin{bmatrix} 5 & 0 \\ -1 & 6 \end{bmatrix}$
- **정의 2-2 (행렬의 차)**: $A - B = A + (-1)B$. $A$에서 $B$를 뺀 **차(difference)** 다.
- **정의 2-3 (스칼라 곱)**: 실수 $k$ 에 대해 $kA = [ka_{ij}]$. 모든 성분에 $k$를 곱한다.
- **정의 2-4 (상등)**: 두 $m \times n$ 행렬에서 모든 $i, j$ 에 대해 $a_{ij} = b_{ij}$ 이면 **상등(equal)** 이라 한다.
  - 예제 2-6: $3\begin{bmatrix} x & y \\ z & t \end{bmatrix} = \begin{bmatrix} x & 6 \\ -1 & 2t \end{bmatrix} + \begin{bmatrix} 4 & x+y \\ z+t & 3 \end{bmatrix}$ → 대응 성분을 비교하면 $x = 2, y = 4, z = 1, t = 3$

#### 정리 2-1 (합과 스칼라 곱의 연산법칙)

같은 크기의 $A, B, C$ 와 상수 $c, d$, 영행렬 $O$ 에 대해:

| 식 | 이름 |
|---|---|
| $A + B = B + A$ | 덧셈의 교환법칙 |
| $(A + B) + C = A + (B + C)$ | 덧셈의 결합법칙 |
| $A + O = O + A = A$ | 덧셈의 항등법칙 |
| $A + (-A) = (-A) + A = O$ | 덧셈의 역원 |
| $c(A + B) = cA + cB$ | 스칼라 곱의 배분법칙 |
| $(c + d)A = cA + dA$ | 스칼라 곱의 배분법칙 |

### 2.1.3 행렬의 곱

- **정의 2-5**: $A$가 $m \times n$, $B$가 $n \times p$ 이면 $AB = C = [c_{ij}]$ 는 $m \times p$ 행렬이다.

$$
c_{ij} = \sum_{k=1}^{n} a_{ik}b_{kj} = a_{i1}b_{1j} + a_{i2}b_{2j} + \cdots + a_{in}b_{nj}
$$

  - $c_{ij}$ = **$A$의 $i$번째 행**과 **$B$의 $j$번째 열**을 곱해서 더한 값
- **곱이 정의되는 조건**: **$A$의 열 개수 = $B$의 행 개수**
  - $(m \times r)(r \times n) = (m \times n)$: **내측** 숫자가 같아야 하고, 결과 크기는 **외측** 숫자로 정해진다.
  - 예: $(2\times3)(3\times4) = 2\times4$, $(1\times2)(3\times1)$ → 정의 안 됨, $(5\times2)(2\times3) = 5\times3$
- 예제 2-11: $\begin{bmatrix} 1 & 2 & -1 \\ 0 & -5 & 3 \end{bmatrix}\begin{bmatrix} 4 \\ 3 \\ 7 \end{bmatrix} = \begin{bmatrix} 3 \\ 6 \end{bmatrix}$
- 단위행렬을 곱하면 그대로: $I\mathbf{x} = \mathbf{x}$

#### 교환법칙은 성립하지 않는다

- 예제 2-12: $A = \begin{bmatrix} 5 & 1 \\ 3 & -2 \end{bmatrix}, B = \begin{bmatrix} 2 & 0 \\ 4 & 3 \end{bmatrix}$ → $AB = \begin{bmatrix} 14 & 3 \\ -2 & -6 \end{bmatrix} \neq BA = \begin{bmatrix} 10 & 2 \\ 29 & -2 \end{bmatrix}$
- 예: $\begin{bmatrix} 1 & 0 \\ 1 & 0 \end{bmatrix}\begin{bmatrix} 0 & 0 \\ 1 & 1 \end{bmatrix} = O$ 인데 $\begin{bmatrix} 0 & 0 \\ 1 & 1 \end{bmatrix}\begin{bmatrix} 1 & 0 \\ 1 & 0 \end{bmatrix} = \begin{bmatrix} 0 & 0 \\ 2 & 0 \end{bmatrix}$
- 예제 2-10: $A \neq O$, $C \neq O$ 인데 $AC = O$ 가 될 수 있다.

[보충] 행렬에서는 $AB = O$ 라도 $A = O$ 또는 $B = O$ 라고 결론 내릴 수 없다(**영인자**). 또 $AB = AC$ 라고 $B = C$ 라고 할 수 없다(소거법칙 불성립). 실수의 계산 습관과 다르니 주의할 것.

#### 행렬-벡터 곱을 구하는 두 가지 방법 (예제 2-13, 2-17)

1. **행 중심**: 각 행과 벡터의 곱(내적)
2. **열 중심**: 열들의 선형결합. 결과는 항상 같다.

$$
\begin{bmatrix} 2 & 3 & 4 \\ -1 & 5 & -3 \\ 6 & -2 & 8 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}
= x_1\begin{bmatrix} 2 \\ -1 \\ 6 \end{bmatrix} + x_2\begin{bmatrix} 3 \\ 5 \\ -2 \end{bmatrix} + x_3\begin{bmatrix} 4 \\ -3 \\ 8 \end{bmatrix}
$$

[보충] 열 중심 관점은 "$A\mathbf{x}$ 는 $A$의 열벡터들의 선형결합"이라는 뜻이다. 이후 6장의 **생성(span)**, **열공간** 개념과 바로 이어지므로 꼭 익혀 둘 것.

#### 정리 2-2 (곱의 연산법칙)

| 식 | 이름 |
|---|---|
| $A(BC) = (AB)C$ | 곱셈의 결합법칙 |
| $A(B + C) = AB + AC$ | 왼쪽 배분법칙 |
| $(B + C)A = BA + CA$ | 오른쪽 배분법칙 |
| $k(AB) = (kA)B = A(kB)$ | 스칼라 곱 |

- 정리: 행렬의 곱셈에서는 **결합법칙, 배분법칙은 성립**하지만 **교환법칙은 성립하지 않는다**.

#### 행렬의 거듭제곱

- **정의 2-6**: $n \times n$ 행렬 $A$와 양의 정수 $k$에 대해 $A^k = \underbrace{A \cdots A}_{k}$ 를 **행렬의 거듭제곱(Powers of a Matrix)** 이라 한다.
  - $A^0 = I$, $A^k = A^{k-1}A$
  - 예제 2-15: $A = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$ → $A^n = \begin{bmatrix} 2^{n-1} & 2^{n-1} \\ 2^{n-1} & 2^{n-1} \end{bmatrix}$
- 예제 2-16 (행렬 방정식): $4A + 2X = B$ → $X = \frac{1}{2}(B - 4A)$. 일반 방정식처럼 이항해서 풀 수 있다.

#### 부행렬 (블록 분할)

- **정의 2-7**: 행렬 $A$를 **부행렬(submatrix)** 들로 분할할 수 있다.

$$
A = \begin{bmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{bmatrix}
$$

- 분할된 블록끼리도 일반 행렬 곱처럼 계산할 수 있다(예제 2-18): $C_{11} = A_{11}B_{11} + A_{12}B_{21}$ 등

---

## 2.2 특수한 행렬

### 2.2.1 대각행렬

- **정의 2-8**: $n \times n$ 정방행렬에서 **대각선을 제외한 모든 항이 0**인 행렬 $D$를 **대각행렬(diagonal matrix)** 이라 한다.
- **정의 2-9 (대각합)**: 주대각선 위의 성분을 **대각항**이라 하고, 대각항의 합을 **대각합(trace)** 이라 한다. $\text{tr}(A)$ 로 표기한다.
  - 예: $A = \begin{bmatrix} -5 & 3 \\ 4 & 2 \end{bmatrix}$ → $\text{tr}(A) = -5 + 2 = -3$
  - 대각합은 **정방행렬에서만** 정의된다.
- **정리 2-3 (대각합의 성질)**: 같은 크기의 정방행렬 $A, B$ 에 대해
  1. $\text{tr}(A^T) = \text{tr}(A)$
  2. $\text{tr}(cA) = c\,\text{tr}(A)$
  3. $\text{tr}(A + B) = \text{tr}(A) + \text{tr}(B)$
  4. $\text{tr}(A - B) = \text{tr}(A) - \text{tr}(B)$
  5. $\text{tr}(AB) = \text{tr}(BA)$

[보충] $AB \neq BA$ 이더라도 $\text{tr}(AB) = \text{tr}(BA)$ 는 항상 성립한다. 7장에서 배우는 "대각합 = 고유값의 합" 성질과도 연결된다.

### 2.2.2 항등행렬과 영행렬

- **정의 2-10**: 대각행렬이면서 대각선의 항이 모두 1인 $n \times n$ 행렬을 **항등행렬(identity matrix)** 또는 **단위행렬**이라 한다. $I_n$ 또는 $I$ 로 쓴다.
  - 중요한 성질: $AI_n = A = I_nA$
- **정의 2-11**: 성분이 모두 0인 행렬을 **영행렬(zero matrix)** 이라 한다. $O$ 또는 $O_{m \times n}$ 으로 쓴다.
  - 정리 2-4: $A + O = O + A = A$
- **정의 2-12 (덧셈의 역원)**: $-A = [-a_{ij}]$. $A + (-A) = O$ 이다. $-A$ 를 **덧셈에 대한 역원(additive inverse)** 이라 한다.

### 2.2.3 전치행렬

- **정의 2-13**: $m \times n$ 행렬 $A = [a_{ij}]$ 에 대해 $b_{ij} = a_{ji}$ 인 $n \times m$ 행렬을 $A$의 **전치행렬(transpose matrix)** $A^T$ 라 한다. **행과 열을 서로 바꾼 행렬**이다.
  - 예: $A = \begin{bmatrix} 2 & 1 & 0 \\ 1 & 3 & 5 \end{bmatrix}$ → $A^T = \begin{bmatrix} 2 & 1 \\ 1 & 3 \\ 0 & 5 \end{bmatrix}$
  - $1 \times 3$ 행벡터의 전치는 $3 \times 1$ 열벡터다.
- **정리 2-5 (전치의 성질)**
  1. $(A^T)^T = A$
  2. $(A \pm B)^T = A^T \pm B^T$
  3. $(cA)^T = cA^T$
  4. $(AB)^T = B^TA^T$ ← **순서가 뒤바뀜에 주의**

### 2.2.4 대칭행렬과 교대행렬

- **정의 2-14**: $A = A^T$, 즉 모든 $i, j$ 에 대해 $a_{ij} = a_{ji}$ 인 정방행렬을 **대칭행렬(symmetric matrix)** 이라 한다.
  - 예: $\begin{bmatrix} 2 & 4 & 0 \\ 4 & 1 & 6 \\ 0 & 6 & 3 \end{bmatrix}$
- **정의 2-15**: $A = -A^T$, 즉 $a_{ij} = -a_{ji}$ 인 행렬을 **교대행렬(skew-symmetric matrix)** 이라 한다.
  - 예: $\begin{bmatrix} 0 & 4 & 0 \\ -4 & 0 & -6 \\ 0 & 6 & 0 \end{bmatrix}$
- 대칭행렬: 주대각선 기준 대칭 위치의 항이 **같다**. 교대행렬: 대칭 위치의 항이 **절댓값은 같고 부호는 반대**다.

[보충] 교대행렬은 $a_{ii} = -a_{ii}$ 이므로 **주대각선 성분이 반드시 모두 0**이다. 또 임의의 정방행렬은 $A = \frac{1}{2}(A + A^T) + \frac{1}{2}(A - A^T)$ 처럼 대칭행렬과 교대행렬의 합으로 분해할 수 있다.

### 2.2.5 삼각행렬

- **정의 2-16**
  - **상부삼각행렬(upper triangular matrix)**: 주대각선 **아래**의 모든 항이 0
  - **하부삼각행렬(lower triangular matrix)**: 주대각선 **위**의 모든 항이 0
  - 둘을 합쳐 **삼각행렬(triangular matrix)** 이라 한다.
- **정리 2-6**: 상부삼각행렬의 전치는 하부삼각행렬이고, 하부삼각행렬의 전치는 상부삼각행렬이다.
- 간략 표기: 상부삼각 $\begin{bmatrix} & * \\ 0 & \end{bmatrix}$, 하부삼각 $\begin{bmatrix} & 0 \\ * & \end{bmatrix}$

#### 여러 가지 행렬 정리

| 행렬 | 특징 |
|---|---|
| 정방행렬 | 행과 열의 크기가 같음 |
| 대각행렬 | 주대각선만 빼고 모두 0 |
| 항등행렬 | 대각행렬 중 주대각선이 모두 1 |
| 영행렬 | 모든 성분이 0 |
| 전치행렬 | 행과 열을 바꾼 행렬 |
| 대칭행렬 | $A = A^T$ |
| 교대행렬 | $A = -A^T$ |
| 상부삼각행렬 | 주대각선 아래가 모두 0 |
| 하부삼각행렬 | 주대각선 위가 모두 0 |

---

## 2.3 행렬의 기본 연산과 사다리꼴

### 2.3.1 행렬의 기본 연산

- **정의 2-17 (기본 행 연산, elementary row operation)**
  - **Type I**: 두 행을 서로 바꾼다. 표기 $R_1 \leftrightarrow R_2$
  - **Type II**: 어떤 행에 0이 아닌 상수를 곱한다. 표기 $(-2) \times R_3 \to R_3$
  - **Type III**: 어떤 행에 상수를 곱한 후 다른 행에 더한다. 표기 $(-3) \times R_2 + R_3 \to R_3$
- **정의 2-18**
  - 기본 행 연산을 한 번 이상 거친 행렬을 **행 동치(row equivalent)** 라 한다.
  - $I_n$ 에서 **한 번의** 기본 행 연산으로 만들어지는 행렬을 **기본행렬(elementary matrix)** 이라 한다.
  - 예: $\begin{bmatrix} 1 & 0 \\ 0 & -2 \end{bmatrix}$ ($I_2$의 2행 × (−2)), $\begin{bmatrix} 1 & 0 & 3 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$ ($I_3$의 3행 × 3을 1행에 더함)
- 기본 행 연산은 선형방정식, 행렬식, 응용 문제 등에 많이 쓰인다.

[보충] 기본행렬 $E$를 왼쪽에서 곱하면($EA$) $A$에 그 기본 행 연산을 적용한 것과 같다. 이 사실이 3장의 역행렬 계산과 4장의 LU 분해의 기초다.

### 2.3.2 행 사다리꼴 (Echelon Form)

- **정의 2-19 (피벗)**: 각 행에서 0이 아닌 가장 처음 수를 **피벗(pivot)** 으로 삼는다. 책에 따라 **선행자(leading one)** 라고도 한다.
- **정의 2-20 (행 사다리꼴, REF)**: 기본 행 연산 후 다음 3가지를 만족하면 **행 사다리꼴(row echelon form, REF)** 이다.
  1. 0으로만 이루어진 행은 (있다면) 행렬의 **아래쪽**에 있다.
  2. 0이 아닌 행은 가장 왼쪽의 0이 아닌 수를 피벗으로 삼는다.
  3. 연이은 두 행에서 **아래 행의 피벗은 위 행의 피벗보다 오른쪽**에 있다.
- **정의 2-21 (기약 행 사다리꼴, RREF)**: 행 사다리꼴의 3가지 조건에 더해
  4. 각 행의 피벗을 포함하는 **열에는 피벗 이외의 항이 모두 0**이다.
  - 이를 **기약 행 사다리꼴(reduced row echelon form, RREF)** 이라 한다.
- 행 사다리꼴은 피벗의 **아래**가 모두 0이고, 기약 행 사다리꼴은 피벗의 **아래와 위**가 모두 0이다.
  - 모든 기약 행 사다리꼴은 행 사다리꼴이다. 역은 성립하지 않는다.
  - 예: $\begin{bmatrix} 1 & 3 & 0 & 0 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 1 & 1 \end{bmatrix}$ 은 REF이지만 RREF는 아니다.

[보충] 대부분의 교재에서는 RREF의 조건으로 "**피벗이 모두 1일 것**"도 요구한다. 이 책의 예제(2-30, 2-31)에서도 RREF를 구할 때 피벗을 1로 만든다. 그러니 RREF는 피벗을 1로 만든 형태로 기억하는 것이 안전하다.

- **정의 2-22 (RREF를 구하는 두 단계)**
  - **전향단계(forward phase)**: 피벗의 **아래**를 0으로 만든다 → 행 사다리꼴. 이 단계까지가 **가우스 소거법(Gauss elimination)** 이다.
  - **후향단계(backward phase)**: 피벗의 **위**까지 0으로 만든다 → 기약 행 사다리꼴. 전향 + 후향 = **가우스-조단 소거법(Gauss-Jordan elimination)**
- 책의 표기: 피벗은 동그라미 ①, 소거될 항은 네모 [2] 로 표시한다.

#### 예제 2-30 (RREF 구하기)

$$
A = \begin{bmatrix} 1 & 1 & 0 \\ 2 & 2 & 1 \\ -3 & -3 & 1 \end{bmatrix}
\xrightarrow{(-2)R_1 + R_2 \to R_2}
\xrightarrow{3R_1 + R_3 \to R_3}
\begin{bmatrix} 1 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 1 \end{bmatrix}
\xrightarrow{(-1)R_2 + R_3 \to R_3}
\begin{bmatrix} 1 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix}
$$

#### 예제 2-31

$\begin{bmatrix} 1 & 2 & 3 & 4 \\ 5 & 6 & 7 & 8 \\ 9 & 10 & 11 & 12 \end{bmatrix}$ → RREF: $\begin{bmatrix} 1 & 0 & -1 & -2 \\ 0 & 1 & 2 & 3 \\ 0 & 0 & 0 & 0 \end{bmatrix}$

### 2.3.3 계수 (Rank)

- **정의 2-23**: 행렬을 행 사다리꼴로 만들었을 때 **행 전체가 0이 아닌 행의 개수**를 행렬의 **계수(rank)** 라 한다.
- **행렬의 계수 = 피벗의 개수**
- 예제 2-33: $\begin{bmatrix} 1 & 2 & -3 & 1 & 2 \\ 2 & 4 & -4 & 6 & 10 \\ 3 & 6 & -6 & 9 & 13 \end{bmatrix}$ → REF $\begin{bmatrix} 1 & 2 & -3 & 1 & 2 \\ 0 & 0 & 2 & 4 & 6 \\ 0 & 0 & 0 & 0 & -2 \end{bmatrix}$ → rank = 3
- 예제 2-34: $\begin{bmatrix} 3 & -3 & 0 \\ 1 & 4 & 6 \\ 4 & 6 & -3 \end{bmatrix}$ → $\begin{bmatrix} 1 & -1 & 0 \\ 0 & 5 & 6 \\ 0 & 0 & -15 \end{bmatrix}$ → rank = 3
- 예제 2-35: $4 \times 4$ 행렬인데 0이 아닌 행이 2개 → rank = 2
- $n$차 정방행렬에서 $\text{Rank}(A) = n$ 이면 **역행렬이 존재한다**. 3장의 크래머 규칙 등을 적용할 수 있는지 판별하는 지표가 된다.

[보충] $\text{rank}(A) = \text{rank}(A^T)$ 가 항상 성립한다(행 계수 = 열 계수). 또 $m \times n$ 행렬의 rank는 $\min(m, n)$ 을 넘을 수 없다.

### 2.3.4 행렬의 표현과 응용

- **인접행렬(adjacency matrix)**: 점 $i$ 에서 점 $j$ 로 연결이 있으면 $a_{ij} = 1$, 없으면 0인 $n \times n$ 행렬. 그래프 표현, 최단 거리 경로(path), 통신 네트워크, 그래프 이론 등에 쓰인다.
- **예제 2-37 (패스트푸드 세트메뉴)**: 각 세트의 재료(달걀, 칩, 콩, 햄버거)를 열벡터 $A, B, C, D$ 로 두면 필요한 총 재료는 $A + 4B + 2C + 2D$ 다. 주문 변경에 따른 차이는 $C - D$ 로 계산한다.
- **예제 2-38 (함수 변환)**: $\mathbf{y} = A\mathbf{x}$
  - $A = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$: $(a, b) \to (a, -b)$, **x축 대칭(반사)**
  - $A = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$: $(a, b) \to (-a, b)$, **y축 대칭(반사)**
  - $A = \begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$: $(a, b) \to (-a, -b)$, **원점 대칭**
- 행렬은 인공지능에서 입력과 연결강도를 표현하고, 연산을 편리하게 해 준다.

---

## 2.4 컴퓨터 프로그램에 의한 연산

- 손으로 계산하면 시간이 오래 걸리고 정확성을 기하기 어렵다. 그래서 C 프로그램이나 MATLAB, Mathematica, Maple 등을 이용한다.
- 튜링(Alan Turing, 1912–1954): "컴퓨터 과학의 아버지". 튜링 테스트와 튜링 기계(1936)를 고안했다.

### 2.4.1 C 프로그램에 의한 연산

- 행렬의 합: 2차원 배열 `vMatrixA[MAX][MAX]`, `vMatrixB[MAX][MAX]` 에 값을 입력받고, 이중 `for` 문으로 `vResult[i][j] = vMatrixA[i][j] + vMatrixB[i][j]` 를 계산한다.
- 행렬의 곱 등도 같은 방식(삼중 반복문)으로 구현한다.

[보충] 행렬 곱의 C 코드 핵심은 `for i, for j, for k: C[i][j] += A[i][k] * B[k][j]` 다. 정의식 $c_{ij} = \sum_k a_{ik}b_{kj}$ 를 그대로 옮긴 것이다.

### 2.4.2 MATLAB에 의한 연산

- **MATLAB**: MathWorks사의 수치해석·프로그래밍 환경. **행렬 데이터가 기본 연산 단위**다.
  - 특징: M-file 프로그래밍, Toolbox, 심볼릭 계산, GUI, SIMULINK
- 주요 명령어

| 기능 | 명령어 |
|---|---|
| 입력 | `A = [1, 2, 3; 4, 5, 6; 7, 8, 9];` |
| 기본연산 | `A+B`, `A-B`, `A*B`, `A/B` |
| 행렬식 | `det(A)` |
| 역행렬 | `inv(A)` |
| 대각합 | `trace(A)` |
| 고유값 | `eig(A)` |
| 계수 | `rank(A)` |

[보충] 전치는 `A'`, 기약 행 사다리꼴은 `rref(A)` 로 구할 수 있다.

---

## 2.5 인공지능과 행렬

- 신경망에서는 여러 **뉴런(neuron)** 으로부터 들어오는 입력값 $X_i$ 와 **연결강도(weight)** $W_i$ 를 곱해 모두 합한다. 이 곱셈은 주로 행렬의 곱이나 벡터의 내적으로 계산된다.
- 예: $\begin{bmatrix} 6 & 5 \\ -4 & -3 \\ 7 & 6 \end{bmatrix}\begin{bmatrix} 2 \\ -3 \end{bmatrix} = \begin{bmatrix} -3 \\ 1 \\ -4 \end{bmatrix}$, 입력 $[x_1\ x_2\ x_3] \times [w_{ij}]$

## 행렬의 생활 속 응용 (책 151쪽)

- 선형방정식의 간단한 표현: $2x + 3y = -5,\ -3x + y = 2$ → $\begin{bmatrix} 2 & 3 & -5 \\ -3 & 1 & 2 \end{bmatrix}$
- 경영의 재무 분석, 손익 분기점, 위기 관리
- GPS(Global Positioning System)를 이용한 항로·길 안내
- 컴퓨터 통신의 네트워크 관리
- 가계부(수입·지출 관계), 사회 현상 판단을 위한 근사값 짐작
- 인공지능의 입력·연결강도 표현

---

## 핵심 정리

- $AB$ 는 **$A$의 열 수 = $B$의 행 수**일 때만 정의된다. 결과는 (A의 행 수) × (B의 열 수)다.
- 행렬 곱은 **결합·배분법칙 O, 교환법칙 X**
- $(AB)^T = B^TA^T$, $\text{tr}(AB) = \text{tr}(BA)$
- 대칭 $A = A^T$, 교대 $A = -A^T$
- 기본 행 연산 3가지: **교환 / 상수배 / 상수배 후 더하기**
- REF: 피벗 아래가 0 / RREF: 피벗 위아래가 모두 0
- 가우스 소거법 = 전향단계(→REF), 가우스-조단 소거법 = 전향 + 후향(→RREF)
- **계수(rank) = REF에서 0이 아닌 행의 개수 = 피벗의 개수**
