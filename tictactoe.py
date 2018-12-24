#!/usr/bin/env python3

import traceback

from game import Game, Minimax, Move, human, computer


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class UiBoard:
    def __init__(self):
        self.ui_board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.game = Game()

    def move(self, pos, player):
        mc = self.game.move(Move(player, pos))
        if mc is not None:
            self.ui_board[pos] = player.piece

    def computer_move(self):
        minimax = Minimax(self.game, computer)
        choice = minimax.get_best_choice()
        pos = choice.move.move_initiated.pos
        self.move(pos, computer)
        return pos

    def check_winner(self):
        winner = self.game.determine_winner()
        if winner == computer:
            return "I win!, ha ha ha you will never beat robots!"
        if winner == human:
            return "Did you win? There must be a mistake in my programming"
        else:
            return "Draw!, We robots recognize an awesome opponent but I will beat you next time!"

    def __repr__(self):
        value = ""
        for i, item in enumerate(self.ui_board):
            if item is computer.piece:
                value = value + bcolors.WARNING + str(item) + bcolors.ENDC + " \t"
            elif item is human.piece:
                value = value + bcolors.OKBLUE + str(item) + bcolors.ENDC + " \t"
            else:
                value = value + str(item) + " \t"

            if i is 2 or i is 5 or i is 8:
                value = value + "\n"
        return value

def main():
    print("Tictactoe...")
    print("Do your moves with numbers between 1 and 9, you're 'O' ")
    ui_board = UiBoard()
    print(ui_board)
    player = human
    while not ui_board.game.is_done():
        if player == computer:
            print("My turn... I move...")
            pos = ui_board.computer_move()
            print("I choose " + str(pos + 1))
            player = human
        else:
            h_move = int(input("Your move:")) - 1
            try:
                ui_board.move(h_move, human)
                player = computer
            except Exception as e:
                print("Uh oh, something went wrong: " + str(e))
                print(traceback.format_exc())

        print(ui_board)

    print(ui_board.check_winner())
    print("Goodbye!")


if __name__ == "__main__":
    main()
