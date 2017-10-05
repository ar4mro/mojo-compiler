import json

from .variable_table import VariableTable

class FunctionDirectory():
    """A class that contains a list of functions and procedures a program has,
    its parameters and some other useful information"""

    def __init__(self):
        """Class constructor"""
        self.function_list = {}

    def add_function(self, function_type, function_name,
            function_parameter_list = []):
        """Adds a function to the list"""
        self.function_list[function_name] = {
            'name' : function_name,
            'return_type' : function_type,
            'parameters' : function_parameter_list,
            'variables': VariableTable()
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

    def add_parameter_to_function(self, function_name, parameter_list):
        """Adds a parameter to its function"""
        function = self.get_function(function_name)
        if function is not None:
            function['parameters'] = parameter_list
        else:
            print("The function you are trying to add the paremeter doesnt exist")

    def add_variabe_to_function(self, function_name, variable_type,
            variable_name):
        """Adds a variable to its function variable table"""
        function = self.get_function(function_name)
        if function is not None:
            if function['variables'].has_variable(variable_name):
                print("This function already has a variable with that name")
            else:
                function['variables'].add_variable(variable_type, variable_name)
        else:
            print("The function you are trying to add the variable doesnt exist")

    def print_directory(self):
        """Prints the list of functions and its properties"""
        for function, properties in self.function_list.items():
            print("function : " + function)

            # Prints the variable table only if the value is ans instance of
            # the class
            for prop, value in properties.items():
                if isinstance(value, VariableTable):
                    print("  " + str(prop) + " : " +
                        json.dumps(value.variable_list, indent=4))
                else:
                    print("  " + str(prop) + " : " + str(value))
