#!/usr/bin/env python3

import traceback

from game import computer, human
from ui import CliBoard


def main():
    print("Tictactoe...")
    print("Do your moves with numbers between 1 and 9, you're 'O' ")
    ui_board = CliBoard()
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
