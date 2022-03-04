import numpy as np
import random

board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
player_mark = ''
computer_mark = ''
move_num = 0
state = [n for n in range(0, 9)]
# np.save('data.npy',{})
experience = np.load('data.npy', allow_pickle='TRUE').item()
for key in experience:
    experience[key].sort(reverse=True, key=lambda a: (a[1], len(a[0])))


# print(experience)


def choice_mark():
    global player_mark
    player_mark = random.choice(['X', 'O'])


def choice_move(board):
    free_moves = [m for row in board for m in row if str(m).isdigit()]

    move = random.choice(free_moves)
    # print(move)
    for row in board:
        for i in range(len(row)):
            if row[i] == move:
                row[i] = player_mark


def computer_mark_choice():
    global computer_mark
    computer_mark = 'O' if player_mark == 'X' else 'X'


def check_player_moves(board, mark):
    r_c_d_board = [board[0], board[1], board[2], [board[0][0], board[1][0], board[2][0]],
                   [board[0][1], board[1][1], board[2][1]], [board[0][2], board[1][2], board[2][2]],
                   [board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]
    for r_c_d in r_c_d_board:
        count = 0
        index = ''
        for x in r_c_d:
            if x == mark:
                count += 1
            elif str(x).isdigit():
                index = x
        if count == 2 and str(index).isdigit():
            return index


def check_computer_moves(board, mark):
    r_c_d_board = [board[0], board[1], board[2], [board[0][0], board[1][0], board[2][0]],
                   [board[0][1], board[1][1], board[2][1]], [board[0][2], board[1][2], board[2][2]],
                   [board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]
    for r_c_d in r_c_d_board:
        count = 0
        index = ''
        for x in r_c_d:
            if x == mark:
                count += 1
            elif str(x).isdigit():
                index = x
        if count == 2 and str(index).isdigit():
            return index


def computer_choice_move(board):
    move = ""
    free_moves = [m for row in board for m in row if str(m).isdigit()]
    if state in experience and len(experience[state]) > 0:
        # print(state)
        # print(experience[state][0])
        for i in range(len(experience[state][0][0])):
            if experience[state][0][0][i] in free_moves:
                move = experience[state][0][0][i]
                break
    if check_player_moves(board, player_mark) in free_moves:
        move = check_player_moves(board, player_mark)
    if check_computer_moves(board, computer_mark) in free_moves:
        move = check_computer_moves(board, computer_mark)
    if move == "":
        move = random.choice(free_moves)
    for row in board:
        for i in range(len(row)):
            if row[i] == move:
                row[i] = computer_mark


def check_winner(mark, board):
    first_row = all([x == mark for x in board[0]])
    second_row = all([x == mark for x in board[1]])
    third_row = all([x == mark for x in board[2]])
    first_column = all([x == mark for x in [board[0][0], board[1][0], board[2][0]]])
    second_column = all([x == mark for x in [board[0][1], board[1][1], board[2][1]]])
    third_column = all([x == mark for x in [board[0][2], board[1][2], board[2][2]]])
    first_diagonal = all([x == mark for x in [board[0][0], board[1][1], board[2][2]]])
    second_diagonal = all([x == mark for x in [board[0][2], board[1][1], board[2][0]]])
    if any([first_row, second_row, third_row, first_column, second_column, third_column, first_diagonal,
            second_diagonal]):
        if player_mark == mark:

            return True
        else:
            return True
    elif len([m for row in board for m in row if str(m).isdigit()]) == 0:
        return True


def play(board):
    global move_num
    if player_mark == '':
        choice_mark()
        computer_mark_choice()
    choice_move(board)
    move_num += 1
    states_memory(board, move_num)
    if check_winner(player_mark, board):
        return True
    computer_choice_move(board)
    move_num += 1
    states_memory(board, move_num)
    if check_winner(computer_mark, board):
        return True


def states_memory(board, num):
    global state
    state = list(state)
    # print(state)
    new_board = [m for row in board for m in row]

    for i in range(len(new_board)):
        if (new_board[i] == 'X' or new_board[i] == 'O') and str(state[i]).isdigit():
            state[i] = (new_board[i], num)

    state = tuple(state)
    # print(state)
    if state not in experience:
        experience[state] = []
    # print(experience)


def learning(board):
    win_board = [m for row in board for m in row]
    win_moves = list(state)
    num_moves = []
    mark_X = 0
    mark_O = 0
    for p in win_board:
        if p == 'X':
            mark_X += 1
        elif p == 'O':
            mark_O += 1
    if mark_X > mark_O:
        for i in range(len(win_moves)):
            if isinstance(win_moves[i], tuple):
                mark, move = win_moves[i]
                if mark == 'X':
                    num_moves.append([move, i])
    elif mark_O >= mark_X:
        for i in range(len(win_moves)):

            if isinstance(win_moves[i], tuple):
                mark, move = win_moves[i]
                if mark == 'O':
                    num_moves.append([move, i])
    num_moves.sort(key=lambda a: a[0])
    num_moves = [i[1] for i in num_moves]
    for key in experience:
        for l in experience[key]:
            if l[0] == num_moves and (mark_O + mark_X) < 9:
                l[1] += 1
                break
        experience[key].append([num_moves, 0])
    np.save('data.npy', experience)


for n in range(250):
    if play(board):
        learning(board)
        board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        player_mark = ''
        computer_mark = ''
        move_num = 0
        state = [n for n in range(0, 9)]
        experience = np.load('data.npy', allow_pickle='TRUE').item()
        for key in experience:
            experience[key].sort(reverse=True, key=lambda a: (a[1], len(a[0])))

        print(experience)
