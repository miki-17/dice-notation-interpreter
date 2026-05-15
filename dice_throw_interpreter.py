import lark
import random
from dice_roll import DiceRoll
from collections import Counter

class DiceThrowInterpreter():
    def __init__(self, data: lark.Tree):
        self.data = data

    def compare(self, operator, num1, num2):
        if operator == "<":
            return num1 < num2
        elif operator == ">":
            return num1 > num2
        elif operator == "<=":
            return num1 <= num2
        elif operator == ">=":
            return num1 >= num2
        elif operator == "=":
            return num1 == num2
        elif operator == "<>" or operator == "!=":
            return num1 != num2
    
    def interpret_extreme(self, data: lark.Tree, rolls):
        operation = data.children[0].value
        extreme = int(data.children[1].children[0].value)
        
        for roll in range(len(rolls)):
            if (rolls[roll] < extreme if operation == "min" else rolls[roll] > extreme):
                rolls[roll] = extreme
        
        return rolls
    
    def interpret_exploding(self, data: lark.Tree, rolls, dice_roll: DiceRoll):
        comparison = bool(list(data.find_data("compare")))
        comparison_operator = list(data.find_data("compare_symbol"))[0].children[0].value if comparison else "="
        comparison_number = int(list(data.find_data("compare_number"))[0].children[0].value) if comparison else dice_roll.n_faces
        penetrating = bool(list(data.find_data("penetrating")))
        actual_rolls = rolls.copy()

        roll = 0
        while roll < len(rolls):
            if self.compare(comparison_operator, rolls[roll], comparison_number):
                new_roll = dice_roll.die_roll()
                rolls.insert(roll + 1, new_roll)
                actual_rolls.insert(roll + 1, new_roll - 1)
            roll += 1
        
        return actual_rolls if penetrating else rolls
    
    def interpret_reroll(self, data: lark.Tree, rolls, dice_roll: DiceRoll):
        comparison = bool(list(data.find_data("compare")))
        comparison_operator = list(data.find_data("compare_symbol"))[0].children[0].value if comparison else "="
        comparison_number = int(list(data.find_data("compare_number"))[0].children[0].value) if comparison else 1
        unique_type = data.children[0]
        max_iterations = 1000 if unique_type == "r" else 1
        
        for roll in range(len(rolls)):
            iteration_count = 0
            while self.compare(comparison_operator, rolls[roll], comparison_number) and iteration_count < max_iterations:
                rolls[roll] = dice_roll.die_roll()
                iteration_count += 1
        
        return rolls
    
    def interpret_unique(self, data: lark.Tree, rolls, dice_roll: DiceRoll):
        comparison = bool(list(data.find_data("compare")))
        comparison_operator = list(data.find_data("compare_symbol"))[0].children[0].value if comparison else "="
        comparison_number = int(list(data.find_data("compare_number"))[0].children[0].value) if comparison else 1
        unique_type = data.children[0]
        max_iterations = 1000 if unique_type == "u" else 1

        for roll in range(len(rolls)):
            iteration_count = 0
            counts = Counter(rolls)
            while (self.compare(comparison_operator, rolls[roll], comparison_number) if comparison else counts[rolls[roll]] > 1) and iteration_count < max_iterations:
                rolls[roll] = dice_roll.die_roll()
                counts = Counter(rolls)
                iteration_count += 1
        
        return rolls
    
    def interpret_keep(self, data: lark.Tree, rolls, dice_roll: DiceRoll):
        keep_type = list(data.find_data("keep_type"))[0].children[0].value
        keep_number = int(list(data.find_data("keep_num"))[0].children[0].value) % dice_roll.n_faces
        rolls = list(reversed(sorted(rolls, reverse=keep_type == "kl")))[:keep_number]
        return rolls

    def interpret_drop(self, data: lark.Tree, rolls, dice_roll: DiceRoll):
        drop_type = list(data.find_data("drop_type"))[0].children[0].value
        drop_number = int(list(data.find_data("drop_num"))[0].children[0].value) % dice_roll.n_faces
        rolls = list(reversed(sorted(rolls, reverse=drop_type == "dh")))[:len(rolls) - drop_number]
        return rolls
    
    def roll(self):
        n_rolls_tree = list(self.data.find_data("n_rolls"))
        n_faces_tree = list(self.data.find_data("n_faces"))
        n_rolls = int(n_rolls_tree[0].children[0].value) if n_rolls_tree[0].children else 1
        n_faces = int(n_faces_tree[0].children[0].value)

        dice_roll = DiceRoll(n_faces, n_rolls)
        dice_roll.roll()

        print("Rolls prior:", dice_roll.rolls)
        
        for node in self.data.children:
            if node.data == "extreme":
                dice_roll.rolls = self.interpret_extreme(node, dice_roll.rolls)
            elif node.data == "explode":
                dice_roll.rolls = self.interpret_exploding(node, dice_roll.rolls, dice_roll)
            elif node.data == "reroll":
                dice_roll.rolls = self.interpret_reroll(node, dice_roll.rolls, dice_roll)
            elif node.data == "unique":
                dice_roll.rolls = self.interpret_unique(node, dice_roll.rolls, dice_roll)
            elif node.data == "keep":
                dice_roll.rolls = self.interpret_keep(node, dice_roll.rolls, dice_roll)
            elif node.data == "drop":
                dice_roll.rolls = self.interpret_drop(node, dice_roll.rolls, dice_roll)
        
        return dice_roll.rolls