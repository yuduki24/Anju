import pygame
from pygame.locals import *
from loader import load_image, load_font, split_image
from tetrimino import *
import os
import sys
import random

SCR_RECT = Rect(0, 0, 900, 600)
CELL_SIZE = 20
WINDOW_ROW = SCR_RECT.height // CELL_SIZE   # フィールドの行数
WINDOW_COL = SCR_RECT.width // CELL_SIZE  # フィールドの列数

class Tetris:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption(u"Tetris")
        self.load_images()
        self.init_game()

        # メインループ開始
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def init_game(self):
        """ゲームオブジェクトの初期化"""
        self.all = pygame.sprite.RenderUpdates()
        #Tetrimino.containers = self.all
        TetriminoBlock.containers = self.all
        TetriminoBlock.tetrimino_img = self.tetrimino_img
        # デバッグ用.7種類置く
        for color in range(7):
            Tetrimino(40+(5 * color * CELL_SIZE), 60, color)

    def update(self):
        """ゲーム状態の更新"""
        self.all.update()

    def draw(self, screen):
        """描画"""
        screen.fill((10, 10, 10))
        self.all.draw(screen)
        self.draw_grid(screen)

    def draw_grid(self, screen):
        """グリッドの描画(主にデバッグ用)"""
        for y in range(WINDOW_ROW):
            for x in range(WINDOW_COL):
                pygame.draw.rect(screen, (50,50,50), Rect(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE*2,CELL_SIZE*2), 1)
    def key_handler(self):
        """キーハンドラー"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
    def load_images(self):
        """イメージのロード"""
        self.tetrimino_img = split_image(load_image("tetrimino.png"), 7)

class Tetrimino():
    """テトリミノ"""
    TETRIMINO_PATTERN = (TETRIMINO_T, TETRIMINO_L, TETRIMINO_J, TETRIMINO_S, TETRIMINO_Z, TETRIMINO_I, TETRIMINO_O)
    def __init__(self, x, y, color):
        for i in range(len(self.TETRIMINO_PATTERN[color])):
            for j in range(len(self.TETRIMINO_PATTERN[color])):
                print(self.TETRIMINO_PATTERN[color][i][j])
                if self.TETRIMINO_PATTERN[color][i][j] == 1:
                    TetriminoBlock((x+CELL_SIZE*j), (y+CELL_SIZE*i), color)

class TetriminoBlock(pygame.sprite.Sprite):
    """テトリミノを構成する一つ一つのブロック"""
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.tetrimino_img[color]
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

if __name__ == "__main__":
    Tetris()