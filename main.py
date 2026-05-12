from parser import Parser

def main():
    p = Parser()

    print("Welcome to Dice notatIon interprEter pro!")

    while True:
        txt = input("Enter your dice notation: ")
        p.parse(txt)

if __name__ == "__main__":
    main()