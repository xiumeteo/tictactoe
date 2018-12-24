#!/usr/bin/env python3

from game import Game, Minimax, Move, human, computer


def main():
    print("Tictactoe...")
    print("Do your moves with numbers between 1 and 9, you're 'O' ")
    game = Game()
    print(game)
    player = human
    while not game.is_done():
        if player == computer:
            minimax = Minimax(game, computer)
            choice = minimax.get_best_choice()
            game.move(choice.move.move_initiated)
            player = human
        else:
            h_move = int(input()) -1
            game.move(Move(human, h_move))
            player = computer

        print(game)


if __name__ == "__main__":
    main()
