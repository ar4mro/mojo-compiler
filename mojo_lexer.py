# -----------------------------------------------------------------------------
# mojo_lexer.py
#
# A simple lexer for the mojo language.
# -----------------------------------------------------------------------------

import ply.lex as lex

# Reserved words
reserved = {
    'program': 'PROGRAM',
    'if': 'IF',
    'else': 'ELSE',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
    'bool': 'BOOLEAN',
    'void': 'VOID',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'input' : 'READ',
    'print' : 'PRINT',
    'def' : 'DEF',
    'while' : 'WHILE',
    'main' : 'MAIN',
    'return' : 'RETURN',
    'True' : 'TRUE',
    'False' : 'FALSE',

    # Predefined functions
    'create_turtle' : 'CREATE_TURTLE',
    'reset' : 'RESET',
    'pen_up' : 'PEN_UP',
    'pen_down' : 'PEN_DOWN',
    'pick_color' : 'PICK_COLOR',
    'set_line_width' : 'SET_LINE_WIDTH',
    'move_forward' : 'MOVE_FORWARD',
    'move_right' : 'MOVE_RIGHT',
    'move_left' : 'MOVE_LEFT',
    'turn_right' : 'TURN_RIGHT',
    'turn_left' : 'TURN_LEFT',
    'draw_line' : 'DRAW_LINE',
    'draw_square' : 'DRAW_SQUARE',
    'draw_triangle' : 'DRAW_TRIANGLE',
    'draw_circle' : 'DRAW_CIRCLE',
    'draw_rectangle' : 'DRAW_RECTANGLE'
}

# Token list (Tuple)
tokens = list(reserved.values()) + [
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'COLON',
    'SEMICOLON',
    'COMMA',
    'GT',
    'LT',
    'LE',
    'GE',
    'EQ',
    'NE',
    'ASSIGN',
    'ICONST',
    'FCONST',
    'SCONST'
]

# Regular expressions for each token
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE= r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
t_ASSIGN = r'='
t_SCONST = r'\".*\" | \'.*\''

# Characteres that will be ignored
t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verifies that is not a reserved word
    t.type = reserved.get(t.value, 'ID')
    return t

def t_FCONST(t):
    r'-?[0-9]+\.[0-9][0-9]*'
    return t

def t_ICONST(t):
    r'-?[0-9]+'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error lexico
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Runs lex
mojo_lexer = lex.lex()
input_data = ''
mojo_lexer.input(input_data)

while True:
    token = mojo_lexer.token()
    if not token:
        break
    print(token)
