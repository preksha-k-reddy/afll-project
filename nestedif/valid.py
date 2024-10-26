import ply.lex as lex
import ply.yacc as yacc

# Lexer rules for tokens
tokens = [
    'ID', 'LBRACE', 'RBRACE', 'NUMBER', 'LESS',
    'LPAREN', 'RPAREN', 'IF', 'SEMICOLON'
]

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LESS = r'<'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'

# Define reserved words
reserved = {
    'if': 'IF',
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
t_ignore = ' \t\n'

# Handle comments
def t_COMMENT(t):
    r'//.*'
    pass  # Ignore comments

# Error handling for lexer
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    lexer.has_error = True  # Set error flag
    t.lexer.skip(1)

# Parser rules
def p_program(p):
    '''program : statement_list'''
    p[0] = True  # Successfully parsed

def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE'''
    p[0] = True  # Valid nested if

def p_statement_simple(p):
    '''statement : ID SEMICOLON'''
    p[0] = True  # Treat any identifier followed by a semicolon as a valid statement

def p_statement_list(p):
    '''statement_list : statement statement_list
                      | statement SEMICOLON statement_list
                      | empty'''
    if len(p) == 3:  # statement statement_list
        p[0] = p[1] and p[2]  # Accumulate validity
    elif len(p) == 2:  # single statement
        p[0] = p[1]  # Single statement
    else:  # empty
        p[0] = True  # Empty statement list is valid


def p_expression(p):
    '''expression : ID LESS NUMBER'''
    p[0] = ('less_than', p[1], p[3])

# Error rule for syntax errors
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Empty production
def p_empty(p):
    'empty :'
    pass

# Build lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Test input for the parser
code = """
if (x < 10) {
    if (y < 5) {
        inner_statement;
    }
}

"""

# Tokenize and check for errors
lexer.input(code)
lexer.has_error = False  # Initialize the error flag

for tok in lexer:
    pass  # Ignore tokens for output

# Parse the input only if there are no lexer errors
if not lexer.has_error:
    result = parser.parse(code)

    # Output result based on the parsing
    if result:
        print("Valid")
    else:
        print("Invalid")
else:
    print("Invalid")

