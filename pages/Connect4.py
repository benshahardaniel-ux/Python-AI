import time

import streamlit as st
import random
import copy

from PIL.ImageChops import offset

ROWS = 6
COLS = 7

PLAYER = "🔵"
COMPUTER = "🔴"
EMPTY = "⚪"

#moves = 3

if "moves" not in st.session_state:
    st.session_state.moves = 3

with st.sidebar:
    st.text(f"Player {PLAYER}")
    st.text(f"Computer {COMPUTER}")

    st.divider()

    moves = st.slider(
        label="Difficulty",
        min_value=1,
        max_value=5,
        value=st.session_state.moves,
    )

def minimax(board_copy,move_number,current_player, alpha, beta):
    computer_score = calc_board(board_copy,COMPUTER)
    user_score = calc_board(board_copy,PLAYER)

    big_number = 999999999
    if computer_score > 10000:
        return big_number
    if user_score > 10000:
        return -big_number

    all_cols = available_cols(board_copy)
    if all_cols == []:
        return 0

    if move_number == 0:
        return computer_score

    if current_player == PLAYER:
        best_score = -big_number
        for col in all_cols:
            new_copy_board = virtual_board(board_copy, COMPUTER, col)
            col_score = minimax(new_copy_board,move_number-1,PLAYER, alpha, beta)
            if best_score < col_score:
                best_score = col_score
            if alpha < best_score:
                alpha = best_score
            if alpha >= beta:
                break
        return best_score
    else:
        worst_score = big_number
        for col in all_cols:
            new_copy_board = virtual_board(board_copy, PLAYER, col)
            col_score = minimax(new_copy_board,move_number-1,COMPUTER, alpha, beta)
            if col_score < worst_score:
                worst_score = col_score
        return worst_score




def virtual_board(board,player,col):
    copy_board = copy.deepcopy(board)
    for i in range(ROWS - 1, -1, -1):
        if copy_board[i][col] == EMPTY:
            copy_board[i][col] = player
            break
    return copy_board

def get_best_col(board,player):
    valid_cols = available_cols(board)
    best_col = -1
    best_score = -9999999999

    scores = ["-"] * COLS

    for c in valid_cols:
        temp_board = virtual_board(board,player,c)
        #col_score = calc_board(temp_board,player)
        col_score = minimax(temp_board,moves -1, PLAYER if player == COMPUTER else COMPUTER, -999999, 999999)
        scores[c] = col_score
        if col_score > best_score:
            best_score = col_score
            best_col = c

    st.session_state.scores = scores
    return best_col


def newBoard():
    board = []
    for r in range(ROWS):
        row = []
        for cell in range(COLS):
            row.append(EMPTY)
        board.append(row)
    return board

if "board" not in st.session_state:
    st.session_state.board = newBoard()

board = st.session_state.board

if "turn" not in st.session_state:
    st.session_state.turn = PLAYER

turn = st.session_state.turn

def switchTurn():
    if st.session_state.turn == PLAYER:
        st.session_state.turn = COMPUTER
    else:
        st.session_state.turn = PLAYER

def available_cols(board):
    cols = []
    for c in range(COLS):
        if board[0][c] == EMPTY:
            cols.append(c)
    return cols

def calculate_score(range4, good):
    if good == PLAYER:
        bad = COMPUTER
    else:
        bad = PLAYER

    score = 0

    if range4.count(good) == 1:
        score += 50000
    elif range4.count(good) == 3 and range4.count(EMPTY) == 1:
        score += 100
    elif range4.count(good) == 3 and range4.count(EMPTY) == 2:
        score += 10

    if range4.count(bad) == 4:
        score -= 50000
    elif range4.count(bad) == 3 and range4.count(EMPTY) == 1:
        score -= 500
    elif range4.count(bad) == 2 and range4.count(EMPTY) == 2:
        score -= 50

    #print(range4, good, score)
    return score

def calc_board(board, good):
    score = 0

    for r in range(ROWS):
        row = board[r]
        for c in range(COLS-3):
            range4 = row[c:c+4]
            score += calculate_score(range4, good)

    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS-3):
            range4 = col[r:r+4]
            score += calculate_score(range4, good)

    for r in range(ROWS-3):
        for c in range(COLS-3):
            range4 = [board[r+i][c+i] for i in range(4)]
            score += calculate_score(range4, good)
            range4 = [board[r+3-i][c+i] for i in range(4)]
            score += calculate_score(range4, good)


    middle_col_number = COLS // 2
    middle_col = [board[r][middle_col_number] for r in range(ROWS)]
    score += middle_col.count(good) * 5

    right_col = [board[r][middle_col_number + 1] for r in range(ROWS)]
    score += right_col.count(good) * 2

    left_col = [board[r][middle_col_number - 1] for r in range(ROWS)]
    score += left_col.count(good) * 2

    return score

#print(calc_board(board,turn),turn)


def checkWinner(check_row, check_col):
    row = check_row
    for cell in range(COLS-3):
        if board[row][cell] == EMPTY:
            continue
        for i in range(cell, cell+4):
            if board[row][i] != board[row][cell]:
                print(f"No Win starts with row {row}, cell {cell}")
                break
        else:
            print("Won")
            #print(board[row][cell])
            return board[row][cell]

    col = check_col
    for cell in range(ROWS-3):
        if board[cell][col] == EMPTY:
            continue
        for i in range(cell, cell+4):
            if board[i][col] != board[cell][col]:
                print(f"No Win starts with row {col}, cell {cell}")
                break
        else:
            print("Won")
            #print(board[cell][col])
            return board[cell][col]

        offset = min(check_row, check_col)
        start_row = check_row - offset
        start_col = check_col - offset

        if start_row + 4 > ROWS or start_col + 4 > COLS:
            print("no win")
        else:
            count = 0
            for i in range(ROWS):
                row = start_row + i
                col = start_col + i

                print(f"start checking: {row} {col}")

                if col == COLS or row == ROWS:
                    break
                elif board[row][col] == EMPTY:
                    count = 0
                elif board[row][col] != board[check_row][check_col]:
                    count = 0
                else:
                    count += 1
                if count == 4:
                    print("win")
                    #print(board[row][col])
                    return board[row][col]

    dist_bottom = ROWS -1 - check_row
    dist_left = check_col
    offset = min(dist_left, dist_bottom)

    start_row = check_row - offset
    start_col = check_col - offset

    if start_row + 4 > ROWS or start_col + 4 > COLS:
        print("no win")
    else:
        count = 0
        for i in range(ROWS):
            row = start_row - i
            col = start_col + i
            print(f"start checking: {row} {col}")
            if col == COLS or row == ROWS:
                break
            elif board[row][col] == EMPTY:
                count = 0
            elif board[row][col] != board[check_row][check_col]:
                count = 0
            else:
                count += 1
            if count == 4:
                print("win")
                #print(board[row][col])
                return board[row][col]
    return None

def click(col):
    if board[0][col] != EMPTY:
        return

    #st.write(col)
    for i in range(ROWS -1, -1, -1):
        if board[i][col] == EMPTY:
            board[i][col] = turn
            st.session_state.winner = checkWinner(i, col)
            break
    #board[0][col] = PLAYER
    st.session_state.board = board
    #checkWinner()
    switchTurn()
    st.rerun()

def computerTurn():
    time.sleep(1)
    # randomCol = random.randint(0, COLS-1)
    # click(randomCol)
    best_col = get_best_col(board,COMPUTER)
    click(best_col)


winner = None
if "winner" in st.session_state:
    winner = st.session_state.winner

can_play = True

#print(available_cols(board))

def resetGame():
    if st.button("New Game"):
        st.session_state.winner = None
        st.session_state.scores = [0] * COLS
        st.session_state.board = newBoard()
        st.session_state.turn = PLAYER
        st.rerun()

if winner == PLAYER:
    st.info("player won!")
    can_play = False
    resetGame()
    st.balloons()
elif winner == COMPUTER:
    st.info("computer won!")
    can_play = False
    resetGame()
elif available_cols(board) == []:
    st.info("draw")
    can_play = False
    resetGame()
else:
    if turn == PLAYER:
        st.info("player's turn")
    else:
        st.status("computer thinking")


if "scores" not in st.session_state:
    st.session_state.scores = [0] * COLS

scores = st.session_state.scores
print(scores)


for r in range(ROWS):
    columns = st.columns(COLS)
    for c in range(COLS):
        with columns[c]:
            cell = board[r][c]
            if st.button(cell, key=f"row_{r}_col{c}", use_container_width=True, disabled = turn == COMPUTER or not can_play):
                click(c)


columns = st.columns(COLS)
for c in range(COLS):
    with columns[c]:
        col_score = scores[c]
        if col_score == 0 or col_score == "-":
            st.badge(str(col_score), color="gray")
        elif col_score < 0:
            st.badge(str(col_score), color="red")
        else:
            st.badge(str(col_score), color="green")



if turn == COMPUTER and can_play:
    computerTurn()
