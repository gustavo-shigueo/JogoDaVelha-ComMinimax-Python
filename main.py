import os
import time

# Show board
def show_board():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("Mapa do tabuleiro:")
    print(" 1 | 2 | 3 ")
    print("-----------")
    print(" 4 | 5 | 6 ")
    print("-----------")
    print(" 7 | 8 | 9 ")
    print("")
    
    print("Jogo:")
    print(" " + board[0][0] + " | " + board[0][1] + " | " + board[0][2] + " ")
    print("-----------")
    print(" " + board[1][0] + " | " + board[1][1] + " | " + board[1][2] + " ")
    print("-----------")
    print(" " + board[2][0] + " | " + board[2][1] + " | " + board[2][2] + " ")

# Check win
def check_win():
    global winner

    # Checking rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            winner = board[i][0]            

    # Checking columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != " ":
            winner = board[0][i]

    # Checking diagonals
    diagonal_1 = board[0][0] == board[1][1] == board[2][2] != " "
    diagonal_2 = board[0][2] == board[1][1] == board[2][0] != " "
    if diagonal_1 or diagonal_2:
        winner = board[1][1]

    return winner != None

# Check Tie or Check End
def check_game_over():
    global winner

    # Check for win
    if check_win(): return True

    # Check for tie 
    tie = True
    for i in range(3):
        if " " in board[i]: tie = False

    winner = "Tie!" if tie else None
    return tie

# Human player movement
def human_move():
    global current_player

    move = None
    while move not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        move = input("Digite um número: ")
    move = int(move)
    i = move - 1
    j = int((move - 1) / 3)

    if j == 1: i -= 3
    elif j == 2: i -= 6

    if board[j][i] != " ": human_move()
    else: board[j][i] = current_player

    os.system('cls' if os.name == 'nt' else 'clear')


# Find ideal move for the AI
def best_move():
    global board
    global bestMove

    depth = 0

    for k in range(3):
        for l in range(3): 
            if board[k][l] == " ": depth += 1

    bestScore = float("-inf")
    for i in range(9):
        row = int(i / 3)
        col = i % 3
        if board[row][col] != " ": continue
        board[row][col] = ai
        score = minimax(depth, False, float("-inf"), float("inf"))
        board[row][col] = " "
        bestScore = max(score, bestScore)
        if score >= bestScore: bestMove = [row, col]


# Minimax Algorithm
def minimax(depth, isMaximizing, alpha, beta):
    global winner
    global scores
    global board

    result = check_game_over()
    if result or depth == 0:
        r = scores[winner]
        if depth >= 2: r *= depth
        winner = None
        result = False
        return r

    if isMaximizing:
        bestScore = float("-inf")
        for i in range(9):
            row = int(i / 3)
            col = i % 3
            if board[row][col] != " ": continue
            board[row][col] = ai
            score = minimax(depth - 1, False, alpha, beta)
            board[row][col] = " "
            bestScore = max(score, bestScore)
            alpha = max(score, alpha)
            if beta <= alpha: break
        return bestScore
    else:
        bestScore = float("inf")
        for i in range(9):
            row = int(i / 3)
            col = i % 3
            if board[row][col] != " ": continue
            board[row][col] = human
            score = minimax(depth - 1, True, alpha, beta)
            board[row][col] = " "
            bestScore = min(score, bestScore)
            beta = min(score, beta)
            if beta <= alpha: break
        return bestScore


# Start game
while True:
    board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    bestMove = []
    human = "X"
    ai = "O"
    scores = {
        "X": -1,
        'O': 1,
        "Tie!": 0
    }
    current_player = human
    winner = None

    # Play
    while check_game_over() == False:
        show_board()
        if current_player == human:
            human_move()
            current_player = ai
        else:
            best_move()
            board[bestMove[0]][bestMove[1]] = ai
            winner = None
            current_player = human

    show_board()
    print("")

    print(winner + (" wins!" if winner != "Tie!" else ""))
    time.sleep(3)
