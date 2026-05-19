from parser import Parser
from interpreter import Interpreter
from lark.exceptions import UnexpectedToken, UnexpectedCharacters, UnexpectedEOF

def main():
    parser = Parser()
    interpreter = Interpreter()

    print("Welcome to Dice notatIon interprEter pro!")

    while True:
        try:
            statement = input("Enter your dice notation: ")
            if statement.lower() in ["exit", "quit"]:
                break
            if not statement:
                print("ERROR: The statement is empty.")
                continue
            parsed_data = parser.parse(statement)
            interpreter.interpret(parsed_data)
        except UnexpectedToken as e:
            print(f"ERROR: Unexpected token '{e.token.value}', line {e.line}, column {e.column}")
            print(f"Expected tokens: {", ".join(e.expected)}")
        except UnexpectedEOF as e:
            print(f"ERROR: Input ended, but parser still expected tokens: {", ".join(e.expected)}")
        except UnexpectedCharacters as e:
            print(f"ERROR: Illegal character '{e.char}' at line {e.line}, column {e.column}")
        except ZeroDivisionError:
            print("ERROR: Trying to divide by zero")
        except Exception as e:
            print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main()