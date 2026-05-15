from lark import Lark

class Parser():
    def __init__(self):
        grammar = """
            statement: value (operator value)*
            value: modifier | dice_throw | opening_bracket statement closing_bracket
            dice_throw: n_rolls "d" n_faces (explode 
                | extreme 
                | reroll 
                | unique 
                | keep 
                | drop 
                | crit 
                | sort)*
            
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
            compare_succ_fail: compare (/f/ compare)?
            compare: compare_symbol compare_number
            compare_symbol: (/[<>][=]?/|/=/|/<>/|/!=/)
            compare_number: SIGNED_NUMBER
            mod_num: NUMBER
            crit: crit_type compare?
            crit_type: /c[sf]/
            sort: /s[ad]?/
            opening_bracket: /\\(/
            closing_bracket: /\\)/
            math_num: SIGNED_NUMBER

            modifier: (minus? mod_num) 
                | sin 
                | cos 
                | tan 
                | cot

            operator: /(\\*\\*)|[-+*\\/%]/

            sin: /sin\\(/ math_num /\\)/
            cos: /cos\\(/ math_num /\\)/
            tan: /tan\\(/ math_num /\\)/
            cot: /cot\\(/ math_num /\\)/

            extreme_val: INT
            n_rolls: INT?
            n_faces: INT
                | percent
                | fudge

            %import common.WS
            %import common.INT
            %import common.SIGNED_NUMBER
            %import common.NUMBER
            %ignore WS
        """
        self.lexer = Lark(grammar, start="statement")

    def parse(self, statement):
        parsed = self.lexer.parse(statement)
        return parsed

    # def lexer(self, statement):
    #     pass
