from game import Game,Move,InvalidMoveException,MoveCompleted,human,computer,draw,Minimax
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
    assert b.move(m) == MoveCompleted('continue', draw, m)

def test_Minimax_next_move():
    b = Game()
    m  = Minimax(b, human)
    validMoves = set(map(lambda x: ''.join(x.game.board), m.next_moves(b, human)))
    expectedMoves = {"X________" , "_X_______", "__X______", "___X_____", "____X____", "_____X___", "______X__", "_______X_", "________X"}
    assert expectedMoves == validMoves

def test_Minimax_game():
    game = Game()
    game.board = list("OX_"
                   "OXO"
                   "XOX")
    minimax = Minimax(game, computer)
    move = minimax.do()
    print(move)
    assert move == MoveCompleted('continue', computer, Move(computer, 2))


