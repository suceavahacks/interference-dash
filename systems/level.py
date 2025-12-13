import random
from entities.obstacle import Obstacle
from entities.collectible import EnergyDrink
from utils.constants import *

class Level:
    def __init__(self):
        self.obstacles = []
        self.collectibles = []
        self.next_obstacle_x = SCREEN_WIDTH
        self.next_collectible_x = SCREEN_WIDTH + 300
        self.ground_y = SCREEN_HEIGHT - 100

    def generate_obstacle(self):
        obstacle_type = random.choice(["spike", "block"])
        height = OBSTACLE_HEIGHT if obstacle_type == "spike" else random.randint(40, 100)
        obs = Obstacle(self.next_obstacle_x, self.ground_y - height, OBSTACLE_WIDTH, height, obstacle_type)
        self.obstacles.append(obs)
        self.next_obstacle_x += random.randint(200, 400)

    def generate_collectible(self):
        y_pos = self.ground_y - random.randint(50, 250)
        drink = EnergyDrink(self.next_collectible_x, y_pos)
        self.collectibles.append(drink)
        self.next_collectible_x += random.randint(400, 700)

    def update(self, speed):
        for obs in self.obstacles:
            obs.update(speed)
        
        for drink in self.collectibles:
            drink.update(speed)

        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen()]
        self.collectibles = [drink for drink in self.collectibles if not drink.is_off_screen()]

        if self.next_obstacle_x < SCREEN_WIDTH + 500:
            self.generate_obstacle()
        
        if self.next_collectible_x < SCREEN_WIDTH + 600:
            self.generate_collectible()

    def draw(self, screen, shake_offset):
        offset_x, offset_y = shake_offset
        for obs in self.obstacles:
            screen_obs = Obstacle(obs.x + offset_x, obs.y + offset_y, obs.width, obs.height, obs.type)
            screen_obs.draw(screen)
        
        for drink in self.collectibles:
            if not drink.collected:
                rect = drink.get_rect()
                shifted_drink = EnergyDrink(rect.x + offset_x, rect.y + offset_y)
                shifted_drink.draw(screen)