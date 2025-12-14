import pygame
import random

class AnimatedObstacle:
    def __init__(self, x, y, size=80):
        self.x = x
        self.y = y
        self.size = size
        self.facing_left = True
        self.animation_frame = 0
        self.animation_speed = 0.08
        self.passed_by_player = False
        
        try:
            self.going_left_normal = pygame.image.load("assets/going_left_normal.png")
            self.going_left_hands = pygame.image.load("assets/going_left_hands.png")
            self.going_right_normal = pygame.image.load("assets/going_right_normal.png")
            self.going_right_hands = pygame.image.load("assets/going_right_hands.png")
            self.going_right_legs = pygame.image.load("assets/going_right_legs.png")
            

            self.going_left_normal = pygame.transform.scale(self.going_left_normal, (size, size))
            self.going_left_hands = pygame.transform.scale(self.going_left_hands, (size, size))
            self.going_right_normal = pygame.transform.scale(self.going_right_normal, (size, size))
            self.going_right_hands = pygame.transform.scale(self.going_right_hands, (size, size))
            self.going_right_legs = pygame.transform.scale(self.going_right_legs, (size, size))
            
            self.left_frames = [self.going_left_normal, self.going_left_hands]
            self.right_frames = [self.going_right_normal, self.going_right_hands, self.going_right_legs]
            
            self.images_loaded = True
        except Exception as e:
            print(f"Error loading animated obstacle images: {e}")
            self.images_loaded = False
    
    def update(self, speed, player_x=None):
        self.x -= speed
        
        if player_x is not None and not self.passed_by_player:
            if player_x > self.x + self.size:
                self.passed_by_player = True
                self.facing_left = False
        
        self.animation_frame += self.animation_speed
        
    def draw(self, screen):
        if not self.images_loaded:
            pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, self.size, self.size))
            return
        
        if self.facing_left:
            frames = self.left_frames
        else:
            frames = self.right_frames
        
        frame_index = int(self.animation_frame) % len(frames)
        current_image = frames[frame_index]
        
        screen.blit(current_image, (self.x, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def is_off_screen(self):
        return self.x < -200
