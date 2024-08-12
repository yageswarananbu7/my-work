import math

# Define the board
board = [' ' for _ in range(9)]


# Function to print the board
def print_board():
    for row in [board[i * 3:(i + 1) * 3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')


# Function to check for a win
def check_win(player):
    win_patterns = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for pattern in win_patterns:
        if all(board[i] == player for i in pattern):
            return True
    return False


# Function to check for a draw
def check_draw():
    return ' ' not in board


# Function to make a move
def make_move(position, player):
    if board[position] == ' ':
        board[position] = player
        return True
    return False


# Minimax algorithm with Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_win('O'):
        return -10 + depth
    elif check_win('X'):
        return 10 - depth
    elif check_draw():
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval


# Function to find the best move for AI
def best_move():
    best_score = -math.inf
    move = 0
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            score = minimax(board, 0, False, -math.inf, math.inf)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move


# Main game loop
def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print_board()

    while True:
        # Human move
        move = int(input("Enter your move (1-9): ")) - 1
        if make_move(move, 'O'):
            print_board()
            if check_win('O'):
                print("You win!")
                break
            elif check_draw():
                print("It's a draw!")
                break
        else:
            print("Invalid move. Try again.")

        # AI move
        ai_move = best_move()
        make_move(ai_move, 'X')
        print("AI move:")
        print_board()
        if check_win('X'):
            print("AI wins!")
            break
        elif check_draw():
            print("It's a draw!")
            break


if __name__ == "__main__":
    play_game()

