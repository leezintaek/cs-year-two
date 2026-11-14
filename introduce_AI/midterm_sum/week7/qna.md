# Week7 Q&A

---

## Q1. Activation Functions 파이썬 코드 분석 (슬라이드 14~15)

### 0) 원본 코드
```python
import torch
import torch.nn.functional as F

x = torch.tensor(output_layer_z)

# ReLU: max(0, x)
relu_output = F.relu(x)
print('--- ReLU ---')
print(relu_output)
print("=> Predicted Class: ", np.argmax(relu_output, axis=0))

# Sigmoid: 1 / (1 + exp(-x))
sigmoid_output = torch.sigmoid(x)
print('--- Sigmoide ---')
print(sigmoid_output)
print("=> Predicted Class: ", np.argmax(sigmoid_output, axis=0))

# Softmax: exp(x) / sum(exp(x))
softmax_output = F.softmax(x, dim=0)
print('--- Softmax ---')
print(softmax_output)
print("=> Predicted Class: ", np.argmax(softmax_output, axis=0))
```

### 1) 입력 `output_layer_z`는 어디서 왔나
- 슬라이드 10~11의 NumPy MLP(입력 2 → 은닉 4 → 출력 3)에서 계산한 **출력층의 z (활성 함수 적용 전 값)**다.
- 직접 계산하면:
  - 은닉층 z = [−0.22, 0.88, 0.58, 0.04] → Heaviside → [0, 1, 1, 1]
  - 출력층 z = W⁽²⁾ · [0, 1, 1, 1]ᵀ + b = **[−1.3, 0.34, 2.1]ᵀ** (Setosa, Versicolor, Virginica)
- 모양은 **(3, 1)** 열벡터다. 클래스 3개가 **세로(0번 축)**로 놓여 있다.
- 이 코드는 "출력층에 Heaviside 대신 **다른 활성 함수**를 쓰면 결과가 어떻게 달라지나"를 비교하는 코드다.

### 2) 한 줄씩 보기
- `x = torch.tensor(output_layer_z)`
  - NumPy 배열을 PyTorch 텐서로 바꾼다. 모양 (3, 1)은 그대로, dtype은 float64가 된다.
- `F.relu(x)`
  - 원소마다 max(0, x). 음수는 0으로, 양수는 그대로.
- `torch.sigmoid(x)`
  - 원소마다 1 / (1 + e⁻ˣ). 각 값을 **독립적으로** (0, 1) 사이로 눌러 준다.
- `F.softmax(x, dim=0)`
  - eˣ를 계산한 뒤 **dim=0 방향(세로, 클래스 축)의 합**으로 나눈다. 결과는 합이 1인 확률 분포.
  - `dim=0`인 이유: x가 (3, 1) 열벡터라 클래스가 0번 축에 있기 때문이다.
- `np.argmax(..., axis=0)`
  - 0번 축(클래스 축)에서 **가장 큰 값의 인덱스**를 돌려준다. 결과는 `[2]` 같은 배열 (열이 1개라서).
  - 인덱스 0 = Setosa, 1 = Versicolor, 2 = Virginica.

### 3) 실제 출력값 (손으로 계산)
| 함수      | Setosa | Versicolor | Virginica | 합     | argmax |
| --------- | ------ | ---------- | --------- | ------ | ------ |
| z         | -1.3   | 0.34       | 2.1       | 1.14   | 2      |
| Heaviside | 0      | 1          | 1         | 2      | 1      |
| ReLU      | 0      | 0.34       | 2.1       | 2.44   | 2      |
| Sigmoid   | 0.2142 | 0.5842     | 0.8909    | 1.6893 | 2      |
| Softmax   | 0.0277 | 0.1427     | 0.8296    | 1      | 2      |

- Heaviside 행은 비교용으로 넣은 것이다 (슬라이드 11, 16의 결과).

### 4) 분석 포인트
**(1) ReLU, Sigmoid, Softmax는 모두 예측 클래스가 2 (Virginica)로 같다**
- 세 함수 모두 **단조 증가** 함수라서 값의 크기 순서를 바꾸지 않는다. 그래서 argmax 결과는 z에 바로 argmax를 한 것과 같다.
- 그래서 슬라이드 18처럼 `output_z.argmax()`로 예측해도 `output_o.argmax()`와 결과가 같다.

**(2) Heaviside만 1 (Versicolor)이 나온다 → 정보 손실**
- Heaviside는 0.34와 2.1을 둘 다 **1로 뭉개 버린다**. 동점이 되면 `np.argmax`는 **앞쪽 인덱스**를 고르므로 1이 나온다.
- 실제로는 Virginica(2.1)가 훨씬 강한 신호였는데 그 차이가 사라진 것이다. 이것이 출력층에 연속적인 활성 함수를 쓰는 이유다.

**(3) 같은 예측이어도 "해석"이 다르다**
- **ReLU**: 음수만 잘라낼 뿐 값의 크기에 의미 있는 범위가 없다. 출력층보다는 **은닉층**에 주로 쓴다.
- **Sigmoid**: 각 값이 (0, 1)이지만 **합이 1이 아니다** (1.6893). 클래스마다 따로 "예/아니오 확률"을 주는 셈이라, 한 샘플이 여러 클래스에 동시에 속할 수 있는 **다중 레이블(multi-label)**이나 **이진 분류**에 맞다.
- **Softmax**: 합이 1인 **확률 분포**다. "Virginica일 확률 83%"처럼 읽을 수 있어서 **다중 클래스 분류의 출력층**에 표준으로 쓴다.

**(4) `dim=0` vs `dim=1`**
- 이 코드는 열벡터 방식 (3, 1)이라 `dim=0`, `axis=0`을 쓴다.
- 슬라이드 17~18의 `nn.Module` 코드는 PyTorch 관례대로 (샘플 수, 클래스 수) = (1, 3) 행벡터라 `nn.Softmax(dim=1)`, `argmax(dim=1)`을 쓴다.
- 원칙: **클래스가 놓인 축**을 dim으로 준다. 축을 잘못 주면 softmax가 클래스끼리가 아니라 엉뚱한 방향으로 정규화된다. (이 코드에서 dim=1로 바꾸면 원소 하나짜리 행마다 정규화돼서 전부 1.0이 된다)

### 5) 코드상 사소한 점
- `np.argmax`에 torch 텐서를 넣고 있다. 동작은 하지만(NumPy 배열로 변환됨) NumPy와 PyTorch를 섞은 것이다. PyTorch답게 쓰면 `relu_output.argmax(dim=0)`.
- 이 코드 조각에는 `import numpy as np`가 없다. 앞 슬라이드에서 이미 import했다고 가정한 것.
- `'--- Sigmoide ---'`는 오타 (Sigmoid).

### 6) 한 줄 정리
- 출력층 z = [−1.3, 0.34, 2.1]에 ReLU, Sigmoid, Softmax를 적용해 비교하는 코드다. 셋 다 순서를 보존해서 예측은 Virginica로 같지만, **합이 1인 확률로 해석할 수 있는 것은 Softmax뿐**이라 다중 클래스 분류 출력층에는 Softmax를 쓴다.

---

## Q2. 활성 함수를 출력층(output layer)에서만 바꿔도 되나?

**질문**: 슬라이드 14~15 코드는 `output_layer_z`를 `x`로 받아서 ReLU, Sigmoid, Softmax를 적용한다. 이렇게 출력층의 활성 함수만 바꿔도 되나?

### 1) 결론: 된다. layer마다 활성 함수가 달라도 된다
- 신경망은 **layer마다 다른 활성 함수**를 쓸 수 있고, 실제로도 대부분 그렇게 한다.
- 강의의 다른 코드에서도 이미 그렇게 쓰고 있다.
  - 슬라이드 17 `MLP`: 은닉층은 **Sigmoid**, 출력층은 **Softmax**
  - 슬라이드 43 `our_first_nn`: 은닉층은 **Sigmoid**, 출력층은 활성 함수 없이 logits를 내보낸다 (softmax는 loss 함수 안에서 계산)
- 은닉층과 출력층은 하는 일이 달라서 고르는 기준도 다르다.
  - **은닉층**: 특징을 뽑아내는 곳 → 학습이 잘 되는 **비선형 함수** (ReLU, Sigmoid, tanh 등)
  - **출력층**: 최종 답의 **형태**를 정하는 곳 → 문제 유형에 맞는 함수
    - 다중 클래스 분류: Softmax (합이 1인 확률)
    - 이진 분류, multi-label 분류: Sigmoid (클래스마다 0~1)
    - 회귀(regression): Identity (활성 함수 없음, 값의 범위를 제한하지 않음)

### 2) 이 코드가 출력층만 바꿀 수 있었던 이유
- 은닉층 결과 `hidden_layer_y = [0, 1, 1, 1]`과 출력층 `z = [−1.3, 0.34, 2.1]`은 **이미 계산이 끝난 값**이다.
- 출력층 활성 함수는 마지막에 z를 한 번 변환하는 단계일 뿐이라, 그것만 바꿔도 앞 계산에는 영향이 없다.
- 반대로 **은닉층** 활성 함수를 바꾸면 `hidden_layer_y`가 달라지고, 그것이 출력층의 입력이므로 **output z부터 전부 다시 계산**해야 한다.
  - 예: 은닉층을 Heaviside 대신 Sigmoid로 바꾸면 hidden 출력이 [0, 1, 1, 1]이 아니라 [0.445, 0.707, 0.641, 0.510] 같은 연속값이 되어 output z가 완전히 달라진다.

### 3) 주의: 이 코드는 "비교용 데모"다
- 이 코드는 weight를 사람이 직접 정해 둔 모델에 활성 함수만 갈아 끼워서 **결과가 어떻게 달라지는지 보여주는** 예시다. 학습은 하지 않는다.
- 실제로 **학습(backpropagation)** 을 하려면 은닉층에 Heaviside를 그대로 두면 안 된다.
  - Heaviside는 거의 모든 점에서 기울기(gradient)가 **0**이다 (z = 0에서는 미분 불가능).
  - gradient가 0이면 `loss.backward()`로 계산한 값이 0이라 `optimizer.step()`을 해도 weight가 바뀌지 않는다 → 학습이 안 된다.
  - 그래서 학습하는 모델(슬라이드 17, 43)은 은닉층에 **Sigmoid**처럼 미분 가능한 함수를 쓴다.
- 즉 "출력층만 바꾸는 것"이 문법상 틀린 건 아니지만, 은닉층에 Heaviside를 남겨둔 이 구조는 **학습용으로는 부적절**하다.

### 4) 추가: 출력층 활성 함수를 바꿔도 예측 class는 거의 같다
- ReLU, Sigmoid, Softmax는 모두 **단조 증가**라 z의 크기 순서를 보존한다 → argmax 결과가 같다 (Q1 참고).
- 따라서 출력층 활성 함수를 바꿨을 때 달라지는 것은 주로 **출력값의 해석**(확률인지 아닌지)과 **학습할 때의 loss 계산**이다.
- Heaviside는 0/1로 뭉개서 동점을 만들기 때문에 예측이 달라질 수 있다 (이 예에서는 Versicolor로 틀어짐).

### 5) 한 줄 정리
- 활성 함수는 layer마다 따로 고를 수 있으니 출력층만 바꾸는 것도 가능하다. 출력층은 **문제 유형**(Softmax, Sigmoid, Identity)에 맞추고, 은닉층은 **학습이 되는 비선형 함수**(ReLU, Sigmoid 등)를 쓴다. 이 코드처럼 은닉층에 Heaviside를 두면 출력 형태를 비교할 수는 있어도 학습은 할 수 없다.

---

## Q3. `axis`와 `dim`은 뭐야?

### 1) 같은 개념, 이름만 다르다
- 둘 다 **"배열의 어느 축(차원) 방향으로 연산할지"** 를 정하는 인자다.
  - **NumPy**는 `axis`라고 부른다: `np.argmax(a, axis=0)`, `np.sum(a, axis=1)`
  - **PyTorch**는 `dim`이라고 부른다: `t.argmax(dim=1)`, `F.softmax(t, dim=0)`
- 축 번호는 **shape의 순서**와 같다. shape이 `(2, 3)`이면
  - `axis=0` (`dim=0`): 첫 번째 차원 = **행(row) 방향, 세로 ↓**
  - `axis=1` (`dim=1`): 두 번째 차원 = **열(column) 방향, 가로 →**
  - 음수도 쓸 수 있다: `-1`은 마지막 축 (2차원이면 `-1` = `1`)

### 2) 예시
```python
import numpy as np

a = np.array([
    [1, 5, 2],
    [7, 3, 4]
])  # shape: (2, 3)

np.sum(a, axis=0)     # [8, 8, 6]  ← 세로로 더함 (열마다 하나씩)
np.sum(a, axis=1)     # [8, 14]    ← 가로로 더함 (행마다 하나씩)

np.argmax(a, axis=0)  # [1, 0, 1]  ← 각 열에서 가장 큰 값이 몇 번째 행인지
np.argmax(a, axis=1)  # [1, 0]     ← 각 행에서 가장 큰 값이 몇 번째 열인지
```
- `axis=0`: 위아래 원소끼리 비교/계산한다. (1 vs 7, 5 vs 3, 2 vs 4)
- `axis=1`: 좌우 원소끼리 비교/계산한다. ([1, 5, 2] 안에서, [7, 3, 4] 안에서)
- 외우는 요령: **지정한 축이 사라진다.**
  - shape `(2, 3)`에서 `axis=0`으로 연산하면 0번 축(2)이 사라져서 결과 shape이 `(3,)`
  - `axis=1`로 연산하면 1번 축(3)이 사라져서 결과 shape이 `(2,)`

### 3) 강의 코드에 적용
**NumPy perceptron 코드 (슬라이드 8, 11, 14~15)**
- 출력이 **열벡터** `(3, 1)`: 3개 클래스가 **세로(0번 축)** 로 놓여 있다.
```text
[[-1.3 ],   ← Setosa
 [ 0.34],   ← Versicolor
 [ 2.1 ]]   ← Virginica
```
- 그래서 `np.argmax(output_layer_y, axis=0)`, `F.softmax(x, dim=0)`처럼 **0번 축**을 쓴다.
- 결과 shape은 0번 축이 사라진 `(1,)`이라 `[2]`처럼 대괄호가 붙어서 출력된다.

**PyTorch `nn.Module` 코드 (슬라이드 17~18, 43~51)**
- 입력이 `(샘플 수, feature 수)` 형태의 **행벡터** → 출력은 `(샘플 수, 클래스 수)`
  - 슬라이드 18: `x = torch.tensor([[0.2, 1.4]])` → shape `(1, 2)`, 출력 shape `(1, 3)`
  - mini-batch: 출력 shape `(32, 10)` (32개 샘플 × 10개 클래스)
- 클래스가 **가로(1번 축)** 에 놓여 있으므로 `nn.Softmax(dim=1)`, `logits.argmax(dim=1)`을 쓴다.
  - `argmax(dim=1)` 결과 shape `(32,)`: 샘플마다 예측 클래스 하나씩

### 4) 축을 잘못 주면?
- 원칙: **클래스가 놓인 축**을 지정해야 한다.
- 예: mini-batch 출력 `(32, 10)`에 `softmax(dim=0)`을 하면 클래스끼리가 아니라 **32개 샘플끼리** 확률을 나눠 버린다 → 에러는 안 나지만 의미가 틀린 값이 나온다.
- 예: NumPy 코드 `(3, 1)`에 `softmax(dim=1)`을 하면 원소 1개짜리 행마다 정규화돼서 전부 `1.0`이 된다 (Q1 참고).

### 5) 한 줄 정리
- `axis`(NumPy)와 `dim`(PyTorch)은 같은 것으로, **연산할 축 번호**다. 지정한 축 방향으로 계산하고 그 축은 결과에서 사라진다. 분류 코드에서는 **클래스가 놓인 축**을 넣는다: 열벡터 `(3, 1)`이면 0, `(샘플, 클래스)` 형태면 1.

---

## Q4. PyTorch 구현 코드의 `__init__`과 `self`가 이해가 안 돼

대상 코드 (슬라이드 17):
```python
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden_layer = nn.Linear(2, 4)
        self.output_layer = nn.Linear(4, 3)
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        hidden_z = self.hidden_layer(x)
        hidden_o = self.sigmoid(hidden_z)
        output_z = self.output_layer(hidden_o)
        output_o = self.softmax(output_z)
        return hidden_z, hidden_o, output_z, output_o

model = MLP()
```

### 1) 먼저 class와 object
- **class**는 **설계도**, **object(인스턴스)** 는 그 설계도로 **실제로 만든 물건**이다.
  - `class MLP`: "이런 신경망을 만들 거다"라는 설계도
  - `model = MLP()`: 설계도대로 신경망 **하나를 실제로 만든 것**
- 설계도 하나로 물건을 여러 개 만들 수 있다.
```python
model_a = MLP()
model_b = MLP()   # model_a와 별개의 신경망 (weight도 각자 따로 랜덤 초기화)
```

### 2) `__init__`: 만들어질 때 자동으로 한 번 실행되는 함수
- `MLP()`를 호출하는 순간 Python이 **자동으로 `__init__`을 실행**한다. (이런 함수를 **생성자, constructor**라고 함)
- 역할: 새로 만든 object에 **필요한 부품을 준비해 두는 것**
  - MLP에서는 hidden layer, output layer, sigmoid, softmax를 만들어서 붙여 둔다.
- 앞뒤 밑줄 두 개(`__`)는 "Python이 정한 특별한 이름"이라는 뜻이다. 이름을 `init`이나 `_init_`으로 바꾸면 자동 실행되지 않는다.

### 3) `self`: "지금 만들어지고 있는 바로 그 object 자신"
- `model = MLP()`를 하면 내부적으로 대략 이렇게 동작한다.
```python
model = (빈 MLP object 생성)
MLP.__init__(model)    # self 자리에 model이 들어간다
```
- 즉 `__init__` 안의 `self`는 곧 `model`이다.
  - `self.hidden_layer = nn.Linear(2, 4)` → `model.hidden_layer = nn.Linear(2, 4)`와 같은 의미
- **왜 `self.`를 붙여야 하나?**
  - 그냥 `hidden_layer = nn.Linear(2, 4)`라고 쓰면 `__init__` 안에서만 쓰는 **임시 변수**라서 함수가 끝나면 사라진다.
  - `self.hidden_layer`로 쓰면 **object에 저장**되어서 나중에 `forward`에서도 꺼내 쓸 수 있다.
  - 비유: 지역 변수는 메모지에 잠깐 적은 것, `self.변수`는 그 물건에 **라벨을 붙여서 달아둔 것**

### 4) `forward`에서의 `self`
- `forward(self, x)`의 `self`도 똑같이 `model` 자신이다.
- 그래서 `self.hidden_layer(x)`는 `__init__`에서 **달아 둔 그 layer**를 꺼내서 x를 통과시키는 것이다.
- 흐름:
```text
__init__ : self.hidden_layer, self.output_layer, ... 를 만들어 저장   (모델 만들 때 1번)
forward  : 저장해 둔 self.hidden_layer, ... 를 꺼내서 x를 통과시킴   (데이터 넣을 때마다)
```
- 메서드(class 안의 함수)를 정의할 때는 첫 번째 인자로 `self`를 **반드시** 적는다. 하지만 호출할 때는 Python이 자동으로 채워 주므로 적지 않는다.
  - 정의: `def forward(self, x)` → 호출: `model(x)` (x만 넘김)

### 5) `super().__init__()`은 왜 있나?
- `class MLP(nn.Module)`: MLP는 PyTorch의 `nn.Module`을 **상속**한다. 즉 `nn.Module`의 기능을 물려받는다.
- `super().__init__()`: **부모 클래스(`nn.Module`)의 `__init__`을 먼저 실행**하라는 뜻이다.
  - `nn.Module`은 이때 "이 모델에 어떤 layer와 parameter가 들어있는지 기록할 장부"를 준비한다.
  - 이게 있어야 `self.hidden_layer = ...`로 붙인 layer의 weight를 PyTorch가 자동으로 찾아서 `model.parameters()`, `optimizer`, `.to(device)` 등에 쓸 수 있다.
  - 빼먹으면 `self.hidden_layer = ...` 줄에서 에러가 난다. 그래서 항상 `__init__`의 **첫 줄**에 쓴다.

### 6) `model(x)`를 하면 왜 `forward`가 실행되나?
- `nn.Module`이 "object를 함수처럼 호출하면 `forward`를 실행"하도록 만들어져 있기 때문이다.
- 그래서 `model(x)`라고 쓰면 내부적으로 `model.forward(x)`가 실행된다. (`forward`를 직접 부르지 말고 `model(x)`로 부르는 것이 관례)

### 7) 전체 실행 순서 정리
```text
model = MLP()
  └─ __init__(self=model) 자동 실행
       ├─ super().__init__()       : nn.Module 기본 준비
       ├─ self.hidden_layer = ...  : 2→4 layer 생성 (weight 랜덤 초기화) 후 model에 저장
       ├─ self.output_layer = ...  : 4→3 layer 생성 후 저장
       └─ self.sigmoid, self.softmax 저장

model(x)
  └─ forward(self=model, x) 실행
       ├─ self.hidden_layer(x) → self.sigmoid(...)
       └─ self.output_layer(...) → self.softmax(...) → return
```

### 8) 한 줄 정리
- `__init__`은 모델을 **만들 때 한 번** 자동 실행되어 layer들을 준비하는 함수이고, `self`는 **그 모델 object 자신**이다. `self.이름 = ...`으로 붙여 둔 layer를 `forward`에서 `self.이름`으로 꺼내 쓴다. `super().__init__()`은 PyTorch가 그 layer들을 관리할 수 있게 부모 클래스를 먼저 준비시키는 줄이다.

---

## Q5. Shallow neural network 예제(슬라이드 30~37)의 o₁,₀은 뭐고, 1과 0은 무슨 뜻이며, 어떻게 계산하나?

### 1) o는 활성 함수 자체가 아니라 "활성 함수를 통과한 결과값"
- **z**: neuron에 들어온 입력의 **가중합** (활성 함수 적용 **전**)
- **o**: z에 **활성 함수를 적용한 출력값** (output, 활성 함수 적용 **후**)
- 즉 o₁,₀ = sigmoid(z₁,₀). 활성 함수는 sigmoid이고, o₁,₀은 그 결과로 나온 **숫자**다.

### 2) 아래 첨자의 의미: o_{l, j} = "l번째 layer의 j번째 neuron 출력"
- **첫 번째 숫자 l**: layer 번호 (0부터 셈)
  - l = 0: input layer
  - l = 1: hidden layer
  - l = 2: output layer
- **두 번째 숫자 j**: 그 layer 안에서 몇 번째 neuron인지 (0부터 셈)
- 따라서
  - **o₁,₀** = hidden layer(1)의 **0번째 neuron** 출력
  - **o₁,₁** = hidden layer(1)의 **1번째 neuron** 출력
  - **o₂,₀** = output layer(2)의 0번째 neuron 출력 = 최종 예측값 ŷ
  - **o₀,ᵢ** = input layer의 출력 = 입력값 그 자체 (o₀,₀ = x₀, o₀,₁ = x₁)

### 3) weight 첨자: w_{l, i, j} = "l번째 layer로 들어가는, (l−1)층 i번 neuron → l층 j번 neuron 연결"
- **l**: 이 weight가 **도착하는** layer
- **i**: **출발** neuron 번호 (이전 layer)
- **j**: **도착** neuron 번호 (현재 layer)
- 예: **w₁,₁,₀** = input의 1번(x₁) → hidden의 0번 neuron으로 가는 weight = 0.2
- 예: **w₂,₁,₀** = hidden의 1번(o₁,₁) → output의 0번 neuron으로 가는 weight = 0.9

### 4) 네트워크 구조 (2 - 2 - 1, bias 없음)
```text
  layer 0 (input)        layer 1 (hidden)          layer 2 (output)

  x₀ = 0.35 ──w₁,₀,₀=0.2──▶ [z₁,₀ → o₁,₀] ──w₂,₀,₀=0.3──┐
            ╲            ╱                             ▼
          w₁,₀,₁=0.3  w₁,₁,₀=0.2                  [z₂,₀ → o₂,₀] = ŷ
            ╱            ╲                             ▲
  x₁ = 0.7  ──w₁,₁,₁=0.3──▶ [z₁,₁ → o₁,₁] ──w₂,₁,₀=0.9──┘
```
- 각 neuron으로 **들어오는 화살표들의 (입력 × weight)를 모두 더한 것**이 z다.

### 5) 계산 과정 (활성 함수: sigmoid(z) = 1 / (1 + e⁻ᶻ))
**hidden neuron 0 (o₁,₀)**: x₀, x₁에서 neuron 0으로 오는 weight는 w₁,₀,₀, w₁,₁,₀
```text
z₁,₀ = x₀ × w₁,₀,₀ + x₁ × w₁,₁,₀
     = 0.35 × 0.2 + 0.7 × 0.2
     = 0.07 + 0.14 = 0.21
o₁,₀ = sigmoid(0.21) = 1 / (1 + e^(−0.21)) ≈ 0.5522
```

**hidden neuron 1 (o₁,₁)**: neuron 1로 오는 weight는 w₁,₀,₁, w₁,₁,₁
```text
z₁,₁ = x₀ × w₁,₀,₁ + x₁ × w₁,₁,₁
     = 0.35 × 0.3 + 0.7 × 0.3
     = 0.105 + 0.21 = 0.315
o₁,₁ = sigmoid(0.315) ≈ 0.5781
```

**output neuron (o₂,₀)**: hidden layer의 출력 o₁,₀, o₁,₁이 **입력**이 된다
```text
z₂,₀ = o₁,₀ × w₂,₀,₀ + o₁,₁ × w₂,₁,₀
     = 0.5522 × 0.3 + 0.5781 × 0.9
     = 0.1657 + 0.5203 ≈ 0.686
o₂,₀ = sigmoid(0.686) ≈ 0.665  (= ŷ, 최종 예측값)
```

- 일반식: **z_{l,j} = Σᵢ o_{l−1,i} × w_{l,i,j}** (+ b_{l,j}, 이 예제는 bias 없음), **o_{l,j} = sigmoid(z_{l,j})**
- 참고: sigmoid(0.21)을 정확히 계산하면 0.55231…이라 반올림하면 0.5523인데 슬라이드는 0.5522로 적혀 있다. 이후 계산에 주는 영향은 무시할 수준이다.

### 6) 뒤 슬라이드에서 o가 다시 쓰이는 곳
- **loss** (슬라이드 32): L = (ŷ − y)² = (o₂,₀ − 0.5)² = (0.665 − 0.5)²
- **δ 계산** (슬라이드 32~34): sigmoid의 미분이 o(1 − o)라서 `o₂,₀(1 − o₂,₀)`, `o₁,₀(1 − o₁,₀)` 형태가 나온다.
- **weight 갱신** (슬라이드 35~37): Δw_{l,i,j} = −η · δ_{l,j} · **o_{l−1,i}**
  - weight의 **출발 neuron의 출력** o를 곱한다.
  - 예: Δw₂,₀,₀ = −1.0 × δ₂,₀ × **o₁,₀** = −1.0 × 0.0735 × 0.5522 ≈ −0.0406
  - 예: Δw₁,₁,₀ = −1.0 × δ₁,₀ × **o₀,₁**(= x₁ = 0.7) ≈ −0.0039

### 7) 한 줄 정리
- o_{l,j}는 **l번째 layer의 j번째 neuron이 활성 함수를 통과해서 내보낸 출력값**이다. o₁,₀은 hidden layer의 0번 neuron 출력이고, 그 neuron으로 들어오는 입력과 weight를 곱해 더한 z₁,₀ = 0.21에 sigmoid를 적용해서 0.5522를 얻는다.

---

## Q6. w는 layer 번호에 +1을 쓰는 것 같은데, o는 0을 그대로 쓰나?

### 1) +1을 하는 게 아니라, 둘 다 "같은 layer 번호 체계"를 쓴다
- layer 번호는 하나로 정해져 있다: **input = 0, hidden = 1, output = 2**
- **o_{l,j}**: neuron이 **속한** layer 번호를 쓴다.
  - input의 값은 o₀,₀, o₀,₁ (= x₀, x₁)
  - hidden neuron의 출력은 o₁,₀, o₁,₁
- **w_{l,i,j}**: weight가 **도착하는** layer 번호를 쓴다.
  - input → hidden 사이의 weight는 hidden(1)으로 들어가므로 **w₁,·,·**
  - hidden → output 사이의 weight는 output(2)으로 들어가므로 **w₂,·,·**
- 그래서 출발 neuron 기준으로 보면 +1처럼 보일 뿐이다. 실제로는 **"그 weight를 받는 layer"의 번호**를 붙인 것이다.
  - weight와 bias는 받는 쪽 layer의 parameter로 본다. (`nn.Linear(2, 4)`가 hidden layer의 W와 b를 갖는 것과 같은 관점)
  - z_{l,j}와 b_{l,j}도 같은 l을 쓴다. 한 neuron의 계산에 필요한 w, b, z, o의 layer 번호가 모두 **l로 통일**된다.

```text
z₁,₀ = o₀,₀ × w₁,₀,₀ + o₀,₁ × w₁,₁,₀ (+ b₁,₀)
o₁,₀ = sigmoid(z₁,₀)
        ↑      ↑            ↑              ↑
     layer 1  layer 1    layer 1        layer 1   ← 계산되는 neuron의 layer
       o₀,₀, o₀,₁        ← 입력은 이전 layer(0)의 출력
```
- 일반식: **z_{l,j} = Σᵢ o_{l−1,i} × w_{l,i,j} + b_{l,j}**
  - w의 l과 결과 o의 l은 **같고**, 곱해지는 입력 o만 **l−1**이다.

### 2) 뒤의 두 숫자(i, j)는 neuron 번호이고 +1 없이 0부터 센다
- o₁,₀의 **0**은 layer가 아니라 **neuron 번호**다. hidden layer의 **0번째** neuron이라는 뜻
- w_{l,i,j}의 i, j도 똑같이 0부터 센 neuron 번호다.
  - i: 출발 neuron 번호 (layer l−1 안에서)
  - j: 도착 neuron 번호 (layer l 안에서)
- 따라서 w_{l,i,j}는 **o_{l−1,i} → o_{l,j}** 를 잇는 선이다.
  - w₁,₁,₀: o₀,₁(x₁) → o₁,₀
  - w₂,₁,₀: o₁,₁ → o₂,₀

### 3) 헷갈리지 않는 확인법
- w_{l,i,j}의 **(l, j)** 를 떼어 보면 **도착 neuron o_{l,j}** 와 같다.
- w_{l,i,j}의 **(l−1, i)** 가 **출발 neuron o_{l−1,i}** 다.
- 예: w₁,₁,₀ → 도착 o₁,₀, 출발 o₀,₁ ✔
- weight 갱신 식 Δw_{l,i,j} = −η · δ_{l,j} · o_{l−1,i} 도 같은 규칙이다. δ는 **도착 neuron**(l, j)의 error, o는 **출발 neuron**(l−1, i)의 출력이다.

### 4) 한 줄 정리
- layer 번호는 w, z, b, o 모두 같은 체계(input 0, hidden 1, output 2)를 쓴다. o는 자기가 속한 layer, w는 **도착하는** layer의 번호를 붙이므로 출발 쪽에서 보면 +1처럼 보이는 것이다. o₁,₀의 0은 layer가 아니라 **0번째 neuron**이라는 뜻이다.

---

## Q7. 출력층 δ₂,₀ = 2(o₂,₀ − y) × o₂,₀(1 − o₂,₀) = 0.0735 는 어떤 원리로 구하나?

### 1) δ의 정체: "z가 조금 변하면 loss가 얼마나 변하나"
- **δ_{l,j} = ∂L / ∂z_{l,j}**: neuron (l, j)의 **z에 대한 loss의 기울기(gradient)** 다.
- 이 neuron의 z를 조금 키웠을 때 loss가 얼마나, 어느 방향으로 변하는지를 나타낸다.
  - δ > 0: z를 키우면 loss가 커진다 → z를 **줄여야** 한다
  - δ < 0: z를 키우면 loss가 줄어든다 → z를 **키워야** 한다
- 슬라이드에서는 이를 **error**라고 부른다.

### 2) 핵심 원리: Chain rule (연쇄 법칙)
- loss가 z에 바로 연결되어 있지 않고, 중간에 o를 거친다.
```text
z₂,₀ ──sigmoid──▶ o₂,₀ (= ŷ) ──loss──▶ L = (o₂,₀ − y)²
```
- 이렇게 함수가 이어져 있으면 미분은 **각 단계의 미분을 곱한 것**이다.
```text
δ₂,₀ = ∂L/∂z₂,₀ = (∂L/∂o₂,₀) × (∂o₂,₀/∂z₂,₀)
                    ───────────   ─────────────
                     ① loss 미분   ② sigmoid 미분
```

### 3) ① loss의 미분: 2(o₂,₀ − y)
- L = (o − y)² 를 o로 미분하면 (y는 정답이라 상수)
```text
∂L/∂o = 2(o − y)
```
- 의미: 예측이 정답보다 **얼마나, 어느 쪽으로** 벗어났는지
  - o₂,₀ = 0.665, y = 0.5 → 2 × (0.665 − 0.5) = 2 × 0.165 = 0.33
  - 양수 → 예측이 정답보다 크다 → 출력을 줄여야 한다

### 4) ② sigmoid의 미분: o(1 − o)
- σ(z) = 1 / (1 + e⁻ᶻ) 를 z로 미분하면
```text
dσ/dz = e⁻ᶻ / (1 + e⁻ᶻ)²
      = [1 / (1 + e⁻ᶻ)] × [e⁻ᶻ / (1 + e⁻ᶻ)]
      = σ(z) × (1 − σ(z))          ← e⁻ᶻ/(1+e⁻ᶻ) = 1 − 1/(1+e⁻ᶻ)
      = o × (1 − o)
```
- sigmoid의 미분은 **출력 o만으로** 계산할 수 있다 → forward에서 구해 둔 o를 그대로 재사용
  - o₂,₀ = 0.665 → 0.665 × (1 − 0.665) = 0.665 × 0.335 ≈ 0.2228
- 의미: z가 변할 때 sigmoid 출력이 얼마나 민감하게 변하는지
  - 최댓값은 o = 0.5일 때 0.25
  - o가 0이나 1에 가까우면 거의 0 → gradient가 작아져 학습이 느려진다 (**vanishing gradient**의 원인)

### 5) 곱해서 δ₂,₀
```text
δ₂,₀ = 2(o₂,₀ − y)     ×  o₂,₀(1 − o₂,₀)
     = 2 × 0.165       ×  0.665 × 0.335
     = 0.33            ×  0.2228
     ≈ 0.0735
```

### 6) 이 δ로 weight를 갱신하는 이유
- 결국 필요한 것은 **∂L/∂w** (weight를 바꾸면 loss가 어떻게 변하나)다. chain rule을 한 번 더 쓴다.
```text
z₂,₀ = o₁,₀ × w₂,₀,₀ + o₁,₁ × w₂,₁,₀

∂L/∂w₂,₀,₀ = (∂L/∂z₂,₀) × (∂z₂,₀/∂w₂,₀,₀) = δ₂,₀ × o₁,₀
```
- z를 w₂,₀,₀로 미분하면 곱해져 있던 입력 **o₁,₀**만 남는다.
- gradient descent는 gradient의 **반대 방향**으로 이동하므로
```text
Δw₂,₀,₀ = −η × δ₂,₀ × o₁,₀ = −1.0 × 0.0735 × 0.5522 ≈ −0.0406
```
- 이것이 슬라이드의 일반식 **Δw_{l,i,j} = −η · δ_{l,j} · o_{l−1,i}** 이다.
- 결과: w₂,₀,₀가 0.3 → 0.2594로 줄어든다 → z₂,₀가 줄고 → ŷ가 줄어 정답 0.5에 가까워진다. (δ > 0이면 출력을 줄여야 한다는 것과 일치)

### 7) hidden layer의 δ도 같은 원리 (슬라이드 33~34)
- hidden neuron의 z는 **output을 거쳐서** loss에 영향을 준다. chain rule을 한 단계 더 이어 붙인다.
```text
z₁,₀ ─sigmoid─▶ o₁,₀ ─(×w₂,₀,₀)─▶ z₂,₀ ─▶ ... ─▶ L

δ₁,₀ = ∂L/∂z₁,₀
     = (∂L/∂z₂,₀) × (∂z₂,₀/∂o₁,₀) × (∂o₁,₀/∂z₁,₀)
     =    δ₂,₀    ×     w₂,₀,₀     ×  o₁,₀(1 − o₁,₀)
     = 0.0735 × 0.3 × 0.5522 × 0.4478 ≈ 0.0055
```
- **뒤 layer의 δ를 weight를 따라 앞으로 전달**하는 구조라서 **backpropagation(역전파)** 이라고 부른다.
  - 출력층 δ: (loss 미분) × (활성 함수 미분)
  - hidden δ: (뒤 layer δ × 연결 weight) × (활성 함수 미분)

### 8) 한 줄 정리
- δ₂,₀는 **z₂,₀에 대한 loss의 기울기**다. chain rule로 "loss를 o로 미분한 값 2(o − y)"와 "sigmoid를 z로 미분한 값 o(1 − o)"을 곱해서 구한다. 여기에 입력 o_{l−1,i}를 곱하면 weight의 gradient가 되고, 그 반대 방향(−η)으로 weight를 갱신한다.

---

## Q8. `self.flatten = nn.Flatten()`은 뭐야? (슬라이드 43)

### 1) 역할: 여러 차원의 데이터를 1줄로 쭉 펼친다
- Fashion-MNIST 이미지 1장은 **28 × 28** 픽셀의 2차원 격자다.
- `nn.Flatten()`은 이것을 **784(= 28 × 28)개 숫자가 한 줄로 늘어선 벡터**로 바꾼다.
```text
[[a, b, c],                         
 [d, e, f],     ──Flatten──▶   [a, b, c, d, e, f, g, h, i]
 [g, h, i]]                    
  (3 × 3)                           (9,)
```
- 행을 순서대로 이어 붙일 뿐, 값 자체는 하나도 바뀌지 않는다. (weight가 없는 layer)

### 2) 왜 필요한가: `nn.Linear`는 1차원 입력만 받는다
- 다음 layer인 `nn.Linear(784, 128)`은 "**샘플마다 784개짜리 feature 벡터**"를 입력으로 기대한다.
  - z = xWᵀ + b 계산을 하려면 x가 벡터여야 한다.
- 이미지를 28 × 28 그대로 넣으면 shape이 맞지 않아 에러가 난다.
- 그래서 `forward`에서 **가장 먼저** flatten을 한다.
```python
def forward(self, x):
    x = self.flatten(x)                      # (N, 1, 28, 28) → (N, 784)
    x = self.sigmoid(self.hidden_layer(x))   # (N, 784) → (N, 128)
    x = self.output_layer(x)                 # (N, 128) → (N, 10)
    return x
```
- Iris 예제(입력 2개)는 처음부터 1차원 feature라서 flatten이 필요 없었다.
- 784라는 숫자가 `nn.Linear(784, 128)`의 **입력 neuron 수**가 된다. (슬라이드 40의 "# of input neurons?" 질문의 답)

### 3) shape 변화: batch 차원은 남긴다
- 실제로 들어오는 이미지 tensor는 `(batch, channel, height, width)` 형태다.
  - 흑백이라 channel = 1
  - 샘플 1개씩 학습(슬라이드 44): `unsqueeze(0)` 후 `(1, 1, 28, 28)`
  - mini-batch(슬라이드 50): `(32, 1, 28, 28)`
- `nn.Flatten()`은 기본값이 `start_dim=1`이라서 **0번 축(batch)은 그대로 두고** 나머지만 펼친다.
```text
(32, 1, 28, 28)  ──Flatten──▶  (32, 784)      # 1 × 28 × 28 = 784
```
- 만약 batch까지 펼치면 32장 이미지가 하나의 긴 벡터(25,088개)로 섞여 버린다. 그래서 batch 차원을 남기는 것이 중요하다.

### 4) 직접 해보면
```python
import torch
import torch.nn as nn

flatten = nn.Flatten()
images = torch.rand(32, 1, 28, 28)   # 가짜 이미지 32장

print(images.shape)            # torch.Size([32, 1, 28, 28])
print(flatten(images).shape)   # torch.Size([32, 784])
```
- 같은 동작을 `x.view(x.size(0), -1)` 또는 `torch.flatten(x, start_dim=1)`로도 할 수 있다.

### 5) 단점: 공간 정보가 사라진다
- 펼치고 나면 "어떤 픽셀이 어떤 픽셀의 **위/아래/옆**에 있었는지" 하는 2차원 위치 관계를 모델이 직접 알 수 없다.
  - 예: 원래 바로 위아래로 붙어 있던 두 픽셀이 펼친 뒤에는 28칸 떨어진다.
- 그래도 단순한 이미지(MNIST, Fashion-MNIST)는 이 방식으로도 꽤 잘 분류된다.
- 공간 구조를 살려서 처리하는 모델이 **CNN (Convolutional Neural Network)** 이다.

### 6) 한 줄 정리
- `nn.Flatten()`은 `(batch, 1, 28, 28)` 이미지를 `(batch, 784)`로 **한 줄로 펼치는 layer**다. `nn.Linear`가 1차원 feature 벡터만 받기 때문에 맨 앞에 둔다. batch 차원은 남기고, 값은 바꾸지 않으며, 학습할 weight도 없다.

---

## Q9. Batch(슬라이드 46)부터 Python 코드(슬라이드 49~51)까지 자세히 설명

전체 흐름:
```text
46 Batch       : 데이터를 1개씩이 아니라 여러 개를 묶어서 한 번에 계산
47 Mini-batch  : 전부 묶기(full-batch)와 1개씩의 중간 → 작은 묶음(16, 32 ...)
48 Epoch       : 전체 training data를 한 바퀴 다 도는 것
49 DataLoader  : 데이터를 batch 단위로 잘라 주는 도구
50 학습 코드    : batch 단위로 forward → loss → backward → update
51 테스트 코드  : batch 단위로 예측해서 accuracy 계산
```

---

### 1) 왜 batch가 필요한가 — 1개씩 학습의 문제 (슬라이드 44 복습)
- 슬라이드 44 코드는 이미지를 **1장씩** 모델에 넣고, **1장마다** weight를 갱신했다.
  - Fashion-MNIST training data 60,000장 → 1 epoch에 **60,000번** forward + backward + update
- 문제점
  - **느리다**: GPU는 많은 계산을 동시에 하는 데 강한데, 1장씩 넣으면 그 능력을 거의 못 쓴다.
  - **불안정하다**: 이미지 1장의 loss만 보고 weight를 바꾸니, 이상한 샘플 하나에도 weight가 크게 흔들린다.
- 해결: 여러 장을 **묶어서(batch)** 한 번에 계산하고, 묶음 단위로 weight를 갱신한다.

---

### 2) Batch의 수식 — 행렬 곱 하나로 여러 샘플을 동시에 계산 (슬라이드 46)

**(a) 샘플 1개일 때** (행벡터 방식)
```text
    x          W            b              결과
 (1 × n)  ×  (n × m)  +  (1 × m)   =   (1 × m)

[x₁ ⋯ xₙ] × [w₁,₁ ⋯ w₁,ₘ]  + [b₁ ⋯ bₘ]
             [ ⋮  ⋱   ⋮ ]
             [wₙ,₁ ⋯ wₙ,ₘ]
```
- n: 입력 feature 수 (Fashion-MNIST는 784)
- m: 이 layer의 neuron 수 (hidden layer는 128)
- 주의: week7 앞부분(Wx + b, 열벡터)과 **곱하는 순서가 반대**다. PyTorch는 샘플을 **행(row)** 으로 놓는 이 방식(xW + b)을 쓴다.

**(b) 샘플 s개를 묶었을 때**
```text
    X          W            B              결과
 (s × n)  ×  (n × m)  +  (s × m)   =   (s × m)

[x₁,₁ ⋯ x₁,ₙ]   ← 샘플 1
[ ⋮   ⋱   ⋮ ]
[xₛ,₁ ⋯ xₛ,ₙ]   ← 샘플 s
```
- 샘플들을 **행으로 쌓아서** 행렬 X를 만든다. → 행렬 곱 **한 번**으로 s개 샘플 결과가 동시에 나온다.
- 결과의 **i번째 행 = i번째 샘플의 출력**이다. 샘플끼리 섞이지 않는다.
- **W는 그대로**다. 모든 샘플이 **같은 weight**를 공유한다. (batch를 키워도 parameter 수는 안 늘어남)
- **b의 모든 행이 같다** (슬라이드의 "Same"). 같은 bias 벡터를 s번 복사해서 더하는 것이다.
  - 실제 코드에서는 복사하지 않고 PyTorch가 자동으로 각 행에 더해 준다 (**broadcasting**).

**(c) 작은 숫자 예시** (s = 3 샘플, n = 2 feature, m = 2 neuron)
```text
     X (3×2)        W (2×2)        b (1×2)
   [1  2]         [1  0]         [10  20]
   [3  4]    ×    [0  1]    +
   [5  6]

 = [1  2]   [10 20]   [11  22]   ← 샘플 1
   [3  4] + [10 20] = [13  24]   ← 샘플 2
   [5  6]   [10 20]   [15  26]   ← 샘플 3
```
- (W를 단위행렬로 잡아서 X가 그대로 나왔다.) b가 **모든 행에 똑같이** 더해지는 것을 볼 수 있다.

---

### 3) Full-batch vs Mini-batch (슬라이드 47)
- **Full-batch**: training data **전체**를 한 batch로 (s = 60,000)
  - 장점: 계산이 빠르다 (행렬 곱 한 번), gradient가 안정적이다
  - 단점: **메모리가 엄청 많이 든다** (60,000 × 784 입력 + 중간 결과 전부를 한 번에 올려야 함). 1 epoch에 update가 1번뿐이라 학습 진행도 느리다.
- **Mini-batch**: 작은 묶음으로 (s = 16, 32, 64 ...)
  - 메모리를 감당할 수 있으면서, GPU 병렬 계산의 이점도 얻는다.
  - 1 epoch에 update를 여러 번 한다.
  - **실제로는 거의 항상 mini-batch를 쓴다.**
- 세 방식 비교 (training data 60,000개 기준)
```text
방식          batch 크기    1 epoch당 update 횟수
1개씩         1             60,000
mini-batch    32            1,875  (= 60,000 / 32)
full-batch    60,000        1
```

---

### 4) Epoch, Batch, Iteration (슬라이드 48)
- **Epoch**: training data **전체를 한 번** 다 사용하는 것
- **Batch size**: 한 번에 묶는 샘플 수
- **Iteration (step)**: batch 하나를 처리하고 weight를 **한 번 갱신**하는 것
- 관계: **1 epoch의 iteration 수 = training data 수 / batch size**
  - 슬라이드 예: 1,000개, batch 100 → 1 epoch = 10 iteration
  - Fashion-MNIST: 60,000개, batch 32 → 1 epoch = 1,875 iteration
  - `epochs = 5`라면 총 1,875 × 5 = 9,375번 weight 갱신
- epoch마다 데이터 순서를 **섞어서** batch를 새로 나눈다 → 매번 다른 조합으로 학습해서 특정 순서에 치우치지 않는다.

---

### 5) 코드 ①: DataLoader로 batch 만들기 (슬라이드 49)
```python
# batching
batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
```
- `DataLoader` (`from torch.utils.data import DataLoader`): dataset을 **batch 단위로 잘라서 꺼내 주는 도구**
- `train_dataset`: 이미지 6만 장이 들어있는 dataset. `train_dataset[i]`로 꺼내면 `(image, label)` 한 쌍이 나온다.
  - image shape: `(1, 28, 28)`, label: 0~9 정수
- `batch_size=32`: 32쌍씩 묶어서 준다.
  - 묶인 결과: images `(32, 1, 28, 28)`, labels `(32,)` — 맨 앞에 batch 축이 생긴다.
- `shuffle=True` (train): **epoch마다** 순서를 섞는다. 슬라이드 44의 `torch.randperm`이 하던 일을 대신한다.
- `shuffle=False` (test): 평가는 순서가 결과에 영향이 없으므로 섞지 않는다.
- 나누어떨어지지 않으면 **마지막 batch는 작다**.
  - test 10,000장 / 32 = 312 batch + 남은 16장 → 마지막 batch는 16장

DataLoader는 이렇게 쓴다:
```python
for images, labels in train_loader:   # 한 바퀴 돌면 = 1 epoch
    ...                               # 매 반복마다 images (32,1,28,28), labels (32,)
```

---

### 6) 코드 ②: 학습 루프 (슬라이드 50) — 한 줄씩
```python
for epoch in range(epochs):                          # (A)
    model.train()                                    # (B)
    total_loss = 0                                   # (C)
    correct = 0
    total = 0

    for images, labels in train_loader:              # (D)
        images = images.to(device)                   # (E)
        labels = labels.to(device)

        # Forward propagation
        logits = model(images)                       # (F)
        loss = criterion(logits, labels)             # (G)

        # Backpropagation
        optimizer.zero_grad()                        # (H)
        loss.backward()                              # (I)

        # Update weights and biases
        optimizer.step()                             # (J)

        total_loss += loss.item() * labels.size(0)   # (K)
        predictions = logits.argmax(dim=1)           # (L)
        correct += (predictions == labels).sum().item()  # (M)
        total += labels.size(0)                      # (N)
```

- **(A)** `epochs`번 반복. 한 번 = 전체 데이터 한 바퀴.
- **(B)** `model.train()`: 학습 모드로 전환. (나중에 배울 Dropout 같은 layer는 학습/평가 때 동작이 다르다. 지금 모델엔 차이가 없지만 습관적으로 쓴다.)
- **(C)** 이번 epoch의 통계를 0으로 초기화 (epoch마다 새로 셈)
- **(D)** `train_loader`에서 batch를 하나씩 꺼낸다. 1 epoch에 1,875번 반복.
- **(E)** `.to(device)`: 데이터를 모델과 **같은 장치**(GPU 또는 CPU)로 옮긴다. 모델과 데이터가 다른 장치에 있으면 에러가 난다.
- **(F)** **Forward**: 32장을 한 번에 모델에 넣는다.
  - 내부: Flatten `(32, 784)` → hidden `(32, 128)` → output `(32, 10)`
  - `logits` shape `(32, 10)`: **각 행 = 이미지 1장**, 각 열 = 클래스 10개에 대한 점수 (softmax 전 값)
- **(G)** **Loss 계산**: `criterion`은 보통 `nn.CrossEntropyLoss()`
  - 내부에서 softmax를 계산하고, 32장 각각의 loss를 구한 뒤 **평균**을 낸다 → `loss`는 숫자 1개
- **(H)** `optimizer.zero_grad()`: 이전 batch에서 계산된 gradient를 **0으로 지운다**.
  - PyTorch는 gradient를 **덮어쓰지 않고 누적(+=)** 하기 때문에, 안 지우면 이전 batch의 gradient가 섞인다.
- **(I)** `loss.backward()`: **Backpropagation**. 모든 weight, bias에 대해 ∂loss/∂w를 계산한다. (Q7의 δ 계산을 PyTorch가 자동으로 해 줌)
  - loss가 32장의 **평균**이므로 gradient도 32장 gradient의 **평균**이 된다 → 한 장짜리보다 안정적
- **(J)** `optimizer.step()`: 계산된 gradient로 weight 갱신. (w ← w − η × gradient)
  - **batch 하나에 갱신 1번**. 32장을 봤지만 갱신은 한 번이다.
- **(K)** 통계용 loss 누적
  - `loss`는 batch **평균**이라, 그대로 더하면 batch 크기가 다른 마지막 batch가 왜곡된다.
  - `× labels.size(0)`(= 이번 batch 샘플 수)으로 **합계**로 되돌려서 누적한다.
  - epoch이 끝나면 `total_loss / total` = 샘플 1개당 평균 loss
- **(L)** `logits.argmax(dim=1)`: 각 행(이미지)에서 점수가 가장 큰 열(클래스) 번호 → `(32,)`
  - `dim=1`인 이유: 클래스가 **1번 축(가로)** 에 있기 때문 (Q3 참고)
- **(M)** 맞힌 개수 세기
  - `predictions == labels` → `[True, False, True, ...]` (32개)
  - `.sum()` → True 개수, `.item()` → Python 숫자로 변환
- **(N)** 이번 batch의 샘플 수를 누적 (마지막 batch는 32가 아닐 수 있어서 `32`를 직접 쓰지 않음)

epoch이 끝나면 보통 이렇게 출력한다 (슬라이드에는 생략됨):
```python
print(f"Epoch {epoch+1}: loss = {total_loss/total:.4f}, train acc = {correct/total:.4f}")
```

---

### 7) 1개씩 버전(슬라이드 44)과 비교
```text
항목              1개씩 (슬라이드 44)                 mini-batch (슬라이드 50)
데이터 꺼내기      indices = torch.randperm(...)        for images, labels in train_loader
                  train_dataset[index.item()]
batch 축 추가     image.unsqueeze(0)  → (1,1,28,28)    DataLoader가 자동 → (32,1,28,28)
label 처리        torch.tensor([label])                이미 tensor (32,)
loss 누적         loss.item()                          loss.item() * labels.size(0)
개수 누적         total += 1                           total += labels.size(0)
갱신 횟수/epoch   60,000                               1,875
```
- 학습 핵심 4단계(**forward → zero_grad → backward → step**)는 **완전히 똑같다**. 한 번에 넣는 데이터 양만 다르다.

---

### 8) 코드 ③: 테스트 루프 (슬라이드 51)
```python
model.eval()                                          # (A)
correct = 0
total = 0

with torch.no_grad():                                 # (B)
    for images, labels in test_loader:                # (C)
        images = images.to(device)
        labels = labels.to(device)

        logits = model(images)                        # (D)
        probabilities = model.softmax(logits)         # (E)
        predictions = probabilities.argmax(dim=1)     # (F)

        correct += (predictions == labels).sum().item()
        total += labels.size(0)

# accuracy = correct / total
```
- **(A)** `model.eval()`: 평가 모드로 전환
- **(B)** `torch.no_grad()`: gradient 계산을 끈다. 테스트는 weight를 바꾸지 않으므로 필요 없고, 메모리와 시간을 아낀다.
- **(C)** test 데이터 10,000장을 32장씩 (313 batch, 마지막은 16장)
- **(D)** forward만 한다. **loss, zero_grad, backward, step이 없다** → weight가 변하지 않는다.
- **(E)** `model.softmax`: `__init__`에서 만들어 둔 `nn.Softmax(dim=1)`로 logits를 확률로 변환
  - 각 행의 10개 값이 0~1이고 합이 1
- **(F)** 확률이 가장 큰 클래스 = 예측
  - softmax는 순서를 바꾸지 않으므로 `logits.argmax(dim=1)`을 해도 결과는 같다. 확률로 보고 싶을 때 softmax를 쓴다.
- 마지막에 `correct / total`이 **test accuracy**

---

### 9) 전체 흐름 그림
```text
train_dataset (60,000장)
     │  DataLoader(batch_size=32, shuffle=True)
     ▼
epoch 1
  ├─ batch 1    (32장) → forward → loss → zero_grad → backward → step
  ├─ batch 2    (32장) → forward → loss → zero_grad → backward → step
  ├─ ...
  └─ batch 1875 (32장) → forward → loss → zero_grad → backward → step
epoch 2 (다시 섞어서 batch를 새로 나눔)
  └─ ...
...
     ▼
test_dataset (10,000장) → 32장씩 forward만 → 예측 → accuracy
```

### 10) 한 줄 정리
- **Batch**는 샘플 여러 개를 행으로 쌓아 행렬 곱 한 번에 계산하는 것이고(W는 공유, b는 각 행에 똑같이 더함), **mini-batch**는 메모리와 속도의 절충으로 16~64개 정도씩 묶는 방식이다. 코드는 `DataLoader`가 데이터를 32개씩 잘라 주고, batch마다 **forward → zero_grad → backward → step**으로 weight를 한 번 갱신한다. 이것을 전체 데이터에 대해 한 바퀴 돈 것이 **1 epoch**이다.

---

## Q10. Heaviside 출력 h = [0, 1, 1]처럼 최댓값이 여러 개(동점)일 때 해결법은?

### 1) 문제의 원인: Heaviside가 "얼마나 큰지" 정보를 버린다
- 출력층 z = [−1.3, 0.34, **2.1**] → 실제로는 Virginica(2.1)가 Versicolor(0.34)보다 훨씬 강한 신호다.
- 그런데 Heaviside는 0 이상이면 전부 **1**로 바꾸므로 h = [0, 1, 1]이 되어 차이가 사라진다.
- `np.argmax`는 동점이면 **앞쪽 index**를 돌려주는 규칙이라 1(Versicolor)이 나온다. → **틀린 예측**
- 반대 경우도 있다: z가 모두 음수면 h = [0, 0, 0] → argmax = 0 → 아무 class도 아닌데 **Setosa**로 예측해 버린다.
- 즉 argmax의 동점 규칙이 문제가 아니라, **Heaviside 출력으로 argmax를 하는 것 자체**가 문제다.

### 2) 해결법 ① — 활성 함수 적용 전 z로 argmax (가장 간단)
```python
print("=> Predicted Class: ", np.argmax(output_layer_z, axis=0))   # [2] → Virginica
```
- z에는 크기 정보가 그대로 남아 있으므로 동점이 거의 생기지 않는다.
- 슬라이드 18 PyTorch 코드의 `output_z.argmax(dim=1)`도 같은 방식이다.

### 3) 해결법 ② — 출력층에 연속적인 활성 함수 사용 (강의의 해결 방향, 슬라이드 14~16)
- 출력층 활성 함수를 Heaviside 대신 **Softmax**(또는 Sigmoid, ReLU)로 바꾼다.
```python
softmax_output = F.softmax(torch.tensor(output_layer_z), dim=0)
# [0.028, 0.143, 0.830] → argmax = 2 (Virginica)
```
- 세 함수 모두 **단조 증가**라 z의 크기 순서를 그대로 유지한다 → z로 argmax한 것과 같은 결과 (Q1 참고)
- 그중 **Softmax**가 표준이다.
  - 합이 1인 확률이라 "Virginica일 확률 83%"처럼 해석할 수 있다.
  - 학습할 때 **cross-entropy loss**와 짝을 이루어 쓰기 좋다.
- 주의: ReLU는 음수를 전부 0으로 만들기 때문에 z가 모두 음수면 [0, 0, 0]이 되어 **똑같은 동점 문제**가 생길 수 있다. 그래서 출력층에는 ReLU보다 Softmax를 쓴다.

### 4) 해결법 ③ — 학습으로 weight를 제대로 맞추기 (근본 해결)
- 이 예제의 W, b는 **사람이 임의로 정한 값**이라 원래부터 정확한 분류기가 아니다.
- 데이터로 학습하면 정답 class의 z는 크게, 나머지는 작게 나오도록 weight가 조정되므로 동점이나 오답이 줄어든다.
- 그런데 Heaviside는 gradient가 거의 0이라 backpropagation으로 학습할 수 없다 (Q2 참고).
  - 그래서 **연속 활성 함수 + softmax 출력 + gradient descent 학습** 조합으로 간다. 이것이 슬라이드 17 이후의 흐름이다.

### 5) 임시방편 (참고) — 동점 처리 규칙을 따로 정하기
- **무작위 선택**: 동점인 class 중 하나를 랜덤으로 고른다.
```python
candidates = np.flatnonzero(h == h.max())   # 최댓값을 가진 index들: [1, 2]
pred = np.random.choice(candidates)
```
- **"판단 불가"로 처리**: 1인 class가 정확히 하나일 때만 그 class로, 아니면 "unknown"으로 처리한다.
- 둘 다 정보가 이미 사라진 뒤에 고르는 것이라 **정확도를 올려주지는 못한다**. 실제로는 거의 쓰지 않는다.

### 6) 한 줄 정리
- 동점은 argmax의 문제가 아니라 Heaviside가 크기 정보를 0/1로 뭉갠 탓이다. 해결법은 **크기 정보를 살리는 것**이다. 활성 함수 적용 전 **z로 argmax**하거나, 출력층에 **Softmax** 같은 연속 함수를 쓴다. 근본적으로는 softmax 출력으로 weight를 **학습**시킨다.

---

## Q11. batch로 속도가 빨라지는 건 행렬 크기를 바꿔 행마다 연산해서인가, 아니면 입력 데이터를 실제로 나눠서인가?

### 1) 결론: 두 가지는 "기준"이 다르다
- 속도가 빨라지는 이유는 **여러 샘플을 행으로 쌓아 큰 행렬로 만들고, 행렬 곱 한 번으로 동시에 계산**하기 때문이다. (1개씩 처리하는 것과 비교할 때)
- 입력을 **실제로 나누는 것**(mini-batch로 쪼개기)은 속도를 올리려는 게 아니다. **메모리**를 감당하고 **update를 자주** 하기 위한 것이다. (full-batch와 비교할 때)
```text
1개씩 (s=1)  ──묶는다(합치기)──▶  mini-batch (s=32)  ◀──쪼갠다(나누기)──  full-batch (s=60,000)
             속도가 빨라짐                                 메모리 절약, update 횟수 증가
```
- mini-batch는 **"1개씩보다는 합치고, 전체보다는 나눈"** 중간 지점이다.

### 2) 속도가 빨라지는 진짜 이유: 행렬 곱 한 번 = 여러 샘플 동시 계산
- 1개씩 처리할 때 (60,000번 반복)
```text
x₁ (1×784) × W (784×128) + b   → 결과 1
x₂ (1×784) × W (784×128) + b   → 결과 2
...  (작은 곱셈을 60,000번 순서대로)
```
- batch로 처리할 때 (1,875번 반복)
```text
X (32×784) × W (784×128) + b   → 결과 (32×128)   ← 32개 결과가 한 번에
```
- **행마다 따로 순서대로 계산하는 것이 아니다.** 32개 행을 **동시에(병렬로)** 계산한다.
  - 수학적으로는 결과의 i번째 행 = xᵢW + b로, 1개씩 계산한 것과 **값이 완전히 같다**.
  - 달라지는 건 계산하는 **방식**이다.

### 3) 왜 큰 행렬 곱 한 번이 작은 곱셈 여러 번보다 빠른가
- **GPU 병렬 처리**: GPU에는 계산 코어가 수천 개 있다.
  - 1×784 벡터 하나로는 코어 대부분이 놀고 있다.
  - 32×784 행렬이면 32개 샘플의 계산을 여러 코어에 나눠서 동시에 처리한다.
- **W를 한 번만 읽어 온다**: 행렬 곱에서 시간이 많이 드는 부분은 계산보다 **메모리에서 W를 읽어 오는 것**이다.
  - 1개씩: 샘플마다 W(784×128 ≈ 10만 개 숫자)를 읽음 → 32번 읽음
  - batch: W를 한 번 읽어서 32개 샘플에 **재사용**
- **호출 오버헤드 감소**: Python 반복문 1회, GPU 작업 명령 1회마다 고정 비용이 있다.
  - 60,000번 호출 → 1,875번 호출로 줄어든다.
- **update 횟수 감소**: backward + optimizer.step도 batch당 1번이라 60,000번 → 1,875번
- CPU에서도 NumPy/PyTorch의 행렬 곱은 벡터 명령(SIMD)과 멀티코어로 최적화되어 있어서 같은 효과가 있다.

### 4) "나누기"(mini-batch)는 왜 하나 — 속도가 아니라 메모리와 학습 때문
- 계산 속도만 보면 **한 번에 전부(full-batch)** 넣는 게 가장 효율적이다. 하지만
  - **메모리 한계**: 60,000 × 784 입력에 hidden 결과, backward용 중간값까지 한 번에 올려야 한다. 큰 데이터나 큰 모델에서는 GPU 메모리가 부족하다.
  - **update가 너무 적음**: 1 epoch에 weight 갱신이 1번뿐이라 학습이 진행되는 속도가 느리다.
- 그래서 **GPU가 감당할 만큼(16, 32, 64 ...)** 만 묶어서 병렬 계산의 이점을 얻으면서, update도 자주 하는 것이다.
- 코드로 보면
  - **나누기**: `DataLoader(batch_size=32)`가 60,000개를 32개씩 **실제로 나눠서** 꺼내 준다.
  - **합치기(속도 향상)**: 꺼낸 32개를 `(32, 1, 28, 28)` 하나의 tensor로 **쌓아서** `model(images)`에 한 번에 넣는다.

### 5) 한 줄 정리
- 속도가 빨라지는 것은 **샘플을 행으로 쌓아 큰 행렬 곱 한 번에 병렬로 계산**하기 때문이다. 행마다 차례로 계산하는 것이 아니고, 결과 값은 1개씩 계산한 것과 같다. 데이터를 **나누는 것**은 메모리 한계와 update 빈도 때문에 하는 것이고, 속도를 위한 것이 아니다. mini-batch는 "합쳐서 빠르게, 나눠서 메모리 안에" 두 목적의 절충이다.
