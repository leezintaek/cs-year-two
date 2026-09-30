import random  # 무작위 전략(Random)을 위해 random 모듈을 불러온다

# 승리로 이어지는 모든 라인(가로 3, 세로 3, 대각선 2)을 미리 정의한다 (C++: vector<tuple<int,int,int>>에 대응)
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 가로 세 줄
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 세로 세 줄
    (0, 4, 8), (2, 4, 6),             # 대각선 두 줄
]

PLAYER_MARK = 'X'  # 사용자의 기호는 'X'로 고정한다
BOT_MARK = 'O'  # 봇의 기호는 'O'로 고정한다


def print_reference_board():  # 게임 시작 전, 위치 번호를 안내하기 위한 보드를 출력하는 함수
    print()  # 위쪽 여백을 위한 빈 줄 출력
    print(" 1 | 2 | 3 ")  # 1~3번 칸을 출력
    print("---+---+---")  # 가로 구분선 출력
    print(" 4 | 5 | 6 ")  # 4~6번 칸을 출력
    print("---+---+---")  # 가로 구분선 출력
    print(" 7 | 8 | 9 ")  # 7~9번 칸을 출력
    print()  # 아래쪽 여백을 위한 빈 줄 출력
    print("=" * 36)  # 턴 구분을 위한 긴 구분선 출력
    print()  # 구분선 아래 여백 출력


def print_board(board):  # 현재 보드 상태(빈칸/표시)를 출력하는 함수
    print()  # 위쪽 여백 출력
    print(f" {board[0]} | {board[1]} | {board[2]} ")  # 1행(0,1,2 인덱스) 출력 (C++: std::format/printf와 유사한 문자열 삽입)
    print("---+---+---")  # 가로 구분선 출력
    print(f" {board[3]} | {board[4]} | {board[5]} ")  # 2행(3,4,5 인덱스) 출력
    print("---+---+---")  # 가로 구분선 출력
    print(f" {board[6]} | {board[7]} | {board[8]} ")  # 3행(6,7,8 인덱스) 출력
    print()  # 아래쪽 여백 출력
    print("=" * 36)  # 턴 구분을 위한 긴 구분선 출력
    print()  # 구분선 아래 여백 출력


def get_empty_positions(board):  # 비어있는 칸의 인덱스 목록을 반환하는 함수
    return [i for i in range(9) if board[i] == ' ']  # 공백인 칸의 인덱스만 리스트로 반환 (C++: for문+push_back을 한 줄로 축약한 리스트 컴프리헨션)


def check_winner(board):  # 현재 보드에서 승자가 있는지 확인하는 함수
    for a, b, c in WIN_LINES:  # 미리 정의한 모든 승리 라인을 순회 (C++: 구조체 분해 대입, C++엔 없는 튜플 언패킹)
        if board[a] != ' ' and board[a] == board[b] == board[c]:  # 세 칸이 모두 같은 기호이면 (C++: a==b && b==c로 풀어써야 함, Python은 체이닝 비교 지원)
            return board[a]  # 해당 기호(승자)를 반환
    return None  # 승자가 없으면 None을 반환


def is_draw(board):  # 무승부인지 확인하는 함수
    return ' ' not in board  # 빈 칸이 하나도 없으면 무승부로 판단


def minimax(board, turn):  # BOT은 최대화, PLAYER는 최소화하는 재귀 함수
    winner = check_winner(board)  # 현재 보드의 승자를 확인
    if winner == BOT_MARK:  # 봇이 이겼다면
        return 1  # +1 점수를 반환
    if winner == PLAYER_MARK:  # 사용자가 이겼다면
        return -1  # -1 점수를 반환
    if is_draw(board):  # 무승부라면
        return 0  # 0점을 반환

    if turn == BOT_MARK:  # 봇의 차례(최대화)라면
        best_score = float('-inf')  # 최댓값 초기화(음의 무한대) (C++: -INFINITY 또는 INT_MIN에 대응)
        for pos in get_empty_positions(board):  # 비어있는 모든 칸에 대해
            board[pos] = BOT_MARK  # 임시로 봇의 기호를 놓는다 (C++: vector<char>&로 참조 전달과 동일 — Python 리스트는 기본 참조 전달)
            score = minimax(board, PLAYER_MARK)  # 다음은 사용자 차례로 재귀 호출
            board[pos] = ' '  # 놓았던 기호를 되돌린다(백트래킹)
            best_score = max(best_score, score)  # 더 큰 점수로 갱신
        return best_score  # 최댓값을 반환
    else:  # 사용자의 차례(최소화)라면
        best_score = float('inf')  # 최솟값 초기화(양의 무한대) (C++: INFINITY 또는 INT_MAX에 대응)
        for pos in get_empty_positions(board):  # 비어있는 모든 칸에 대해
            board[pos] = PLAYER_MARK  # 임시로 사용자의 기호를 놓는다
            score = minimax(board, BOT_MARK)  # 다음은 봇 차례로 재귀 호출
            board[pos] = ' '  # 놓았던 기호를 되돌린다(백트래킹)
            best_score = min(best_score, score)  # 더 작은 점수로 갱신
        return best_score  # 최솟값을 반환


def bot_move_minimax(board):  # Minimax 전략으로 봇의 다음 수를 결정하는 함수
    best_score = float('-inf')  # 최댓값 초기화(음의 무한대) (C++: -INFINITY 또는 INT_MIN에 대응)
    best_pos = None  # 최선의 위치를 저장할 변수 초기화 (C++: nullptr/std::nullopt에 대응)
    for pos in get_empty_positions(board):  # 비어있는 모든 칸에 대해
        board[pos] = BOT_MARK  # 임시로 봇의 기호를 놓는다
        score = minimax(board, PLAYER_MARK)  # 그 수를 둔 뒤 사용자 차례로 평가
        board[pos] = ' '  # 놓았던 기호를 되돌린다(백트래킹)
        if score > best_score:  # 지금까지 중 가장 높은 점수라면
            best_score = score  # 최댓값을 갱신
            best_pos = pos  # 최선의 위치를 갱신
    return best_pos  # 최종 선택한 위치를 반환


def bot_move_random(board):  # Random 전략으로 봇의 다음 수를 결정하는 함수
    return random.choice(get_empty_positions(board))  # 비어있는 칸 중 하나를 무작위로 선택


def bot_move_left_up(board):  # Left-up first 전략으로 봇의 다음 수를 결정하는 함수
    return min(get_empty_positions(board))  # 비어있는 칸 중 가장 작은 번호(왼쪽 위 우선)를 선택


def get_bot_position(board, strategy):  # 선택된 전략에 따라 봇의 위치를 계산하는 함수
    if strategy == 1:  # 전략 1(Minimax)이 선택되었다면 (C++: 함수 포인터/std::function 없이 함수를 바로 호출 — Python 함수는 일급 객체)
        return bot_move_minimax(board)  # Minimax 함수를 호출하여 위치 반환
    if strategy == 2:  # 전략 2(Random)가 선택되었다면
        return bot_move_random(board)  # Random 함수를 호출하여 위치 반환
    return bot_move_left_up(board)  # 그 외(전략 3, Left-up first)는 해당 함수를 호출하여 위치 반환


def choose_strategy():  # 게임 시작 시 봇 전략을 입력받는 함수
    print("AI Bot Strategies:")  # 전략 목록 제목 출력
    print("(1) Minimax Search")  # 전략 1 설명 출력
    print("(2) Random")  # 전략 2 설명 출력
    print("(3) Left-up First (Smaller Number First)")  # 전략 3 설명 출력
    print()  # 여백을 위한 빈 줄 출력
    while True:  # 올바른 값이 입력될 때까지 반복
        raw = input("Please select an option (1-3): ")  # 전략 번호를 입력받는다
        if raw in ('1', '2', '3'):  # 입력값이 1,2,3 중 하나라면
            return int(raw)  # 정수로 변환하여 반환
        print("... Wrong number")  # 잘못된 입력이면 안내 메시지 출력


def get_player_position(board):  # 사용자로부터 유효한 위치를 입력받는 함수
    while True:  # 올바른 값이 입력될 때까지 반복
        raw = input("Your turn (1-9): ")  # 사용자에게 위치를 입력받는다
        if not raw.isdigit():  # 입력이 숫자가 아니라면 (C++: cin>>n의 자동 형변환 없음 — input()은 항상 string 반환)
            print("... Wrong number")  # 잘못된 입력 메시지 출력
            continue  # 다시 입력받기 위해 반복문 처음으로
        pos = int(raw)  # 입력값을 정수로 변환
        if pos < 1 or pos > 9:  # 1~9 범위를 벗어난다면
            print("... Wrong number")  # 잘못된 입력 메시지 출력
            continue  # 다시 입력받기 위해 반복문 처음으로
        if board[pos - 1] != ' ':  # 이미 채워진 칸이라면
            print("... Unavailable")  # 사용 불가 메시지 출력
            continue  # 다시 입력받기 위해 반복문 처음으로
        return pos - 1  # 유효한 위치(0-based 인덱스)를 반환


def play_game():  # 전체 게임을 진행하는 메인 함수
    strategy = choose_strategy()  # 봇 전략을 선택받는다
    print()  # 여백을 위한 빈 줄 출력
    print("You 'X' vs. Bot 'O'")  # 선공/기호 안내 문구 출력
    print_reference_board()  # 위치 번호 안내용 보드를 출력

    board = [' '] * 9  # 실제 게임 보드를 9칸 빈칸으로 초기화

    while True:  # 게임이 끝날 때까지 반복
        pos = get_player_position(board)  # 사용자의 유효한 위치를 입력받는다
        board[pos] = PLAYER_MARK  # 사용자의 기호를 보드에 놓는다
        print_board(board)  # 갱신된 보드를 출력

        winner = check_winner(board)  # 사용자가 방금 둔 수로 승자가 결정됐는지 확인
        if winner == PLAYER_MARK:  # 사용자가 이겼다면
            print("You Win!")  # 승리 메시지 출력
            return  # 게임 종료
        if is_draw(board):  # 무승부라면
            print("Draw!")  # 무승부 메시지 출력
            return  # 게임 종료

        bot_pos = get_bot_position(board, strategy)  # 선택된 전략으로 봇의 위치를 계산
        print(f"Bot's turn (1-9): {bot_pos + 1}")  # 봇이 선택한 위치를 출력(1-based로 변환)
        board[bot_pos] = BOT_MARK  # 봇의 기호를 보드에 놓는다
        print_board(board)  # 갱신된 보드를 출력

        winner = check_winner(board)  # 봇이 방금 둔 수로 승자가 결정됐는지 확인
        if winner == BOT_MARK:  # 봇이 이겼다면
            print("Bot Wins!")  # 봇 승리 메시지 출력
            return  # 게임 종료
        if is_draw(board):  # 무승부라면
            print("Draw!")  # 무승부 메시지 출력
            return  # 게임 종료


if __name__ == "__main__":  # 이 파일이 직접 실행될 때만 아래 코드를 실행 (C++: int main()과 같은 진입점 역할)
    play_game()  # 게임을 시작한다
