import random

class InterferenceSystem:
    def __init__(self):
        self.level = 0.0
        self.shake_offset_x = 0
        self.shake_offset_y = 0

    def add_interference(self, amount):
        self.level += amount

    def update(self):
        if self.level > 3:
            self.shake_offset_x = random.randint(-int(self.level), int(self.level))
            self.shake_offset_y = random.randint(-int(self.level), int(self.level))
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0

    def get_shake_offset(self):
        return self.shake_offset_x, self.shake_offset_y

    def get_input_delay(self):
        if self.level > 6:
            return random.randint(0, 10)
        return 0
