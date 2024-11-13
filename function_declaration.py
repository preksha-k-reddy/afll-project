import ply.lex as lex
import ply.yacc as yacc

# Token definitions
tokens = ['FUNCTION', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'IDENTIFIER', 'SEMICOLON']

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'

# Reserved words
reserved = {
    'function': 'FUNCTION'
}

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_COMMENT(t):
    r'//.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
def p_function_declaration(p):
    '''function_declaration : FUNCTION IDENTIFIER LPAREN parameter_list RPAREN block'''
    p[0] = "Valid"

def p_parameter_list(p):
    '''parameter_list : IDENTIFIER
                      | parameter_list COMMA IDENTIFIER
                      | empty'''
    pass

def p_block(p):
    '''block : LBRACE statement_list RBRACE'''
    pass

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | empty'''
    pass

def p_statement(p):
    '''statement : IDENTIFIER SEMICOLON'''
    pass

def p_empty(p):
    'empty :'
    pass

# Global variable to track errors
error_found = False

def p_error(p):
    global error_found
    error_found = True

# Build the parser
parser = yacc.yacc()

# Test data
test_code = """
function hello(a, b {
    // function body
}
"""

# Parse the input and print "Valid" or "Invalid" based on the result
error_found = False  # Reset error flag before parsing
result = parser.parse(test_code)
if error_found:
    print("Invalid")
else:
    print("Valid")
