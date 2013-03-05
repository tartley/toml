import datetime
import logging

from ply import lex, yacc


logging.basicConfig(format='%(message)s', level=logging.WARN)


class TomlParser():

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)
        self.result = {}
        self.group = None

    # ---- lexing rules

    tokens = (
        'DATE', 'GROUP', 'NAME','INTEGER', 'STRING',
    )

    literals = ['=', '[', ']', ","]

    t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'


    def t_DATE(self, token):
        r'(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)Z'
        token.value = datetime.datetime(
            int(token.value[0:4]), # year
            int(token.value[5:7]), # month
            int(token.value[8:10]), # date
            int(token.value[11:13]), # hour
            int(token.value[14:16]), # minute
            int(token.value[17:19]), # second
        )
        return token

    def t_INTEGER(self, token):
        r'\d+'
        logging.info(token)
        token.value = int(token.value)
        return token

    def t_STRING(self, token):
        r'".*"'
        token.value = token.value[1:-1]
        return token

    def t_whitespace(self, token):
        r'\ +'
        # TODO: can this go back to being simple string declaration?
        pass

    def t_GROUP(self, token):
        r'^\[[^.]+\]'
        logging.info('GROUP %s', token)
        token.value = token.value[1:-1]
        self.group = token.value
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

    def p_statements(self, p):
        '''
        statements :
                   | statement
                   | statements statement
        '''
        logging.info('statements %s', [i for i in p])
        if len(p) == 1:
            pass
            #p[0] = {}
        elif len(p) == 2:
            pass
            #p[0] = p[1]
        elif len(p) == 3:
            pass
            #p[0] = p[1]
            #p[0].update(p[2])
        else:
            raise RuntimeError('how did we get here?')


    def p_statement(self, p):
        '''
        statement : assignment
                  | GROUP
        '''
        logging.info('statement %s %s %s', p, vars(p), [i for i in p])
        if isinstance(p[1], str):
            # group
            self.group = p[1]
            self.result[self.group] = {}
        else:
            # assignment
            if self.group:
                self.result[self.group].update(p[1])
            else:
                self.result.update(p[1])


    def p_assignment(self, p):
        '''
        assignment : NAME "=" value
        '''
        logging.info('assignment %s', [i for i in p])
        p[0] = {p[1]: p[3]}


    def p_value(self, p):
        '''
        value : DATE
              | INTEGER
              | STRING
              | array
        '''
        p[0] = p[1]


    def p_array(self, p):
        '''
        array : "[" values "]"
        '''
        logging.info('array %s', [i for i in p])
        p[0] = p[2]


    def p_values(self, p):
        '''
        values :
               | value
               | values "," value
        '''
        logging.info('values %s', [i for i in p])
        if len(p) == 1:
            p[0] = []
        elif len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            raise RuntimeError('how did we get here?')


    def p_error(self, p):
        if p is None:
            raise SyntaxError("Syntax error at EOF")
        else:
            raise SyntaxError(
                "Syntax error at '%s', line %d" % (p.value, p.lexer.lineno)
            )


    def parse(self, text):
        self.parser.parse(text, lexer=self.lexer)
        return self.result



def loads(text):
    return TomlParser().parse(text)

