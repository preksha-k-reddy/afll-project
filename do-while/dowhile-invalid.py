# Lexer rules for tokens
tokens = [
    'ID', 'LBRACE', 'RBRACE', 'EQUALS', 'PLUS', 'NUMBER', 'SEMICOLON', 'LESS',
    'LPAREN', 'RPAREN', 'DO', 'WHILE'
]

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_EQUALS = r'='
t_PLUS = r'\+'
t_SEMICOLON = r';'
t_LESS = r'<'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Define reserved words
reserved = {
    'do': 'DO',
    'while': 'WHILE'
}

# Token for ID and reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Token for numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignore whitespace
t_ignore = ' \t'

# Error handling for lexer
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Parser rules
def p_do_while_statement(p):
    '''do_while_statement : DO LBRACE statement RBRACE WHILE LPAREN expression RPAREN SEMICOLON'''
    p[0] = ('do_while', p[3], p[7])

def p_statement(p):
    '''statement : ID EQUALS ID PLUS NUMBER SEMICOLON'''
    p[0] = ('assign', p[1], p[3], p[5])

def p_expression(p):
    '''expression : ID LESS NUMBER'''
    p[0] = ('less_than', p[1], p[3])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error")
    raise ValueError("Invalid")

# Build lexer and parser
import ply.lex as lex
import ply.yacc as yacc
lexer = lex.lex()
parser = yacc.yacc(start='do_while_statement')

# Test input
code = "do { x = x + 1; while (x < 10);"  # invalid case

# Tokenize and parse
lexer.input(code)

# Try parsing and catching errors
try:
    parser.parse(code)
    print("Valid")
except ValueError:
    print("Invalid")
