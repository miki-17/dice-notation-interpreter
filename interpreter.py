import lark
from dice_throw_interpreter import DiceThrowInterpreter

class Interpreter():
    def __init__(self):
        self.operations = []

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
    
    def evaluate_operations(self, operations):
        for allowed_operations in [["**", "*", "/"], ["+", "-"]]:
            i = 2
            while i < len(operations):
                if operations[i - 1] not in allowed_operations:
                    i += 2
                    continue
                print(operations)
                res = self.evaluate_operation(operations[i - 1], operations[i - 2], operations[i])
                operations.insert(i + 1, res)
                operations.pop(i)
                operations.pop(i - 1)
                operations.pop(i - 2)
                i -= 2
        
        return operations[0]
    
    def interpret_dice_throw(self, data: lark.Tree):
        interpreter = DiceThrowInterpreter(data)
        return interpreter.roll()

    def interpret_modifier(self, data: lark.Tree):
        number = eval(list(data.find_data("mod_num"))[0].children[0].value)
        sign = list(data.find_data("minus"))

        if len(sign) > 0:
            number = -number
        
        return number

    def interpret_operator(self, data: lark.Tree):
        return data.children[0].value
    
    def interpret_value(self, data: lark.Tree):
        opening_brackets = bool(list(data.find_data("opening_bracket")))
        closing_brackets = bool(list(data.find_data("closing_bracket")))
        modifier_node = list(data.find_data("modifier"))
        dice_throw_node = list(data.find_data("dice_throw"))
        statement = list(data.find_data("statement"))

        result_string = ""
        result_value = 0

        if opening_brackets and closing_brackets:
            result, value = self.interpret_statement(statement[-1])
            result_string += "(" + result + ")" 
            result_value = value
        elif modifier_node:
            modifier_node = modifier_node[0]
            number = self.interpret_modifier(modifier_node)
            result_string += str(number)
            result_value = number
        elif dice_throw_node:
            dice_throw_node = dice_throw_node[0]
            rolls, rolls_decorated_string = self.interpret_dice_throw(dice_throw_node)
            result_string += rolls_decorated_string
            result_value = rolls
        
        return result_string, result_value
        
    def interpret_statement(self, data: lark.Tree):
        result_string = ""
        operations_list = []

        for node in data.children:
            if node.data == "value":
                res_string, value = self.interpret_value(node)
                result_string += res_string
                operations_list.append(value)
            if node.data == "operator":
                operator = self.interpret_operator(node)
                result_string += " " + operator + " "
                eval_string += " " + operator + " "
        return result_string, eval_string
    
    def interpret(self, parsed_data: lark.Tree):
        result_string, result = self.interpret_statement(parsed_data)
        print(result_string, "=", result)