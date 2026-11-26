분할하고 링킹하는 이유는?
1. 코드의 재사용성이 용이하다 - 어떤 기능, 역할을 하는 파일을 만들어 두면 나중에 불러오기만 하면 된다.
2. 협업에 용이하다 - 전체에서 각 사람들이 맡은 파트를 나눠 만들어서 합치면 편하다.
3. 개발 시간의 단축에 용이하다 - 병렬로 컴파일하기도 하며, 어떤 부분을 고쳤을 때 그 부분만 따로 컴파일 하면 된다. but, 프로그램 성능과는 무관하다.

어떤 변수를 분할한 파일들이 사용했을 때, extern 과 같이 참조를 통해서 사용해야 한다. 안그러면 변수가 선언이 안되어있거나, 같은 이름의 변수를 여러개 만드는 수가 있다.

헤더 파일이 존재하는 이유? - 어떤 변수를 참조하고 있다고 가정할때 이 변수의 타입을 바꾸고 싶으면 모든 파일에서 바꿔야 한다. 그러다 치명적인 실수가 생기기도 한다.

라이브러리가 필요한 이유? - 재사용이 가장 큰 목적이다. 이를 위해 하나의 파일에 모든 라이브러리에 있는 함수를 적으면 다 뒤져봐야 하기에 비 효율적이고, 각 함수에 파일을 만들면, 사용자가 모두 타이핑 해야 하기에 귀찮다. -> 어떤 함수들을 일정 규칙에 맞게 그룹핑해서 사용한다.

Define vs Declare
Define 같은 경우는 변수나 함수 자체를 만드는 행위이다. 하지만 Declare는 이 변수나 함수 자체가 존재한다고 가정하고(Define된 값 사용) 넘어가게 한다.(레퍼런스를 할것이라고 가정한다)
* 함수는 앞에 extern이 생략되기도 하며, body가 존재해야 define이다.

변수의 속성
1. scope - 지역 변수일 때, 이 변수는 block 안에서만 사용 가능하다. 전역 변수일 때, 파일 전체에서 사용 가능하다.
2. duration - 지역 변수일 때, 블럭의 실행시간동안 존재한다(만약 static이 붙을 경우 data section에 따로 값이 존재한다). 전역 변수일 때, 실행 시간동안 존재한다.(프로그램의 시작과 끝)
3. linkage - 지역 변수일 때, 다른 모듈이 참조 할 수 없다. 전역 변수일 때, 다른 모듈에서 참조가 가능하다.
블럭 안에서 동일한 이름의 전역 변수와 함께 지역 변수가 존재할 때, 지역 변수가 우선적이다.
다른 함수 안에서 같은 이름의 static 변수가 존재하는 경우, 내부에서는 같은 이름의 변수로 여러 개 존재 할 수 있다. Indexing 된 상태로 존재한다.

전역 변수에 static 키워드를 붙이게 되는 경우, internal 속성을 부여 받아 다른 file에서 lingking 할 수 없게 된다.
지역 변수에 static 키워드를 붙이게 되는 경우, permanent 속성을 부여 받아 블럭 밖에서도 존재하게 된다.

링킹

다양한 코드와 데이터를 excutable한 상태의 파일로 만드는 과정
링킹에는 2가지가 존재한다.
1. Static Linking - compile time 동안 수행됨. -> .o file
2. Dynamic Linking - 여기서 다시 2가지로 분류 가능함 1. load time 동안 수행됨 2. run time 동안 수행됨 -> .so file
redundancy를 제거하기 위해 주로 Dynamic Linking을 사용하지만, Static Linking은 Dynamic Linking보다 빠르기에 둘다 알고 있어야 한다.
자주 쓰는 library라도 사용하는 모든 파일에 복사되기 때문에 redundancy가 발생한다.
왜 더 빠른가? 모두 복사가 돼있기 떄문이다.
static linking과 달리 존재 여부만 확인하며 나중에 linking 하기 때문에 중복성이 줄어든다.

.o file, .so file 를 통해 a.out file 생성

Static Linking 과정
1. Symbol resulution? -> symbol table을 보며 symbol reference가 정확히 하나의 definition과 연결되어 있음을 보장시키는 단계이다.
2. Relocation? -> code는 code끼리(함수), data는 data끼리 모은다. 또한 가짜(상대주소)를 실제 주소로 변환한다.
자세한 과정은 후에 기술한다.

Symbol은 전역변수들과 함수들의 정보를 담기 위해 존재한다.
아래 구성을 통한 정보들을 통해 함수와 변수를 찾는다.
Symbol 은 아래와 같이 구성된다
1. name - symbol의 이름이다.
2. type - type으로는 Object와 Function만 존재한다. 함수(코드)만 Function이며, 나머지 변수들은 Object이다.
3. binding - Local, Global, External로 구별된다. Local은 지역 변수를 의미하는 것이 아니라, static 함수 변수를 의미한다. static은 파일안에서만 사용 가능하기 때문에 Local 취급이다. Global은 다른 파일에서 external 할 수 있는 것들을 뜻한다. static과 extern이 없는 것들이 속한다. External은 이 모듈이 다른 모듈을 reference하는 것이다. extern 선언한 것과 선언하지 않은 함수 모두를 포한한다.
4. reserved - 1byte padding 부분이다. 앞 부분 byte의 부분을 빈자리로 채워준다고 생각하면 될것 같다.
5. section - 따로 기술한다.
6. value - 주소를 의미한다. linking이 모두 끝나기 전에는 section안에서의 주소를 의미한다.
7. size - 말 그대로 크기이다.

Symbol Definition and Reference 각각 create 하는 것과 use 하는 것이라 생각하면 된다. 함수는 body가 존재하냐 안하냐로 구별하면 된다. 참조한 것 또한 symbol에 기록된다. 기록되지 않는 것은 지역 변수 뿐이다.

Symbol Section - 같은 속성을 가진 Symbol 끼리 모아둔다.
.text - code들이 들어간다. 함수라고 생각하면 된다.
.rodata - 읽는 것만 가능한 값이 들어간다 (const).
.data - 초기화를 한 값이 포함된다.
.bss - data와 비슷하지만 초기화를 하지 않은 값을 포함한다.(0으로 초기화 한 값도 포함한다)
data와 bss를 나눈 이유는 공간 효율성을 위해서이다. 보충 설명하자면, 초기화를 해두지 않은 것은 중간에 필요한 만큼 따로 할당을 하기 때문에, data와 bss로 나누는게 더 효율적이다.

readelf -h main.o를 통해 object파일을 보면 오브젝트 파일을 볼 수 있다. Magic 항목에는 magic number가 적혀 있는데 7f 다음 수들을 아스키 값 변환을 하면 ELF가 된다. 그 뒤는 64비트, 리틀엔디안임을 알 수 있다. 다른 ABI에서는 다른 값이 나올 수 있다.

.symtab .rel.tex .rel.data .debug section header table라는 것들이 더 존재한다. 이것들은 memory에 로드 되지 않는다.

1. Symbol Resoulution
n개의 object를 입력받아 symbol table을 참고하여, 세 종류로 처리한다.
Local, External, Global symbol
Local은 이미 하나만 존재한다라는 것을 가정하기에 따로 처리하지 않는다.
External은 n-1개(본인 제외)를 찾으며 definition이 하나 있는지 확인한다.
Global 또한 defition이 하나인지 확인하는데, 여기서 2개일 경우 아래와 같은 규칙에 의해 하나르 선택한다.

strong weak
strong symbol 함수/초기화된 변수
weak 초기화되지 않은 변수/static 변수
strong이 2개일 경우 linking error
strong 1 weak 1 일 경우 strong을 선택한다
weak 2개 인경우 임의로 하나를 선택한다
-> 원치 않은 상황이 발생 할 수 있다.

section에서 초기화 되지 않은 값을 .bss가 아닌 *COM*으로 처리하는 것에 주의해야 한다. weak symbol이기 때문에 strong이 나올수 있을지 모르기 때문에 external 처리 할수도 있기 떄문이다.

2. Relocation
Symbol resolution이 끝났기 때문에 모든 reference가 하나의 definition과 연결됐음을 가정한다.
Relocation은 2단계를 거친다.
1. section과 symbol definition의 relocation
여기서 code는 code끼리 data는 data끼리 모은다. 여기서 실제 주소가 value에 입력된다.
2. section 안의 symbol reference 수정
linker는 컴파일러가 남긴 relocation entry 메시지를 이용해 reference주소를 채우는 것이다.
컴파일러가 만약 'A section에 0xa위치 reference 주소좀 넣어줘' 라고 요청한다면
링커가 '그래 나 그 refernce 어딨는지 아니까 A section 0xa 위치에 주소 넣어놓을게' 라는 것이다.