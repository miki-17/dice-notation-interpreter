import random
import lark
from dice_throw_interpreter import DiceThrowInterpreter

class Interpreter():
    def __init__(self):
        self.operations = []
    
    def interpret_dice_throw(self, data: lark.Tree):
        interpreter = DiceThrowInterpreter(data)
        return interpreter.roll()

    def interpret_modifier(self, data: lark.Tree):
        number = eval(list(data.find_data("mod_num"))[0].children[0].value)
        sign = list(data.find_data("minus"))

        if len(sign) > 0:
            number = -number
        
        return number

    def interpret_function(self, data: lark.Tree):
        modifier_node = list(data.find_data("modifier"))[0]
        operator_node = list(data.find_data("operator"))[0]

        number = self.interpret_modifier(modifier_node)
        operator = self.interpret_operator(operator_node)

        return operator, number

    def interpret_operator(self, data: lark.Tree):
        return data.children[0].value
    
    def reset_operation_stack(self):
        self.operations.clear()
    
    def evaluate_operation(self, operation, a, b):
        if operation == "+":
            return a + b
        elif operation == "-":
            return a - b
        elif operation == "*":
            return a * b
        elif operation == "/":
            return a / b
        elif operation == "**":
            return a**b
    
    def construct_operations_string(self):
        result = ""
        for i in range(len(self.operations)):
            result += (str(self.operations[i][0]) if i != 0 else "") + " " + str(self.operations[i][1]) + " "
        return result
    
    def evaluate(self):
        operations_string = self.construct_operations_string()

        for i in range(len(self.operations)):
            if type(self.operations[i][1]) == list:
                self.operations[i] = (self.operations[i][0], sum(self.operations[i][1]))
        
        for allowed_operations in [["*", "**", "/"], ["+", "-"]]:
            active_operations = [True] * len(self.operations)
            for i in range(1, len(self.operations)):
                operator, number = self.operations[i]
                if operator not in allowed_operations:
                    continue
                prev_operator, prev_number = self.operations[i - 1]
                result = self.evaluate_operation(operator, prev_number, number)
                self.operations[i] = (prev_operator, result)
                active_operations[i - 1] = False
            new_operations_list = []
            for i in range(len(self.operations)):
                if active_operations[i]:
                    new_operations_list.append(self.operations[i])
            self.operations = new_operations_list
        
        result = self.operations[0][1]
        return result, operations_string
    
    def interpret(self, parsed_data: lark.Tree):
        self.reset_operation_stack()

        all_rolls = []
        saved_operator = "+"

        for node in parsed_data.children:
            if node.data == "dice_throw":
                rolls = self.interpret_dice_throw(node)
                all_rolls.append(rolls)
                self.operations.append((saved_operator, rolls))
            elif node.data == "function":
                operator, number = self.interpret_function(node)
                self.operations.append((operator, number))
            elif node.data == "operator":
                saved_operator = self.interpret_operator(node)
            elif node.data == "modifier":
                number = self.interpret_modifier(node)
                self.operations.append(("+", number))
        
        result, operations_string = self.evaluate()
        print(operations_string, "=", result)
