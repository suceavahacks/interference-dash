import pygame
from utils.constants import *

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self, speed):
        self.x -= speed

    def is_off_screen(self):
        return self.x + self.width < 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.get_rect())
        for i in range(0, int(self.width), 20):
            pygame.draw.line(screen, (70, 70, 70), (self.x + i, self.y), (self.x + i, self.y + self.height), 2)
        pygame.draw.rect(screen, (150, 150, 150), self.get_rect(), 2)
