from parser import Parser
from interpreter import Interpreter

def main():
    parser = Parser()
    interpreter = Interpreter()

    print("Welcome to Dice notatIon interprEter pro!")

    while True:
        statement = input("Enter your dice notation: ")
        parsed_data = parser.parse(statement)
        interpreter.interpret(parsed_data)

if __name__ == "__main__":
    main()