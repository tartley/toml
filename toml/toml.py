from datetime import datetime
import logging
import sys

from ply import lex, yacc


logging.basicConfig(format='%(message)s', level=logging.INFO)


# TODO split out lexer, parser into differnt classes in different modules


class TomlParser():

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

        # the final accumulated result of parsing the given TOML
        self.result = {}

        # sequence of nested subgroup names
        # e.g. "[a.b]" represented as ['a', 'b']
        self.current_group = []

        self.errors = []

    # ---- lexing rules

    tokens = (
        'DATETIME',
        'GROUP',
        'KEY',
        'INTEGER',
        'STRING',
        'NEWLINE',
        'BOOLEAN',
    )

    literals = '=[],'

    t_ignore = ' \t'


    def t_DATETIME(self, token):
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'
        token.value = datetime.strptime(token.value, "%Y-%m-%dT%H:%M:%SZ")
        return token

    def t_INTEGER(self, token):
        r'\d+'
        token.value = int(token.value)
        return token

    def t_STRING(self, token):
        r'"(\\"|[^"\n])*"'
        logging.info('STRING %s', token)
        token.value = token.value[1:-1].encode('utf-8').decode('unicode_escape')
        return token

    def t_comment(self, token):
        r'\#.*'
        pass

    def t_BOOLEAN(self, token):
        r'true|false'
        logging.info('BOOL %s', token)
        token.value = token.value == 'true'
        return token

    def t_KEY(self, token):
        r'[a-zA-Z_][a-zA-Z0-9_#\?]*'
        return token

    def t_GROUP(self, token):
        r'\[[a-zA-Z_][a-zA-Z0-9_#?.]*\]'
        logging.info('GROUP %s', token)
        token.value = token.value[1:-1].split('.')
        return token

    def t_NEWLINE(self, token):
        r'\n+'
        token.lexer.lineno += len(token.value)
        return token

    def t_error(self, token):
        raise SyntaxError(
            "Illegal character %r at line %d" %
            (token.value[0], token.lexer.lineno)
        )


    # ------- parsing rules

    def _flag_error(self, message, line):
        message = 'Line %d: %s' % (line, message)
        self.errors.append(message)
        print(message, file=sys.stderr)
        raise SyntaxError(message)


    def p_statements(self, p):
        '''
        statements :
                   | statement
                   | NEWLINE statements
                   | statement NEWLINE statements
        '''
        pass


    def _get_namespace(self, name_parts):
        '''
        name_parts is list of namespace names
        return self.results[part1][part2][part3]...
        '''
        logging.info('get_namespace %s', name_parts)
        dict_to_update = self.result
        for part in name_parts:
            dict_to_update = dict_to_update.setdefault(part, {})
            assert isinstance(dict_to_update, dict)
        logging.info(str(dict_to_update is self.result))
        return dict_to_update


    def _update_dict(self, dict_to_update, key, value, line_no):
        if key in dict_to_update:
            self._flag_error("Duplicate key '%s'" % key, line_no)
        dict_to_update[key] = value


    def p_statement(self, p):
        '''
        statement : assignment
        '''
        logging.info('statement assignment %s ', [i for i in p])
        key, value = p[1]
        self._update_dict(
            self._get_namespace(self.current_group),
            key, value, p.lineno(1))

    def p_statement_group(self, p):
        '''
        statement : GROUP
        '''
        logging.info('statement GROUP %s ', [i for i in p])
        logging.info('statement.GROUP %s', p[1])
        self.current_group = p[1]
        self._update_dict(
            self._get_namespace(self.current_group[:-1]),
            self.current_group[-1],
            {},
            p.lineno(1))


    def p_assignment(self, p):
        '''
        assignment : KEY "=" value
        '''
        logging.info('assignment %s', [i for i in p])
        p[0] = (p[1], p[3])


    def p_value(self, p):
        '''
        value : DATETIME
              | INTEGER
              | STRING
              | BOOLEAN
              | array
        '''
        p[0] = p[1]


    def p_array(self, p):
        '''
        array : "[" values "]"
        '''
        logging.info('array %s', [i for i in p])
        p[0] = p[2]


    def p_values_empty(self, p):
        '''
        values :
        '''
        logging.info('values_empty %s', [i for i in p])
        p[0] = []

    def p_values_single(self, p):
        '''
        values : value
        '''
        logging.info('values_single %s', [i for i in p])
        p[0] = [p[1]]

    def p_values_multiple(self, p):
        '''
        values : value "," values
        '''
        logging.info('values_multiple %s', [i for i in p])
        p[0] = [p[1]]
        p[0].extend(p[3])


    def p_error(self, p):
        if p is None:
            raise SyntaxError("Syntax error at EOF")
        else:
            raise SyntaxError(
                "Syntax error at %r, line %d" % (p.value, p.lexer.lineno)
            )


    def parse(self, text):
        # TODO return return value instead of accumulated result
        self.parser.parse(text, lexer=self.lexer)
        if self.errors:
            raise SyntaxError(  
                '%d errors:\n' % len(self.errors) +
                '\n'.join(self.errors)
            )
        return self.result


def loads(text):
    return TomlParser().parse(text)

