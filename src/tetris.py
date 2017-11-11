import pygame
from pygame.locals import *
from loader import load_image, load_font, split_image
from tetrimino import *
import os
import sys
import random
import time

SCR_RECT = Rect(0, 0, 900, 600)
CELL_SIZE = 20
WINDOW_ROW = SCR_RECT.height // CELL_SIZE
WINDOW_COL = SCR_RECT.width // CELL_SIZE
# 枠用に+2する.
FIELD_ROW = 20 + 2
FIELD_COL = 10 + 2
LEFT, RIGHT = -1, 1

NEXT_POS = (16, 4)
NEXT_NEXT_POS = (16, 8)
NEXT_NEXT_NEXT_POS = (16, 12)

TETRIMINO_KIND = ((TETRIMINO_T1, TETRIMINO_T2, TETRIMINO_T3, TETRIMINO_T4), \
                      (TETRIMINO_L1, TETRIMINO_L2, TETRIMINO_L3, TETRIMINO_L4), \
                      (TETRIMINO_J1, TETRIMINO_J2, TETRIMINO_J3, TETRIMINO_J4), \
                      (TETRIMINO_Z1, TETRIMINO_Z2), (TETRIMINO_S1, TETRIMINO_S2), \
                      (TETRIMINO_I1, TETRIMINO_I2), (TETRIMINO_O1, ) )
TETRIMINO_TYPE = {0:"T", 1:"L", 2:"J", 3:"Z", 4:"S", 5:"I", 6:"O"}

PLAY, END = 0, 1
GameStatus = PLAY
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
            if GameStatus == END:
                screen.fill((200, 110, 10))
                title_font = pygame.font.SysFont(None, 100)
                title = title_font.render("owariWWWWWWW", False, (0,234,234))
                screen.blit(title, ((SCR_RECT.width-title.get_width())/2, 200))
                time = title_font.render(str(self.result), False, (0,234,234))
                screen.blit(time, ((SCR_RECT.width-title.get_width())/2, 350))

            elif GameStatus == PLAY:
                self.update()
                self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def init_game(self, screen):
        """ゲームオブジェクトの初期化"""
        self.all = pygame.sprite.RenderUpdates()
        Block.containers = self.all

        Tetrimino.tetrimino_img = self.tetrimino_img
        Field.wall_img = self.wall_img
        Field.tetrimino_img = self.tetrimino_img
        Field.screen = screen

        self.field1 = Field(4, 4)
        self.stime = time.time()
        self.next_next_next = random.randint(0,6)
        self.next_next = random.randint(0,6)
        self.next = random.randint(0,6)
        self.acctive_tetrimino = Tetrimino(random.randint(0,6), self.field1)
        self.next_blocks = []
    
    def nextTetrimino(self):
        self.acctive_tetrimino = Tetrimino(self.next, self.field1)
        self.next = self.next_next
        self.next_next = self.next_next_next
        self.next_next_next = random.randint(0,6)

    def nextsDraw(self):
        for block in self.next_blocks:
            block.kill()
        self.drawBlock(self.next, NEXT_POS)
        self.drawBlock(self.next_next, NEXT_NEXT_POS)
        self.drawBlock(self.next_next_next, NEXT_NEXT_NEXT_POS)
    
    def drawBlock(self, color, pos):
        x, y = pos
        pattern = TETRIMINO_KIND[color][0]
        block_row = len(pattern)
        block_col = len(pattern[0])
        for i in range(block_row):
            for j in range(block_col):
                if pattern[i][j] == 1:
                    self.next_blocks.append(Block(x+j, y+i, self.tetrimino_img[color]))
        
    def update(self):
        """ゲーム状態の更新"""
        self.field1.update()
        self.all.update()

    def draw(self, screen):
        """描画"""
        screen.fill((10, 10, 10))
        self.all.draw(screen)
        self.draw_grid(screen)
        self.nextsDraw()
        self.result = time.time() - self.stime
        title_font = pygame.font.SysFont(None, 100)
        title = title_font.render(str(self.result), False, (0,234,234))
        screen.blit(title, ((SCR_RECT.width-title.get_width())/2, 200))

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
            elif event.type == KEYDOWN and event.key == K_x:
                self.acctive_tetrimino.spin(LEFT)
            elif event.type == KEYDOWN and event.key == K_c:
                self.acctive_tetrimino.spin(RIGHT)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                self.acctive_tetrimino.move(RIGHT)
            elif event.type == KEYDOWN and event.key == K_LEFT:
                self.acctive_tetrimino.move(LEFT)
            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.acctive_tetrimino.fixPosition()
                self.nextTetrimino()
    def load_images(self):
        """イメージのロード"""
        self.tetrimino_img = split_image(load_image("tetrimino.png"), 7)
        self.wall_img = load_image("wall.png")

class Tetrimino():
    def __init__(self, color, field):
        self.PATTERN = TETRIMINO_KIND[color]
        self.PATTERN_COUNT = len(self.PATTERN)
        self.pattern_number = 0
        self.current_pattern = self.PATTERN[self.pattern_number]
        self.field = field
        self.block_row = len(self.current_pattern)
        self.block_col = len(self.current_pattern[0])
        self.x, self.y = 4, 0
        self.color = color
        self.blocks = []
        for i in range(self.block_row):
            for j in range(self.block_col):
                if not self.checkMovable(self.x, self.y, self.current_pattern):
                    print("end")
                    global GameStatus
                    GameStatus = END
                    return
                if self.current_pattern[i][j] == 1:
                    self.blocks.append(Block((self.x+j+self.field.LEFT), (self.y+i+self.field.TOP), self.tetrimino_img[color]))

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
            next_pattern_number = self.pattern_number + 1
        elif direction == LEFT:
            next_pattern_number = self.pattern_number - 1
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
        self.field.setTetrimino(self.x, self.y, self.current_pattern, self.blocks)

    def __update(self):
        # 無理やり...
        num = 0
        for i in range(self.block_row):
            for j in range(self.block_col):
                if self.current_pattern[i][j] == 1:
                    self.blocks[num].set_position((self.x+j+self.field.LEFT), (self.y+i+self.field.TOP),)
                    num += 1
    
    def checkMovable(self, x, y, pattern):
        return self.field.checkEmpty(x, y, pattern)

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
        self.block_field = [[0 for i in range(FIELD_COL)] for j in range(FIELD_ROW)]
        self.TOP = top
        self.LEFT = left
        # 枠を埋める.
        for row in range(FIELD_ROW):
            self.block_field[row][0] = Block(self.LEFT, self.TOP+row, self.wall_img)
            self.block_field[row][FIELD_COL-1] = Block(self.LEFT+FIELD_COL-1, self.TOP+row,  self.wall_img)
            if row == 0:
                for col in range(FIELD_COL):
                    # 一番上は描画はするが、フィールドには保存しない.
                    Block(col+self.LEFT, row+self.TOP, self.wall_img)
            if row == FIELD_ROW-1:
                for col in range(FIELD_COL):
                    self.block_field[row][col] = Block(col+self.LEFT, row+self.TOP, self.wall_img)

        print(self.block_field)

    def update(self):
        self.drawBlock()
        self.deleteLine()
    
    def drawBlock(self):
        for y in range(FIELD_ROW):
            for x in range(FIELD_COL):
                if self.block_field[y][x] != 0:
                    self.block_field[y][x].set_position(x + self.LEFT, y + self.TOP)

    def deleteLine(self):
        for y in range(FIELD_ROW-2):
            if self.isDelete(self.block_field[y+1]):
                print(y+1)
                for x in range(FIELD_COL-2):
                    self.printField()
                    print(y+1, x+1)
                    self.block_field[y+1][x+1].kill()
                self.underShift(y)

    def printField(self):
        for row in range(FIELD_ROW):
            print(self.block_field[row])
                    
    def underShift(self, y):
        # 一つ下に詰める.
        while y > 0:
            for x in range(FIELD_COL-2):
                self.block_field[y+1][x+1] = self.block_field[y][x+1]
            y -= 1
        # 一番上は初期値で埋める.
        for x in range(FIELD_COL-2):
            self.block_field[0][x+1] = 0

    def isDelete(self, line):
        for n in line:
            if n == 0:
                return False
        print(line)
        return True

    def checkEmpty(self, x, y, pattern):
        row = len(pattern)
        col = len(pattern[0])
        for i in range(row):
            for j in range(col):
                if pattern[i][j] == 1:
                    print(self.block_field[y+i][x+j], y, i, x, j)
                    if self.block_field[y+i][x+j] != 0:
                        return False
        return True
    
    def setTetrimino(self, x, y, pattern, blocks):
        num = 0
        while self.checkEmpty(x, y+1, pattern):
            y +=1
        row = len(pattern)
        col = len(pattern[0])
        for i in range(row):
            for j in range(col):
                if pattern[i][j] == 1:
                    self.block_field[y+i][x+j] = blocks[num]
                    num += 1

if __name__ == "__main__":
    Tetris()
