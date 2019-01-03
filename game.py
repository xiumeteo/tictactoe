import logging
from copy import deepcopy

LOGGER = logging.getLogger(__name__)


class Player:
    def __init__(self, piece, value):
        self.piece = piece
        self.value = value

    def __eq__(self, other):
        return self.piece == other.piece and \
               self.value == other.value


human = Player('O', -10)
computer = Player('X', 10)
noone = Player('_', 0)


class InvalidMoveException(Exception):
    def __init__(self, reason, pos):
        self.reason = reason
        self.pos = pos

class Move:
    def __init__(self, player, pos):
        self.player = player
        self.pos = pos

    def is_machine(self):
        return self.player == computer

    def __eq__(self, other):
        return self.player == other.player and \
               self.pos == other.pos

class MoveCompleted:
    def __init__(self, winner, move_initiated):
        self.winner = winner
        self.move_initiated = move_initiated

    def __eq__(self, other):
        return self.winner == other.winner and \
               self.move_initiated == other.move_initiated


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

    @staticmethod
    def __to_value(piece):
        if piece == computer.piece:
            return computer.value
        if piece == human.piece:
            return human.value
        else:
            return noone.value

    def move(self, move):
        if move.pos > 8 or move.pos < 0:
            raise InvalidMoveException("Out of range move", move.pos)
        if self.board[move.pos] is not '_':
            raise InvalidMoveException("Overriding move on: " + self.board[move.pos], move.pos)
        self.board[move.pos] = move.player.piece
        self.board_values[move.pos] = move.player.value
        return MoveCompleted(self.determine_winner(), move)

    def is_done(self):
        winner = self.determine_winner()
        if winner is not noone:
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

    @staticmethod
    def __check_winner(value):
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


class Choice:
    def __init__(self, move, game):
        self.move = move
        self.game = game
        self.sort_index = self.move.winner.value

    def __lt__(self, other):
        return self.sort_index < other.sort_index

    def __gt__(self, other):
        return self.sort_index > other.sort_index


class Minimax:
    def __init__(self, current_game, current_player):
        self.game = current_game
        self.player = current_player

    def get_best_choice(self):
        if self.game.is_empty():
            return Choice(MoveCompleted(noone, Move(self.player, 4)), self.game)
        return self.__get_best_choice(self.game, self.player)

    def __get_best_choice(self, current_game, current_player):
        if current_game.is_done():
            return Choice(MoveCompleted(current_game.determine_winner(), Move(current_player, 0)), current_game)

        valid_choices = self.next_moves(current_game, current_player)

        weighted_choices = []
        for choice in valid_choices:
            # deep_choice is the ultimate value of this branch
            deep_choice = self.__get_best_choice(choice.game, self.next_player(current_player))
            choice.sort_index = deep_choice.sort_index
            weighted_choices.append(choice)

        return self.get_choice_value(weighted_choices, current_player)

    def get_choice_value(self, choices, current_player):
        if current_player == computer:
            return max(choices)
        else:
            return min(choices)

    def next_moves(self, current_game, current_player):
        game_level_copy = deepcopy(current_game)
        valid_moves = []
        for pos in range(len(game_level_copy.board)):
            piece = game_level_copy.board[pos]
            if piece == '_':
                game_with_move = deepcopy(game_level_copy)
                move = game_with_move.move(Move(current_player, pos))
                valid_moves.append(Choice(move, game_with_move))

        return valid_moves

    def next_player(self, current_player):
        if current_player == human:
            next_player = computer
        else:
            next_player = human
        return next_player
