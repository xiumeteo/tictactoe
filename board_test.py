import logging

from pytest import raises

from game import Game, Move, InvalidMoveException, MoveCompleted, human, computer, noone, Minimax, Choice

LOGGER = logging.getLogger(__name__)

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

def test_Game_determine_winner_comp():

    computer_winner = [
        list("XXX______"), list("___XXX___"), list("______XXX"),
        list("X__X__X__"), list("_X__X__X_"), list("__X__X__X"),
        list("X___X___X"), list("__X_X_X__")
    ]

    for case in computer_winner:
        game = Game(case)
        assert game.determine_winner() == computer

def test_Game_determine_winner_hum():

    human_winner = [
        list("OOO______"), list("___OOO___"), list("______OOO"),
        list("O__O__O__"), list("_O__O__O_"), list("__O__O__O"),
        list("O___O___O"), list("__O_O_O__")
    ]

    for case in human_winner:
        game = Game(case)
        assert game.determine_winner() == human

def test_Game_determine_winner_none():

    noone_winner = [
        list("OXO______"), list("___OXO___"), list("______XOO"),
        list("O__X__O__"), list("_O__O__X_"), list("__O__X__O"),
        list("X___O___O"), list("__O_O_X__")
    ]

    for case in noone_winner:
        game = Game(case)
        assert game.determine_winner() == noone

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
    game = Game(list("_O_"
                     "OX_"
                     "XOX"))
    #computer
    minimax = Minimax(game, computer)
    choice = minimax.do()
    game.move(choice.move.move_initiated)
    #human
    h_move = game.get_available_slots()[0]
    game.move(Move(human, h_move))

    assert game.is_done()
    assert game.determine_winner() == computer


def test_Minimax_game_from_zero_human_starts():
    game = Game(list("_________"))

    player = computer
    while not game.is_done():
        if player == computer:
            minimax = Minimax(game, computer)
            choice = minimax.do()
            LOGGER.info(choice)
            game.move(choice.move.move_initiated)
            player = human
        else:
            slots = game.get_available_slots()
            if not slots: break
            h_move = slots[0]
            game.move(Move(human, h_move))
            player = computer

        LOGGER.info(game)

    assert game.is_done()
    assert game.determine_winner() == computer
