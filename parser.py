import time
from lark import Lark

#{int}d{int}



class Parser():
    def __init__(self):
        grammar = """
            statement: modifier_back? n_rolls dice n_faces modifier_front?

            modifier_front: add_front | sub_front 
            modifier_back: add_back | sub_back

            add_front: "+" SIGNED_NUMBER
            add_back: SIGNED_NUMBER "+"
            sub_front: "-" SIGNED_NUMBER
            sub_back: SIGNED_NUMBER "-"

            n_rolls: SIGNED_NUMBER?
            dice: "d"
            n_faces: SIGNED_NUMBER

            %import common.WS
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