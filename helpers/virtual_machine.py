from .function_directory import FunctionDirectory
from .memory import Memory
import sys

class VirtualMachine():
    """Simulates the execution a processor performs over a list of instructions"""
    def __init__(self, memory, function_directory, instructions):
        self.memory = memory
        self.function_directory = function_directory
        self.instructions = instructions
        self.number_of_instructions = len(self.instructions)
        self.number_of_current_instruction = 0

    def request_local_addresses(self, function_called):
        """Request the number of local addresses a function has for each type"""
        for i in range(function_called['function']['number_of_local_variables']['int']):
            function_called['memory'].request_local_address('int')
        for i in range(function_called['function']['number_of_local_variables']['float']):
            function_called['memory'].request_local_address('float')
        for i in range(function_called['function']['number_of_local_variables']['string']):
            function_called['memory'].request_local_address('string')
        for i in range(function_called['function']['number_of_local_variables']['bool']):
            function_called['memory'].request_local_address('bool')

    def request_temporal_addresses(self, function_called):
        """Request the number of temporal addresses a function has for each type"""
        for i in range(function_called['function']['number_of_temporal_variables']['int']):
            function_called['memory'].request_temporal_address('int')
        for i in range(function_called['function']['number_of_temporal_variables']['float']):
            function_called['memory'].request_temporal_address('float')
        for i in range(function_called['function']['number_of_temporal_variables']['string']):
            function_called['memory'].request_temporal_address('string')
        for i in range(function_called['function']['number_of_temporal_variables']['bool']):
            function_called['memory'].request_temporal_address('bool')

    def execute(self):
        """Executes the instrucions"""
        function_called = {} # Stores the function information when one is called
        actual_parameter = 0 # The parameter position of a function
        current_memory = self.memory # Global and constant segments never change
        local_segment_pointer_list = [] # Changes when a function is called
        temporal_segment_pointer_list = [] # Changes when a function is called
        # The instruction number we are returning after executing a funtion
        instruction_number_to_back_list = []

        # Executes for each quadruple
        while self.number_of_current_instruction < self.number_of_instructions:
            current_instruction = self.instructions[self.number_of_current_instruction]
            #print(current_instruction)

            # Obtains the type of action, the addresses of the operands
            # and where the result will be stored
            instruction_action = current_instruction.operator
            left_operand_address = current_instruction.left_operand
            right_operand_address = current_instruction.right_operand
            result_address = current_instruction.result

            # Gets value inside the address that is inside the address the
            # dictionary stores, these operands are the result  of dimensioned
            # variables calls
            if isinstance(left_operand_address, dict):
                left_operand_address = current_memory.get_value(
                    left_operand_address['index_address'])
            if isinstance(right_operand_address, dict):
                right_operand_address = current_memory.get_value(
                    right_operand_address['index_address'])
            if isinstance(result_address, dict):
                result_address = current_memory.get_value(
                    result_address['index_address'])

            # print(left_operand_address)
            # print(right_operand_address)
            # print(result_address)

            # Acts like a switch, differents actions, different instructions
            if instruction_action == '+':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand + right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == '-':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand - right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == '*':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand * right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == '/':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)

                if right_operand == 0:
                    print("ERROR: Divisions by 0 are not allowed")
                    sys.exit()
                else:
                    # Exact division if a float is involved
                    if isinstance(left_operand, float) or isinstance(right_operand, float):
                        result = left_operand / right_operand
                    else:
                        result = int(left_operand / right_operand)

                    # Stores the result and pass to the next quadruple
                    current_memory.edit_value(result_address, result)
                    self.number_of_current_instruction += 1
            elif instruction_action == '=':
                left_operand = current_memory.get_value(left_operand_address)
                result = left_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == '>':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand > right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == '<':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand < right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == '>=':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand >= right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == '<=':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand <= right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == '==':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand == right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == '!=':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand != right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == 'and':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand and right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == 'or':
                left_operand = current_memory.get_value(left_operand_address)
                right_operand = current_memory.get_value(right_operand_address)
                result = left_operand or right_operand

                # Stores the result and pass to the next quadruple
                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == 'PRINT':
                left_operand = current_memory.get_value(left_operand_address)

                print(str(left_operand))
                self.number_of_current_instruction += 1
            elif instruction_action == 'GOTO':
                # Points to a new quadruple
                self.number_of_current_instruction = result_address - 1
            elif instruction_action == 'GOTOF':
                left_operand = current_memory.get_value(left_operand_address)

                if not left_operand:
                    self.number_of_current_instruction = result_address - 1
                else:
                    self.number_of_current_instruction += 1
            elif instruction_action == 'VERF_INDEX':
                index = current_memory.get_value(left_operand_address)
                lower_limit = right_operand_address
                upper_limit = result_address

                if index >= lower_limit and index < upper_limit:
                    self.number_of_current_instruction += 1
                else:
                    print("Index out of bound")
                    sys.exit()
            elif instruction_action == 'RETURN':
                left_operand = current_memory.get_value(left_operand_address)
                result = left_operand

                current_memory.edit_value(result_address, result)
                self.number_of_current_instruction += 1
            elif instruction_action == 'ERA':
                # Gets the information of the function called and creates it a
                # memory to store its local and temporal variables
                function_called['function'] = self.function_directory.get_function(left_operand_address)
                function_called['memory'] = Memory()
                actual_parameter = 0

                # Asks to allocate the number of local and temporaral variables
                # the function has
                self.request_local_addresses(function_called)
                self.request_temporal_addresses(function_called)

                # Pass to the next quadruple
                self.number_of_current_instruction += 1
            elif instruction_action == 'PARAMETER':
                # Gets the value of the parameter and the address where will
                # be stored and increments the position of the parameter called
                left_operand = current_memory.get_value(left_operand_address)
                parameter_adress = function_called['function']['parameters']['addresses'][actual_parameter]
                actual_parameter += 1

                # Stores the value of the parameter in its corresponding function
                # segment menory
                function_called['memory'].edit_value(parameter_adress, left_operand)

                # Pass to the next quadruple
                self.number_of_current_instruction += 1
            elif instruction_action == 'GOSUB':
                # Stores the number of instruction we will return after the function
                # execution ends
                instruction_number_to_back_list.append(self.number_of_current_instruction)

                # Stores the local and temporal memory segments of the function
                # that is making the call
                local_segment_pointer_list.append(current_memory.local_memory)
                temporal_segment_pointer_list.append(current_memory.temporal_memory)

                # Change the local and temporal memory segments for the ones the
                # function that will be executed has
                current_memory.local_memory = function_called['memory'].local_memory
                current_memory.temporal_memory = function_called['memory'].temporal_memory

                # Points where the function called starts
                self.number_of_current_instruction = result_address - 1
            elif instruction_action == 'ENDPROC':
                # Destroys the local information of the function when it ends
                # and returns to the local and temporal segments of the function caller
                function_called.clear()
                current_memory.local_memory = local_segment_pointer_list.pop()
                current_memory.temporal_memory = temporal_segment_pointer_list.pop()

                # Returns to the next instruction of the function caller
                self.number_of_current_instruction = instruction_number_to_back_list.pop() + 1
