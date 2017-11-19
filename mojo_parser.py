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
# amf_action -> Adds the main function to the directory
# pio_action -> Push a variable operand to the stack
# pfo_action -> Push float operand to the stack
# pso_action -> Push string operand to the stack
# pbo_action -> Push boolean operand to the stack
# pid_action -> Push id operand to stack
# pop_action -> Push an operator to its stack
# sot_action -> Solve term
# sof_action -> Solve factor
# sor_action -> Solve relational operations
# sol_action -> Solve logical operations
# soa_action -> Solve assignment
# abm_action -> Add bottom mark
# rbm_action -> Remove bottom mark
# cif_action -> Create if conditional quadruple
# sif_action -> Solve if conditional quadruple
# cel_action -> Create else quadruple
# cwl_action -> Creates the while quadruple
# cwr_action -> Creates the write quadruple
# swl_action -> Solves the while quadruple
# enp_action -> Ends the procedure closing with a quadruple and solve returns
# cra_action -> Creates de era quadruple action
# sar_action -> Solve argument
# sfc_action -> Solve function call
# srf_action -> Sets on the return flag and creates its quadruples
# vtc_action -> Verifies the type of the procedure call
# arf_action -> Adds the result of the function to the stack
# cmq_action -> Creates the main quadruple GoTo action

import sys
import ply.yacc as yacc

from mojo_lexer import tokens
from helpers.program import Program
from helpers.quadruple import Quadruple
from helpers.virtual_machine import VirtualMachine

my_program = Program()

# Parsing rules
def p_program(p):
    '''program : PROGRAM ID cmq_action cfd_action SEMICOLON vars functions MAIN amf_action block'''
    print('Syntax correct')

# Creates the main quadruple GoTo action
def p_cmq_action(p):
    '''cmq_action : '''
    quadruple = Quadruple(my_program.quadruple_number, 'GOTO', 'MAIN', None, None)
    my_program.quadruple_list.append(quadruple)
    my_program.quadruple_number += 1

# Creates the function directory
def p_cfd_action(p):
    '''cfd_action : '''
    my_program.global_scope = p[-2]
    my_program.current_scope = p[-2]

    # Adds the program, the global scope, to the directory
    my_program.function_directory.add_function(my_program.global_scope, 'void')

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
    my_program.temporal_variables.reverse()

    # Adds all the variables declared in the line to the function
    for variable in my_program.temporal_variables:
        # Request the addresses depending of the scope
        if my_program.current_scope == my_program.global_scope:
            variable_address = my_program.memory.request_global_address(variable_type)
        else:
            variable_address = my_program.memory.request_local_address(variable_type)

        my_program.function_directory.add_variable_to_function(
                my_program.current_scope, variable_type, variable, variable_address)

    # Clears the list of temporal variables to start a new line of declarations
    del my_program.temporal_variables[:]

def p_functions(p):
    '''functions : DEF function_type ID LPAREN parameters RPAREN adf_action block enp_action functions
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
        parameter_name = p[-1]
        parameter_type = p[-2]
        my_program.temporal_parameters_names.insert(0, parameter_name)
        my_program.temporal_parameters_types.insert(0, parameter_type)

def p_type(p):
    '''type : INT
            | FLOAT
            | STRING
            | BOOLEAN'''
    p[0] = p[1]

# Adds a new function and its parameters to the directory
def p_adf_action(p):
    '''adf_action : '''
    ### 1. Need to separate space in the global memory for the return value if its
    ### not a void function, the whole function acts like a variable in te global memory
    ### 2. Validate the te funcion hasn't been declared yet

    # Determines the name of the function and its type
    my_program.current_scope = p[-4]
    function_type = p[-5]
    parameter_adresses_list = []

    # Adds the function to the directory
    my_program.function_directory.add_function(my_program.current_scope, function_type)

    # Sets the starting quadruple of the function
    my_program.function_directory.set_function_quadruple_number(my_program.current_scope,
        my_program.quadruple_number)

    if function_type != 'void':
        # Sets the address return of the function
        function_address = my_program.memory.request_global_address(function_type)
        my_program.function_directory.set_function_address(my_program.current_scope,
            function_address)

    # Adds the parameters to the function variable table
    parameters = zip(my_program.temporal_parameters_names,
        my_program.temporal_parameters_types)

    for parameter_name, parameter_type in parameters:
        parameter_adress = my_program.memory.request_local_address(parameter_type)
        parameter_adresses_list.append(parameter_adress)
        my_program.function_directory.add_variable_to_function(
                my_program.current_scope, parameter_type, parameter_name, parameter_adress)

    # Adds the parameters signature to the function
    my_program.function_directory.add_parameter_to_function(my_program.current_scope,
            list(my_program.temporal_parameters_types), list(parameter_adresses_list))

    # Clears the temporal parameters
    del my_program.temporal_parameters_names[:]
    del my_program.temporal_parameters_types[:]

# Creates the quadruple that indicates the end of the procedure
def p_enp_action(p):
    '''enp_action : '''
    function_type = p[-7]

    # Checks if the functions and procedures have the correct return semantics
    if function_type == 'void' and my_program.return_flag:
        print('Function {0} of type {1} should not have return statement.'.format(
            my_program.current_scope, function_type))
        sys.exit()
    elif function_type != 'void' and not my_program.return_flag:
        print('Function {0} of type {1} should have return statement.'.format(
            my_program.current_scope, function_type))
        sys.exit()
    else:
        # Creates the end of function quadruple
        quadruple = Quadruple(my_program.quadruple_number, 'ENDPROC', None, None, None)
        my_program.quadruple_list.append(quadruple)

    # Fills the returns quadruples if exist
    if my_program.return_flag:
        while my_program.return_list:
            quadruple_number_to_fill = my_program.return_list.pop()
            my_program.quadruple_list[quadruple_number_to_fill - 1].fill_quadruple_jump(
                my_program.quadruple_number)

    my_program.quadruple_number += 1
    my_program.return_flag = False

    # Reset the temporal memory
    my_program.memory.reset_temporal_memory()

# Adds the main function to function directory
def p_amf_action(p):
    '''amf_action : '''
    my_program.current_scope = p[-1]
    my_program.function_directory.add_function(my_program.current_scope, 'void')
    my_program.function_directory.set_function_quadruple_number(my_program.current_scope,
        my_program.quadruple_number)

    # Fills the quadruple jump number of the program to the main function
    quadruple = my_program.quadruple_list[0]
    quadruple.fill_quadruple_jump(my_program.quadruple_number)

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
                 | procedure_call
                 | predefined_function_call
                 | return'''

def p_assignment(p):
    '''assignment : ID pid_action list_assignment ASSIGN pop_action super_expression SEMICOLON soa_action'''

def p_list_assignment(p):
    '''list_assignment : LBRACKET exp RBRACKET
                       | empty'''

# Solves the assignment and creates its quadruple
def p_soa_action(p):
    '''soa_action : '''
    # Gets the operator
    operator = my_program.operator_stack.pop()

    if operator == '=':
        # Gets the operands and its types
        right_operand = my_program.operand_stack.pop()
        right_type = my_program.type_stack.pop()
        left_operand = my_program.operand_stack.pop()
        left_type = my_program.type_stack.pop()

        # Gets the type of the result
        result_type = my_program.semantic_cube.get_semantic_type(left_type ,
            right_type, operator)

        if result_type != 'error':
            # Creates the quadruple
            quadruple = Quadruple(my_program.quadruple_number, operator,
                right_operand, None , left_operand)

            # Adds the quadruple to its list and increments the counter
            my_program.quadruple_list.append(quadruple)
            my_program.quadruple_number += 1
        else:
            print('Operation type mismatch at {0}'.format(p.lexer.lineno))
            sys.exit()

def p_condition(p):
    '''condition : IF LPAREN super_expression RPAREN cif_action block else sif_action'''

# Create if conditional quadruple action
def p_cif_action(p):
    '''cif_action : '''
    create_conditional_quadruple(p)

def p_else(p):
    '''else : ELSE cel_action block
            | empty'''

# Create else quadruple
def p_cel_action(p):
    '''cel_action : '''
    # Creates the GoTo quadruple
    quadruple = Quadruple(my_program.quadruple_number, 'GOTO', None, None, None)
    my_program.quadruple_list.append(quadruple)

    # Gets the number of the GotoF quadruple to be filled
    quadruple_number_to_fill = my_program.jump_list.pop()
    quadruple = my_program.quadruple_list[quadruple_number_to_fill]

    # Stores the actual quadruple_number GoTo in the jump list
    my_program.jump_list.append(my_program.quadruple_number - 1)
    my_program.quadruple_number += 1

    # Fills the pending GoToF quadruple with the number of the next quadruple
    # after GoTo was created
    quadruple.fill_quadruple_jump(my_program.quadruple_number)

# Fills the pending GoToF quadruples
def p_sif_action(p):
    '''sif_action : '''
    # Gets the number of the GotoF quadruple to be filled
    quadruple_number_to_fill = my_program.jump_list.pop()
    quadruple = my_program.quadruple_list[quadruple_number_to_fill]

    # Fills the pending GoToF quadruple with the number of the next quadruple
    quadruple.fill_quadruple_jump(my_program.quadruple_number)

def p_super_expression(p):
    '''super_expression : negation expression sol_action
                        | negation expression sol_action AND pop_action negation super_expression
                        | negation expression sol_action OR pop_action negation super_expression'''

# Solve logical operations
def p_sol_action(p):
    '''sol_action : '''
    if len(my_program.operator_stack) > 0 and len(my_program.operand_stack) > 1:
        if my_program.operator_stack[-1] == 'and' or my_program.operator_stack[-1] == 'or':
            solve_operation(p)

def p_negation(p):
    '''negation : NOT
                | empty'''

def p_expression(p):
    '''expression : exp sor_action
                  | exp GT pop_action exp sor_action
                  | exp LT pop_action exp sor_action
                  | exp LE pop_action exp sor_action
                  | exp GE pop_action exp sor_action
                  | exp EQ pop_action exp sor_action
                  | exp NE pop_action exp sor_action'''

# Solve relational operations
def p_sor_action(p):
    '''sor_action : '''
    if len(my_program.operator_stack) > 0 and len(my_program.operand_stack) > 1:
        if my_program.operator_stack[-1] in my_program.relational_operations:
            solve_operation(p)

def p_exp(p):
    '''exp : term sot_action
           | term sot_action PLUS pop_action exp
           | term sot_action MINUS pop_action exp '''

# Solve term
def p_sot_action(p):
    '''sot_action : '''
    if len(my_program.operator_stack) > 0 and len(my_program.operand_stack) > 1:
        if my_program.operator_stack[-1] == '+' or my_program.operator_stack[-1] == '-':
            solve_operation(p)

def p_term(p):
    '''term : factor sof_action
            | factor sof_action TIMES pop_action term
            | factor sof_action DIVIDE pop_action term'''

# Solve factor
def p_sof_action(p):
    '''sof_action : '''
    if len(my_program.operator_stack) > 0 and len(my_program.operand_stack) > 1:
        if my_program.operator_stack[-1] == '*' or my_program.operator_stack[-1] == '/':
            solve_operation(p)

def p_factor(p):
    '''factor : LPAREN abm_action super_expression RPAREN rbm_action
              | var_const '''

# Adds a false bottom mark to the operator stack
def p_abm_action(p):
    '''abm_action : '''
    my_program.operator_stack.append('()')

# Removes the false bottom mark
def p_rbm_action(p):
    '''rbm_action : '''
    my_program.operator_stack.pop()

# Push an operator to its stack
def p_pop_action(p):
    '''pop_action : '''
    my_program.operator_stack.append(p[-1])

def p_var_const(p):
    '''var_const : ID pid_action list_call
                 | ICONST pio_action
                 | FCONST pfo_action
                 | SCONST pso_action
                 | boolean_value pbo_action
                 | function_call'''

# Push a variable to the operand stack
def p_pid_action(p):
    '''pid_action : '''
    # Checks if the variable exists in the local scope
    # print("Scope : " + my_program.current_scope)
    variable = my_program.function_directory.get_function_variable(
        my_program.current_scope, p[-1])

    if variable is None:
        # Checks if the variable exists in the global scope
        # print("Scope : " + my_program.global_scope)
        variable = my_program.function_directory.get_function_variable(
            my_program.global_scope, p[-1])
        if variable is None:
            print("The variable " + p[-1] + " has not been declared")
            sys.exit()
        else:
            # Adds the variale to the operand stack
            my_program.operand_stack.append(variable['memory_adress'])
            my_program.type_stack.append(variable['type'])
    else:
        # Adds the variale to the operand stack
        my_program.operand_stack.append(variable['memory_adress'])
        my_program.type_stack.append(variable['type'])

# Push an intenger to the operand stack
def p_pio_action(p):
    '''pio_action : '''
    # Gets the constant address, creates one if doesn't exists
    constant_address = my_program.memory.check_existing_constant_value('int', int(p[-1]))
    if constant_address is None:
        constant_address = my_program.memory.request_constant_address('int', int(p[-1]))

    my_program.operand_stack.append(constant_address)
    my_program.type_stack.append('int')

# Push a float to the operand stack
def p_pfo_action(p):
    '''pfo_action : '''
    # Gets the constant address, creates one if doesn't exists
    constant_address = my_program.memory.check_existing_constant_value('float', float(p[-1]))
    if constant_address is None:
        constant_address = my_program.memory.request_constant_address('float', float(p[-1]))

    my_program.operand_stack.append(constant_address)
    my_program.type_stack.append('float')

# Push a string to the operand stack
def p_pso_action(p):
    '''pso_action : '''
    # Gets the constant address, creates one if doesn't exists
    constant_address = my_program.memory.check_existing_constant_value('string', str(p[-1]))
    if constant_address is None:
        constant_address = my_program.memory.request_constant_address('string', str(p[-1]))

    my_program.operand_stack.append(constant_address)
    my_program.type_stack.append('string')

# Push a boolean to the operand stack
def p_pbo_action(p):
    '''pbo_action : '''
    if p[-1] == "True":
        # Gets the constant address, creates one if doesn't exists
        constant_address = my_program.memory.check_existing_constant_value('bool', True)
        if constant_address is None:
            constant_address = my_program.memory.request_constant_address('bool', True)

        my_program.operand_stack.append(constant_address)
        my_program.type_stack.append('bool')
    else:
        # Gets the constant address, creates one if doesn't exists
        constant_address = my_program.memory.check_existing_constant_value('bool', False)
        if constant_address is None:
            constant_address = my_program.memory.request_constant_address('bool', False)

        my_program.operand_stack.append(constant_address)
        my_program.type_stack.append('bool')

def p_boolean_value(p):
    '''boolean_value : TRUE
                     | FALSE'''
    p[0] = p[1]

def p_list_call(p):
    '''list_call : LBRACKET exp RBRACKET
                 | empty'''

def p_loop(p):
    '''loop : WHILE cwl_action LPAREN super_expression RPAREN cif_action block swl_action'''

# Stores the actual quaduple number to be used later for the while
def p_cwl_action(p):
    '''cwl_action : '''
    my_program.jump_list.append(my_program.quadruple_number)

def p_swl_action(p):
    '''swl_action : '''
    # Gets the number of the GotoF quadruple and where the while starts
    quadruple_number_to_fill = my_program.jump_list.pop()
    quadruple_number_to_return = my_program.jump_list.pop()

    while_quadruple = Quadruple(my_program.quadruple_number, 'GOTO', None, None,
        quadruple_number_to_return)

    my_program.quadruple_list.append(while_quadruple)
    my_program.quadruple_number += 1

    conditional_quadruple = my_program.quadruple_list[quadruple_number_to_fill]
    # Fills the pending GoToF quadruple with the number of the next quadruple
    conditional_quadruple.fill_quadruple_jump(my_program.quadruple_number)

def p_procedure_call(p):
    '''procedure_call : ID LPAREN abm_action cra_action arguments RPAREN rbm_action sfc_action vtc_action SEMICOLON'''

def p_function_call(p):
    '''function_call : ID LPAREN abm_action cra_action arguments RPAREN rbm_action sfc_action arf_action'''

# Verifies if the procedure call is void type
def p_vtc_action(p):
    '''vtc_action : '''
    function = p[-8]
    function_type = my_program.function_directory.get_function_type(function)

    if function_type != 'void':
        print("This function {0} can't be called as a procedure".format(function))
        sys.exit()

# Checks if the function directory has the function called and creates its
# ERA action
def p_cra_action(p):
    '''cra_action : '''
    function = p[-3]
    # Checks if the function exists
    if my_program.function_directory.has_function(function):
        # Creates its quadruple action
        quadruple = Quadruple(my_program.quadruple_number, 'ERA', function, None, None)
        my_program.quadruple_list.append(quadruple)
        my_program.quadruple_number += 1

        # Retrieves the parameters of the function
        parameters = my_program.function_directory.get_function_parameters(function)
        my_program.temporal_arguments_types = list(parameters['types'])
    else:
        print("The function " + function + " you are trying to call doesn't exists")
        sys.exit()

def p_arguments(p):
    '''arguments : super_expression sar_action more_arguments
                 | empty'''

def p_more_arguments(p):
    '''more_arguments : COMMA super_expression sar_action more_arguments
                      | empty'''

# Solve argument
def p_sar_action(p):
    '''sar_action : '''
    # If there are more arguments than parameters
    if my_program.temporal_arguments_types:
        # Gets the argument and its type from the stacks
        argument = my_program.operand_stack.pop()
        argument_type = my_program.type_stack.pop()
        parameter_type = my_program.temporal_arguments_types.pop(0)

        # Creates the quadruple for the parameter
        if argument_type == parameter_type:
            quadruple = Quadruple(my_program.quadruple_number, 'PARAMETER', argument,
                None, None)
            my_program.quadruple_list.append(quadruple)
            my_program.quadruple_number += 1
        else:
            print('Argument type mismatch at {0} line '.format(p.lexer.lineno))
            sys.exit()
    else:
        print('Agument number mismatch at {0} line '.format(p.lexer.lineno))
        sys.exit()

# Solves the function-procedure called
def p_sfc_action(p):
    '''sfc_action : '''
    # If there are more parameters than arguments
    if not my_program.temporal_arguments_types:
        # Retrieves the function and is quadruple number
        function = p[-7]
        function_quadruple_number = my_program.function_directory.get_function_quadruple_number(function)

        # Creates its call quadruple
        quadruple = Quadruple(my_program.quadruple_number, 'GOSUB', function,
            None, function_quadruple_number)
        my_program.quadruple_list.append(quadruple)
        my_program.quadruple_number += 1
    else:
        print('Argument number mismatch at {0} line '.format(p.lexer.lineno))
        sys.exit()

# Adds the result of the function to the stack and creates its quadruple
def p_arf_action(p):
    '''arf_action : '''
    function_called = p[-8]
    function = my_program.function_directory.get_function(function_called)
    function_return = function['return_address']
    function_type = function['return_type']

    #my_program.temporal_variable_counter += 1

    # Requests a temporal variable to store the result of the function
    temporal_variable_address = my_program.memory.request_temporal_address(function_type)
    my_program.function_directory.add_temporal_to_function(my_program.current_scope,
        function_type)

    # Assignates the result to a new temporal variable and adds it to the
    # operand stack
    quadruple = Quadruple(my_program.quadruple_number, '=', function_return, None,
        temporal_variable_address)
    my_program.quadruple_list.append(quadruple)
    my_program.quadruple_number += 1

    my_program.operand_stack.append(temporal_variable_address)
    my_program.type_stack.append(function_type)

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
    '''return : RETURN super_expression SEMICOLON srf_action'''

# Sets on the return flag and creates the return quadruples
def p_srf_action(p):
    '''srf_action : '''
    my_program.return_flag = True

    # Gets the return operand and the function been called
    operand = my_program.operand_stack.pop()
    operand_type = my_program.type_stack.pop()
    function = my_program.function_directory.get_function(my_program.current_scope)
    function_type = function['return_type']
    function_return_address = function['return_address']

    # Checks if the types match
    if function_type != operand_type:
        print("Return type of function {0} doesn't match function return type".format(
            my_program.current_scope))
        sys.exit()

    # Creates the returns quadruples and sets the adress they will return
    quadruple = Quadruple(my_program.quadruple_number, 'RETURN', operand, None,
        function_return_address)
    my_program.quadruple_list.append(quadruple)
    my_program.quadruple_number += 1

    # Creates the GOTO quadruple and stores them in a stack for multiple returns
    quadruple = Quadruple(my_program.quadruple_number, 'GOTO', None, None, None)
    my_program.return_list.append(my_program.quadruple_number)
    my_program.quadruple_list.append(quadruple)
    my_program.quadruple_number += 1


def p_write(p):
    '''write : PRINT LPAREN super_expression cwr_action RPAREN SEMICOLON'''

def p_cwr_action(p):
    '''cwr_action : '''
    operand = my_program.operand_stack.pop()

    quadruple = Quadruple(my_program.quadruple_number, 'PRINT', operand, None, None)
    my_program.quadruple_list.append(quadruple)
    my_program.quadruple_number += 1

def p_empty(p):
    '''empty : '''

def p_error(p):
    print('Syntax error at input line {0}'.format(p.lexer.lineno))
    sys.exit()

def solve_operation(p):
    """Solve an operation from the stacks"""
    # Gets the operands and its types
    right_operand = my_program.operand_stack.pop()
    right_type = my_program.type_stack.pop()
    left_operand = my_program.operand_stack.pop()
    left_type = my_program.type_stack.pop()

    # Gets the operator
    operator = my_program.operator_stack.pop()

    # Gets the type of the result
    result_type = my_program.semantic_cube.get_semantic_type(left_type ,
        right_type, operator)

    if result_type != 'error':
        #my_program.temporal_variable_counter += 1
        #temporal_variable = "t" + str(my_program.temporal_variable_counter)

        # Gets an address of the temporal memory
        temporal_variable_address = my_program.memory.request_temporal_address(result_type)
        my_program.function_directory.add_temporal_to_function(my_program.current_scope,
            result_type)

        # Creates the quadruple
        quadruple = Quadruple(my_program.quadruple_number, operator, left_operand,
            right_operand , temporal_variable_address)

        # Adds the quadruple to its list and the results to the stacks
        my_program.quadruple_list.append(quadruple)
        my_program.quadruple_number += 1
        my_program.operand_stack.append(temporal_variable_address)
        my_program.type_stack.append(result_type)
    else:
        print('Operation type mismatch at {0}'.format(p.lexer.lineno))
        sys.exit()

def create_conditional_quadruple(p):
    """Creates the quadruple when an if or a while is reached"""
    type_result = my_program.type_stack.pop()

    # It makes no action when the result's type is not a boolean
    if type_result != 'bool':
        print('Operation type mismatch in line {0}'.format(p.lexer.lineno))
        sys.exit();
    else:
        # Creates the GotoF quadruple
        result = my_program.operand_stack.pop()
        quadruple = Quadruple(my_program.quadruple_number, 'GOTOF', result, None, None)
        my_program.quadruple_list.append(quadruple)

        # Stores the number of the GotoF quaduple in order to be filled later
        my_program.jump_list.append(my_program.quadruple_number - 1)
        my_program.quadruple_number += 1

def make_parser():
    parser = yacc.yacc()

    #print("Name of the file to be parsed")
    #file_name = input()
    file_name = 'factorials.txt'

    with open(file_name) as file_object:
        code = file_object.read()
        parser.parse(code)

    #my_program.function_directory.print_directory()
    #print(str(my_program.temporal_parameters_types))
    #my_program.print_stacks()
    #my_program.print_quadruples()
    #my_program.memory.print_memory('global')

    virtual_machine = VirtualMachine(my_program.memory, my_program.function_directory,
        my_program.quadruple_list)
    #virtual_machine.memory.print_memory('global')
    #virtual_machine.execute()
    #virtual_machine.memory.print_memory('local', 'int')
    #virtual_machine.memory.print_memory('global', 'int')

    return parser
make_parser()
