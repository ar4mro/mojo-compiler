class VariableTable():
    """A class that contains a list of variables a function has,
       its name and type"""

    def __init__(self):
        """Class constructor"""
        self.variable_list = {}

    def add_variable(self, variable_type, variable_name):
        """Adds a variable to the list """
        self.variable_list[variable_name] = {
            'name' : variable_name,
            'type' : variable_type,
        }

    def has_variable(self, variable_name):
        """Checks if the list contains the variable asked"""
        return variable_name in self.variable_list.keys()

    def get_variable(self, variable_name):
        """Gets a variable from the list"""
        if self.has_variable(variable_name):
            return self.variable_list(variable_name)
        else:
            return None

    def __str__(self):
        """The string representation of the class"""
        return self.variable_list
