import random
from Game_T_T_T import learning, check_moves, check_winner, computer_choice_move
from board import BoardStatus
from experience import Experience


def choice_move(board: BoardStatus):
    free_moves = [m for row in board.board for m in row if str(m).isdigit()]
    move = ''
    computer_move = check_moves(board.board, board.computer_mark)
    if computer_move in free_moves:
        move = computer_move
    player_move = check_moves(board.board, board.player_mark)
    if player_move in free_moves:
        move = player_move
    if move == "":
        move = random.choice(free_moves)

    board.change_status_board(move, board.player_mark)
    return move


def play_self(board: BoardStatus, current_exp, experience):
    if board.player_mark == '':
        board.player_mark = random.choice(['X', 'O'])
        board.computer_mark = 'O' if board.player_mark == 'X' else 'X'
    move = choice_move(board)
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


if __name__ == '__main__':
    board = BoardStatus()
    current_exp = {}
    experience = Experience()

    for n in range(250):
        if play_self(board, current_exp, experience):
            learning(board, current_exp, experience)
            # for i in experience:
            #     print(i)
            #     print(experience[i])
            board = BoardStatus()
            current_exp = {}
            experience = Experience()
