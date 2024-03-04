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
        self.last_move = None

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

    def move(self, piece, move):
        self.squares[move.initial.row][move.initial.col].piece = None
        self.squares[move.final.row][move.final.col].piece = piece
        piece.moved = True
        if piece.name == 'pawn':
            self.check_promotion(piece, move.final)
        if piece.name == 'king' and self.castling(move.initial, move.final):
            diff = move.final.col - move.initial.col
            rook = piece.left_rook if diff < 0 else piece.right_rook
            self.move(rook, rook.moves[-1])
        piece.clear_moves()
        self.last_move = move

    def valid_moves(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def calc_moves(self, piece, row, col):
        def pawn_moves(piece, row, col):
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (steps + 1))

            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        break
                else:
                    break

            possible_move_row = row + piece.dir
            possible_move_cols = [col -1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

            # TODO on passant

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
                    if self.squares[possible_move[0]][possible_move[1]].is_empty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move[0], possible_move[1])
                        move = Move(initial, final)
                        piece.add_move(move)

        def straightline_moves(piece, row, col, incrs):
            for incr in incrs:
                possible_move_row = row + incr[0]
                possible_move_col = col + incr[1]

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)

                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            piece.add_move(move)
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    else:
                        break

                    possible_move_row += incr[0]
                    possible_move_col += incr[1]

        def bishop_moves(piece, row, col):
            straightline_moves(piece, row, col, [(-1, +1), (-1, -1), (+1, +1), (+1, -1)])

        def rook_moves(piece, row, col):
            straightline_moves(piece, row, col, [(-1, 0), (+1, 0), (0, +1), (0, -1)])

        def queen_moves(piece, row, col):
            straightline_moves(piece, row, col, [(-1, 0), (+1, 0), (0, +1), (0, -1), (-1, +1), (-1, -1), (+1, +1), (+1, -1)])

        def king_moves(piece, row, col):
            adjs = [
                (row-1, col-1),
                (row-1, col),
                (row-1, col+1),
                (row, col-1),
                (row, col+1),
                (row+1, col-1),
                (row+1, col),
                (row+1, col+1)
            ]

            for possible_move in adjs:
                if Square.in_range(possible_move[0], possible_move[1]):
                    if self.squares[possible_move[0]][possible_move[1]].is_empty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move[0], possible_move[1])
                        move = Move(initial, final)
                        piece.add_move(move)

            if not piece.moved:
                left_rook = self.squares[row][0].piece
                right_rook = self.squares[row][0].piece
                if left_rook.name == 'rook' and not left_rook.moved:
                    if self.squares[row][1].is_empty() and self.squares[row][2].is_empty() and self.squares[row][3].is_empty():
                        piece.left_rook = left_rook
                        initial = Square(row, 0)
                        final = Square(row, 3)
                        move = Move(initial, final)
                        left_rook.add_move(move)

                        piece.left_rook = left_rook
                        initial = Square(row, col)
                        final = Square(row, 2)
                        move = Move(initial, final)
                        piece.add_move(move)

                if right_rook.name == 'rook' and not right_rook.moved:
                    if self.squares[row][5].is_empty() and self.squares[row][6].is_empty():
                        piece.right_rook = left_rook
                        initial = Square(row, 7)
                        final = Square(row, 5)
                        move = Move(initial, final)
                        left_rook.add_move(move)

                        piece.right_rook = left_rook
                        initial = Square(row, col)
                        final = Square(row, 6)
                        move = Move(initial, final)
                        piece.add_move(move)

        if piece.name == 'pawn':
            pawn_moves(piece, row, col)
        elif piece.name == 'knight':
            knight_moves(piece, row, col)
        elif piece.name == 'bishop':
            bishop_moves(piece, row, col)
        elif piece.name == 'rook':
            rook_moves(piece, row, col)
        elif piece.name == 'queen':
            queen_moves(piece, row, col)
        elif piece.name == 'king':
            king_moves(piece, row, col)
