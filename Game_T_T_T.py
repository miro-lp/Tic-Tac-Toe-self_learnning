import random
from board import BoardStatus
from experience import Experience


def check_moves(board, mark):
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


def computer_choice_move(board: BoardStatus, experience: Experience):
    move = ""
    free_moves = [m for row in board.board for m in row if str(m).isdigit()]
    exp_move = experience.move(board.state, free_moves)
    if exp_move in [n for n in range(0, 9)]:
        move = exp_move
    player_move = check_moves(board.board, board.player_mark)
    if player_move in free_moves:
        move = player_move
    computer_move = check_moves(board.board, board.computer_mark)
    if computer_move in free_moves:
        move = computer_move
    if move == "":
        move = random.choice(free_moves)
    return move


def check_winner(mark, board: BoardStatus):
    first_row = all([x == mark for x in board.board[0]])
    second_row = all([x == mark for x in board.board[1]])
    third_row = all([x == mark for x in board.board[2]])
    first_column = all([x == mark for x in [board.board[0][0], board.board[1][0], board.board[2][0]]])
    second_column = all([x == mark for x in [board.board[0][1], board.board[1][1], board.board[2][1]]])
    third_column = all([x == mark for x in [board.board[0][2], board.board[1][2], board.board[2][2]]])
    first_diagonal = all([x == mark for x in [board.board[0][0], board.board[1][1], board.board[2][2]]])
    second_diagonal = all([x == mark for x in [board.board[0][2], board.board[1][1], board.board[2][0]]])
    if any([first_row, second_row, third_row, first_column, second_column, third_column, first_diagonal,
            second_diagonal]):
        if board.player_mark == mark:
            board.win_mark = mark
            board.is_winner = True
            print('Player won!')
            board.display_board()
            return True
        else:
            board.win_mark = mark
            board.is_winner = True
            print('Computer won!')
            board.display_board()
            return True
    elif len([m for row in board.board for m in row if str(m).isdigit()]) == 0:
        print('No winner!')
        board.display_board()
        return True


def play(board: BoardStatus, current_exp, experience):
    if board.player_mark == '':
        board.display_choice_mark()
        board.computer_mark_choice()
    board.display_board()
    move = board.display_choice_move()
    board.change_status_board(move, board.player_mark)
    board.move_num += 1
    board.states_memory(current_exp)
    if check_winner(board.player_mark, board):
        return True
    move = computer_choice_move(board, experience)
    board.change_status_board(move, board.computer_mark)
    board.move_num += 1
    board.states_memory(current_exp)
    if check_winner(board.computer_mark, board):
        return True


def learning(board: BoardStatus, current_exp, experience: Experience):
    if board.is_winner:
        win_moves = list(board.state)
        num_moves = []

        for i in range(len(win_moves)):
            if isinstance(win_moves[i], tuple):
                mark, move = win_moves[i]
                if mark == board.win_mark:
                    num_moves.append([move, i])

        num_moves.sort(key=lambda a: a[0])
        num_moves = [i[1] for i in num_moves]
        for key in current_exp:
            current_exp[key].append([num_moves, 0])
        experience.safe(current_exp, num_moves)
