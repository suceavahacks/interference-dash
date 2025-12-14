import pygame
from utils.constants import *
from entities.player import Player
from systems.level import Level
from systems.interference import InterferenceSystem
from systems.apocalypse import Apocalypse

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("interference-dash")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def reset_game():
    player = Player(200, SCREEN_HEIGHT - 100 - PLAYER_SIZE)
    level = Level()
    interference = InterferenceSystem()
    apocalypse = Apocalypse()
    score = 0
    speed = BASE_SPEED
    multiplier = SCORE_MULTIPLIER_BASE
    return player, level, interference, apocalypse, score, speed, multiplier

player, level, interference, apocalypse, score, speed, multiplier = reset_game()
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.jump()
            if event.key == pygame.K_r and game_over:
                player, level, interference, apocalypse, score, speed, multiplier = reset_game()
                game_over = False
            if event.key == pygame.K_ESCAPE:
                running = False

    if not game_over:
        player.update(level.ground_y)
        level.update(speed)
        apocalypse.update()
        interference.update()

        for drink in level.collectibles:
            if not drink.collected and player.get_rect().colliderect(drink.get_rect()):
                drink.collected = True
                speed += SPEED_INCREMENT
                multiplier += 0.2
                interference.add_interference(INTERFERENCE_PER_DRINK)

        for obs in level.obstacles:
            if player.get_rect().colliderect(obs.get_rect()):
                game_over = True

        if apocalypse.is_touching_player(player):
            game_over = True

        score += int(1 * multiplier)

    screen.fill(DARK_RED)

    shake_offset = interference.get_shake_offset()
    level.draw(screen, shake_offset)
    
    ground_rect = pygame.Rect(0, level.ground_y, SCREEN_WIDTH, SCREEN_HEIGHT - level.ground_y)
    pygame.draw.rect(screen, (30, 30, 30), ground_rect)

    apocalypse.draw(screen)
    player.draw(screen)

    rosen_text = font.render("ROSEN SHINGLE CREEK", True, NEON_GREEN)
    screen.blit(rosen_text, (SCREEN_WIDTH - 350, 20))

    score_text = font.render(f"score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    interference_text = font.render(f"interference: {int(interference.level)}", True, NEON_PINK)
    screen.blit(interference_text, (20, 60))

    if game_over:
        game_over_text = font.render("GAME OVER - press R to restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()