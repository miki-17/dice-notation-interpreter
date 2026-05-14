from lark import Lark

class Parser():
    def __init__(self):
        grammar = """
            statement: (modifier (function)* operator)? dice_throw ((operator dice_throw)|function)*
            dice_throw: n_rolls "d" n_faces (explode | extreme | reroll | unique | keep | drop | compare_success | compare_failure | crit | sort)*
            
            minus: /-/
            percent: /%/
            explode: /!/ penetrating? compare?
            fudge: /F/
            penetrating: /p/
            reroll: /ro?/ compare?
            unique: /uo?/ compare?
            keep: keep_type keep_num
            keep_type: /k[hl]?/
            keep_num: INT
            drop: drop_type drop_num
            drop_type: /d[hl]?/
            drop_num: INT
            extreme: (/min/|/max/) extreme_val
            compare_success: compare
            compare_failure: /f/ compare
            compare: compare_symbol compare_number
            compare_symbol: (/[<>][=]?/|/=/|/<>/|/!=/)
            compare_number: SIGNED_NUMBER
            mod_num: NUMBER
            crit: crit_type compare?
            crit_type: /c[sf]/
            sort: /s[ad]?/

            modifier: minus? mod_num
            function: operator modifier

            operator: /(\\*\\*)|[-+*\\/%]/

            extreme_val: INT
            n_rolls: INT?
            n_faces: INT|percent|fudge

            %import common.WS
            %import common.INT
            %import common.SIGNED_NUMBER
            %import common.NUMBER
            %ignore WS
        """
        self.x = Lark(grammar, start="statement")

    def parse(self, statement):
        parsed = self.x.parse(statement)
        print(parsed)
        print(parsed.pretty())
        return parsed

    def lexer(self, statement):
        pass
