from Game_T_T_T import play, learning
from board import BoardStatus
from experience import Experience

if __name__ == '__main__':
    board = BoardStatus()
    current_exp = {}
    experience = Experience()

    while True:
        if play(board, current_exp, experience):
            learning(board, current_exp, experience)
            break
