import ply.lex as lex
import ply.yacc as yacc

# Lexer rules for tokens
tokens = [
    'FOR', 'CONST', 'ID', 'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'OF',
    'DOT', 'SEMICOLON'
]

# Define reserved words
reserved = {
    'for': 'FOR',
    'const': 'CONST',
    'of': 'OF',
}

# Token definitions
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DOT = r'\.'
t_SEMICOLON = r';'

# Token for ID and reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Ignore whitespace
t_ignore = ' \t\n'

# Handle comments
def t_COMMENT(t):
    r'//.*'
    pass  # Ignore comments

# Error handling for lexer
def t_error(t):
    t.lexer.skip(1)

# Parser rules
def p_program(p):
    'program : for_of_statement'
    p[0] = True  # Return True for a valid program

def p_for_of_statement(p):
    'for_of_statement : FOR LPAREN CONST ID OF ID RPAREN LBRACE statement_list RBRACE'
    p[0] = True  # Return True for a valid for-of statement

def p_statement_list(p):
    '''statement_list : statement statement_list
                      | statement
                      | empty'''
    pass  # No need to handle further details

def p_statement(p):
    'statement : ID DOT ID LPAREN ID RPAREN SEMICOLON'
    pass  # No need to handle further details

def p_empty(p):
    'empty :'
    pass  # Empty production

# Error rule for syntax errors
error_flag = False  # Global flag to control error message printing

def p_error(p):
    global error_flag
    if not error_flag:  # Print "Invalid" only once
        print("Invalid")
        error_flag = True  # Set the flag to avoid multiple prints

# Build lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Single test input for an invalid case
test_code = """
for (const item of items) {
   console.log(item);
}
"""

# Reset error_flag for each parse
error_flag = False

# Parse the input and output result
result = parser.parse(test_code)

# Output result based on the parsing
if result and not error_flag:
    print("Valid")
