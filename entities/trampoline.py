import pygame
from utils.constants import *

class Trampoline:
    def __init__(self, x, y, width=100, height=30):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bounce_animation = 0

    def update(self, speed):
        self.x -= speed
        if self.bounce_animation > 0:
            self.bounce_animation -= 0.1

    def is_off_screen(self):
        return self.x + self.width < 0

    def get_rect(self):
        hitbox_shrink = 10
        return pygame.Rect(self.x + hitbox_shrink, self.y, self.width - hitbox_shrink * 2, self.height)
    
    def activate_bounce(self):
        self.bounce_animation = 1.0

    def draw(self, screen):
        bounce_offset = int(self.bounce_animation * 5)
        
        base_color = (255, 100, 0)
        spring_color = (255, 150, 50)
        highlight_color = (255, 200, 100)
        
        pygame.draw.rect(screen, base_color, (self.x, self.y + bounce_offset, self.width, self.height))
        
        num_springs = 5
        spring_width = self.width // num_springs
        for i in range(num_springs):
            spring_x = self.x + i * spring_width
            points = [
                (spring_x + spring_width // 2, self.y + bounce_offset - 5),
                (spring_x + spring_width // 4, self.y + bounce_offset),
                (spring_x + 3 * spring_width // 4, self.y + bounce_offset)
            ]
            pygame.draw.lines(screen, spring_color, False, points, 3)
        
        pygame.draw.rect(screen, highlight_color, (self.x, self.y + bounce_offset, self.width, self.height), 3)
        
        for i in range(0, int(self.width), 20):
            pygame.draw.line(screen, (255, 220, 150), 
                           (self.x + i, self.y + bounce_offset), 
                           (self.x + i, self.y + self.height + bounce_offset), 2)
