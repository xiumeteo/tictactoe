from dataclasses import dataclass, field
from copy import deepcopy

@dataclass
class Player:
    piece:str
    value:int

human = Player('O', -10)
computer = Player('X', 10)
draw = Player('_', 0)

@dataclass 
class InvalidMoveException(Exception):
    reason: str
    pos:int


@dataclass
class Move:
    player:Player
    pos:int

    def is_machine(self):
        return self.player == computer

@dataclass
class MoveCompleted:
    status:str
    winner:Player
    move:Move

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
        self.board[move.pos] = move.player.piece
        return MoveCompleted('continue', self.determine_winner(), move)

    def is_done(self):
        return not set(self.board).issuperset({'_'})

    def determine_winner(self):
        string_board = {''.join(self.board)}
        if self.win_pos.issuperset(string_board):
            return computer
        if self.los_pos.issuperset(string_board):
            return human
        return draw

@dataclass(order=True)
class Choice:
    sort_index: int = field(init=False, repr=False)
    move:MoveCompleted
    board:Board

    def __post_init__(self):
        self.sort_index = self.move.winner.value

class Minimax:
    def __init__(self, currentBoard, currentPlayer):
        self.currentBoard = currentBoard
        self.current_player = currentPlayer

    def do(self):
        return self.__deep(self.currentBoard, self.current_player)

    def __deep(self, currentBoard, currentPlayer):
        if currentBoard.is_done():
            return currentBoard.determine_winner()

        #here we create the track of scores and positions
        moves = self.next_moves(currentBoard, currentPlayer)
        for move,board in moves:
            moves.extend(self.__deep(board, move.player))

        if self.current_player == computer:
            #maximize
            return max(moves)
        else :
            return min(moves)


    def next_moves(self, current_board, current_player):
        nextPlayer = self.next_player(current_player)

        board = deepcopy(current_board)
        valid_moves = []
        for pos in range(len(board.board)):
            piece = board.board[pos]
            if piece == '_':
                futureBoard = deepcopy(board)
                move = futureBoard.move(Move(nextPlayer, pos))
                valid_moves.append(Choice(move, futureBoard))

        return valid_moves

    def next_player(self, currentPlayer):
        if currentPlayer == human:
            nextPlayer = computer
        else:
            nextPlayer = human
        return nextPlayer

