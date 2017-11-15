import json # Used to give format at printing dictionaries

from .variable_table import VariableTable

class FunctionDirectory():
    """A class that contains a list of functions and procedures a program has,
    its parameters and some other useful information"""

    def __init__(self):
        """Class constructor"""
        self.function_list = {}

    def add_function(self, function_name, function_type,
            function_parameter_list = [], function_parameter_adresses = []):
        """Adds a function to the list"""
        self.function_list[function_name] = {
            'name' : function_name,
            'return_type' : function_type,
            'return_address' : -1,
            'quadruple_number' : -1,
            'parameters' : {
                'types' : function_parameter_list,
                'addresses' : function_parameter_adresses,
            },
            'variables': VariableTable(),
            'number_of_local_variables' : {
                'int' : 0,
                'float' : 0,
                'string' : 0,
                'bool' : 0
            },
            'number_of_temporal_variables' : {
                'int' : 0,
                'float' : 0,
                'string' : 0,
                'bool' : 0
            }
        }

    def has_function(self, function_name):
        """Checks if the list contains the function asked"""
        return function_name in self.function_list.keys()

    def get_function(self, function_name):
        """Gets a function from the list"""
        if self.has_function(function_name):
            return self.function_list[function_name]
        else:
            print("A function with this name doesn't exist")
            return None

    def add_parameter_to_function(self, function_name, type_list, addresses_list):
        """Adds a parameter to its function"""
        function = self.get_function(function_name)
        if function is not None:
            function['parameters']['types'] = type_list
            function['parameters']['addresses'] = addresses_list
        else:
            print("The function you are trying to add the paremeter doesnt exist")

    def add_variable_to_function(self, function_name, variable_type,
            variable_name, variable_adress=0):
        """Adds a variable to its function variable table"""
        function = self.get_function(function_name)
        if function is not None:
            if function['variables'].has_variable(variable_name):
                print("This function already has a variable with that name")
            else:
                # Adds the varaible to the variable table and increments the
                # number of local variables the function will use
                function['variables'].add_variable(variable_type, variable_name, variable_adress)
                function['number_of_local_variables'][variable_type] += 1
        else:
            print("The function you are trying to add the variable doesnt exists")

    def add_temporal_to_function(self, function_name, temporal_type):
        """Increments the number of temporals the function has"""
        function = self.get_function(function_name)
        if function is not None:
            function['number_of_temporal_variables'][temporal_type] += 1
        else:
            print("The function you are trying to add the temporal doesnt exists")

    def get_function_variable(self, function_name, variable_name):
        """Looks for a variable in the function"""""
        function = self.get_function(function_name)
        if function is not None:
            variable = function['variables'].get_variable(variable_name)
            if variable is not None:
                return variable
            else:
                #print("This variable doesnt exists in this function")
                return None
        else:
            print("The function you are trying to find when looking for the" +
                "variable doesn't exists")

    def get_function_type(self, function_name):
        """Looks for the type of the function"""""
        function = self.get_function(function_name)
        if function is not None:
            function_type = function['return_type']
            return function_type
        else:
            print("This function doesn't exists")

    def get_function_parameters(self, function_name):
        """Returns the parameters of the function if exists"""
        function = self.get_function(function_name)
        if function is not None:
            return function['parameters']
        else:
            print("The function you are trying to retrieve its parameters" +
                "doesnt exists")

    def set_function_quadruple_number(self, function_name, quadruple_number):
        """Establish where the procedure starts"""
        function = self.get_function(function_name)
        if function is not None:
            function['quadruple_number'] = quadruple_number
        else:
            print("The function you are trying to set the quadruple doesn't exists")

    def set_function_address(self, function_name, address_number):
        """Sets the address return of the function"""
        function = self.get_function(function_name)
        if function is not None:
            function['return_address'] = address_number
        else:
            print("The function you are trying to add the adress doesn't exists")

    def get_function_quadruple_number(self, function_name,):
        """Retrieves the quadruple number of a function"""
        function = self.get_function(function_name)
        if function is not None:
            return function['quadruple_number']
        else:
            print("The function you are trying to retrieve its quadruple doesn't exists")

    def print_directory(self):
        """Prints the list of functions and its properties"""
        for function, properties in self.function_list.items():
            print("function : " + str(function))

            # Prints the variable table only if the value is an instance of
            # the class
            for prop, value in properties.items():
                if isinstance(value, VariableTable):
                    print("  " + str(prop) + " : " +
                        json.dumps(value.variable_list, indent=4))
                elif isinstance(value, dict):
                    print("  " + str(prop) + " : " +
                        json.dumps(value, indent=4))
                else:
                    print("  " + str(prop) + " : " + str(value))

            # Prints a dashed line
            print("-" * 80)
