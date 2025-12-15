import pygame
from utils.constants import *
from entities.player import Player
from systems.level import Level
from systems.interference import InterferenceSystem
from systems.menu import Menu

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("interference-dash")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

try:
    pygame.mixer.music.load("assets/background_music.ogg")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"Error loading background music: {e}")
    import traceback
    traceback.print_exc()

def reset_game(starting_level=0):
    player = Player(200, SCREEN_HEIGHT - 100 - PLAYER_SIZE)
    level = Level()
    level.current_level_index = starting_level
    level.bg_color = level.get_current_level()["bg_color"]
    level.load_level_patterns()
    interference = InterferenceSystem()
    score = 0
    current_level = level.get_current_level()
    speed = BASE_SPEED * current_level["speed_multiplier"]
    multiplier = SCORE_MULTIPLIER_BASE
    difficulty = 1.0
    return player, level, interference, score, speed, multiplier, difficulty

menu = Menu()
player, level, interference, score, speed, multiplier, difficulty = reset_game()
running = True
game_over = False
in_game = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if menu.in_menu:
            if menu.handle_input(event):
                in_game = True
                player, level, interference, score, speed, multiplier, difficulty = reset_game(menu.selected_level)
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    current_level = level.current_level_index
                    player, level, interference, score, speed, multiplier, difficulty = reset_game(current_level)
                    game_over = False
                if event.key == pygame.K_ESCAPE:
                    if game_over:
                        menu.in_menu = True
                        in_game = False
                        game_over = False
                    else:
                        running = False

    if menu.in_menu:
        menu.draw(screen)
    else:
        if not game_over and in_game:
            player.update(level.ground_y, level.platforms, level.trampolines)
            level.update(speed, difficulty, player.x)
            interference.update()

            for drink in level.collectibles:
                if not drink.collected and player.get_rect().colliderect(drink.get_rect()):
                    drink.collected = True
                    speed += SPEED_INCREMENT
                    multiplier += 0.2
                    difficulty += 0.15
                    interference.add_interference(INTERFERENCE_PER_DRINK)

            for obs in level.obstacles:
                if player.get_rect().colliderect(obs.get_rect()):
                    game_over = True
            
            for animated_obs in level.animated_obstacles:
                if player.get_rect().colliderect(animated_obs.get_rect()):
                    game_over = True

            score += int(1 * multiplier * difficulty)
            
            level_changed = level.check_level_progression(score)
            if level_changed:
                menu.unlock_next_level()
                
                current_level = level.get_current_level()
                speed = BASE_SPEED * current_level["speed_multiplier"]
                multiplier = 1.0
                difficulty = 1.0
                interference.level = 0
                player.x = 100
                player.y = level.ground_y - PLAYER_SIZE
                player.velocity_y = 0
                player.on_ground = False
                score = 0
                
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(220)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                
                panel_width = 600
                panel_height = 250
                panel_x = SCREEN_WIDTH // 2 - panel_width // 2
                panel_y = SCREEN_HEIGHT // 2 - panel_height // 2
                
                panel_bg = pygame.Surface((panel_width, panel_height))
                panel_bg.set_alpha(240)
                panel_bg.fill((20, 10, 30))
                screen.blit(panel_bg, (panel_x, panel_y))
                
                pygame.draw.rect(screen, (100, 255, 200), (panel_x, panel_y, panel_width, panel_height), 5, 15)
                
                corner_size = 15
                corners = [
                    (panel_x, panel_y),
                    (panel_x + panel_width - corner_size, panel_y),
                    (panel_x, panel_y + panel_height - corner_size),
                    (panel_x + panel_width - corner_size, panel_y + panel_height - corner_size)
                ]
                for cx, cy in corners:
                    pygame.draw.rect(screen, (100, 255, 200), (cx, cy, corner_size, corner_size))
                
                font_title = pygame.font.Font(None, 84)
                font_subtitle = pygame.font.Font(None, 56)
                
                title_text = font_title.render("LEVEL UP!", True, (100, 255, 200))
                title_shadow = font_title.render("LEVEL UP!", True, (50, 127, 100))
                title_x = panel_x + panel_width // 2 - title_text.get_width() // 2
                screen.blit(title_shadow, (title_x + 4, panel_y + 44))
                screen.blit(title_text, (title_x, panel_y + 40))
                
                level_name = font_subtitle.render(current_level['name'].upper(), True, (255, 200, 120))
                level_x = panel_x + panel_width // 2 - level_name.get_width() // 2
                screen.blit(level_name, (level_x, panel_y + 140))
                
                pygame.display.flip()
                pygame.time.wait(1500)

        shake_offset = interference.get_shake_offset()
        level.draw(screen, shake_offset)

        player.draw(screen)

        panel_x = 20
        panel_y = 20
        panel_width = 280
        panel_height = 210
        panel_padding = 15
        
        panel_bg = pygame.Surface((panel_width, panel_height))
        panel_bg.set_alpha(180)
        panel_bg.fill((20, 10, 30))
        screen.blit(panel_bg, (panel_x, panel_y))
        
        pygame.draw.rect(screen, (100, 255, 200), (panel_x, panel_y, panel_width, panel_height), 3, 8)
        
        corner_size = 10
        corner_color = (100, 255, 200)
        corners = [
            (panel_x, panel_y),
            (panel_x + panel_width - corner_size, panel_y),
            (panel_x, panel_y + panel_height - corner_size),
            (panel_x + panel_width - corner_size, panel_y + panel_height - corner_size)
        ]
        for cx, cy in corners:
            pygame.draw.rect(screen, corner_color, (cx, cy, corner_size, corner_size))
        
        text_x = panel_x + panel_padding
        text_y = panel_y + panel_padding
        line_height = 38
        
        font_label = pygame.font.Font(None, 28)
        font_value = pygame.font.Font(None, 42)
        
        level_name = level.get_current_level()["name"].upper()
        level_label = font_label.render("LEVEL", True, (150, 150, 150))
        level_value = font_value.render(level_name, True, (100, 255, 200))
        screen.blit(level_label, (text_x, text_y))
        screen.blit(level_value, (text_x, text_y + 18))
        
        score_label = font_label.render("SCORE", True, (150, 150, 150))
        score_value = font_value.render(str(score), True, (255, 200, 120))
        screen.blit(score_label, (text_x, text_y + line_height * 1 + 10))
        screen.blit(score_value, (text_x, text_y + line_height * 1 + 28))
        
        interference_label = font_label.render("ENERGY DRINKS", True, (150, 150, 150))
        interference_value = font_value.render(str(int(interference.level)), True, (255, 100, 150))
        screen.blit(interference_label, (text_x, text_y + line_height * 2 + 20))
        screen.blit(interference_value, (text_x, text_y + line_height * 2 + 38))
        
        diff_label = font_label.render("DIFFICULTY", True, (150, 150, 150))
        diff_value = font_value.render(f"{difficulty:.1f}x", True, (255, 150, 50))
        screen.blit(diff_label, (text_x, text_y + line_height * 3 + 30))
        screen.blit(diff_value, (text_x, text_y + line_height * 3 + 48))
        
        bar_panel_x = SCREEN_WIDTH - 260
        bar_panel_y = SCREEN_HEIGHT - 80
        bar_panel_width = 240
        bar_panel_height = 60
        
        bar_bg = pygame.Surface((bar_panel_width, bar_panel_height))
        bar_bg.set_alpha(180)
        bar_bg.fill((20, 10, 30))
        screen.blit(bar_bg, (bar_panel_x, bar_panel_y))
        
        pygame.draw.rect(screen, (100, 255, 200), (bar_panel_x, bar_panel_y, bar_panel_width, bar_panel_height), 3, 8)
        
        corners_bar = [
            (bar_panel_x, bar_panel_y),
            (bar_panel_x + bar_panel_width - corner_size, bar_panel_y),
            (bar_panel_x, bar_panel_y + bar_panel_height - corner_size),
            (bar_panel_x + bar_panel_width - corner_size, bar_panel_y + bar_panel_height - corner_size)
        ]
        for cx, cy in corners_bar:
            pygame.draw.rect(screen, corner_color, (cx, cy, corner_size, corner_size))
        
        speed_bar_width = 200
        speed_bar_height = 20
        speed_bar_x = bar_panel_x + 20
        speed_bar_y = bar_panel_y + 30
        
        pygame.draw.rect(screen, (40, 30, 50), (speed_bar_x, speed_bar_y, speed_bar_width, speed_bar_height), 0, 5)
        
        speed_display = speed / BASE_SPEED
        speed_fill = min((speed / (BASE_SPEED * 3)) * speed_bar_width, speed_bar_width)
        fill_width = int(speed_fill)
        
        if fill_width > 0:
            fill_rect = pygame.Rect(speed_bar_x, speed_bar_y, fill_width, speed_bar_height)
            if speed_display < 1.5:
                bar_color = (100, 255, 200)
            elif speed_display < 2.5:
                bar_color = (255, 200, 100)
            else:
                bar_color = (255, 100, 150)
            pygame.draw.rect(screen, bar_color, fill_rect, 0, 5)
        
        pygame.draw.rect(screen, (100, 255, 200), (speed_bar_x, speed_bar_y, speed_bar_width, speed_bar_height), 2, 5)
        
        speed_label = font_label.render(f"SPEED: {speed_display:.1f}x", True, WHITE)
        screen.blit(speed_label, (speed_bar_x + 5, bar_panel_y + 8))

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            game_over_panel_width = 500
            game_over_panel_height = 300
            panel_x = SCREEN_WIDTH // 2 - game_over_panel_width // 2
            panel_y = SCREEN_HEIGHT // 2 - game_over_panel_height // 2
            
            panel_bg = pygame.Surface((game_over_panel_width, game_over_panel_height))
            panel_bg.set_alpha(220)
            panel_bg.fill((20, 10, 30))
            screen.blit(panel_bg, (panel_x, panel_y))
            
            pygame.draw.rect(screen, (255, 100, 150), (panel_x, panel_y, game_over_panel_width, game_over_panel_height), 4, 12)
            
            corner_size = 12
            corners = [
                (panel_x, panel_y),
                (panel_x + game_over_panel_width - corner_size, panel_y),
                (panel_x, panel_y + game_over_panel_height - corner_size),
                (panel_x + game_over_panel_width - corner_size, panel_y + game_over_panel_height - corner_size)
            ]
            for cx, cy in corners:
                pygame.draw.rect(screen, (255, 100, 150), (cx, cy, corner_size, corner_size))
            
            font_title = pygame.font.Font(None, 72)
            font_info = pygame.font.Font(None, 42)
            font_button = pygame.font.Font(None, 36)
            
            title_text = font_title.render("GAME OVER", True, (255, 100, 150))
            title_shadow = font_title.render("GAME OVER", True, (100, 0, 50))
            title_x = panel_x + game_over_panel_width // 2 - title_text.get_width() // 2
            screen.blit(title_shadow, (title_x + 3, panel_y + 33))
            screen.blit(title_text, (title_x, panel_y + 30))
            
            final_score_label = font_info.render("FINAL SCORE", True, (150, 150, 150))
            final_score_value = font_title.render(str(score), True, (255, 200, 120))
            score_label_x = panel_x + game_over_panel_width // 2 - final_score_label.get_width() // 2
            score_value_x = panel_x + game_over_panel_width // 2 - final_score_value.get_width() // 2
            screen.blit(final_score_label, (score_label_x, panel_y + 110))
            screen.blit(final_score_value, (score_value_x, panel_y + 145))
            
            button_y = panel_y + 220
            
            restart_text = font_button.render("R  RESTART", True, (100, 255, 200))
            menu_text = font_button.render("ESC  MENU", True, (100, 255, 200))
            
            restart_x = panel_x + game_over_panel_width // 2 - restart_text.get_width() - 30
            menu_x = panel_x + game_over_panel_width // 2 + 30
            
            screen.blit(restart_text, (restart_x, button_y))
            screen.blit(menu_text, (menu_x, button_y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()