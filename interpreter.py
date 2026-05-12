import random

class Interpreter():
    def __init__(self):
        pass

    def die_roll(self, die_faces, custom_values = []):
        die = list(range(1, die_faces + 1))
        for i in range(len(die)):
            if i >= len(custom_values):
                break
            die[i] = custom_values[i]
        return random.choice(die)

i = Interpreter()
print(i.die_roll(6))