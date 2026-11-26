image data의 구조
- image는 pixel의 2D 배열이고, pixel이 많을수록 고화질이다.
- grayscale은 pixel마다 밝기 값 1개, color는 RGB 값 3개를 갖는다.
- 값은 보통 uint8로 표현하며 0 ~ 2^8-1 = 255 범위다. 실제로는 그대로 쓰지 않고 대부분 normalization을 거친다.
- CIFAR-10은 32x32 RGB라 input feature가 32x32x3 = 3,072개, MNIST는 28x28 grayscale이라 784개다.

image data는 일반적인 data와 같이 flatten과 같이 한줄로 사용하면 다음과 같은 문제가 발생함.
1. 과도한 parameters 발생 -> fully connected layer는 모든 input에 weight가 필요하다. 720x720x3 이미지면 input만 약 155만 개라 memory도 많이 쓰고 weighted sum 계산도 오래 걸려 비효율적이다. (28x28 MNIST도 input 784개에 hidden 128개면 약 10만 개다.➕)
2. local correlation이 사라진다. -> image data는 주변과의 관계가 중요해지는데, 한줄로 피게 되면 집값 데이터, 꽃 특징과 달리 어떤 상태인지 알수가 없게 된다. Iris는 feature 순서를 바꿔도 학습과 테스트의 순서만 같으면 문제없지만, image는 섞으면 무엇인지 알 수 없다. 숫자 1을 알아보는 것도 "까맣다가, 일렬로 하얗다가, 다시 까맣다"는 주변과의 관계 덕분이다.
3. image를 돌리거나 확대하거나 옮기면 같은 위치의 pixel 값은 완전히 달라지지만, 해석(같은 말이라는 것)은 유지되어야 한다. 한줄로 펴서 위치별로 weight를 주면 이걸 처리할 수 없다.

이것들의 해결을 위해 먼저 invariance와 equivariance를 알아보자.
invariance는 입력이 변하여도 출력값은 동일해야 한다. 예를 들어, 고양이의 사진을 확대하거나 잘라도 고양이 사진임이 바뀌면 안된다.(image classification)
식으로는 f[x] = f[t(x)]로 표현할 수 있다.

equivariance는 입력이 변화된 만큼 출력도 변화해야 한다. 예를 들어, 사진에서 소파가 오른쪽으로 옮겨지면 segmentation 결과(pixel마다 소파/테이블/바닥 등을 표시한 mask)의 소파 영역도 똑같이 오른쪽으로 옮겨져야 한다.(image segmentation)
식으로는 f[t(x)] = t[f(x)]로 표현할 수 있다. 즉 이미지를 먼저 옮기고 segmentation한 결과와, segmentation한 뒤 결과를 옮긴 것이 같아야 한다.

사람도 "(5, 5) 값이 255"처럼 절대 위치로 인식하지 않고, 주변보다 밝은지 어두운지로 판단하기 때문에 변환에 강하다.
이처럼 주변 pixel을 함께 보도록 Convolution Layer을 사용한다. Convolution layer를 하나라도 포함하면 Convolutional Neural Network, CNN 이라고 부른다.

image의 edge detection은 사물의 모서리에 주목하여 특징을 잡는다.
각 pixel에서 주변 값을 빼면 변화가 없는 곳은 사라지고 변화가 큰 곳만 남는데, 변화는 주로 사물의 가장자리에서 일어나므로 이것이 edge detection이다.
- 왼쪽과 오른쪽의 차이를 구하면 세로 방향 edge, 위와 아래의 차이를 구하면 가로 방향 edge를 찾는다.

    Vertical edge      Horizontal edge    Laplacian
    -1  0  1           -1 -1 -1           -1 -1 -1
    -1  0  1            0  0  0           -1  8 -1
    -1  0  1            1  1  1           -1 -1 -1

- Vertical: 왼쪽 값을 빼고 오른쪽 값을 더한다. 결과가 양수면 왼쪽이 어둡고 오른쪽이 밝다(dark → bright), 음수면 반대(bright → dark)다. 부호를 뒤집은 filter를 써도 원리는 같다.
- Horizontal: 위쪽 값을 빼고 아래쪽 값을 더한다. 가로 edge에는 반응하지만 세로 edge에는 거의 반응하지 않는다. (예: 일자 눈썹은 horizontal에서 선명하고 vertical에서는 거의 안 보인다.)
- Laplacian: 자신과 주변 전체를 비교하므로 모든 방향의 edge를 찾는다. 배경처럼 주변과 값이 같으면 0이 되고, 값이 변하는 곳에서만 0이 아니다.

이를 위해선, Filter(Kernel)을 사용한다. MxN크기의 사각형을 이미지 위에서 이동시키며 각 위치의 값을 곱하고 더한다(weighted sum).
- Filter는 곧 weight다. fully connected는 모든 input에 weight를 곱해 더하지만, convolution layer는 관심 있는 영역만 곱해 더한다.
- kernel 값은 위의 edge kernel처럼 고정된 것이 아니라 학습되는 weight다. 학습을 통해 어떤 edge(특징)를 찾을지 결정된다.

계산 예시: 3x3 이미지(a~i)에 2x2 kernel(j k / l m)을 적용하면

    C(0,0) = aj + bk + dl + em      C(0,1) = bj + ck + el + fm
    C(1,0) = dj + ek + gl + hm      C(1,1) = ej + fk + hl + im

MNIST 예시: 0~1로 normalization한 5x5 영역에 3x3 kernel을 적용하면 3x3 feature map이 나온다.

    입력 영역                  kernel
    0.0 0.0 0.0 0.0 0.0        0.4  1.7  0.9
    0.0 0.0 0.3 0.7 0.6        2.3 -2.1  4.0
    0.0 0.0 0.9 1.0 1.0       -1.4  0.7  2.1
    0.0 0.0 0.3 0.4 0.3
    0.0 0.0 0.0 0.0 0.0

- 첫 칸은 0이 아닌 항만 남아 0.3 x 4.0 + 0.9 x 2.1 = 3.09다.
- check-in quiz: 같은 입력에 vertical kernel을 적용하면 아래와 같다. 왼쪽과 오른쪽의 차이가 드러나므로 그 위치에 pixel 변화가 있음을 알 수 있다.

    1.2  1.7  0.4
    1.5  2.1  0.4
    1.2  1.4  0.1

- 나온 feature map에 다시 kernel을 적용해 convolution layer를 여러 층 쌓을 수 있다.

Feature map 계산 코드

    img = Image.open("dog.png").convert("L")   # grayscale로 변환
    image_array = np.array(img, dtype=np.float32)
    H, W = image_array.shape
    padded = np.pad(image_array, pad_width=1, mode="constant", constant_values=0)
    feature_map = np.zeros((H, W), dtype=np.float32)
    for row in range(H):
        for col in range(W):
            patch = padded[row:row+3, col:col+3]
            feature_map[row, col] = np.sum(patch * filter)  # assume no bias

- 양쪽에 padding 1을 넣으므로 feature map 크기는 (H+2-3+1) x (W+2-3+1) = H x W 로 입력과 같다.
- row:row+3 은 row, row+1, row+2 를 뜻한다. 이 3x3 patch에 filter를 곱해 모두 더한 값이 feature 하나가 되고, 오른쪽으로 옮기며 반복한다.
- 이 이중 for문이 convolution layer의 전부다.

이것들이 수행되면 Feature Map이 생성된다. JxK 크기의 입력 image에 MxN kernel을 쓰면 Feature Map은 (J-M+1)x(K-N+1) 의 크기를 갖는다.
- 한쪽 끝에 kernel을 놓으면 J-M pixel이 남고, 한 칸씩 움직이므로 처음 위치 1을 더한다.

convolution을 하면 크기가 줄어드는데, 입력 크기를 유지하고 싶을 때 Padding을 사용한다. Padding은 image 주위에 가짜 값(주로 0)을 채워 넣는 것이다.
Padding을 사용한다면 (J+2P-M+1)x(K+2P-N+1) 의 크기를 갖게 된다. padding은 image의 모서리에 있는 값의 가중치를 주기에도 좋다.➕ (padding이 없으면 가장자리 pixel은 kernel 계산에 덜 들어간다.)
원래 image의 크기로 만들 수도 있다. J+2P-M+1 = J 이므로 P = (M-1)/2 로 잡으면 된다.
- MNIST(28x28, 3x3 kernel): padding 없음 → 26x26, P = 1 → 28+2-3+1 = 28 → 28x28

Stride는 image의 크기가 너무 크다면(예: 720x720) Filter을 모두 계산하기에 부담되는 경우 Stride(S)만큼 건너뛰며 계산할 수 있다.
이때 Feature Map의 크기는 ⌊(J+2P-M)/S + 1⌋ x ⌊(K+2P-N)/S + 1⌋ 이다. 항상 나누어떨어지지는 않으므로 양쪽 모두 반내림(floor)한다.
- floor를 쓰는 이유: stride로 건너뛰다가 끝에서 filter가 더 들어갈 자리가 없으면 그 칸은 계산에서 빠지기 때문이다.
- MNIST(28x28, 3x3 kernel), P = 1, S = 2 → ⌊(28+2-3)/2 + 1⌋ = 14 → 14x14
- 14x14, 3x3 kernel, P = 2, S = 3 → ⌊15/3 + 1⌋ = 6 → 6x6

downsampling -> image(feature map)의 크기가 너무 커서 전부 계산하면 오래 걸리는 경우, convolution layer와 함께 크기를 절반, 1/4 등으로 줄이는데 사용한다
1. stride -> 듬성 듬성 계산해 크기를 줄인다
2. pooling -> 일단 계산한 뒤, 영역마다 값 하나로 줄인다. DxD 영역 크기와 stride를 정하며, 크기 계산은 convolution과 같은 공식을 쓴다.
   - Max pooling -> 일정한 크기에서 최댓값 하나를 선택한다
   - Mean(Average) pooling -> 평균을 계산하여 선택한다.
- 4x4 입력, 2x2 pooling, stride 2 → (4-2)/2 + 1 = 2 → 2x2. 일반적으로 이렇게 영역이 겹치지 않게 쓴다.
- 4x4 입력, 3x3 pooling, stride 1 → (4-3)/1 + 1 = 2 → 역시 2x2.
- 슬라이드 average pooling(2x2, stride 2) 예시: 12/4 = 3, 16/4 = 4, 20/4 = 5, 8/4 = 2

upsampling -> feature map에는 잘 쓰이진 않지만, 입력 image가 저화질처럼 크기가 너무 작은 경우 키우는데 사용한다
1. duplicate -> 같은 값으로 복제하여 사용한다 (한 점을 2x2, 3x3 등으로 그대로 복제). 작은 이미지를 크게 늘렸을 때 화질이 깨져 보이는 현상이 이것이다.
2. Max unpooling -> max pooling에서 왔다고 가정하고, 이 값을 최댓값으로 나머지를 이보다 작은 값으로 채운다.(작은 어떤 값을 사용할지 몰라 잘 사용하지 않는다)
3. Bi-linear interpolation -> 가장 많이 쓴다. 두 점을 직선으로 이어 그 사이를 연속된 값으로 채운다.
   - 0과 6 사이에 1개를 넣으면 3, 2개를 넣으면 2, 4
   - 2, 4, 4, 8 예시: 2와 4 사이는 3, 4와 8 사이는 6
   - 오른쪽 끝은 padding처럼 바깥을 0으로 가정한다. 그래서 8과 0 사이는 4

input channel & output channel

color image는 pixel마다 R, G, B 값 3개를 가진다. R 값끼리 모은 행렬, G 값끼리, B 값끼리 모은 행렬을 각각 channel이라 한다.
JxK pixel, C_in개 channel인 이미지면 input feature는 JxKxC_in개다.

먼저 input channel은 필터 안의 두께라 생각하면 된다. kernel도 input channel마다 따로 필요하므로(R용, G용, B용) filter 크기는 m x m x C_in이다.
하나의 input data에 C_in 두께(RGB면 3)를 channel별로 모두 계산한 뒤, 같은 위치의 값을 더해 하나의 output(feature map 한 장)이 발생한다.
그렇기에 weight parameters는 m^2xC_in 이지만, bias는 1이다. kernel을 이미지 전체에 재사용하므로 이미지 크기와는 무관하다.
- 결국 다 더해지므로 feature map의 장수와 크기는 input channel 수의 영향을 받지 않는다. 크기는 여전히 ⌊(J+2P-M)/S + 1⌋ 로만 정해진다.

예시: input channel 2개 (3x3 input, 2x2 kernel, padding 0, stride 1 → 2x2 feature map)

    channel 1: input 0..8, kernel [0 1; 2 3]    왼쪽 위 = 0x0 + 1x1 + 3x2 + 4x3 = 19
    channel 2: input 1..9, kernel [1 2; 3 4]    왼쪽 위 = 1x1 + 2x2 + 4x3 + 5x4 = 37
    합: 19 + 37 = 56
    오른쪽 위: (1x0 + 2x1 + 4x2 + 5x3) + (2x1 + 3x2 + 5x3 + 6x4) = 25 + 47 = 72
    결과: [56 72; 104 120]

output의 개수(feature map 장수)를 정하는 것은 output channel이다. edge detection에서 봤듯이 filter(kernel set) 하나는 horizontal이면 horizontal, vertical이면 vertical처럼 한 가지 feature만 학습할 수 있기 때문에, 여러가지 속성을 잡을 수 없다. 그렇기에 kernel set을 C_out개 만들어 output channel을 통해 다양한 filter를 씌울 수 있다. 즉 전체 parameter는 (m^2xC_in+1)xC_out이다.
- filter 하나는 fully connected의 hidden node 하나와 비슷하다. hidden node는 모든 입력에 대한 weighted sum이고, filter는 특정 영역(patch)에 대한 weighted sum이다.
- input channel: RGB처럼 입력이 가진 여러 성분을 다루기 위한 것 (계산 후 더해짐)
- output channel: 여러 종류의 feature를 학습하기 위해 여러 filter를 쓰는 것 (feature map 장수가 됨)

    filter 차원   = M x M x C_in x C_out
    parameter 수  = (M^2 x C_in + 1) x C_out

- 외우는 법: "filter size x input channel + bias 1, 이것이 output channel 수만큼"

일반적인 CNN 구조
Input → Convolution → Pooling → Convolution → Pooling → Flatten → Fully connected → Softmax
- Convolution layer: 주변 pixel과의 관계(edge, 변화)를 계산한다. class 확률을 계산하는 layer가 아니다.
- Fully connected layer: class 확률을 계산한다. 대부분의 CNN은 맨 뒤에 이 layer를 둔다. classification이면 output neuron 수를 class 수에 맞춘다.
- Flatten: 마지막 feature map을 한줄로 펴서 neuron으로 만든다.
- 마지막 feature map이 7x7이고 class가 10개면 Linear(49, 10), 3x3이면 Linear(9, 10)이다.
- feature map이 6x6이면 neuron은 36개이고, hidden neuron이 128개면 weight는 36 x 128개가 필요하다.
- 그래서 feature map 크기 계산을 할 줄 알아야 마지막 fully connected layer를 설계할 수 있다. (교수님 강조) channel 수까지 알아야 flatten 후 Linear(400, 120)인지 Linear(300, 120)인지 정할 수 있다.

LeNet-5 (Yann LeCun이 만든 가장 기본이 되는 CNN)
- 입력은 32x32, channel 1(grayscale)로 고정이다. 28x28인 MNIST는 padding이나 interpolation upscaling으로 맞춘다.
- feature map 크기 흐름 (Maps 열 = output channel 수)

    Layer                       계산                 출력        Parameter
    Input                       -                    32x32x1     -
    C1 Conv (kernel 5, s 1)     (32-5)/1 + 1 = 28    28x28x6     (5x5x1 + 1) x 6  = 156
    S2 Avg pool (2x2, s 2)      (28-2)/2 + 1 = 14    14x14x6     0
    C3 Conv (kernel 5, s 1)     (14-5)/1 + 1 = 10    10x10x16    (5x5x6 + 1) x 16 = 2,416
    S4 Avg pool (2x2, s 2)      (10-2)/2 + 1 = 5     5x5x16      0
    Flatten                     5 x 5 x 16           400 neurons

- pooling은 channel마다 따로 적용하므로 장수는 그대로, 크기만 줄어든다. 학습할 parameter도 없다.
- C3의 input channel 6은 앞 layer의 output channel 6에서 온 것이다.
- 슬라이드 20의 (5x5x6x10) + 16 = 1516은 무시하라고 하셨다. 원래 LeNet은 6장을 전부 더하지 않고 일부씩 묶는 특수한 연결로 parameter를 줄였는데, 그 모델 고유의 구조라 잊어도 된다. 일반 convolution이면 (5x5x6 + 1) x 16이 맞다.
- fully connected layer의 parameter 수 (weight + bias)

    Dense 1 (400 → 120)   400 x 120 + 120 = 48,120
    Dense 2 (120 → 84)    120 x 84 + 84   = 10,164
    Output  (84 → 10)     84 x 10 + 10    = 850

Fully connected = 입력과 같은 크기의 convolution
5x5x16에서 120으로 가는 layer는 두 가지로 표현할 수 있다.
1. flatten해서 400개 입력 → 120 neuron fully connected: 400 x 120 + 120 = 48,120
2. 5x5 kernel, input channel 16, output channel 120인 convolution: (5x5x16 + 1) x 120 = 48,120
- kernel 크기가 입력 크기와 같으면 출력은 (5-5)/1 + 1 = 1, 즉 1x1이고 이는 입력 전체에 대한 weighted sum이다. kernel set 하나가 neuron 하나의 역할을 하므로, 120세트는 neuron 120개짜리 fully connected와 같다.
- 그래서 LeNet-5를 검색하면 이 layer가 convolution(C5)으로도, fully connected(F5)로도 나온다.

Convolution이 parameter를 줄이는 이유
- convolution의 weight 수는 filter 크기와 같다. 5x5 filter 하나는 5 x 5 + 1(bias) = 26개의 parameter를 가진다 (channel 무시).
- 32x32x1 입력을 fully connected로 연결하면 hidden neuron이 1개여도 1024 + 1 = 1025개가 필요하다.
- fully connected는 feature마다 weight가 따로 있지만, convolution은 같은 filter를 모든 위치에 곱한다(weight sharing). 그래서 전체 parameter가 크게 줄어든다.

PyTorch 구현
- filter를 직접 구현할 일은 크게 없고 nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)를 쓴다. 앞의 두 숫자가 input / output channel이다.

    self.c1 = nn.Conv2d(1, 6, kernel_size=5, stride=1, padding=2)
    self.c3 = nn.Conv2d(6, 16, kernel_size=5, stride=1, padding=0)
    self.c5 = nn.Conv2d(16, 120, kernel_size=5, stride=1, padding=0)
    self.pool = nn.AvgPool2d(kernel_size=2, stride=2)
    self.f6 = nn.Linear(120, 84)
    self.output = nn.Linear(84, num_classes)
    self.tanh = nn.Tanh()

- MNIST는 28x28x1인데 LeNet-5는 32x32 입력용이므로 c1에 padding=2를 넣어 32x32로 맞춘다. 입력이 32x32면 padding 0, 30x30이면 padding 1이다.
- Linear 입력이 400이 아닌 이유: 위에서 본 것처럼 c5가 5x5 convolution으로 이미 120을 만들기 때문에 다음 Linear는 120에서 시작한다.
- Implementation (2): c5 대신 self.f5 = nn.Linear(400, 120)을 써도 된다. 단, fully connected는 flatten 이후에 와야 하므로 forward에서 torch.flatten 아래로 위치가 옮겨진다. parameter 수(48,120)는 동일하다.
- torchsummary.summary(model, input_size=(1, 28, 28))로 각 layer의 output shape과 parameter 수(156, 2,416, 48,120, 10,164, 850)를 확인할 수 있다.
- activation function은 tanh를 쓴다.
- MNIST batch training 코드와 거의 같고, 모델 선언 부분과 forward propagation 순서만 다르다.
- 성능: LeNet-5는 MNIST 97.92%, Fashion-MNIST 85.92%로, fully connected(Fashion-MNIST 약 81%)보다 높다.

CIFAR-10 & CIFAR-100 (color dataset)
- CIFAR-10: 32x32 RGB color 이미지, 10개 class(airplane, automobile, bird, cat, …), class당 6,000장. 개수는 안 외워도 되지만 32x32, RGB라는 것은 기억할 것.
- CIFAR-100: 100개 class, class당 600장(training 500 / test 100)
  - label이 두 개다: 세부 class 100개(fine label)와 superclass 20개(coarse label). superclass 하나 아래에 class가 5개씩 묶여 있다.
  - 예: bicycle, bus, motorcycle, pickup truck, train → vehicles 1 / bee, beetle, butterfly, caterpillar, cockroach → insects
  - 그래서 100-class 분류도, 20-class 분류도 할 수 있다.

LeNet-5를 CIFAR에 쓰려면
1. padding: CIFAR는 이미 32x32이므로 padding=0
2. input channel: 첫 convolution layer의 input channel을 1 → 3으로. 뒤쪽 feature map 개수나 크기는 바뀌지 않는다(input channel은 계산 후 더해지므로).
3. CIFAR-100이면 마지막 output layer를 100(superclass면 20)으로
- color 이미지라고 항상 RGB 3 channel인 것은 아니다. 투명도까지 4 channel이거나 명도·채도 등 다른 표현일 수도 있으니 데이터에 맞게 input channel 수를 정한다.

CIFAR-10 feature map 크기 예시 (32x32, kernel 3x3)
- padding 없음: 32 - 3 + 1 = 30 → 30x30
- padding 2: 32 + 2x2 - 3 + 1 = 34 → 34x34 (양쪽이라 2를 두 번 더함)
- padding 2, stride 2: ⌊(32 + 2x2 - 3)/2 + 1⌋ = 17 → 17x17

Normalization

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))
    ])

- 필수는 아니지만 입력 데이터의 범위를 맞추기 위해 보통 한다. 숫자는 외울 필요 없다.
- Normalize(mean, std)는 (input - mean) / std, 즉 z-score normalization을 R, G, B channel마다 따로 적용한다.
- 적용 후에도 shape(32x32x3)은 그대로이고, 각 channel의 평균이 0, 표준편차가 1이 된다.
