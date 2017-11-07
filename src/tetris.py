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
        # メインループ開始
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            pygame.display.update()
            self.key_handler()

    def key_handler(self):
        """キーハンドラー"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    Tetris()