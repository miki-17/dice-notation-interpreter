import time
from lark import Lark

#{int}d{int}



class Parser():
    def __init__(self):
        grammar = """
            statement: sint

            modifier_front: add_front | sub_front 
            modifier_back: add_back | sub_back

            dice_throw_sub: "-" n_rolls "d" n_faces
            dice_throw_add: "+" n_rolls "d" n_faces

            add_front: "+" SIGNED_NUMBER
            add_back: SIGNED_NUMBER "+"
            sub_front: "-" SIGNED_NUMBER
            sub_back: SIGNED_NUMBER "-"

            sint: ["+"|"-"]
            modifier: SIGNED_NUMBER


            n_rolls: INT?
            n_faces: INT

            %import common.WS
            %import common.INT
            %import common.SIGNED_NUMBER
            %ignore WS
        """
        self.x = Lark(grammar, start="statement")

    def parse(self, statement):
        statement = statement.replace(" ", "")
        print(self.x.parse(statement).pretty())
        st_lexed = self.lexer(statement)
        return st_lexed

    def lexer(self, statement):
        pass