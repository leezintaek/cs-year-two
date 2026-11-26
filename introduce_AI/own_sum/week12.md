지금까지 배운 neural networks (fully connected, CNN)
1. 한 방향으로만 진행된다. input → output으로 앞으로만 가고, 자기 노드로 다시 돌아오는 경로, 즉 cycle이 없다.
2. 입력과 출력의 길이가 고정돼있다.
   - Iris는 input feature 4개, LeNet-5는 32 x 32 x 1만 받음 (MNIST 28 x 28은 padding 2로 맞춤)
   - output도 CIFAR-10은 10개, Iris는 3개로 정해져 있음
3. 이런 데이터는 표(row = example, column = attribute)로 나타낼 수 있어서 tabular data라고 부른다.
4. input 하나를 넣으면 한 시점에서 정답 하나를 예측한다.

Recurrent Neural Networks (RNNs)
순서가 있는 데이터(sequential / time-series data)에 주로 사용된다.
예시 : 주가(그저께, 어제, 오늘 → 내일), 자율주행 car trajectory(지금까지 위치 → 다음 위치), NLP(단어 순서가 바뀌면 의미가 바뀜)
응용 :
 - image captioning : 이미지(고정 길이 input)를 보고 설명 문장(가변 길이 output)을 만듦. 단어 순서를 섞으면 다른 말이 됨
 - translation : 스페인어 단어 sequence → 영어 단어 sequence
sequence가 시간에 따라 어떻게 변하는지를 학습해서 미래를 예측한다.
input 길이도, output 길이도 가변(nonfixed-size)으로 다룰 수 있다. (2일, 10일, 20일 등)
이를 위해 layer 안에서 순환(cycle)한다.

Recurrent connection과 unfolding
fully connected neuron : input 전체에 weight를 곱해 더함
convolution neuron : 특정 영역에 filter(weight)를 곱해 더함
recurrent neuron : 위와 같이 x로 weighted sum + 활성함수를 해 y를 내는데, 자기 output이 자기에게 다시 돌아오는 cycle이 추가됨
unfolding : 이 cycle을 시간 축으로 펼쳐 그린 것. 시점 t의 neuron은 현재 input x(t)와 이전 시점의 output y(t-1)을 함께 받는다.
neuron이 여러 개여도 같다. 모든 neuron이 input vector x(t)와 이전 시점의 output vector y(t-1)을 받는다.
* 첫 시점(t = 0)에는 이전 output이 없으므로 y(-1)은 0으로 초기화한다.

계산 방법
W_x : 현재 시점의 input x(t)에 대한 가중치
W_y : 이전 시점(t-1)의 output y(t-1)에 대한 가중치 (다른 뉴런이 아니라 자기 자신의 이전 시점 output)
y(t) = 활성함수(x(t) * W_x + y(t-1) * W_y + b)
     = 활성함수([x(t)  y(t-1)] * W + b),  W = [W_x ; W_y] (x와 y는 옆으로, W_x와 W_y는 세로로 이어 붙임)
두 식은 완전히 같다. 편한 쪽을 쓰면 됨 (교수님은 위쪽이 편하다고 하심)
* RNN은 주로 활성함수로 tanh를 사용한다. 단, 시험에서 tanh 값을 직접 구하라고 하지는 않는다.

mini-batch에서의 dimension
m : mini-batch 하나의 size (instance 수)
n_inputs : input features의 개수
n_neurons : 뉴런의 개수
X(t) : m x n_inputs 크기의 행렬, 현재 시점의 input
W_x : n_inputs x n_neurons, n_inputs개 feature를 받아 n_neurons개 output을 만들어야 하므로
Y(t-1) : m x n_neurons, 이전 시점의 layer output
W_y : n_neurons x n_neurons, 이전 output n_neurons개를 받아 다시 n_neurons개 output을 만들어야 하므로
b : n_neurons, neuron마다 bias 하나
* XW, WᵀX 같은 transpose 표기는 정의하기 나름이니 연연하지 말 것

Time window
sequence의 길이. 몇 개 시점을 보고 예측할지를 정한다.
window = 3이면 t = 0, 1, 2에서 각각 x(t)와 y(t-1)로 y(t)를 구한다.
핵심 : 같은 시점의 x와 이전 시점의 y로 계산한다.

예시 1 : x(0)=3, x(1)=2, x(2)=4, W_x = 0.5, W_y = 0.2, bias 없음, window = 3
y(0) = tanh(3 x 0.5 + 0    x 0.2) = tanh(1.5)   ≈ 0.91  ← y(-1) = 0
y(1) = tanh(2 x 0.5 + 0.91 x 0.2) = tanh(1.182) ≈ 0.83
y(2) = tanh(4 x 0.5 + 0.83 x 0.2) = tanh(2.166) ≈ 0.97

예시 2 : input feature가 시점마다 2개
x(0) = [3, 1], x(1) = [2, 7], x(2) = [4, 5]
예측값은 시점마다 1개 → W_x = [0.5, -0.1]ᵀ (2 x 1), W_y = [0.2] (1 x 1)
y(0) = tanh(3 x 0.5 + 1 x (-0.1) + 0 x 0.2) = tanh(1.4) ≈ 0.89
y(1) = tanh(2 x 0.5 + 7 x (-0.1) + 0.89 x 0.2) ≈ 0.44
y(2) = tanh(4 x 0.5 + 5 x (-0.1) + 0.44 x 0.2) ≈ 0.92
dimension 확인 : (1 x 2)(2 x 1) = 1 x 1, (1 x 1)(1 x 1) = 1 x 1
이어 붙인 형태 [3 1 0] * [0.5; -0.1; 0.2]로 계산해도 같다.
* output 개수는 input feature 개수와 상관없다. 원하는 만큼 예측할 수 있다.

Memory Cells
Y_t 는 X_t와 Y_t-1
Y_t-1 는 X_t-1와 Y_t-2
... 을 거쳐서 온다
-> Y_t는 X_0, X_1, ..., X_t 전부의 함수다. 즉 이전의 기록을 모두 가지고 있다(일종의 memory).
그래서 이 neuron을 memory cell이라 부른다. 시간 단계를 넘어 state를 보존하는 부분이다.
문제점 : Y_100 같은 경우 100 시점 전 정보는 Wy를 100번 거쳐서 오며, 가중치는 보통 1보다 작기 때문에(예: 0.01^100) 값이 희미해진다.
-> 가까운 시점의 패턴은 반영되지만 먼 시점의 패턴은 잘 반영되지 않는다. 즉 기본 cell은 짧은 pattern만 학습한다.

Hidden state
이 한계를 조금이나마 극복하기 위해 hidden state가 도입되었다. (완전한 해결은 아님 → LSTM, GRU)
input과 output 사이에 숨겨진 state H를 하나 둔다.
기본 cell : output이 곧 state다. Y가 순환한다.
  H(t) = Y(t) = 활성함수(X_t * W_x + Y_t-1 * W_y + b)
hidden state cell : H가 순환하고, Y는 그 시점의 H에 linear layer를 한 번 더 거쳐 나온다.
  H(t) = 활성함수(X_t * W_x + H_t-1 * W_h + b_h)
  Y(t) = 활성함수(H_t * W_y + b_y)
weight 3개의 역할
  W_x : input → hidden
  W_h : hidden → 다음 시점 hidden (순환)
  W_y : hidden → output (linear)
기억(H)과 내보내는 값(Y)이 분리되므로 H에 나중에 쓸 정보를 담아 둘 수 있다. 하지만 H도 W_h가 반복해서 곱해지므로 오래된 정보가 희미해지는 문제는 남는다.

체크인 퀴즈 (hidden state 구조)
x(0) → RNN → h(0) → linear → y(0), h(0)은 다음 시점으로 넘어가 x(1)과 함께 h(1) → y(1), ... window = 3
h(t) = tanh(x(t) * W_x + h(t-1) * W_h),  y(t) = 활성함수(h(t) * W_y)   (h(-1) = 0, bias 없음)
값(전사 기준, 슬라이드로 확인 필요) : x는 지난 퀴즈와 같음 [3,1], [2,7], [4,5], W_x = [0.5, -0.1]ᵀ, W_h = -0.1, W_y = 0.2

주가 예측 RNN
data : IBM 주가 데이터. 날짜마다 시가(Open), 최고가(High), 최저가(Low), 종가(Close) 4개 값 → 인덱스 [0]~[3], 종가는 [3]
전처리 : 원본이 날짜순이 아니어서 날짜순으로 sorting → normalization
목표 : 하루치 4개 값으로 다음 날 종가 1개 예측 → input 4, output 1
4개짜리 세트 여러 개(sequence)로 예측하며, 몇 개를 볼지는 time window가 정한다. 여기서는 window = 7, hidden = 64

sliding window : 한 칸씩 밀면서 (7일치 input, 다음 날 종가) 쌍을 만든다.
  [x(0), ..., x(6)] → x(7)[3]
  [x(1), ..., x(7)] → x(8)[3]
  ...
x(1)[3] : ( )는 시간(몇 번째 날), [ ]는 그날 값 4개 중 몇 번째인지. 즉 1일차 종가

def create_inout_sequences(input, tw):  #여기서 input은 sorting과 normalization을 마친 input (L x 4) / tw는 window로 7이다
    inout_seq = []
    L = len(input)  #전체 날짜수
    for i in range(L-tw):   #쌍은 총 L-tw개
        data_seq = input[i:i+tw]    #i=0일 때 x_0-x_6, shape (7, 4)
        data_label = input[i+tw:i+tw+1][0][3]   #윈도우 다음 날의 종가. i=0일 때 7일차 종가 = input[i+tw][3]
        inout_seq.append((data_seq ,data_label))    #(7일치 sequence, 다음 날 종가) 쌍을 저장

    data = inout_seq;   #train/test 나누기. 섞지 않고 시간순으로 자름
    test_set_size = 20  #마지막(가장 최근) 20개 쌍을 test로 고정
    train_set_size = len(data) - (test_set_size);

    train = data[:train_set_size]
    test = data[train_set_size:]

    return train,test

종류
vec-to-seq : one-to-many. 예) image captioning
  첫 시점 뒤의 input은 알 수 없기에 0으로 놓는다. (슬라이드에는 같은 input vector를 매 시점 반복해 넣는 방식으로 나옴)
seq-to-vec : many-to-one. 마지막 output을 제외하고 모두 무시한다. 예) 영화 리뷰 → 좋아요/싫어요(감성 점수)
seq-to-seq : many-to-many. 예) 지난 N일 주가 → 하루씩 민 주가
encoder-decoder networks : many-to-many. 예) 번역
  seq-to-vec encoder에 vec-to-seq decoder를 붙인 경우이며, seq-to-seq보다 더 잘 된다.
  이유 : seq-to-seq는 각 시점이 자기 앞의 단어까지만 안다. 하지만 언어는 문장 끝의 단어가 앞의 번역에 영향을 줄 수 있어 끝까지 들어야 한다.
  input을 끝까지 읽고 이해하는 과정이 encoder, 다 들은 뒤 출력을 만드는 과정이 decoder다.

Seq-to-vec architecture (주가 예측)
7일간 4개 값의 변화를 보고 마지막 날의 다음 날 종가 하나만 맞추므로 seq-to-vec이다.
7 x 4 ─(rnn)→ 7 x 64 ─(linear)→ 7 x 1 → 마지막 값만 사용
  X(t) : 1 x 4,  W_x : 4 x 64,  H(t-1) : 1 x 64,  W_h : 64 x 64,  H(t) : 1 x 64
  linear : H(t) 1 x 64 * W_y 64 x 1 → 1 x 1
hidden 64 : RNN layer 안에 recurrent neuron이 64개 있다는 뜻(n_neurons = 64). H(t)는 지금까지의 흐름을 숫자 64개로 요약한 것

class RNN(nn.Module):
    def __init__(self, input_size=4, hidden_layer_size=64, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        self.rnn = nn.RNN(input_size, hidden_layer_size)    #4 → hidden 64로 순환, 기본 활성함수 tanh
        self.linear = nn.Linear(hidden_layer_size, output_size)     #hidden 64 → output 1 (W_y)

    def forward(self, input_seq):
        rnn_out, hidden_out = self.rnn(input_seq.view(len(input_seq), 1, -1))   #(7, 4) → (7, 1, 4) = (시간, batch, input). rnn_out은 모든 시점의 H (7, 1, 64), H(-1)은 0
        predictions = self.linear(rnn_out.view(len(input_seq), -1))     #(7, 64) → (7, 1), 시점마다 종가 예측 1개
        return predictions[-1]      # 마지막 시점만 → seq-to-vec, data_label(다음 날 종가)과 비교해 loss 계산

Prediction of several time-steps
지금까지는 결국 하루 뒤 하나만 예측했다.
여러 시점을 예측하려면 다음 값을 예측한 뒤 그 값을 실제로 일어난 것처럼 input에 추가해 다시 돌리는 것을 반복한다.
예) 0~5일만 알 때 6일 예측 → 그 값을 넣어 7일 예측

RNN의 장단점
장점
1. time window로 input/output 길이를 자유롭게 정할 수 있다.
2. sequence가 길어져도 model size가 커지지 않는다. (W_x, W_h, W_y를 시점마다 재사용)
3. 이전 시점의 정보를 계산에 반영할 수 있다.
4. 시간에 걸쳐 weight sharing을 한다.
단점
1. 계산이 느리다. time window만큼 반복 계산해야 한다.
2. 오래된 정보를 알기 어렵다. 100 시점 전 정보는 W가 100번 곱해져 온다.
3. 현재 state에 미래 input을 반영할 수 없다. → 이를 해결하려고 나온 것이 encoder-decoder