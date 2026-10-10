# 선형대수학 용어 정리

> 챕터 구분 없이 가나다순으로 정리했다. 괄호 안은 영어 표기다.

---

### ㄱ

- **가역적 (invertible, nonsingular)**: $AB = BA = I$ 인 $B$가 존재하는 정방행렬의 성질. $\det(A) \neq 0$ 과 같은 뜻이다.
- **가우스 소거법 (Gaussian elimination)**: 기본 행 연산으로 피벗 아래를 0으로 만들어 행 사다리꼴(REF)로 바꾸는 방법(전향단계).
- **가우스-조단 소거법 (Gauss-Jordan elimination)**: 전향단계 + 후향단계로 기약 행 사다리꼴(RREF)까지 만드는 방법. 책에 따라 "전향 소거법 + 역대입법"으로 설명하기도 한다.
- **거리 (distance)**: 두 벡터 사이의 거리. $\|\mathbf{u} - \mathbf{v}\|$
- **계수 (rank)**: 행 사다리꼴에서 0이 아닌 행의 개수. 피벗의 개수와 같다.
- **계수 (coefficient)**: 선형방정식에서 변수 앞에 곱해진 상수 $a_i$. (rank와 한글 표기가 같으니 주의)
- **계수행렬 (coefficient matrix)**: 선형시스템의 계수들로 만든 행렬 $A$.
- **고유값 (eigenvalue)**: $A\mathbf{x} = \lambda\mathbf{x}$ ($\mathbf{x} \neq \mathbf{0}$) 를 만족하는 스칼라 $\lambda$. 특성방정식의 근이다.
- **고유값 문제 (eigenvalue problem)**: 주어진 행렬의 모든 고유값과 고유벡터를 구하는 것.
- **고유공간 (eigenspace)**: 한 고유값에 대응하는 고유벡터들(과 영벡터)의 집합.
- **고유벡터 (eigenvector)**: $A\mathbf{x} = \lambda\mathbf{x}$ 를 만족하는 영벡터가 아닌 벡터 $\mathbf{x}$. 변환 후에 방향은 그대로이고 크기만 $\lambda$배가 된다.
- **공변역 (codomain)**: 함수 $f: X \to Y$ 에서 $Y$.
- **교대행렬 (skew-symmetric matrix)**: $A = -A^T$ 인 정방행렬. 주대각선 성분이 모두 0이다.
- **교환법칙 (commutative law)**: $a + b = b + a$. 행렬의 **곱셈**에서는 성립하지 않는다($AB \neq BA$).
- **기본 행 연산 (elementary row operation)**: ① 두 행 교환, ② 한 행에 0이 아닌 상수 곱하기, ③ 한 행의 상수배를 다른 행에 더하기.
- **기본행렬 (elementary matrix)**: 항등행렬에 기본 행 연산을 **한 번** 적용한 행렬.
- **기약 행 사다리꼴 (reduced row echelon form, RREF)**: 행 사다리꼴에 더해 피벗이 있는 열의 다른 성분이 모두 0인 형태. (보통 피벗은 1)
- **기저 (basis)**: **선형독립**이면서 벡터공간을 **생성**하는 벡터들의 집합.
- **기저벡터 (basis vector)**: 기저를 이루는 벡터. 예: $\mathbf{i}, \mathbf{j}, \mathbf{k}$

### ㄴ

- **내적 (inner product, dot product)**: $\mathbf{u} \cdot \mathbf{v} = \sum u_iv_i = \|\mathbf{u}\|\|\mathbf{v}\|\cos\theta$. 결과는 **스칼라**다.
- **내적공간 (inner product space)**: 내적의 성질(교환, 배분, 양의 정부호 등)을 만족하는 벡터공간.
- **노름 (norm)**: 벡터의 크기(길이). $\|\mathbf{v}\| = \sqrt{v_1^2 + \cdots + v_n^2} = \sqrt{\mathbf{v} \cdot \mathbf{v}}$

### ㄷ

- **단사함수 (injective function)**: $f(a_i) = f(a_j) \Rightarrow a_i = a_j$ 인 함수. 서로 다른 원소를 서로 다른 원소로 보낸다.
- **단위벡터 (unit vector)**: 크기가 1인 벡터. $\mathbf{e} = \mathbf{v} / \|\mathbf{v}\|$
- **단위좌표벡터 (unit coordinate vector)**: 좌표축 방향의 단위벡터. $\mathbf{i} = (1, 0)$, $\mathbf{j} = (0, 1)$ 등.
- **단위행렬 / 항등행렬 (identity matrix)**: 주대각선이 모두 1이고 나머지는 0인 정방행렬 $I$. $AI = IA = A$
- **닮은행렬 (similar matrix)**: $B = C^{-1}AC$ 를 만족하는 $A$와 $B$. 같은 고유값을 가진다.
- **대각합 (trace)**: 정방행렬의 주대각선 원소의 합. $\text{tr}(A)$. 고유값의 합과 같다.
- **대각행렬 (diagonal matrix)**: 주대각선 이외의 모든 성분이 0인 정방행렬.
- **대각화 (diagonalization)**: $C^{-1}AC = D$ (대각행렬)가 되도록 하는 것. $C$의 열은 $A$의 고유벡터다.
- **대칭행렬 (symmetric matrix)**: $A = A^T$ 인 정방행렬.
- **동차선형시스템 (homogeneous system)**: 상수항이 모두 0인 선형시스템 $A\mathbf{x} = \mathbf{0}$. 항상 자명해를 가진다.
- **동치 (equivalent)**: 두 선형시스템의 해가 같거나, 두 벡터의 크기와 방향이 같은 경우.

### ㄹ

- **레온티에프 입출력 모형 (Leontief input-output model)**: 산업 간 수요·공급을 선형방정식으로 나타낸 경제 모형.

### ㅁ

- **마르코프 체인 (Markov chain)**: 상태벡터를 추이행렬로 반복 변환하는 확률 모델. $\mathbf{x}(k+1) = P\mathbf{x}(k)$

### ㅂ

- **반사변환 (reflection transformation)**: 축이나 직선에 대해 대칭시키는 선형변환. 예: x축 반사 $\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$
- **벡터 (vector)**: 크기와 방향을 함께 가진 양.
- **벡터공간 (vector space)**: 벡터의 합과 스칼라 곱에 대해 닫혀 있고 10가지 공리를 만족하는 집합.
- **변수 (variable, unknown)**: 선형방정식의 미지수 $x_1, \dots, x_n$.
- **변환 (transformation)**: 입력값과 출력값이 모두 벡터인 함수. $L, T, F$ 등으로 쓴다.
- **부분공간 (subspace)**: 벡터공간의 부분집합 중 합과 스칼라 곱에 대해 닫혀 있는 것. 반드시 영벡터를 포함한다.
- **부행렬 (submatrix)**: 행렬을 블록으로 나눈 각 부분 행렬.
- **비자명해 (nontrivial solution)**: 동차선형시스템에서 0이 아닌 성분을 하나라도 가진 해.

### ㅅ

- **사루스의 공식 (Sarrus's formula)**: $3 \times 3$ 이하 행렬식을 대각선 방향 곱으로 구하는 도식적 방법.
- **사영변환 (projection transformation)**: 높은 차원의 벡터를 낮은 차원(평면, 축)으로 수직 투영하는 선형변환.
- **상 (image)**: 함수 $f(x) = y$ 에서 $y$. 이미지 또는 함수값이라고도 한다.
- **상등 (equal)**: 두 행렬(벡터)의 대응 성분이 모두 같은 것.
- **상부삼각행렬 (upper triangular matrix)**: 주대각선 아래가 모두 0인 정방행렬.
- **생성 (span)**: 벡터공간의 모든 벡터를 주어진 벡터들의 선형결합으로 나타낼 수 있는 것.
- **선형 (linear)**: 원소들의 선형결합이 다시 그 집합에 속하는 성질. 그래프가 직선이고 1차식이다.
- **선형결합 (linear combination)**: $a_1\mathbf{v}_1 + a_2\mathbf{v}_2 + \cdots + a_n\mathbf{v}_n$ 의 형태. 1차결합이라고도 한다.
- **선형대수학 (linear algebra)**: 선형방정식, 행렬, 벡터공간, 선형사상을 다루는 학문.
- **선형독립 (linearly independent)**: $\sum a_i\mathbf{v}_i = \mathbf{0}$ 의 해가 $a_1 = \cdots = a_n = 0$ 뿐인 경우.
- **선형방정식 (linear equation)**: $a_1x_1 + \cdots + a_nx_n = b$ 꼴의 방정식. 변수가 1차항으로만 나타난다.
- **선형변환 / 선형사상 (linear transformation / linear mapping)**: $L(\mathbf{u} + \mathbf{v}) = L(\mathbf{u}) + L(\mathbf{v})$, $L(\alpha\mathbf{u}) = \alpha L(\mathbf{u})$ 를 만족하는 함수.
- **선형시스템 (linear system)**: 유한개의 선형방정식의 집합. 선형연립방정식이라고도 한다.
- **선형연산자 (linear operator)**: 정의역과 공변역이 같은($V \to V$) 선형변환.
- **선형종속 (linearly dependent)**: 적어도 하나는 0이 아닌 계수로 $\sum a_i\mathbf{v}_i = \mathbf{0}$ 을 만들 수 있는 경우. 어떤 벡터가 나머지의 선형결합으로 표현된다.
- **성분 (component)**: 행렬의 $a_{ij}$ 나 벡터의 각 좌표값. 항(entry)이라고도 한다.
- **소거법 (method of elimination)**: 방정식에 상수를 곱해 더하면서 변수를 하나씩 없애는 방법.
- **소행렬식 (minor)**: $i$행과 $j$열을 제거한 부분행렬의 행렬식 $M_{ij}$.
- **수반행렬 (adjugate matrix)**: 여인수 행렬의 전치행렬 $\text{Adj}(A)$. $A^{-1} = \frac{1}{\det A}\text{Adj}(A)$
- **스칼라 (scalar)**: 크기만 가진 양(실수).
- **스칼라 곱 (scalar multiplication)**: 스칼라 × 벡터(행렬). 모든 성분에 스칼라를 곱한다.
- **시점 (initial point, tail)**: 벡터(화살표)의 시작점.
- **심볼행렬 (symbolic matrix)**: 외적 계산에 쓰는 $\begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ u_1 & u_2 & u_3 \\ v_1 & v_2 & v_3 \end{vmatrix}$ 형태.

### ㅇ

- **역대입법 (back-substitution)**: 마지막 식에서 구한 값을 위의 식에 차례로 대입해 해를 구하는 방법.
- **역행렬 (inverse matrix)**: $AA^{-1} = A^{-1}A = I$ 를 만족하는 $A^{-1}$. 존재하면 유일하다.
- **여인수 (cofactor)**: $A_{ij} = (-1)^{i+j}M_{ij}$. 여인자라고도 한다.
- **여인수 전개 (cofactor expansion)**: $\det(A) = \sum_j a_{ij}A_{ij}$ 처럼 한 행(열)을 기준으로 행렬식을 계산하는 방법.
- **열벡터 (column vector)**: $m \times 1$ 행렬 형태의 벡터.
- **영벡터 (zero vector)**: 모든 성분이 0인 벡터 $\mathbf{0}$. 크기가 0이다.
- **영벡터공간 (zero vector space)**: 영벡터 하나로만 이루어진 벡터공간.
- **영행렬 (zero matrix)**: 모든 성분이 0인 행렬 $O$.
- **외적 (cross product)**: $R^3$에서 $\mathbf{u} \times \mathbf{v} = (\|\mathbf{u}\|\|\mathbf{v}\|\sin\theta)\mathbf{e}$. 두 벡터에 모두 수직인 **벡터**이며, 크기는 평행사변형의 면적이다.
- **위치벡터 (position vector)**: 원점에서 한 점으로 향하는 벡터.
- **유클리드 거리 (Euclidean distance)**: $\sqrt{\sum(q_i - p_i)^2}$. 두 점 사이의 직선 거리.
- **유클리드 노름 (Euclidean norm)**: 유클리드 거리에 대응하는 노름.
- **유향선분 (directed segment)**: 방향을 가진 선분 $\overrightarrow{PQ}$.
- **인접행렬 (adjacency matrix)**: 점 $i$와 $j$가 연결되어 있으면 1, 아니면 0인 행렬. 그래프 표현에 쓴다.

### ㅈ

- **자명해 (trivial solution)**: 동차선형시스템의 해 $x_1 = \cdots = x_n = 0$.
- **자유변수 (free variable)**: 피벗이 없는 열에 대응하는 변수. 임의의 값을 가질 수 있어 무한히 많은 해를 만든다.
- **전단사함수 (bijective function)**: 단사이면서 전사인 함수. 1대1 대응함수라고도 한다.
- **전사함수 (surjective function, onto)**: 공변역의 모든 원소가 대응되는 함수.
- **전치행렬 (transpose matrix)**: 행과 열을 바꾼 행렬 $A^T$. $(AB)^T = B^TA^T$
- **전향단계 / 전향 소거법 (forward phase / forward elimination)**: 피벗 아래를 0으로 만드는 단계.
- **정방행렬 (square matrix)**: 행의 수와 열의 수가 같은 행렬.
- **정사영 (orthogonal projection)**: 한 벡터를 다른 벡터 위로 수직으로 내린 벡터. $p_{\mathbf{u}}(\mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\mathbf{u} \cdot \mathbf{u}}\mathbf{u}$
- **정의역 (domain)**: 함수 $f: X \to Y$ 에서 $X$.
- **정칙행렬 (non-singular matrix)**: $\det(A) \neq 0$ 인 행렬. 역행렬이 존재한다.
- **정규 직교 집합 (orthonormal set)**: 서로 직교하고 각 벡터의 크기가 1인 벡터들의 집합.
- **종점 (terminal point, head)**: 벡터(화살표)의 끝점.
- **주대각선 (main diagonal)**: 정방행렬의 $a_{11}, a_{22}, \dots, a_{nn}$ 이 놓인 선.
- **중복 해 (multiplicity solution)**: 특성방정식에서 $k$번($k \ge 2$) 나타나는 고유값.
- **직교 (orthogonal)**: $\mathbf{u} \cdot \mathbf{v} = 0$, 즉 두 벡터가 수직인 것.
- **직교 집합 (orthogonal set)**: 서로 다른 벡터끼리 모두 직교하는 벡터들의 집합.
- **차원 (dimension)**: 기저를 이루는 벡터의 개수. $\dim(V)$
- **첨가행렬 (augmented matrix)**: 계수행렬 오른쪽에 상수항(또는 다른 행렬)을 덧붙인 행렬. $[A \mid \mathbf{b}]$

### ㅊ

- **체적 (volume)**: 평행육면체의 부피. $|\det[\mathbf{u}\ \mathbf{v}\ \mathbf{w}]| = |\mathbf{u} \cdot (\mathbf{v} \times \mathbf{w})|$
- **추이행렬 (transition matrix)**: 마르코프 체인에서 상태 간 이동 확률을 나타낸 행렬.
- **축소변환 (contraction transformation)**: $L(\mathbf{v}) = r\mathbf{v}$, $0 < r < 1$ 인 선형변환.
- **층밀림변환 (shear transformation)**: 바닥을 고정하고 윗부분을 옆으로 미는 변환. 표준행렬 $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$
- **치역 (range)**: 함수값(상)들의 집합.

### ㅋ

- **커널 (kernel)**: $L(\mathbf{v}) = \mathbf{0}$ 을 만족하는 벡터들의 집합 $\ker(L)$.
- **코시-슈바르츠 부등식 (Cauchy-Schwarz inequality)**: $|\mathbf{u} \cdot \mathbf{v}| \le \|\mathbf{u}\|\|\mathbf{v}\|$
- **크래머의 규칙 (Cramer's rule)**: $x_j = \det(A_j) / \det(A)$. $A_j$는 $A$의 $j$번째 열을 $\mathbf{b}$로 바꾼 행렬이다.
- **키르히호프 법칙 (Kirchhoff's laws)**: 전류법칙(들어오는 전류 = 나가는 전류)과 전압법칙(전압강하의 합 = 기전력).

### ㅌ

- **특성다항식 (characteristic polynomial)**: $\det(A - \lambda I)$. 고유다항식이라고도 한다.
- **특성방정식 (characteristic equation)**: $\det(A - \lambda I) = 0$. 고유방정식이라고도 한다.
- **특이행렬 (singular matrix)**: $\det(A) = 0$ 인 행렬. 역행렬이 존재하지 않는다.

### ㅍ

- **평행육면체 (parallelepiped)**: 세 벡터로 만들어지는 입체. 체적 = 행렬식의 절댓값.
- **표준기저 / 자연기저 (standard basis / natural basis)**: $\mathbf{e}_i$ 가 $i$번째 성분만 1이고 나머지는 0인 기저. $R^3$에서는 $\mathbf{i}, \mathbf{j}, \mathbf{k}$.
- **표준행렬 (standard matrix)**: 선형변환 $L$에 대해 $L(\mathbf{x}) = A\mathbf{x}$ 를 만족하는 유일한 행렬. $A = [L(\mathbf{e}_1) \cdots L(\mathbf{e}_n)]$
- **피벗 (pivot)**: 각 행에서 0이 아닌 첫 번째 수. 선행자(leading one)라고도 한다.

### ㅎ

- **하부삼각행렬 (lower triangular matrix)**: 주대각선 위가 모두 0인 정방행렬.
- **함수 (function)**: 정의역의 모든 원소가 공변역의 원소 하나와만 대응하는 관계.
- **합성함수 (composition function)**: $g \circ f(a) = g(f(a))$
- **해 (solution)**: 방정식(시스템)을 성립시키는 변수 값.
- **해가 없다 / 해가 있다 (inconsistent / consistent)**: 선형시스템의 해 존재 여부.
- **해집합 (solution set)**: 선형시스템의 모든 해의 집합.
- **행 동치 (row equivalent)**: 기본 행 연산으로 서로 바꿀 수 있는 두 행렬.
- **행 사다리꼴 (row echelon form, REF)**: 영행은 아래에 있고, 아래 행의 피벗이 위 행의 피벗보다 오른쪽에 있는 형태.
- **행렬 (matrix)**: 수나 문자를 직사각형 배열로 나타낸 것. $m \times n$ 행렬.
- **행렬식 (determinant)**: 정방행렬에 하나의 스칼라를 대응시키는 함수. $\det(A)$ 또는 $|A|$
- **행벡터 (row vector)**: $1 \times n$ 행렬 형태의 벡터.
- **확대변환 (dilation transformation)**: $L(\mathbf{v}) = r\mathbf{v}$, $r > 1$ 인 선형변환.
- **회전변환 (rotation transformation)**: 원점을 중심으로 $\phi$만큼 회전. $\begin{bmatrix} \cos\phi & -\sin\phi \\ \sin\phi & \cos\phi \end{bmatrix}$ (반시계 방향)
- **후향단계 (backward phase)**: 피벗 위까지 0으로 만들어 RREF를 완성하는 단계.

### 영문 약어 / 기타

- **LU-분해 (LU-decomposition)**: $A = LU$ ($L$: 하부삼각, $U$: 상부삼각)로 분해해 선형시스템을 푸는 방법.
- **삼각 부등식 (triangle inequality)**: $\|\mathbf{u} + \mathbf{v}\| \le \|\mathbf{u}\| + \|\mathbf{v}\|$
- **피타고라스 정리 (Pythagorean theorem)**: $\mathbf{u} \perp \mathbf{v} \iff \|\mathbf{u} + \mathbf{v}\|^2 = \|\mathbf{u}\|^2 + \|\mathbf{v}\|^2$
- **$R^n$ (유클리드 공간)**: $n$개의 실수 순서쌍으로 이루어진 벡터공간. $R^1$ 직선, $R^2$ 평면, $R^3$ 공간.

### 인공지능 관련

- **신경망 (neural network)**: 뉴런 사이의 연결강도를 조정하며 학습하는 인공지능 모델.
- **뉴런 (neuron)**: 신경망의 기본 단위.
- **연결강도 (weight)**: 신경망에서 입력에 곱해지는 가중치. 입력과 연결강도의 곱은 벡터 내적(행렬 곱)으로 계산한다.
- **역전파 (backpropagation)**: 다층 퍼셉트론의 학습 알고리즘.
- **딥러닝 / 심층신경망 (deep learning / DNN)**: 여러 층의 신경망을 이용한 학습.
- **분류 (classification) / 클러스터링 (clustering)**: 데이터를 그룹으로 나누는 작업. 유클리드 거리를 이용한 K-mean, K-NN 등이 있다.
