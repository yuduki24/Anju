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
# 枠用に+2する.
FIELD_ROW = 20 + 2
FIELD_COL = 10 + 2
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

        self.field1 = Field(4, 4)
        self.acctive_tetriminos = []
        self.debug_count = 1
        # デバッグ用.7種類置く
        for color in range(self.debug_count):
            self.acctive_tetriminos.append(Tetrimino(color, self.field1))

    def update(self):
        """ゲーム状態の更新"""
        self.field1.update()
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
                for n in range(self.debug_count):
                    self.acctive_tetriminos[n].spin(RIGHT)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                for n in range(self.debug_count):
                    self.acctive_tetriminos[n].move(RIGHT)
            elif event.type == KEYDOWN and event.key == K_LEFT:
                for n in range(self.debug_count):
                    self.acctive_tetriminos[n].move(LEFT)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                for n in range(self.debug_count):
                    self.acctive_tetriminos[n].fixPosition()
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
    TETRIMINO_TYPE = {0:"T", 1:"L", 2:"J", 3:"Z", 4:"S", 5:"I", 6:"O"}
    def __init__(self, color, field):
        self.PATTERN = self.TETRIMINO_KIND[color]
        self.PATTERN_COUNT = len(self.PATTERN)
        self.pattern_number = 0
        self.current_pattern = self.PATTERN[self.pattern_number]
        self.field = field
        self.block_row = len(self.current_pattern)
        self.block_col = len(self.current_pattern[0])
        self.x, self.y = self.getFastPosition(self.TETRIMINO_TYPE[color])
        self.blocks = []
        for i in range(self.block_row):
            for j in range(self.block_col):
                if self.current_pattern[i][j] == 1:
                    self.blocks.append(Block((self.x+j+self.field.LEFT), (self.y+i+self.field.TOP), self.tetrimino_img[color]))
    def getFastPosition(self, teto_type):
        if teto_type in {"T", "L", "J", "Z", "S", "I"}:
            return 4, 0
        elif teto_type == "O":
            return 3, 0
        else:
            return 0, 0
    def spin(self, direction):
        # ただただ回転させるコード.
        # next_pattern = [[0 for i in range(self.block_row)] for j in range(self.block_col)]
        # for i in range(self.block_row):
        #     for j in range(self.block_col):
        #         if direction == RIGHT:
        #             next_pattern[j][self.block_row-1-i] = self.pattern[i][j]
        #         elif firection == LEFT:
        #             next_pattern[self.block_col-1-j][i] = self.pattern[i][j]
        next_pattern_number = self.pattern_number
        if direction == RIGHT:
            next_pattern_number += 1
        elif direction == LEFT:
            next_pattern_number -= 1
        next_pattern = self.PATTERN[next_pattern_number % self.PATTERN_COUNT]

        # [TODO]next_patternがblock_fieldとかぶっていないか調べる.
        if not self.checkMovable(self.x, self.y, next_pattern):
            return

        self.current_pattern = next_pattern
        self.pattern_number = next_pattern_number
        self.block_row = len(self.current_pattern)
        self.block_col = len(self.current_pattern[0])
        self.__update()

    def move(self, direction):
        if direction == RIGHT:
            if self.checkMovable(self.x + 1, self.y, self.current_pattern):
                self.x += 1
        elif direction == LEFT:
            if self.checkMovable(self.x - 1, self.y, self.current_pattern):
                self.x -= 1
        self.__update()

    def fixPosition(self):
        self.field.setTetrimino(self.x, self.y, self.current_pattern)
    def __update(self):
        # 無理やり...
        num = 0
        for i in range(self.block_row):
            for j in range(self.block_col):
                if self.current_pattern[i][j] == 1:
                    self.blocks[num].set_position((self.x+j+self.field.LEFT), (self.y+i+self.field.TOP),)
                    num += 1
    
    def checkMovable(self, x, y, next_pattern):
        return self.field.checkEmpty(x, y, next_pattern)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = x * CELL_SIZE
        self.rect.top = y * CELL_SIZE
    def set_position(self, x, y):
        self.rect.left = x * CELL_SIZE
        self.rect.top = y * CELL_SIZE

class Field():
    def __init__(self, top, left):
        # 描画用と実際にブロックを置く用の2つ用意.
        self.image_field = [[0 for i in range(FIELD_COL)] for j in range(FIELD_ROW)]
        self.block_field = [[0 for i in range(FIELD_COL)] for j in range(FIELD_ROW)]
        self.TOP = top
        self.LEFT = left
        # 両端を埋める.
        for row in range(FIELD_ROW):
            self.image_field[row][0] = -1
            self.image_field[row][FIELD_COL-1] = -1
            self.block_field[row][0] = -1
            self.block_field[row][FIELD_COL-1] = -1
        # 底を埋める.
        # image_fieldは天井も埋める.
        for col in range(FIELD_COL):
            self.image_field[FIELD_ROW-1][col] = -1
            self.image_field[0][col] = -1
            self.block_field[FIELD_ROW-1][col] = -1

        # 枠だけは初めに描画.
        for y in range(FIELD_ROW):
            for x in range(FIELD_COL):
                if self.image_field[y][x] == -1:
                     Block(x+self.TOP, y+self.LEFT, self.image)

    def update(self):
        for y in range(FIELD_ROW):
            for x in range(FIELD_COL):
                # image_fieldの値に応じて、tetrimino_imgを配置
                if self.image_field[y][x] == 1 and self.block_field[y][x] == 0:
                    
                    #self.screen.blit(self.image, (x*CELL_SIZE+FIELD_TOP,  y*CELL_SIZE+FIELD_LEFT))
                    #self.screen.blit(self.image, ((x+self,TOP)*CELL_SIZE, (y+self.LEFT)*CELL_SIZE))
                    self.block_field[y][x] = Block(x+self.TOP, y+self.LEFT, self.image)

    def checkEmpty(self, x, y, pattern):
        row = len(pattern)
        col = len(pattern[0])
        for i in range(row):
            for j in range(col):
                if pattern[i][j] == 1 and self.block_field[y+i][x+j] != 0:
                    return False
        return True
    
    def setTetrimino(self, x, y, pattern):
        
        while self.checkEmpty(x, y+1, pattern):
            print("offset")
            y +=1
        row = len(pattern)
        col = len(pattern[0])
        for i in range(row):
            for j in range(col):
                if pattern[i][j] == 1:
                    print("set")
                    self.image_field[y+i][x+j] = 1

if __name__ == "__main__":
    Tetris()
