import pygame
import json
import os
import math
from data.levels import LEVELS
from utils.constants import *

class Menu:
    def __init__(self):
        self.selected_level = 0
        self.unlocked_levels = 1
        self.in_menu = True
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 28)
        self.progress_file = "levels_progress.txt"
        self.load_progress()
        
        try:
            self.background = pygame.image.load("assets/bg_level5.jpeg")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Error loading menu background: {e}")
            self.background = None
        
        try:
            self.character = pygame.image.load("assets/walking1.png")
            self.character = pygame.transform.scale(self.character, (300, 300))
        except Exception as e:
            print(f"Error loading character: {e}")
            self.character = None
        
        self.button_hover_offset = 0
        self.animation_counter = 0

    def save_progress(self):
        try:
            with open(self.progress_file, 'w') as f:
                json.dump({
                    'unlocked_levels': self.unlocked_levels,
                    'total_levels': len(LEVELS)
                }, f)
        except Exception as e:
            print(f"Error saving menu progress: {e}")
    
    def load_progress(self):
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    self.unlocked_levels = data.get('unlocked_levels', 1)
        except Exception as e:
            print(f"Error loading menu progress: {e}")
            self.unlocked_levels = 1

    def unlock_next_level(self):
        if self.unlocked_levels < len(LEVELS):
            self.unlocked_levels += 1
            self.save_progress()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_level = max(0, self.selected_level - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_level = min(self.unlocked_levels - 1, self.selected_level + 1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.in_menu = False
                return True
        return False

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((20, 0, 60))
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        self.animation_counter += 0.05
        self.button_hover_offset = int(math.sin(self.animation_counter) * 5)
        
        title_color = (100, 255, 200)
        title = self.font_large.render("INTERFERENCE DASH", True, title_color)
        title_shadow = self.font_large.render("INTERFERENCE DASH", True, (0, 40, 30))
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        screen.blit(title_shadow, (title_x + 3, 33))
        screen.blit(title, (title_x, 30))
        
        subtitle_color = (255, 180, 100)
        subtitle = self.font_small.render("ESCAPE THE APOCALYPSE", True, subtitle_color)
        subtitle_x = SCREEN_WIDTH // 2 - subtitle.get_width() // 2
        screen.blit(subtitle, (subtitle_x, 100))
        
        if self.character:
            char_x = SCREEN_WIDTH - 380
            char_y = SCREEN_HEIGHT // 2 - 100
            
            frame_padding = 20
            frame_rect = pygame.Rect(char_x - frame_padding, char_y - frame_padding, 340, 400)
            pygame.draw.rect(screen, (0, 0, 0, 180), frame_rect, 0, 10)
            pygame.draw.rect(screen, (100, 255, 200), frame_rect, 3, 10)
            
            char_surface = self.character.convert_alpha()
            screen.blit(char_surface, (char_x, char_y))
            
            name_color = (100, 255, 200)
            name_text = self.font_large.render("MAX", True, name_color)
            name_shadow = self.font_large.render("MAX", True, (0, 40, 30))
            name_x = char_x + 150 - name_text.get_width() // 2
            screen.blit(name_shadow, (name_x + 2, char_y + 312))
            screen.blit(name_text, (name_x, char_y + 310))
        
        start_y = 180
        button_width = 520
        button_height = 70
        button_x = 50
        button_spacing = 85
        
        for i, level in enumerate(LEVELS):
            button_y = start_y + i * button_spacing
            
            if i < self.unlocked_levels:
                is_selected = i == self.selected_level
                
                border_color = (20, 20, 20)
                pygame.draw.rect(screen, border_color, (button_x, button_y, button_width, button_height), 0, 8)
                
                if is_selected:
                    button_color = (120, 80, 200)
                    text_color = WHITE
                    offset = self.button_hover_offset
                else:
                    button_color = (50, 40, 70)
                    text_color = (180, 180, 200)
                    offset = 0
                
                pygame.draw.rect(screen, button_color, (button_x + 5, button_y + 5 + offset, button_width - 10, button_height - 10), 0, 5)
                
                if is_selected:
                    pygame.draw.rect(screen, (200, 180, 255, 80), (button_x + 10, button_y + 10 + offset, button_width - 20, 6))
                
                corner_color = (100, 255, 200) if is_selected else (80, 80, 100)
                corner_size = 8
                corners = [
                    (button_x + 5, button_y + 5 + offset),
                    (button_x + button_width - 13, button_y + 5 + offset),
                    (button_x + 5, button_y + button_height - 13 + offset),
                    (button_x + button_width - 13, button_y + button_height - 13 + offset)
                ]
                for corner_x, corner_y in corners:
                    pygame.draw.rect(screen, corner_color, (corner_x, corner_y, corner_size, corner_size))
                
                badge_x = button_x + 15
                badge_y = button_y + 15 + offset
                badge_size = 40
                pygame.draw.circle(screen, (0, 0, 0), (badge_x + badge_size // 2, badge_y + badge_size // 2), badge_size // 2)
                badge_color = (100, 255, 200) if is_selected else (100, 100, 120)
                pygame.draw.circle(screen, badge_color, (badge_x + badge_size // 2, badge_y + badge_size // 2), badge_size // 2 - 3)
                
                number_text = self.font_medium.render(str(i + 1), True, WHITE)
                number_x = badge_x + badge_size // 2 - number_text.get_width() // 2
                number_y = badge_y + badge_size // 2 - number_text.get_height() // 2
                screen.blit(number_text, (number_x, number_y))
                
                level_name = level["name"].upper()
                level_text = self.font_medium.render(level_name, True, text_color)
                text_shadow = self.font_medium.render(level_name, True, (0, 0, 0))
                text_x = button_x + 70
                text_y = button_y + 12 + offset
                screen.blit(text_shadow, (text_x + 2, text_y + 2))
                screen.blit(level_text, (text_x, text_y))
                
                if level["end_score"] == -1:
                    mode_text = self.font_tiny.render("∞ ENDLESS MODE", True, (100, 255, 200) if is_selected else (120, 120, 140))
                else:
                    mode_text = self.font_tiny.render(f"Goal: {level['end_score']} pts", True, (255, 200, 120) if is_selected else (120, 120, 140))
                screen.blit(mode_text, (text_x, text_y + 35))
                
            else:
                button_color = (30, 30, 30)
                border_color = (20, 20, 20)
                pygame.draw.rect(screen, border_color, (button_x, button_y, button_width, button_height), 0, 8)
                pygame.draw.rect(screen, button_color, (button_x + 5, button_y + 5, button_width - 10, button_height - 10), 0, 5)
                
                lock_x = button_x + 25
                lock_y = button_y + 22
                pygame.draw.rect(screen, (80, 80, 80), (lock_x, lock_y + 10, 20, 18))
                pygame.draw.rect(screen, (80, 80, 80), (lock_x + 5, lock_y, 10, 15), 3)
                pygame.draw.circle(screen, (60, 60, 60), (lock_x + 10, lock_y + 18), 3)
                
                level_text = self.font_medium.render("LOCKED", True, (80, 80, 80))
                screen.blit(level_text, (button_x + 70, button_y + 20))
        
        key_color = (100, 255, 200)
        action_color = (255, 200, 120)
        
        instructions = self.font_small.render("⬆️ ⬇️  SELECT     ENTER  START", True, WHITE)
        instructions_shadow = self.font_small.render("⬆️ ⬇️  SELECT     ENTER  START", True, (0, 0, 0))

        inst_x = SCREEN_WIDTH // 2 - instructions.get_width() // 2
        inst_y = SCREEN_HEIGHT - 40
        
        screen.blit(instructions_shadow, (inst_x + 2, inst_y + 2))
        screen.blit(instructions, (inst_x, inst_y))
