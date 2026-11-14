분할하고 링킹하는 이유는?
1. 코드의 재사용성이 용이하다 - 어떤 기능, 역할을 하는 파일을 만들어 두면 나중에 불러오기만 하면 된다.
2. 협업에 용이하다 - 전체에서 각 사람들이 맡은 파트를 나눠 만들어서 합치면 편하다.
3. 개발 시간의 단축에 용이하다 - 병렬로 컴파일하기도 하며, 어떤 부분을 고쳤을 때 그 부분만 따로 컴파일 하면 된다.

어떤 변수를 분할한 파일들이 사용했을 때, extern 과 같이 참조를 통해서 사용해야 한다. 안그러면 변수가 선언이 안되어있거나, 같은 이름의 변수를 여러개 만드는 수가 있다.

헤더 파일이 존재하는 이유? - 어떤 변수를 참조하고 있다고 가정할때 이 변수의 타입을 바꾸고 싶으면 모든 파일에서 바꿔야 한다. 그러다 치명적인 실수가 생기기도 한다.

라이브러리가 필요한 이유? - 재사용이 가장 큰 목적이다. 이를 위해 하나의 파일에 모든 라이브러리에 있는 함수를 적으면 다 뒤져봐야 하기에 비 효율적이고, 각 함수에 파일을 만들면, 사용자가 모두 타이핑 해야 하기에 귀찮다. -> 어떤 함수들을 그룹핑해서 사용한다.

Define vs Declare
Define 같은 경우는 변수나 함수 자체를 만드는 행위이다. 하지만 Declare는 이 변수나 함수 자체가 존재한다고 가정하고 넘어가게 한다.(레퍼런스를 할것이라고 가정한다)

변수의 속성
1. scope - 지역 변수일 때, 이 변수는 block 안에서만 사용 가능하다. 전역 변수일 때, 파일 전체에서 사용 가능하다.
2. duration - 지역 변수일 때, 블럭의 실행시간동안 존재한다(만약 static이 붙을 경우 data section에 따로 값이 존재한다). 전역 변수일 때, 실행 시간동안 존재한다.
3. linkage - 지역 변수일 때, 다른 모듈이 참조 할 수 없다. 전역 변수일 때, 다른 모듈에서 참조가 가능하다.

다른 함수 안에서 같은 이름의 static 변수가 존재하는 경우, 내부에서는 같은 이름의 변수로 여러 개 존재 할 수 있다. Indexing 된 상태로 존재한다.

링킹

다양한 코드와 데이터를 excutable한 상태의 파일로 만드는 과정
링킹에는 2가지가 존재한다.
1. Static Linking - compile time 동안 수행됨. -> .o file
2. Dynamic Linking - 여기서 다시 2가지로 분류 가능함 1. load time 동안 수행됨 2. run time 동안 수행됨 -> .so file
redundancy를 제거하기 위해 주로 Dynamic Linking을 사용하지만, Static Linking은 Dynamic Linking보다 빠르기에 둘다 알고 있어야 한다.
왜 더 빠른가?
왜 중복성이 제거되나?

를 통해 a.out file 생성

Linking 과정
1. Symbol resulution?
2. Relocation?

Symbol 은 아래와 같이 구성된다
name
type
binding
reserved
section
value
size

Symbol Definition and Reference 각각 create 하는 것과 use 하는 것이라 생각

Symbol Type Funcion Object

Symbol binding 은 3가지로 나뉜다
1. Local symbols - 지역 변수가 아니다. static과 같이 지역적으로 사용 가능한 값을 말한다.
2. Global symbols - 전역 변수와 같은 것을 말한다.
3. External symbols - Extern 키워드를 사용한 것과 같이 참조하는 값을 말한다.

Symbol Section
.text - code들이 들어간다
.rodata - 읽는 것만 가능한 값이 들어간다 (const)
.data - 초기화를 한 값이 포함된다.
.bss - data와 비슷하지만 초기화를 하지 않은 값을 포함한다.(0으로 초기화 한 값도 포함한다)
data와 bss를 나눈 이유는 공간 효율성을 위해서이다.
