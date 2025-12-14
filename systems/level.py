import random
from entities.obstacle import Obstacle
from entities.collectible import EnergyDrink
from entities.platform import Platform
from utils.constants import *

class Level:
    def __init__(self):
        self.obstacles = []
        self.collectibles = []
        self.platforms = []
        self.next_obstacle_x = SCREEN_WIDTH
        self.next_collectible_x = SCREEN_WIDTH + 300
        self.next_platform_x = SCREEN_WIDTH + 600
        self.ground_y = SCREEN_HEIGHT - 100

    def generate_obstacle(self):
        obstacle_type = random.choice(["spike", "block", "double_spike"])
        
        if obstacle_type == "spike":
            height = OBSTACLE_HEIGHT
            width = OBSTACLE_WIDTH
        elif obstacle_type == "block":
            height = random.randint(40, 100)
            width = OBSTACLE_WIDTH
        elif obstacle_type == "double_spike":
            height = OBSTACLE_HEIGHT
            width = OBSTACLE_WIDTH * 2
        
        obs = Obstacle(self.next_obstacle_x, self.ground_y - height, width, height, obstacle_type)
        self.obstacles.append(obs)
        self.next_obstacle_x += random.randint(200, 400)

    def generate_collectible(self):
        y_pos = self.ground_y - random.randint(50, 250)
        drink = EnergyDrink(self.next_collectible_x, y_pos)
        self.collectibles.append(drink)
        self.next_collectible_x += random.randint(400, 700)

    def generate_platform(self):
        width = random.randint(80, 150)
        height = 20
        y_pos = self.ground_y - random.randint(80, 180)
        platform = Platform(self.next_platform_x, y_pos, width, height)
        self.platforms.append(platform)
        self.next_platform_x += random.randint(300, 600)

    def update(self, speed):
        for obs in self.obstacles:
            obs.update(speed)
        
        for drink in self.collectibles:
            drink.update(speed)

        for platform in self.platforms:
            platform.update(speed)

        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen()]
        self.collectibles = [drink for drink in self.collectibles if not drink.is_off_screen()]
        self.platforms = [p for p in self.platforms if not p.is_off_screen()]

        if self.next_obstacle_x < SCREEN_WIDTH + 500:
            self.generate_obstacle()
        
        if self.next_collectible_x < SCREEN_WIDTH + 600:
            self.generate_collectible()

        if self.next_platform_x < SCREEN_WIDTH + 700:
            self.generate_platform()

    def draw(self, screen, shake_offset):
        offset_x, offset_y = shake_offset
        
        for platform in self.platforms:
            shifted_platform = Platform(platform.x + offset_x, platform.y + offset_y, platform.width, platform.height)
            shifted_platform.draw(screen)
        
        for obs in self.obstacles:
            screen_obs = Obstacle(obs.x + offset_x, obs.y + offset_y, obs.width, obs.height, obs.type)
            screen_obs.draw(screen)
        
        for drink in self.collectibles:
            if not drink.collected:
                rect = drink.get_rect()
                shifted_drink = EnergyDrink(rect.x + offset_x, rect.y + offset_y)
                shifted_drink.draw(screen)