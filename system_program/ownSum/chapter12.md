computer system 속 예외적 상황을 정리한다.
Interrupt와 exceptions를 구분하는데 집중하자!
여기서 우산 용어로 event로 칭하겠다.
Dual mode.
1. kernel mode : 관리자 모드 생각하면 좋을 것 같다. 많은 권력을 가진다.
2. user mode : 대대분의 권력이 없다. 평민..?
두 mode를 번갈아 가며 실행한다. mode bit를 가지는 CS register에 현재 모드 상태를 저장한다.
현재 x86-64에서는 2개의 비트로 4가지 상태를 가질 수 있고, 0은 커널 모드, 3은 유저 모드이다.
1과 2도 구상 초기에는 안정적으로 사용하기 위해 두었다곤 하는데, 현재는 두개만 사용중이랜다.
어쩌다 kernel mode는 막강한 권력을 가졌는가?
kernel mode에서만 실행 가능한 instruction이 존재한다. ex) cli, sti(interrupt를 clear하거나 set 함), hlt(cpu를 정지시킴), change the mode bit
kernel memory에는 user mode에서 접근이 불가능하다. 위험함!
hardware 접근에도 user mode에서는 불가능하다. 대신 OS를 통해 접근한다.
CPU는 단순하게 보면 정해진 한가지 일만 계속한다. instruction을 fetch -> decode -> excuation PC로 다음 instruction 등록. 이걸 죽을때까지 반복함(전원이 꺼질때까지, 나태지옥이다 거의)
Exceptional Control Flow
지금까지 배운 control flow는 jump나 call 등이다. 이런 것들을 program state라고 부른다. 하지만 아래와 같은 일들도 처리해야 하는데, 이걸 system state라고 부른다.
- system timer generates
- data arrives from a network adapter
이런 것들을 빨리 처리해야 한다는데, 아직은 자세히는 모르겠다. 이 예외 처리 일들을 외부 문제(=interrupt) 또는 내부 문제(=exception)이다.
이런 예외적 일들이 생기면, kernel mode로 전환해서, kernel code를 받는다. 이 event마다 식별코드가 존재하며, 각자 핸들러가 존재한다.
이 일들을 처리하고, 다음 instruction을 수행하거나 다시 이 instruction을 수행하거나, 완전히 중단해버린다.
식별코드를 받았을때 이거에 맞는 코드들이 존재하는 것을 IDT table이라고 부른다.
Interrupt 보통 외부적 일들을 말한다. I/O device 일들이 보통 적용된다. 이 event들은 비동기적이며, 처리가 끝나면 다음 instruction을 진행한다.
Exception도 3가지로 나뉜다. 먼저 Trap은 의도적으로 실행시켜 멈추는 경우가 많다. 디버깅을 생각하면 편하며, 동기적이다. 처리가 끝나면 다음 Instruction을 진행한다. software interrupt라고도 부른다. Interrupt와 헷갈리지 않게 주의하자.
Fault와 Abort는 동기적이며, 내부적으로 문제가 생긴 경우이다. 여기서 둘의 차이는 예외 처리를 진행하고 다시 실행하던 instruction을 재실행하면 falut이며 완전히 프로그램을 끝내버리면 abort이다.