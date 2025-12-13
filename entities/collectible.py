import pygame
from utils.constants import *

class EnergyDrink:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = ENERGY_DRINK_SIZE
        self.collected = False

    def update(self,speed):
        self.x -= speed

    def is_off_screen(self):
        return self.x + self.size < 0
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        if not self.collected:
            pygame.draw.rect(screen, NEON_PINK, self.get_rect())
            pygame.draw.rect(screen, WHITE, self.get_rect(), 2)
            