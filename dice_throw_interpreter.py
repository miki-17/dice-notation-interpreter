import lark
import random
from collections import Counter

class DiceThrowInterpreter():
    def __init__(self, data: lark.Tree):
        self.data = data
        self.rolls_decorated = []
        self.operations_queue = {
            "minmax": [],
            "explode": [],
            "reroll": [],
            "unique": [],
            "keep": [],
            "drop": []
        }
    
    def die_roll(self):
        for _ in range(self.n_rolls):
            self.rolls_decorated.append({
                "value": random.randint(1, self.n_faces),
                "decorations": "",
                "active": True,
                "kept": False,
                "deleted": True
            })

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
    
    def interpret_extreme(self, data: lark.Tree):
        operation = data.children[0].value
        extreme = int(data.children[1].children[0].value)
        
        for roll in range(len(self.rolls_decorated)):
            if (self.rolls_decorated[roll]["value"] < extreme if operation == "min" else self.rolls_decorated[roll]["value"] > extreme):
                self.rolls_decorated[roll]["value"] = extreme
                self.rolls_decorated[roll]["decorations"] = "^" if operation == "min" else "v"
    
    def interpret_exploding(self, data: lark.Tree):
        comparison = bool(list(data.find_data("compare")))
        comparison_operator = list(data.find_data("compare_symbol"))[0].children[0].value if comparison else "="
        comparison_number = int(list(data.find_data("compare_number"))[0].children[0].value) if comparison else self.n_faces
        penetrating = bool(list(data.find_data("penetrating")))
        actual_rolls = self.rolls_decorated.copy()

        roll = 0
        while roll < len(self.rolls_decorated):
            if self.compare(comparison_operator, actual_rolls[roll]["value"], comparison_number):
                new_roll = random.randint(1, self.n_faces)
                actual_rolls.insert(roll + 1, {"value": new_roll})
                self.rolls_decorated[roll]["decorations"] += "!p" if penetrating else "!"
                self.rolls_decorated.insert(roll + 1, {
                    "value": new_roll - 1 if penetrating else new_roll,
                    "decorations": "",
                    "active": True,
                    "kept": False,
                    "deleted": True
                })
            roll += 1
    
    def interpret_reroll(self, data: lark.Tree):
        comparison = bool(list(data.find_data("compare")))
        comparison_operator = list(data.find_data("compare_symbol"))[0].children[0].value if comparison else "="
        comparison_number = int(list(data.find_data("compare_number"))[0].children[0].value) if comparison else 1
        reroll_type = data.children[0]
        max_iterations = 1000 if reroll_type == "r" else 1
        
        for roll in range(len(self.rolls_decorated)):
            iteration_count = 0
            new_roll = self.rolls_decorated[roll]["value"]

            while self.compare(comparison_operator, new_roll, comparison_number) and iteration_count < max_iterations:
                new_roll = random.randint(1, self.n_faces)
                iteration_count += 1

            if iteration_count > 0:
                self.rolls_decorated[roll]["value"] = new_roll
                self.rolls_decorated[roll]["decorations"] += reroll_type
    
    def interpret_unique(self, data: lark.Tree):
        comparison = bool(list(data.find_data("compare")))
        comparison_operator = list(data.find_data("compare_symbol"))[0].children[0].value if comparison else "="
        comparison_number = int(list(data.find_data("compare_number"))[0].children[0].value) if comparison else 1
        unique_type = data.children[0]
        max_iterations = 1000 if unique_type == "u" else 1

        for roll in range(len(self.rolls_decorated)):
            iteration_count = 0
            new_roll = self.rolls_decorated[roll]["value"]
            counts = Counter(i["value"] for i in self.rolls_decorated)

            while (self.compare(comparison_operator, self.rolls_decorated[roll]["value"], comparison_number) if comparison else counts[self.rolls_decorated[roll]["value"]] > 1) and iteration_count < max_iterations:
                new_roll = random.randint(1, self.n_faces)
                self.rolls_decorated[roll]["value"] = new_roll
                counts = Counter(i["value"] for i in self.rolls_decorated)
                iteration_count += 1
            
            if iteration_count > 0:
                self.rolls_decorated[roll]["value"] = new_roll
                self.rolls_decorated[roll]["decorations"] += unique_type
    
    def interpret_keep(self, data: lark.Tree):
        keep_type = list(data.find_data("keep_type"))[0].children[0].value
        keep_number = int(list(data.find_data("keep_num"))[0].children[0].value) % self.n_faces
        values_to_keep = sorted(self.rolls_decorated, key=lambda x: x["value"], reverse=keep_type != "kl")[:keep_number]

        for value in values_to_keep:
            value["kept"] = True
        for value in self.rolls_decorated:
            if value not in values_to_keep:
                value["active"] = False
                value["decorations"] += "d" if not "d" in value["decorations"] else ""

    def interpret_drop(self, data: lark.Tree):
        drop_type = list(data.find_data("drop_type"))[0].children[0].value
        drop_number = int(list(data.find_data("drop_num"))[0].children[0].value) % self.n_faces
        values_to_keep = sorted(self.rolls_decorated, key=lambda x: x["value"], reverse=drop_type != "dh")[:len(self.rolls_decorated) - drop_number]

        for value in values_to_keep:
            value["deleted"] = False
        for value in self.rolls_decorated:
            if value not in values_to_keep:
                value["active"] = False
                value["decorations"] += "d" if not "d" in value["decorations"] else ""
    
    def roll(self):
        n_rolls_tree = list(self.data.find_data("n_rolls"))
        n_faces_tree = list(self.data.find_data("n_faces"))
        n_rolls = int(n_rolls_tree[0].children[0].value) if n_rolls_tree[0].children else 1
        n_faces = int(n_faces_tree[0].children[0].value)

        self.n_faces = n_faces
        self.n_rolls = n_rolls
        self.die_roll()
        
        for node in self.data.children:
            if node.data == "extreme":
                self.operations_queue["minmax"].append(node)
            elif node.data == "explode":
                self.operations_queue["explode"].append(node)
            elif node.data == "reroll":
                self.operations_queue["reroll"].append(node)
            elif node.data == "unique":
                self.operations_queue["unique"].append(node)
            elif node.data == "keep":
                self.operations_queue["keep"].append(node)
            elif node.data == "drop":
                self.operations_queue["drop"].append(node)
        
        for operation, node_list in self.operations_queue.items():
            for node in node_list:
                if operation == "minmax":
                    self.interpret_extreme(node)
                elif operation == "explode":
                    self.interpret_exploding(node)
                elif operation == "reroll":
                    self.interpret_reroll(node)
                elif operation == "unique":
                    self.interpret_unique(node)
                elif operation == "keep":
                    self.interpret_keep(node)
                elif operation == "drop":
                    self.interpret_drop(node)
        
        rolls_decorated_string = []
        rolls = []
        for roll in self.rolls_decorated:
            rolls_decorated_string.append(str(roll["value"]) + roll["decorations"])
            if roll["active"] == True:
                rolls.append(roll["value"])
        rolls_decorated_string = "[" + ", ".join(rolls_decorated_string) + "]"

        return sum(rolls), rolls_decorated_string