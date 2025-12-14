import pygame
from utils.constants import *

try:
    energy_drink_img = pygame.image.load("assets/energy_drink.png")
    energy_drink_img = pygame.transform.scale(energy_drink_img, (ENERGY_DRINK_SIZE, ENERGY_DRINK_SIZE))
except:
    energy_drink_img = None

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
            if energy_drink_img:
                screen.blit(energy_drink_img, (self.x, self.y))
            else:
                pygame.draw.rect(screen, NEON_PINK, self.get_rect())
                pygame.draw.rect(screen, WHITE, self.get_rect(), 2)