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
