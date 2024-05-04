import numpy as np


class Environment:

    def __init__(self):
        self.board = np.zeros((3, 3))
        self.x = -1
        self.o = 1
        self.winner = None
        self.ended = False

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def game_over(self):
        for i in range(3):
            if sum(self.board[i, :]) == 3 or sum(self.board[i, :]) == -3:
                self.winner = self.o if sum(self.board[i, :]) == 3 else self.x
                self.ended = True
                return True

        for j in range(3):
            if sum(self.board[:, j]) == 3 or sum(self.board[:, j]) == -3:
                self.winner = self.o if sum(self.board[:, j]) == 3 else self.x
                self.ended = True
                return True

        if np.abs(np.trace(self.board)) == 3 or np.abs(np.trace(np.fliplr(self.board))) == 3:
            self.winner = self.o if np.trace(self.board) == 3 else self.x
            self.ended = True
            return True

        if np.all(self.board != 0):
            self.ended = True
            return True

        return False

    def draw_board(self):
        print("   0 1 2")
        for i in range(3):
            print(f"{i} |{'|'.join(['X' if self.board[i, j] == self.x else 'O' if self.board[i, j] == self.o else ' ' for j in range(3)])}|")
        print()


class HumanPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def take_action(self, env):
        while True:
            move = input(f"Player '{self.symbol}': Enter the row and column numbers (0-2) separated by comma: ")
            try:
                i, j = map(int, move.split(','))
                if 0 <= i <= 2 and 0 <= j <= 2 and env.is_empty(i, j):
                    env.board[i, j] = self.symbol
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter row and column numbers separated by comma.")


class TicTacToe:
    def __init__(self):
        self.env = Environment()
        self.player_x = HumanPlayer(-1)
        self.player_o = HumanPlayer(1)

    def play(self):
        print("Welcome to Tic Tac Toe!")
        print("The board is represented as follows:")
        print("   0 1 2")
        print("0 | | | |")
        print("1 | | | |")
        print("2 | | | |")
        print("Players will input the row and column numbers (0-2) separated by comma.")

        current_player = self.player_x
        while not self.env.game_over():
            self.env.draw_board()
            current_player.take_action(self.env)
            current_player = self.player_o if current_player == self.player_x else self.player_x

        self.env.draw_board()
        if self.env.winner:
            print(f"Player '{'X' if self.env.winner == -1 else 'O'}' wins!")
        else:
            print("It's a draw!")


if __name__ == "__main__":
    game = TicTacToe()
    game.play()
