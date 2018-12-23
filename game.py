import logging
from copy import deepcopy
from dataclasses import dataclass, field

LOGGER = logging.getLogger(__name__)

@dataclass
class Player:
    piece: str
    value: int


human = Player('O', -10)
computer = Player('X', 10)
noone = Player('_', 0)


@dataclass
class InvalidMoveException(Exception):
    reason: str
    pos: int


@dataclass
class Move:
    player: Player
    pos: int

    def is_machine(self):
        return self.player == computer


@dataclass
class MoveCompleted:
    winner: Player
    move_initiated: Move


class Game:

    def __init__(self, board=None):
        self.EMPTY_BOARD = "_________"
        if board is None:
            self.board = list(self.EMPTY_BOARD)
            self.board_values = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            self.board = board
            self.board_values = list(map(self.__to_value, self.board))

        self.winner_row_positions = [(0, 3), (3, 6), (6, 9)]
        self.winner_column_positions = [(0, 3, 6), (1, 4, 7), (2, 5, 8)]
        self.winner_diag_positions = [(0, 4, 8), (2, 4, 6)]

    def __to_value(self, piece):
        if piece == computer.piece:
            return computer.value
        if piece == human.piece:
            return human.value
        else:
            return noone.value

    def move(self, move):
        # if self.is_done():
        #     LOGGER.error("entering to its done")
        #     return
        if move.pos > 8 or move.pos < 0:
            raise InvalidMoveException("Out of range move", move.pos)
        if self.board[move.pos] is not '_':
            raise InvalidMoveException("Overriding move on: " + self.board[move.pos], move.pos)
        self.board[move.pos] = move.player.piece
        self.board_values[move.pos] = move.player.value
        return MoveCompleted(self.determine_winner(), move)

    def is_done(self):
        winner = self.determine_winner()
        if winner is computer or winner is human:
            return True
        return not set(self.board).issuperset({'_'})

    def determine_winner(self):
        for x, y in self.winner_row_positions:
            total = sum(self.board_values[x:y])
            winner = self.__check_winner(total)
            if winner != noone:
                return winner

        for x, y, z in self.winner_column_positions:
            total = self.board_values[x] + \
                    self.board_values[y] + \
                    self.board_values[z]
            winner = self.__check_winner(total)
            if winner != noone:
                return winner

        for x, y, z in self.winner_diag_positions:
            total = self.board_values[x] + \
                    self.board_values[y] + \
                    self.board_values[z]
            winner = self.__check_winner(total)
            if winner != noone:
                return winner

        return noone

    def __check_winner(self, value):
        if value == computer.value * 3:
            return computer
        if value == human.value * 3:
            return human
        return noone

    def get_available_slots(self):
        slots = []
        for i, item in enumerate(self.board_values):
            if item == 0:
                slots.append(i)
        return slots

    def is_empty(self):
        return self.board == list(self.EMPTY_BOARD)

    def __repr__(self):
        return ''.join(self.board)


@dataclass
class Choice:
    sort_index: int = field(init=False, repr=False)
    move: MoveCompleted
    game: Game

    def __post_init__(self):
        self.sort_index = self.move.winner.value

    def __lt__(self, other):
        return self.sort_index < other.sort_index

    def __gt__(self, other):
        return self.sort_index > other.sort_index


class Minimax:
    def __init__(self, currentBoard, currentPlayer):
        self.game = currentBoard
        self.player = currentPlayer

    def do(self):
        if self.game.is_empty():
            return Choice(MoveCompleted(noone, Move(self.player, 4)), self.game)
        return self.__deep(self.game, self.player)

    def __deep(self, current_board, current_player):
        if current_board.is_done():
            return Choice(MoveCompleted(current_board.determine_winner(), Move(current_player, 0)), current_board)

        choices = self.next_moves(current_board, current_player)

        evaluated_choices = []
        for choice in choices:
            # deep_choice is the ultimate value of this branch
            deep_choice = self.__deep(choice.game, self.next_player(current_player))
            choice.sort_index = deep_choice.sort_index
            evaluated_choices.append(choice)

        return self.get_best_choice(evaluated_choices)

    def get_best_choice(self, choices):
        if self.player == computer:
            return max(choices)
        else:
            return min(choices)

    def next_moves(self, current_board, current_player):
        board = deepcopy(current_board)
        valid_moves = []
        for pos in range(len(board.board)):
            piece = board.board[pos]
            if piece == '_':
                futureBoard = deepcopy(board)
                move = futureBoard.move(Move(current_player, pos))
                valid_moves.append(Choice(move, futureBoard))

        return valid_moves

    def next_player(self, currentPlayer):
        if currentPlayer == human:
            nextPlayer = computer
        else:
            nextPlayer = human
        return nextPlayer
