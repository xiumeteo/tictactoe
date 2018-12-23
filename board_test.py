from game import Game,Move,InvalidMoveException,MoveCompleted,human,computer,noone,Minimax,Choice
from pytest import raises

def test_blank_board():
    b = Game()
    assert ''.join(b.board) == '_________'

def test_outside_of_range_move():
    b = Game()
    m = Move(computer, 10)
    with raises(InvalidMoveException):
        b.move(m)

def test_below_of_range_move():
    b = Game()
    m = Move(computer, -1)
    with raises(InvalidMoveException):
        b.move(m)

def test_override_move_not_allowed():
    b = Game()
    m = Move(computer, 5)
    b.move(m)
    with raises(InvalidMoveException):
        b.move(m)

def test_valid_move():
    b = Game()
    m = Move(computer, 5)
    assert b.move(m) == MoveCompleted(noone, m)

def test_Minimax_next_move():
    b = Game()
    m = Minimax(b, human)
    validMoves = set(map(lambda x: ''.join(x.game.board), m.next_moves(b, computer)))
    expectedMoves = {"X________" , "_X_______", "__X______", "___X_____", "____X____", "_____X___", "______X__", "_______X_", "________X"}
    assert expectedMoves == validMoves

def test_Game_determine_winner():
    game = Game(list("OXX"
                     "OXO"
                     "XOX"))
    assert game.determine_winner() == computer

def test_Minimax_game_almost_complete():
    game = Game(list("OX_"
                     "OXO"
                     "XOX"))
    print("initial game = ", game)
    minimax = Minimax(game, computer)
    choice = minimax.do()
    print(choice)
    assert choice.move == MoveCompleted(computer, Move(computer, 2))

def test_Choice_ordering():
    computer_choice = Choice(MoveCompleted(computer, Move(computer, 5)), Game())
    human_choice = Choice(MoveCompleted(human, Move(human, 5)), Game())
    noone_choice = Choice(MoveCompleted(noone, Move(computer, 5)), Game())
    choices = [computer_choice, human_choice, noone_choice]

    assert max(choices) == computer_choice
    assert min(choices) == human_choice

def test_Minimax_game_incomplete():
    game = Game(list("_X_"
                     "OX_"
                     "XOX"))
    #human asks for move
    minimax = Minimax(game, computer)
    choice = minimax.do()
    game.move(choice.move.move_initiated)
    #human
    h_move = game.get_available_slots()[0]
    game.move(Move(human, h_move))
    #computer
    minimax = Minimax(game, computer)
    choice = minimax.do()
    game.move(choice.move.move_initiated)

    assert game.is_done()
    assert game.determine_winner() == computer


