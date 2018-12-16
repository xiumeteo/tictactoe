from dataclasses import dataclass

@dataclass 
class InvalidMoveException(Exception):
    reason: str
    pos:int


@dataclass
class Move:
    player:str
    pos:int

    def is_machine(self):
        return player == 'X'

@dataclass
class MoveCompleted:
    status:str
    winner:str

class Board:
    win_pos = {'XXX______', '___XXX___', '_____XXX', 
            'X__X__X__', '_X__X__X_', '__X__X__X',
            'X___X___X', '__X_X_X__'}
    los_pos = {'OOO______', '___OOO___', '_____OOO', 
            'O__O__O__', '_O__O__O_', '__O__O__O',
            'O___O___O', '__O_O_O__'}    

    def __init__(self):
         self.board = list("_________")
    
    def move(self, move):
        if move.pos > 8 or move.pos < 0:
            raise InvalidMoveException("Out of range move", move.pos)
        if self.board[move.pos] is not '_':
            raise InvalidMoveException("Overriding move on: " + self.board[move.pos], move.pos)
        self.board[move.pos] = move.player
        return MoveCompleted('continue', self.__determine_winner())

    def __determine_winner(self):
        string_board = {''.join(self.board)}
        if self.win_pos.issuperset(string_board):
            return 'X'
        if self.los_pos.issuperset(string_board):
            return 'O'

        return ''
