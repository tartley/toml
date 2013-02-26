from ply import yacc


# Public outermost function,
# only system tested, not unit tested
def loads(string):
    return yacc.parse(string)

