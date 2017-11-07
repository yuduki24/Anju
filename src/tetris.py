import pygame
from pygame.locals import *
from loader import load_image, load_font, split_image
import os
import sys
import random

SCR_RECT = Rect(0, 0, 900, 600)

class Tetris:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption(u"Tetris")

        # 画像の読み込み
        self.load_images()

        # ゲームオブジェクトを初期化
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
        Tetromino.containers = self.all

        for x in range(0, 7):
            Tetromino(x, self.tetromino_img[x])

    def update(self):
        """ゲーム状態の更新"""
        self.all.update()

    def draw(self, screen):
        """描画"""
        screen.fill((10, 10, 10))
        self.all.draw(screen)

    def key_handler(self):
        """キーハンドラー"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
    def load_images(self):
        """イメージのロード"""
        self.tetromino_img = split_image(load_image("tetromino.png"), 7)

class Tetromino(pygame.sprite.Sprite):
    """テトロミノ"""
    def __init__(self, x, image):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = SCR_RECT.left + x * self.rect.width
        self.reload_timer = 0

if __name__ == "__main__":
    Tetris()