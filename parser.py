from lark import Lark

class Parser():
    def __init__(self):
        grammar = """
            statement: (modifier (function)* operator)? dice_throw ((operator dice_throw)|function)*
            dice_throw: n_rolls "d" n_faces
            
            minus: /-/
            mod_num: NUMBER

            modifier: minus? mod_num
            function: operator modifier

            operator: /(\\*\\*)|[-+*\\/]/


            n_rolls: INT?
            n_faces: INT

            %import common.WS
            %import common.INT
            %import common.SIGNED_NUMBER
            %import common.NUMBER
            %ignore WS
        """
        self.x = Lark(grammar, start="statement")

    def parse(self, statement):
        parsed = self.x.parse(statement)
        print(parsed.pretty())
        return parsed

    def lexer(self, statement):
        pass
