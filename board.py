class BoardStatus:
    def __init__(self):
        self.board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.player_mark = ''
        self.computer_mark = ''
        self.move_num = 0
        self.state = [n for n in range(0, 9)]
        self.is_winner = False
        self.win_mark = ''

    def display_board(self):
        """Display current position of all moves"""

        for i in range(len(self.board)):
            print(f' {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}')
            if i < 2:
                print('---+---+---')

    def display_choice_mark(self):
        """Display mark choice and save it"""

        while True:
            mark = input('Make choice between O and X: ')
            if mark == 'O' or mark == 'X':
                break
        self.player_mark = mark

    def change_status_board(self, move, mark):
        for row in self.board:
            for i in range(len(row)):
                if row[i] == move:
                    row[i] = mark

    def display_choice_move(self):
        """Display all possible moves"""

        free_moves = [m for row in self.board for m in row if str(m).isdigit()]

        while True:
            move = input(f'Make your choice between {", ".join(map(str, free_moves))}: ')
            if move.isdigit() and int(move) in range(0, 9):
                move = int(move)
            if move in free_moves:
                break
        return move

    def computer_mark_choice(self):
        self.computer_mark = 'O' if self.player_mark == 'X' else 'X'

    def states_memory(self, experience):
        state = list(self.state)
        new_board = [m for row in self.board for m in row]

        for i in range(len(new_board)):
            if (new_board[i] == 'X' or new_board[i] == 'O') and str(self.state[i]).isdigit():
                state[i] = (new_board[i], self.move_num)

        self.state = tuple(state)
        if self.state not in experience:
            experience[self.state] = []
