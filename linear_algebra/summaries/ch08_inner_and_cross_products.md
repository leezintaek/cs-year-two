# Chapter 08. 벡터의 내적과 외적

> 원본: `chapters/ch08_inner_and_cross_products.pdf` (책 426–461쪽)

---

## 8.1 내적

### 8.1.1 내적의 정의

- **정의 8-1**: $\mathbf{u}, \mathbf{v}$ 가 $R^n$의 벡터일 때, $R^n$의 **내적(inner product, dot product, 內積)** 은 다음과 같은 **스칼라 값**으로 정의되며 $\mathbf{u} \cdot \mathbf{v}$ 로 쓴다.

$$
\mathbf{u} \cdot \mathbf{v} = \mathbf{u}^T\mathbf{v} = [u_1\ u_2\ \cdots\ u_n]\begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{bmatrix} = u_1v_1 + u_2v_2 + \cdots + u_nv_n
$$

  - $R^2$: $\mathbf{u} \cdot \mathbf{v} = u_1v_1 + u_2v_2$
  - $R^3$: $\mathbf{u} \cdot \mathbf{v} = u_1v_1 + u_2v_2 + u_3v_3$
- **예제 8-1**: $\mathbf{u} = (2, -5, -1)$, $\mathbf{v} = (3, 2, -3)$ → $\mathbf{u} \cdot \mathbf{v} = 6 - 10 + 3 = -1$, $\mathbf{v} \cdot \mathbf{u} = -1$ (같음)
- **예제 8-2**: $\mathbf{u} = (1,2,4), \mathbf{v} = (2,-3,5), \mathbf{w} = (4,2,-3)$ → $\mathbf{u} \cdot \mathbf{v} = 16$, $\mathbf{u} \cdot \mathbf{w} = -4$, $\mathbf{v} \cdot \mathbf{w} = -13$
- **정리 8-1**: 표준기저로 표현된 벡터 $\mathbf{u} = u_1\mathbf{i} + u_2\mathbf{j} + u_3\mathbf{k}$, $\mathbf{v} = v_1\mathbf{i} + v_2\mathbf{j} + v_3\mathbf{k}$ 도 내적은 각 성분끼리 곱해서 더한다.
  - 예: $\mathbf{u} = -3\mathbf{i} + 3\mathbf{j} + 5\mathbf{k}$, $\mathbf{v} = -2\mathbf{i} + 3\mathbf{j} - 2\mathbf{k}$ → $6 + 9 - 10 = 5$

#### 노름과 거리

- **정의 8-2**: 벡터 $\mathbf{u} = (u_1, u_2, u_3)$ 의 **노름(norm)** 또는 **길이(length)**:

$$
\|\mathbf{u}\| = \sqrt{\mathbf{u} \cdot \mathbf{u}} = \sqrt{u_1^2 + u_2^2 + u_3^2}
$$

  - 두 벡터 사이의 **거리(distance)**: $\|\mathbf{u} - \mathbf{v}\| = \|\mathbf{v} - \mathbf{u}\| = \sqrt{(u_1 - v_1)^2 + (u_2 - v_2)^2 + (u_3 - v_3)^2}$
- **예제 8-3**: $\mathbf{u} = (1, 2, 3), \mathbf{v} = (-4, 3, 5)$ → $\|\mathbf{v} - \mathbf{u}\| = \sqrt{25 + 1 + 4} = \sqrt{30}$
- **예제 8-4**: $\mathbf{u} = (2, -5, -1), \mathbf{v} = (-7, -4, 6)$ → $\mathbf{u} \cdot \mathbf{v} = 0$, $\|\mathbf{u}\|^2 = 30$, $\|\mathbf{u} - \mathbf{v}\|^2 = 81 + 1 + 49 = 131$

#### 내적과 각

- **정의 8-3**: 두 벡터 $\mathbf{u}, \mathbf{v}$ 가 이루는 각을 $\theta$ ($0 \le \theta \le \pi$) 라 하면

$$
\mathbf{u} \cdot \mathbf{v} = \begin{cases} \|\mathbf{u}\|\|\mathbf{v}\|\cos\theta & \mathbf{u} \neq \mathbf{0},\ \mathbf{v} \neq \mathbf{0} \\ 0 & \mathbf{u} = \mathbf{0} \text{ 또는 } \mathbf{v} = \mathbf{0} \end{cases}
\qquad\Rightarrow\qquad
\cos\theta = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|\|\mathbf{v}\|}
$$

- **예제 8-5**: $\mathbf{u} = (1, 1, 0), \mathbf{v} = (0, 1, 1)$ → $\cos\theta = \frac{1}{\sqrt{2}\sqrt{2}} = \frac{1}{2}$ → $\theta = 60°$
- **예제 8-6**: $\mathbf{u} = (1, -1, 0), \mathbf{v} = (2, -1, 2)$ → $\mathbf{u} \cdot \mathbf{v} = 3$, $\|\mathbf{u}\| = \sqrt{2}$, $\|\mathbf{v}\| = 3$ → $\cos\theta = \frac{1}{\sqrt{2}}$ → $\theta = 45°\ (\frac{\pi}{4})$
- 자주 쓰는 $\cos$ 값: $\cos 0° = 1$, $\cos 30° = \frac{\sqrt{3}}{2}$, $\cos 45° = \frac{1}{\sqrt{2}}$, $\cos 60° = \frac{1}{2}$, $\cos 90° = 0$
- **정리 8-2 (피타고라스 정리)**: 두 벡터 $\mathbf{u}, \mathbf{v}$ 가 수직일 필요충분조건은 $\|\mathbf{u} + \mathbf{v}\|^2 = \|\mathbf{u}\|^2 + \|\mathbf{v}\|^2$ 이다.

### 8.1.2 내적의 성질과 직교

- **정리 8-3 (내적의 성질)**: $R^2$나 $R^3$의 벡터 $\mathbf{u}, \mathbf{v}, \mathbf{w}$ 와 스칼라 $c$ 에 대해
  1. $\mathbf{u} \cdot \mathbf{u} \ge 0$
  2. $\mathbf{u} \cdot \mathbf{v} = \mathbf{v} \cdot \mathbf{u}$ (교환법칙)
  3. $(\mathbf{u} + \mathbf{v}) \cdot \mathbf{w} = \mathbf{u} \cdot \mathbf{w} + \mathbf{v} \cdot \mathbf{w}$ (배분법칙)
  4. $\mathbf{u} \cdot (\mathbf{v} + \mathbf{w}) = \mathbf{u} \cdot \mathbf{v} + \mathbf{u} \cdot \mathbf{w}$
  5. $c\mathbf{u} \cdot \mathbf{v} = c(\mathbf{u} \cdot \mathbf{v})$
  6. $\mathbf{u} \cdot \mathbf{0} = \mathbf{0} \cdot \mathbf{u} = 0$
  7. $\mathbf{u} \cdot \mathbf{u} = \|\mathbf{u}\|^2$
  - 이러한 내적의 성질을 만족하는 벡터공간을 **내적공간(inner product space)** 이라 한다.
- **정의 8-4 (직교)**: 내적공간 $V$의 두 벡터에서 $\mathbf{u} \cdot \mathbf{v} = 0$ 이면 **직교(orthogonal, 直交)** 한다 또는 **수직**이라 한다.
  - 예: $(1, 2) \cdot (6, -3) = 6 - 6 = 0$ → 직교
  - $\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\|\|\mathbf{v}\|\cos\theta = 0$ 이면 $\cos\theta = 0$, 즉 $\theta = 90°\ (\frac{\pi}{2})$
- **예제 8-7**: $(2, -4) \cdot (4, 2) = 8 - 8 = 0$ → 직교
- **예제 8-8**: (1) $(3, 2, -5, 0) \cdot (-4, 1, -2, 6) = -12 + 2 + 10 + 0 = 0$ → 직교, (2) $(0, -1, 1, 4) \cdot (2, 0, -8, 2) = 0$ → 직교
- **예제 8-9**: $\mathbf{u} = (1,1,1), \mathbf{v} = (1,2,-3), \mathbf{w} = (1,-4,3)$ → $\mathbf{u} \perp \mathbf{v}$, $\mathbf{u} \perp \mathbf{w}$ 이지만 $\mathbf{v} \cdot \mathbf{w} = -16$ 이므로 $\mathbf{v}$와 $\mathbf{w}$는 직교하지 않는다.
- **정리 8-4 (내적의 부호와 각)**: $\mathbf{u}, \mathbf{v}$ 가 영벡터가 아닐 때 (역도 성립)
  1. $\mathbf{u} \cdot \mathbf{v} = 0$ 이면 $\theta$는 **직각** ($\cos\theta = 90°$)
  2. $\mathbf{u} \cdot \mathbf{v} > 0$ 이면 $\theta$는 **예각**
  3. $\mathbf{u} \cdot \mathbf{v} < 0$ 이면 $\theta$는 **둔각**
  - 예: $(1, 0) \cdot (1, 1) = 1 > 0$ → 예각(45°)

#### 정규 직교 집합

- **정의 8-5**: $R^n$의 벡터 집합 $S = \{\mathbf{v}_1, \dots, \mathbf{v}_k\}$ 가 다음을 만족하면 **정규 직교 집합(orthonormal set)** 이라 한다.
  1. $\mathbf{v}_i \cdot \mathbf{v}_j = 0$ ($i \neq j$)
  2. $\mathbf{v}_i \cdot \mathbf{v}_i = 1$
  - (1)식만 만족하면 **직교 집합(orthogonal set)** 이라 한다.
- **정리 8-5**: $S$가 영벡터가 아닌 벡터들의 직교 집합이면 $S$는 **선형독립**이다.
  - 증명: $c_1\mathbf{v}_1 + \cdots + c_k\mathbf{v}_k = \mathbf{0}$ 의 양변에 $\mathbf{v}_i$ 를 내적하면 다른 항은 모두 0이 되고 $c_i\|\mathbf{v}_i\|^2 = 0$ 이 남는다. $\mathbf{v}_i \neq \mathbf{0}$ 이므로 $c_i = 0$ 이다.

[보충] 직교 집합은 서로 수직인 벡터들의 모임이고, 정규 직교 집합은 거기에 **각 벡터의 길이가 1**이라는 조건을 더한 것이다. 표준기저 $\{\mathbf{i}, \mathbf{j}, \mathbf{k}\}$ 가 대표적인 정규 직교 집합이다. 직교 집합을 정규 직교 집합으로 바꾸려면 각 벡터를 자기 길이로 나누면 된다(정규화).

#### 정사영과 부등식

- **정의 8-6 (정사영)**: 두 벡터 $\mathbf{u}, \mathbf{v}$ ($\mathbf{u} \neq \mathbf{0}$) 에서, $\mathbf{v}$의 끝에서 $\mathbf{u}$ 위로 수직으로 내린 발까지의 벡터 $p_{\mathbf{u}}(\mathbf{v})$ 를 $\mathbf{u}$에 대한 $\mathbf{v}$의 **정사영(orthogonal projection, 正射影)** 이라 한다. ($\mathbf{u}$ 위에서 $\mathbf{v}$와 거리가 가장 가까운 벡터)

[보충] 정사영 공식: $p_{\mathbf{u}}(\mathbf{v}) = \dfrac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|^2}\mathbf{u} = \dfrac{\mathbf{u} \cdot \mathbf{v}}{\mathbf{u} \cdot \mathbf{u}}\mathbf{u}$. 예: $\mathbf{u} = (1, 0)$, $\mathbf{v} = (3, 4)$ → $p_{\mathbf{u}}(\mathbf{v}) = \frac{3}{1}(1, 0) = (3, 0)$. 이때 $\mathbf{v} - p_{\mathbf{u}}(\mathbf{v})$ 는 $\mathbf{u}$와 직교한다.

- **정리 8-6 (코시-슈바르츠 부등식, Cauchy-Schwartz Inequality)**: $|\mathbf{u} \cdot \mathbf{v}| \le \|\mathbf{u}\|\|\mathbf{v}\|$
  - 간편한 증명: $\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\|\|\mathbf{v}\|\cos\theta$ 이고 $-1 \le \cos\theta \le 1$ 이므로 $-\|\mathbf{u}\|\|\mathbf{v}\| \le \mathbf{u} \cdot \mathbf{v} \le \|\mathbf{u}\|\|\mathbf{v}\|$
  - 여러 분야에 응용되는 중요한 부등식이다.
- **정리 8-7 (삼각 부등식, Triangle Inequality)**: $\|\mathbf{u} + \mathbf{v}\| \le \|\mathbf{u}\| + \|\mathbf{v}\|$
  - 증명: $\|\mathbf{u} + \mathbf{v}\|^2 = \|\mathbf{u}\|^2 + 2\mathbf{u} \cdot \mathbf{v} + \|\mathbf{v}\|^2 \le \|\mathbf{u}\|^2 + 2\|\mathbf{u}\|\|\mathbf{v}\| + \|\mathbf{v}\|^2 = (\|\mathbf{u}\| + \|\mathbf{v}\|)^2$
  - 의미: 두 벡터의 합의 길이는 각각의 길이의 합보다 작거나 같다.
- 벡터의 내적은 **신경망에서 입력과 연결강도의 곱**을 효율적으로 수행한다.

---

## 8.2 외적

### 8.2.1 외적의 정의

- **정의 8-7**: $R^3$의 두 벡터 $\mathbf{u}, \mathbf{v}$ 의 다음과 같은 벡터 곱을 **외적(cross product, 外積)** 이라 한다.

$$
\mathbf{u} \times \mathbf{v} = (\|\mathbf{u}\|\|\mathbf{v}\|\sin\theta)\,\mathbf{e}
$$

  - $\theta$ ($0 \le \theta \le \pi$): 두 벡터 사이의 각
  - $\mathbf{e}$: **오른손 법칙**에 따라 방향을 가지며, $\mathbf{u}$와 $\mathbf{v}$가 만드는 평면에 **수직인 단위벡터**. $\mathbf{u}$와 $\mathbf{v}$에 공통으로 수직인 단위벡터는 2가지 방향이 있다.
  - 오른손 네 손가락을 $\mathbf{u}$에서 $\mathbf{v}$ 방향으로 감으면 엄지 방향이 $\mathbf{u} \times \mathbf{v}$, 반대로 감으면 $\mathbf{v} \times \mathbf{u}$ 다.
- **정리 8-8**: $\|\mathbf{u} \times \mathbf{v}\| = \|\mathbf{u}\|\|\mathbf{v}\|\sin\theta$
  - 이 크기는 **$\mathbf{u}$와 $\mathbf{v}$가 이루는 평행사변형의 면적**과 같다(밑변 $\|\mathbf{u}\|$ × 높이 $\|\mathbf{v}\|\sin\theta$).
  - 즉 외적 $\mathbf{u} \times \mathbf{v}$ 는 $\mathbf{u}, \mathbf{v}$ 에 각각 수직이고, 크기는 평행사변형의 면적이다.
- 자주 쓰는 $\sin$ 값: $\sin 0° = 0$, $\sin 30° = \frac{1}{2}$, $\sin 45° = \frac{1}{\sqrt{2}}$, $\sin 60° = \frac{\sqrt{3}}{2}$, $\sin 90° = 1$
- **정리 8-9 (성분 계산)**: $\mathbf{u} = u_1\mathbf{i} + u_2\mathbf{j} + u_3\mathbf{k}$, $\mathbf{v} = v_1\mathbf{i} + v_2\mathbf{j} + v_3\mathbf{k}$ 일 때

$$
\mathbf{u} \times \mathbf{v} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ u_1 & u_2 & u_3 \\ v_1 & v_2 & v_3 \end{vmatrix}
= \begin{vmatrix} u_2 & u_3 \\ v_2 & v_3 \end{vmatrix}\mathbf{i} - \begin{vmatrix} u_1 & u_3 \\ v_1 & v_3 \end{vmatrix}\mathbf{j} + \begin{vmatrix} u_1 & u_2 \\ v_1 & v_2 \end{vmatrix}\mathbf{k}
$$

$$
= (u_2v_3 - u_3v_2,\ u_3v_1 - u_1v_3,\ u_1v_2 - u_2v_1)
$$

  - 이 형태의 행렬을 **심볼행렬(Symbolic matrix)** 이라고 부른다. 3장의 여인수 전개와 같은 방식으로 계산한다.
- **예제 8-10**: $\mathbf{u} = 3\mathbf{i} - \mathbf{j} + 2\mathbf{k}$, $\mathbf{v} = \mathbf{i} - 2\mathbf{j} + 4\mathbf{k}$
  - $\mathbf{u} \times \mathbf{v} = (-4 + 4)\mathbf{i} - (12 - 2)\mathbf{j} + (-6 + 1)\mathbf{k} = 0\mathbf{i} - 10\mathbf{j} - 5\mathbf{k}$

[보충] 내적과 외적 비교:

| | 내적 $\mathbf{u} \cdot \mathbf{v}$ | 외적 $\mathbf{u} \times \mathbf{v}$ |
|---|---|---|
| 결과 | **스칼라** | **벡터** |
| 정의되는 공간 | $R^n$ (모든 차원) | $R^3$ |
| 크기 | $\|\mathbf{u}\|\|\mathbf{v}\|\cos\theta$ | $\|\mathbf{u}\|\|\mathbf{v}\|\sin\theta$ |
| 0이 되는 경우 | 두 벡터가 **직교** | 두 벡터가 **평행** |
| 교환 | $\mathbf{u} \cdot \mathbf{v} = \mathbf{v} \cdot \mathbf{u}$ | $\mathbf{u} \times \mathbf{v} = -(\mathbf{v} \times \mathbf{u})$ |
| 기하학적 의미 | 각, 정사영, 직교 판정 | 법선 벡터, 평행사변형 면적 |

### 8.2.2 외적의 성질

- **정리 8-10**: $R^3$의 벡터 $\mathbf{u}, \mathbf{v}, \mathbf{w}$ 와 스칼라 $\alpha$ 에 대해
  1. $\mathbf{u} \times \mathbf{0} = \mathbf{0} \times \mathbf{u} = \mathbf{0}$
  2. $\mathbf{u} \times \mathbf{v} = -(\mathbf{v} \times \mathbf{u})$ (**교대법칙**)
  3. $(\alpha\mathbf{u}) \times \mathbf{v} = \alpha(\mathbf{u} \times \mathbf{v}) = \mathbf{u} \times (\alpha\mathbf{v})$ (배분법칙)
  4. $\mathbf{u} \times (\mathbf{v} + \mathbf{w}) = (\mathbf{u} \times \mathbf{v}) + (\mathbf{u} \times \mathbf{w})$
  5. $(\mathbf{u} \times \mathbf{v}) \cdot \mathbf{w} = \mathbf{u} \cdot (\mathbf{v} \times \mathbf{w}) = \begin{vmatrix} u_1 & u_2 & u_3 \\ v_1 & v_2 & v_3 \\ w_1 & w_2 & w_3 \end{vmatrix}$
  6. $\mathbf{u} \cdot (\mathbf{u} \times \mathbf{v}) = \mathbf{v} \cdot (\mathbf{u} \times \mathbf{v}) = 0$, 즉 $\mathbf{u} \times \mathbf{v}$ 는 $\mathbf{u}$와 $\mathbf{v}$ **모두와 직교**한다.
  7. $\mathbf{u} \times \mathbf{v} = \mathbf{0}$ 일 때 $\mathbf{u}$와 $\mathbf{v}$는 **평행**이다.
  8. $\mathbf{u} \times \mathbf{u} = \mathbf{0}$
  9. $\|\mathbf{u} \times \mathbf{v}\|$ 는 $\mathbf{u}, \mathbf{v}$ 에 의해 결정되는 **평행사변형의 면적**이다.
  10. $\mathbf{u} \cdot (\mathbf{v} \times \mathbf{w}) = (\mathbf{u} \times \mathbf{v}) \cdot \mathbf{w} = \pm$($\mathbf{u}, \mathbf{v}, \mathbf{w}$ 에 의해 결정되는 **체적**)
- **예제 8-11**: $\mathbf{u} \times \mathbf{v} = -(\mathbf{v} \times \mathbf{u})$ 확인 → 행렬식에서 **두 행을 교환하면 부호가 바뀌므로**($d \to -d$) 성립한다.
- **정리 8-11**: $\mathbf{u}$와 $\mathbf{v}$가 같은 방향이나 반대 방향을 가지거나, 어느 하나가 영벡터면 $\mathbf{u} \times \mathbf{v} = \mathbf{0}$ 이다. 그 밖의 경우에는 $\mathbf{u} \times \mathbf{v}$ 의 크기가 $\mathbf{u}$와 $\mathbf{v}$를 두 변으로 하는 평행사변형의 면적과 같고, 방향은 $\mathbf{u}$와 $\mathbf{v}$에 모두 수직이다.
- **정리 8-12 (표준단위벡터의 외적)**: $\mathbf{e}_1 = (1,0,0), \mathbf{e}_2 = (0,1,0), \mathbf{e}_3 = (0,0,1)$ 에 대해
  - $\mathbf{e}_1 \times \mathbf{e}_1 = \mathbf{e}_2 \times \mathbf{e}_2 = \mathbf{e}_3 \times \mathbf{e}_3 = \mathbf{0}$
  - $\mathbf{e}_1 \times \mathbf{e}_2 = \mathbf{e}_3 = -\mathbf{e}_2 \times \mathbf{e}_1$
  - $\mathbf{e}_2 \times \mathbf{e}_3 = \mathbf{e}_1 = -\mathbf{e}_3 \times \mathbf{e}_2$
  - $\mathbf{e}_3 \times \mathbf{e}_1 = \mathbf{e}_2 = -\mathbf{e}_1 \times \mathbf{e}_3$

[보충] 외우는 법: $\mathbf{i} \to \mathbf{j} \to \mathbf{k} \to \mathbf{i}$ 순환 순서대로 곱하면 다음 것이 $+$로 나온다($\mathbf{i} \times \mathbf{j} = \mathbf{k}$, $\mathbf{j} \times \mathbf{k} = \mathbf{i}$, $\mathbf{k} \times \mathbf{i} = \mathbf{j}$). 역순으로 곱하면 $-$가 붙는다.

### 8.2.3 외적의 응용

- 외적은 물리량이 작용하는 곳에 광범위하게 쓰인다. 여기서는 벡터공간 내의 **평행사변형과 삼각형의 면적**, **평행육면체의 체적**을 구한다.
- **예제 8-12 (평행사변형의 면적)**: $\mathbf{u} = (3, 1, 0), \mathbf{v} = (1, 3, 2)$
  - $\mathbf{u} \times \mathbf{v} = 2\mathbf{i} - 6\mathbf{j} + 8\mathbf{k}$ → 면적 $= \|\mathbf{u} \times \mathbf{v}\| = \sqrt{4 + 36 + 64} = 2\sqrt{26}$
- **예제 8-13 (삼각형의 면적)**: 꼭짓점 $(-1, 2, 0), (2, 1, 3), (1, 1, -1)$
  - 기준점 $(-1, 2, 0)$ 에서 $\mathbf{u} = (3, -1, 3)$, $\mathbf{v} = (2, -1, -1)$
  - $\mathbf{u} \times \mathbf{v} = 4\mathbf{i} + 9\mathbf{j} - \mathbf{k}$ → $\|\mathbf{u} \times \mathbf{v}\| = \sqrt{98} = 7\sqrt{2}$
  - 삼각형 면적 = 평행사변형 면적의 $\frac{1}{2}$ = $\frac{7\sqrt{2}}{2}$
- **예제 8-14 (평행육면체의 체적)**: $\mathbf{u} = (4, 1, 1), \mathbf{v} = (2, 1, 0), \mathbf{w} = (0, 2, 3)$
  - 체적 $= \begin{vmatrix} 4 & 1 & 1 \\ 2 & 1 & 0 \\ 0 & 2 & 3 \end{vmatrix} = 10$
  - 평행육면체(parallelepiped)의 체적은 그것을 이루는 벡터들의 행렬식 값(의 절댓값)으로 결정된다.

---

## 8.3 MATLAB에 의한 연산

- 내적: `dot(u, v)` → 예: `u=[2; -5; -1]; v=[3; 2; -3]; dot(u, v)` → `-1`
- 직교 확인: `dot([2; -4], [4; 2])` → `0`

[보충] 외적은 `cross(u, v)`, 노름은 `norm(u)` 로 구한다.

---

## 8.4 벡터 내적과 인공지능

### 8.4.1 인공지능과 벡터의 내적

- 신경망에서는 여러 뉴런으로부터 들어오는 입력값 $X_i$ 와 그 사이의 **연결강도(weight)** $W_i$ 를 곱해 모두 더한 뒤, **합성함수 $f$** 를 적용해 출력값을 계산한다.

$$
y = f\left(\sum_{i=0}^{N-1} W_iX_i - \theta\right)
$$

- 입력값과 연결강도를 각각 곱해 더하는 것은 사실상 **벡터 내적**이다. 행렬의 곱을 쓰면 매우 효율적이다.
- $\mathbf{u}, \mathbf{v}$ 의 **차원이 같아야** 한다. 신경망의 입력값과 연결강도가 각각 대응되어야 하기 때문이다.
- 예: $\mathbf{u} = (1, 2, 4)$, $\mathbf{v} = (4, 2, -3)$ → $\mathbf{u} \cdot \mathbf{v} = 4 + 4 - 12 = -4$

### 8.4.2 거리 개념과 인공지능 응용

#### (1) 유클리드 거리

- 인공지능에서는 두 점이나 벡터 사이의 거리를 이용해 **패턴(pattern)을 분류**하는 경우가 많다.
- **유클리드 거리(Euclidean distance)**: 두 점 사이의 거리를 계산할 때 흔히 쓰는 방법. 이 거리를 사용해 유클리드 공간을 정의할 수 있다. 이 거리에 대응하는 노름을 **유클리드 노름(Euclidean norm)** 이라 한다.

$$
d = \sqrt{(q_1 - p_1)^2 + (q_2 - p_2)^2 + \cdots + (q_n - p_n)^2} = \sqrt{\sum_{i=1}^{n}(q_i - p_i)^2}
$$

  - 예: $\mathbf{u} = (1, 2, 4)$, $\mathbf{v} = (4, 2, -3)$ → $d = \sqrt{9 + 0 + 49} = \sqrt{58}$
- 거리 개념은 신경망의 **K-mean, K-NN** 등 **분류(classification)** 를 위한 **클러스터링(clustering)** 에 쓰인다.

#### (2) 벡터 내적의 인공지능 활용

1. 신경망 학습에서 뉴런으로 들어오는 입력과 연결강도의 곱은 주로 벡터의 내적으로 연산된다.
2. 문과/이과에 관계없이 인공지능 관련 지식에는 벡터의 기초 개념이 필요하다.
3. 유클리드 거리는 각 점 사이의 거리를 측정해 신경망의 분류 작업에 유용하게 쓰인다.

---

## 벡터의 내적과 외적의 생활 속 응용 (책 460쪽)

- 내적: 복잡한 벡터공간에서 수직과 직선 방정식 구하기
- 내적: 역학, 자기공학, 전기공학
- 내적: 신경망에서 입력과 연결강도의 곱
- 외적: 벡터공간에서 면적, 체적 계산
- 외적: 물리학의 운동량과 토크
- 외적: 자기장의 로렌츠 힘(Lorentz force), 초음파 탐지, 전자레인지, 스피커 원자력 등

---

## 핵심 정리

- 내적 $\mathbf{u} \cdot \mathbf{v} = \sum u_iv_i = \|\mathbf{u}\|\|\mathbf{v}\|\cos\theta$ (결과는 **스칼라**)
- $\cos\theta = \dfrac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|\|\mathbf{v}\|}$
- **직교 ⟺ $\mathbf{u} \cdot \mathbf{v} = 0$** / 양수면 예각, 음수면 둔각
- $\|\mathbf{u}\| = \sqrt{\mathbf{u} \cdot \mathbf{u}}$, 거리 $= \|\mathbf{u} - \mathbf{v}\|$
- 코시-슈바르츠: $|\mathbf{u} \cdot \mathbf{v}| \le \|\mathbf{u}\|\|\mathbf{v}\|$ / 삼각 부등식: $\|\mathbf{u} + \mathbf{v}\| \le \|\mathbf{u}\| + \|\mathbf{v}\|$
- 영벡터가 아닌 벡터들의 직교 집합은 선형독립이다.
- 외적 $\mathbf{u} \times \mathbf{v}$: $R^3$에서만 정의, 결과는 **벡터**, 두 벡터 모두에 수직이다.
- $\|\mathbf{u} \times \mathbf{v}\| = \|\mathbf{u}\|\|\mathbf{v}\|\sin\theta$ = 평행사변형 면적 (삼각형은 그 절반)
- $\mathbf{u} \times \mathbf{v} = -(\mathbf{v} \times \mathbf{u})$, $\mathbf{u} \times \mathbf{u} = \mathbf{0}$, 평행이면 $\mathbf{0}$
- 평행육면체 체적 = $|\mathbf{u} \cdot (\mathbf{v} \times \mathbf{w})|$ = $|\det[\mathbf{u}; \mathbf{v}; \mathbf{w}]|$
