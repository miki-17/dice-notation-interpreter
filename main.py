from parser import Parser
from interpreter import Interpreter
from lark.exceptions import UnexpectedToken, UnexpectedCharacters, UnexpectedEOF

def translate_tokens(tokens):
    tokens_translated = []
    for token in tokens:
        if token.startswith("__ANON_"):
            tokens_translated.append("Special character / Modifier")
        else:
            tokens_translated.append(token)
    return list(set(tokens_translated))



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
            tokens = translate_tokens(e.expected)
            print(f"ERROR: Unexpected token '{e.token.value}' at column {e.column}")
            print(f"Expected tokens:\n {", ".join(tokens)}")
        except UnexpectedEOF as e:
            tokens = translate_tokens(e.expected)
            print(f"ERROR: Input ended, but parser still expected tokens:\n {", ".join(tokens)}")
        except UnexpectedCharacters as e:
            print(f"ERROR: Illegal character '{e.char}' at column {e.column}")
        except ZeroDivisionError:
            print("ERROR: Trying to divide by zero")
        except Exception as e:
            print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main()