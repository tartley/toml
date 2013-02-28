from ply import lex, yacc

class TomlParser():

    # ---- lexing rules

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

    def t_comment(self, token):
        r'\#.*'
        pass


    def t_newline(self, token):
        r'\n+'
        token.lexer.lineno += len(token.value)


    def t_error(self, token):
        print("Illegal character '%s'" % token.value[0])
        token.lexer.skip(1)


    # ------- parsing rules


    def p_document(self, p):
        '''
        document :
                 | assignment
        '''
        if len(p) == 1:
            p[0] = {}
        elif len(p) > 1:
            p[0] = p[1]
        else:
            raise RuntimeError('how did we get here?')


    def p_assignment(self, p):
        'assignment : NAME "=" expression'
        p[0] = {p[1]: p[3]}


    def p_expression_number(self, p):
        "expression : NUMBER"
        p[0] = p[1]


    def p_error(self, p):
        if p is None:
            raise SyntaxError("Syntax error at EOF")
        else:
            raise SyntaxError(
                "Syntax error at '%s', line %d" % (p.value, p.lexer.lineno)
            )


toml_parser = TomlParser()
lexer = lex.lex(module=toml_parser)
parser = yacc.yacc(module=toml_parser)


def loads(text):
    return parser.parse(text, lexer=lexer)










