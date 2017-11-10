import pygame
from pygame.locals import *
from loader import load_image, load_font, split_image
from tetrimino import *
import os
import sys
import random

SCR_RECT = Rect(0, 0, 900, 600)
CELL_SIZE = 20
WINDOW_ROW = SCR_RECT.height // CELL_SIZE
WINDOW_COL = SCR_RECT.width // CELL_SIZE
FIELD_ROW = 20
FIELD_COL = 10
FIELD_TOP = 80
FIELD_LEFT = 80
LEFT, RIGHT = -1, 1
class Tetris:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption(u"Tetris")
        self.load_images()
        self.init_game(screen)

        # メインループ開始
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def init_game(self, screen):
        """ゲームオブジェクトの初期化"""
        self.all = pygame.sprite.RenderUpdates()
        Block.containers = self.all

        Tetrimino.tetrimino_img = self.tetrimino_img
        Field.image = self.wall_img
        Field.screen = screen

        Field()
        self.acctive_tetriminos = []
        # デバッグ用.7種類置く
        for color in range(7):
            self.acctive_tetriminos.append(Tetrimino(40+(5 * color * CELL_SIZE), 60, color))

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
            elif event.type == KEYDOWN and event.key == K_SPACE:
                for n in range(7):
                    self.acctive_tetriminos[n].spin(RIGHT)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                for n in range(7):
                    self.acctive_tetriminos[n].move(RIGHT)
            elif event.type == KEYDOWN and event.key == K_LEFT:
                for n in range(7):
                    self.acctive_tetriminos[n].move(LEFT)
    def load_images(self):
        """イメージのロード"""
        self.tetrimino_img = split_image(load_image("tetrimino.png"), 7)
        self.wall_img = load_image("wall.png")

class Tetrimino():
    TETRIMINO_KIND = ((TETRIMINO_T1, TETRIMINO_T2, TETRIMINO_T3, TETRIMINO_T4), \
                      (TETRIMINO_L1, TETRIMINO_L2, TETRIMINO_L3, TETRIMINO_L4), \
                      (TETRIMINO_J1, TETRIMINO_J2, TETRIMINO_J3, TETRIMINO_J4), \
                      (TETRIMINO_Z1, TETRIMINO_Z2), (TETRIMINO_S1, TETRIMINO_S2), \
                      (TETRIMINO_I1, TETRIMINO_I2), (TETRIMINO_O1, ) )
    def __init__(self, x, y, color):
        self.PATTERN = self.TETRIMINO_KIND[color]
        self.PATTERN_COUNT = len(self.PATTERN)
        self.pattern_number = 0
        self.current_pattern = self.PATTERN[self.pattern_number]
        print(self.current_pattern)
        self.block_row = len(self.current_pattern)
        self.block_col = len(self.current_pattern[0])
        self.x = x
        self.y = y
        self.blocks = []
        for i in range(self.block_row):
            for j in range(self.block_col):
                if self.current_pattern[i][j] == 1:
                    self.blocks.append(Block((x+CELL_SIZE*j), (y+CELL_SIZE*i), self.tetrimino_img[color]))
    def spin(self, direction):
        # ただただ回転させるコード.
        # next_pattern = [[0 for i in range(self.block_row)] for j in range(self.block_col)]
        # for i in range(self.block_row):
        #     for j in range(self.block_col):
        #         if direction == RIGHT:
        #             next_pattern[j][self.block_row-1-i] = self.pattern[i][j]
        #         elif firection == LEFT:
        #             next_pattern[self.block_col-1-j][i] = self.pattern[i][j]
        if direction == RIGHT:
            self.pattern_number += 1
        elif direction == LEFT:
            self.pattern_number -= 1
        next_pattern = self.PATTERN[self.pattern_number % self.PATTERN_COUNT]

        # [TODO]next_patternがblock_fieldとかぶっていないか調べる.

        self.current_pattern = next_pattern
        self.block_row = len(self.current_pattern)
        self.block_col = len(self.current_pattern[0])
        self.__update()

    def move(self, direction):
        if direction == RIGHT:
            self.x += CELL_SIZE
        elif direction == LEFT:
            self.x -= CELL_SIZE
        self.__update()

    def __update(self):
        # 無理やり...
        num = 0
        for i in range(self.block_row):
            for j in range(self.block_col):
                if self.current_pattern[i][j] == 1:
                    self.blocks[num].set_position((self.x+CELL_SIZE*j), (self.y+CELL_SIZE*i))
                    num += 1

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
    def set_position(self, x, y):
        self.rect.left = x
        self.rect.top = y

class Field():
    def __init__(self):
        # 描画用と実際にブロックを置く用の2つ用意.
        # 周りの壁用に+2する.
        self.image_field = [[0 for i in range(FIELD_COL+2)] for j in range(FIELD_ROW+2)]
        self.block_field = self.image_field[:][:]

        # 両端を埋める.
        for row in range(FIELD_ROW+2):
            self.image_field[row][0] = -1
            self.image_field[row][FIELD_COL+1] = -1
            self.block_field[row][0] = -1
            self.block_field[row][FIELD_COL+1] = -1
        # 底を埋める.
        # image_fieldは天井も埋める.
        for col in range(FIELD_COL+2):
            self.image_field[FIELD_ROW+1][col] = -1
            self.image_field[0][col] = -1
            self.block_field[FIELD_ROW+1][col] = -1

        for y in range(FIELD_ROW+2):
            for x in range(FIELD_COL+2):
                if self.image_field[y][x] == -1:
                     self.block_field[y][x] = Block(x*CELL_SIZE+FIELD_TOP,  y*CELL_SIZE+FIELD_LEFT, self.image)

    def update(self):
        for y in range(FIELD_ROW):
            for x in range(FIELD_COL):
                if [image_field][y][x] == -1:
                     #self.screen.blit(self.image, (x*CELL_SIZE+FIELD_TOP,  y*CELL_SIZE+FIELD_LEFT))
                     self.screen.blit(self.image, (x*CELL_SIZE,  y*CELL_SIZE))

if __name__ == "__main__":
    Tetris()
