import ply.lex as lex
import ply.yacc as yacc

# Define tokens
tokens = [
    'FUNCTION', 'IDENTIFIER', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'COMMA', 'SEMICOLON', 'ASSIGN', 'NUMBER', 'STRING', 'PLUS', 'RETURN', 'LET'
]

# Token patterns for single-character tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_PLUS = r'\+'

# Keywords
keywords = {
    'function': 'FUNCTION',
    'return': 'RETURN',
    'let': 'LET',
}

# Identifier and keywords
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"'
    return t

# Ignored characters
t_ignore = ' \t\n'

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
def p_program(p):
    '''program : function_definition'''
    p[0] = p[1]

def p_function_definition(p):
    '''function_definition : FUNCTION IDENTIFIER LPAREN parameter_list RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('function_definition', p[2], p[4], p[7])

# Parameter list
def p_parameter_list(p):
    '''parameter_list : IDENTIFIER
                      | IDENTIFIER COMMA parameter_list
                      | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) > 2:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []

# Statement list
def p_statement_list(p):
    '''statement_list : statement
                      | statement statement_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

# Statements for variable declaration and return
def p_statement(p):
    '''statement : LET IDENTIFIER ASSIGN expression SEMICOLON
                 | RETURN expression SEMICOLON'''
    if p[1] == 'let':
        p[0] = ('let', p[2], p[4])
    else:
        p[0] = ('return', p[2])

# Expression rules
def p_expression(p):
    '''expression : IDENTIFIER
                  | STRING
                  | expression PLUS expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('plus', p[1], p[3])

# Empty production
def p_empty(p):
    '''empty :'''
    p[0] = None

# Track if an error has occurred
error_occurred = False

# Syntax error handling
def p_error(p):
    global error_occurred
    if not error_occurred:
        print("Invalid")
        error_occurred = True

# Build the parser
parser = yacc.yacc()

# Test the parser
js_code = """
function greet(name{
    let message = "Hello, " + name;
    return message;
}
"""

# Reset error_occurred before parsing
error_occurred = False
result = parser.parse(js_code, lexer=lexer)

# Output result based on parsing success
if not error_occurred:
    print("Valid")
