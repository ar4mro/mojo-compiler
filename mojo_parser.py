# -----------------------------------------------------------------------------
# mojo_parser.py
#
# A simple parser for the mojo language.
# -----------------------------------------------------------------------------

### LIST OF ACTIONS ###
# Embedded actions not part of the syntax
# cfd_action -> Create function directory
# adv_action -> Add a variable to the current function
# adf_action -> Adds a new function to the directory

import sys
import ply.yacc as yacc

from mojo_lexer import tokens
from helpers.program import Program

my_program = Program()

def p_program(p):
    '''program : PROGRAM ID cfd_action SEMICOLON vars functions MAIN block'''
    print('Syntax correct')

# Creates the function directory
def p_cfd_action(p):
    '''cfd_action : '''
    my_program.global_scope = p[-1]
    my_program.current_scope = p[-1]
    # Adds the program, global scope, to the directory
    my_program.function_directory.add_function('void', my_program.global_scope)

def p_vars(p):
    '''vars : VAR ID list_declaration more_vars COLON type adv_action SEMICOLON vars
            | empty'''


def p_list_declaration(p):
    '''list_declaration : LBRACKET exp RBRACKET
                        | empty'''

def p_more_vars(p):
    '''more_vars : COMMA ID more_vars
                 | empty'''
    # Stores the variables found in the temporal list
    if p[-1] is not None:
        variable_name = p[-1]
        my_program.temporal_variables.append(variable_name)

# Adds the variable to the current function
def p_adv_action(p):
    '''adv_action : '''
    variable_type = p[-1]
    variable_name = p[-5]
    my_program.temporal_variables.append(variable_name)

    # Adds all the variables declared in the line to the function
    for variable in my_program.temporal_variables:
        my_program.function_directory.add_variabe_to_function(
                my_program.current_scope, variable_type, variable)

    # Clears the list of temporal variables to start a new line of declarations
    del my_program.temporal_variables[:]

def p_functions(p):
    '''functions : DEF function_type ID LPAREN parameters RPAREN adf_action block functions
                 | empty'''

def p_function_type(p):
    '''function_type : type
                     | VOID'''
    p[0] = p[1]

def p_parameters(p):
    '''parameters : type ID more_parameters
                  | empty'''

def p_more_parameters(p):
    '''more_parameters : COMMA type ID more_parameters
                       | empty'''
    # Stores the types parameters found in the temporal list, parameters
    # are found from the last one to the first one, they need to be inserted
    # in the first index to keep the order
    if p[-1] is not None:
        parameter_type = p[-2]
        my_program.temporal_parameters.insert(0, parameter_type)

def p_type(p):
    '''type : INT
            | FLOAT
            | STRING
            | BOOLEAN'''
    p[0] = p[1]

# Adds a new function and its parameters to the directory
def p_adf_action(p):
    '''adf_action : '''
    # Determines the name of the function and its type
    my_program.current_scope = p[-4]
    function_type = p[-5]

    # Adds the function to the directory
    my_program.function_directory.add_function(function_type, my_program.current_scope)

    # Adds the parameters to the function
    my_program.function_directory.add_parameter_to_function(my_program.current_scope,
            list(my_program.temporal_parameters))

    # Cleras the temporal parameters
    del my_program.temporal_parameters[:]

def p_block(p):
    '''block : LBRACE vars statements RBRACE'''

def p_statements(p):
    '''statements : statement statements
                  | empty'''

def p_statement(p):
    '''statement : assignment
                 | condition
                 | write
                 | loop
                 | function_call
                 | predefined_function_call
                 | return'''

def p_assignment(p):
    '''assignment : ID list_assignment ASSIGN super_expression SEMICOLON'''

def p_list_assignment(p):
    '''list_assignment : LBRACKET exp RBRACKET
                       | empty'''

def p_condition(p):
    '''condition : IF LPAREN super_expression RPAREN block else'''

def p_else(p):
    '''else : ELSE block
            | empty'''

def p_super_expression(p):
    '''super_expression : negation expression
                        | negation expression AND negation expression
                        | negation expression OR negation expression'''

def p_negation(p):
    '''negation : NOT
                | empty'''

def p_expression(p):
    '''expression : exp
                  | exp GT exp
                  | exp LT exp
                  | exp LE exp
                  | exp GE exp
                  | exp EQ exp
                  | exp NE exp'''

def p_exp(p):
    '''exp : term
           | term PLUS exp
           | term MINUS exp'''

def p_term(p):
    '''term : factor
            | factor TIMES term
            | factor DIVIDE term'''

def p_factor(p):
    '''factor : LPAREN super_expression RPAREN
              | var_const'''

def p_var_const(p):
    '''var_const : ID list_call
                 | ICONST
                 | FCONST
                 | SCONST
                 | boolean_value
                 | function_call'''

def p_boolean_value(p):
    '''boolean_value : TRUE
                     | FALSE'''

def p_list_call(p):
    '''list_call : LBRACKET exp RBRACKET
                 | empty'''

def p_loop(p):
    '''loop : WHILE LPAREN super_expression RPAREN block'''

def p_function_call(p):
    '''function_call : ID LPAREN arguments RPAREN'''

def p_arguments(p):
    '''arguments : var_const more_arguments
                 | empty'''

def p_more_arguments(p):
    '''more_arguments : COMMA var_const more_arguments
                      | empty'''

def p_predefined_function_call(p):
    '''predefined_function_call : CREATE_TURTLE LPAREN RPAREN SEMICOLON
                                | RESET LPAREN RPAREN SEMICOLON
                                | PEN_UP LPAREN RPAREN SEMICOLON
                                | PEN_DOWN LPAREN RPAREN SEMICOLON
                                | PICK_COLOR LPAREN SCONST RPAREN SEMICOLON
                                | SET_LINE_WIDTH LPAREN exp RPAREN SEMICOLON
                                | MOVE_FORWARD LPAREN exp RPAREN SEMICOLON
                                | MOVE_RIGHT LPAREN exp RPAREN SEMICOLON
                                | MOVE_LEFT LPAREN exp RPAREN SEMICOLON
                                | TURN_RIGHT LPAREN exp RPAREN SEMICOLON
                                | TURN_LEFT LPAREN exp RPAREN SEMICOLON
                                | DRAW_LINE LPAREN exp RPAREN SEMICOLON
                                | DRAW_SQUARE LPAREN exp RPAREN SEMICOLON
                                | DRAW_TRIANGLE LPAREN exp RPAREN SEMICOLON
                                | DRAW_CIRCLE LPAREN exp RPAREN SEMICOLON
                                | DRAW_RECTANGLE LPAREN exp RPAREN SEMICOLON'''

def p_return(p):
    '''return : RETURN super_expression SEMICOLON'''

def p_write(p):
    '''write : PRINT LPAREN super_expression RPAREN SEMICOLON'''

def p_empty(p):
    '''empty : '''

def p_error(p):
    print('Syntax error at input line {0}'.format(p.lexer.lineno))
    sys.exit()

def make_parser():
    parser = yacc.yacc()

    #print("Name of the file to be parsed")
    #file_name = input()
    file_name = 'code_test.txt'

    with open(file_name) as file_object:
        code = file_object.read()
        parser.parse(code)

    my_program.function_directory.print_directory()
    #print(str(my_program.temporal_parameters))

    return parser

make_parser()
