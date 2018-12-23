from board import Board,Move, InvalidMoveException,MoveCompleted,human,computer,draw,Minimax
from pytest import raises

def test_blank_board():
    b = Board()
    assert ''.join(b.board) == '_________'

def test_outside_of_range_move():
    b = Board()
    m = Move('X', 10)
    with raises(InvalidMoveException):
        b.move(m)

def test_below_of_range_move():
    b = Board()
    m = Move('X', -1)
    with raises(InvalidMoveException):
        b.move(m)

def test_override_move_not_allowed():
    b = Board()
    m = Move('X', 5)
    b.move(m)
    with raises(InvalidMoveException):
        b.move(m)

def test_valid_move():
    b = Board()
    m = Move('X', 5)
    assert b.move(m) == MoveCompleted('continue', draw)

def test_Minimax_next_move():
    b = Board()
    m  = Minimax(b, human)
    validMoves = set(map(lambda x: ''.join(x[1].board), m.next_moves()))
    expectedMoves = {"X________" , "_X_______", "__X______", "___X_____", "____X____", "_____X___", "______X__", "_______X_", "________X"}
    assert expectedMoves == validMoves


