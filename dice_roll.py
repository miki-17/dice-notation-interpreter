import random

class DiceRoll():
    def __init__(self, n_faces, n_rolls):
        self.n_faces = n_faces
        self.n_rolls = n_rolls
        self.rolls = []
    
    def die_roll(self):
        return random.randint(1, self.n_faces)
    
    def roll(self):
        self.rolls = []
        for _ in range(self.n_rolls):
            self.rolls.append(self.die_roll())