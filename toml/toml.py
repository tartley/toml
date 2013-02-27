from ply import lex, yacc

class TomlParser():

    def __init__(self):
        lex.lex(module=self)
        yacc.yacc(module=self)

    tokens = (
        'NAME','NUMBER',
    )

    literals = ['=']

    #t_ignore = " \t"

    t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def t_NUMBER(self, token):
        r'\d+'
        token.value = int(token.value)
        return token

    #def t_newline(token):
        #r'\n+'
        #token.lexer.lineno += token.value.count("\n")

    def t_error(self, token):
        print("Illegal character '%s'" % token.value[0])
        token.lexer.skip(1)

    # ------- parsing rules

    def p_statement_assign(self, p):
        'statement : NAME "=" expression'
        if p[0] is None:
            p[0] = {}
        p[0][p[1]] = p[3]

    def p_expression_number(self, p):
        "expression : NUMBER"
        p[0] = p[1]

    def p_error(p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")


    # ------- public entry point

    def parse(self, text):
        return yacc.parse(text)


def loads(text):
    return TomlParser().parse(text)










