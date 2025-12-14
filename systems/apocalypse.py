import pygame
from utils.constants import *

class Apocalypse:
    def __init__(self):
        self.x = -800
        self.width = 200
        self.base_speed = 0.8

    def update(self):
        self.x += self.base_speed

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 0, 0), (self.x, 0, self.width, SCREEN_HEIGHT))
        for i in range(5):
            offset = i * 40
            pygame.draw.rect(screen, (100, 0, 0), (self.x + self.width - offset, 0, 20, SCREEN_HEIGHT))

    def is_touching_player(self, player):
        return player.x < self.x + self.width

