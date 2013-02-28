from ply import lex, yacc

class TomlParser():

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)


    # ---- lexing rules

    tokens = (
        'NAME','NUMBER', 'STRING',
    )

    literals = ['=']

    t_ignore = " \t"

    t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'


    def t_NUMBER(self, token):
        r'\d+'
        token.value = int(token.value)
        return token

    def t_STRING(self, token):
        r'".*"'
        token.value = token.value[1:-1]
        return token

    def t_comment(self, token):
        r'\#.*'
        pass

    def t_newline(self, token):
        r'\n+'
        token.lexer.lineno += len(token.value)

    def t_error(self, token):
        raise SyntaxError(
            "Illegal character '%s' at line %d" %
            (token.value[0], token.lexer.lineno)
        )


    # ------- parsing rules

    def p_document(self, p):
        '''
        document :
                 | assignments
        '''
        if len(p) == 1:
            p[0] = {}
        elif len(p) > 1:
            p[0] = p[1]
        else:
            raise RuntimeError('how did we get here?')


    def p_assignments(self, p):
        '''
        assignments : assignment
                    | assignments assignment
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = p[1]
            p[0].update(p[2])
        else:
            raise RuntimeError('how did we get here?')


    def p_assignment(self, p):
        'assignment : NAME "=" value'
        p[0] = {p[1]: p[3]}


    def p_value(self, p):
        '''
        value : NUMBER
              | STRING
        '''
        p[0] = p[1]


    def p_error(self, p):
        if p is None:
            raise SyntaxError("Syntax error at EOF")
        else:
            raise SyntaxError(
                "Syntax error at '%s', line %d" % (p.value, p.lexer.lineno)
            )


    # --------- public API

    def parse(self, text):
        return self.parser.parse(text, lexer=self.lexer)


def loads(text):
    return TomlParser().parse(text)

