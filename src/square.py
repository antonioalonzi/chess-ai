from const import *


class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def has_piece(self):
        return self.piece is not None

    def is_empty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def is_empty_or_rival(self, color):
        return self.is_empty() or self.has_rival_piece(color)

    @staticmethod
    def in_range(x, y):
        return 0 <= x < ROWS and 0 <= y < COLS
