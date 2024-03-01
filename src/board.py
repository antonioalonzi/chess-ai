from const import *
from square import Square
from piece import *
from move import *


class Board:
    def __init__(self):
        self.squares = []

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(COLS)]

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def calc_moves(self, piece, row, col):
        def pawn_moves(piece, row, col):
            pass

        def knight_moves(piece, row, col):
            possible_moves = [
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col + 2),
                (row + 1, col - 2),
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row - 1, col + 2),
                (row - 1, col - 2),
            ]

            for possible_move in possible_moves:
                if Square.in_range(possible_move[0], possible_move[1]):
                    print(possible_move)
                    if self.squares[possible_move[0]][possible_move[1]].is_empty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move[0], possible_move[1])
                        move = Move(initial, final)
                        piece.add_move(move)

        def bishop_moves(piece, row, col):
            pass

        def rook_moves(piece, row, col):
            pass

        def queen_moves(piece, row, col):
            pass

        def king_moves(piece, row, col):
            pass

        if piece.name == 'pawn':
            return pawn_moves(piece, row, col)
        elif piece.name == 'knight':
            return knight_moves(piece, row, col)
        elif piece.name == 'bishop':
            return bishop_moves(piece, row, col)
        elif piece.name == 'rook':
            return rook_moves(piece, row, col)
        elif piece.name == 'queen':
            return queen_moves(piece, row, col)
        elif piece.name == 'king':
            return king_moves(piece, row, col)
