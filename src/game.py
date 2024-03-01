import pygame

from const import *
from board import Board
from dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                color = LIGHT_GREEN if (row + col) % 2 == 0 else DARK_GREY
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if self.dragger.piece is not piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            for move in self.dragger.piece.moves:
                color = MOVE_LIGHT if (move.final.row + move.final.col) %2 == 0 else MOVE_DARK
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
