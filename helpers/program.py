from .function_directory import FunctionDirectory
from .semantic_cube import SemanticCube

class Program():
    """A class that represents the program"""

    def __init__(self, global_scope = "", current_scope = ""):
        """Class constructor"""
        self.global_scope = global_scope
        self.current_scope = current_scope
        self.function_directory = FunctionDirectory()
        self.semantic_cube = SemanticCube()
        self.temporal_variables = []
        self.temporal_parameters = []
        self.operand_stack = []
        self.type_stack = []
        self.operator_stack = []
        self.quadruple_list = []
        self.temporal_variable_counter = 0

    def print_stacks(self):
        """Print the temporal stacks of  the program"""
        print(self.operand_stack)
        print(self.type_stack)
        print(self.operator_stack)

    def print_quadruples(self):
        """Print the list of quadruples"""
        for quadruple in self.quadruple_list:
            print(quadruple)
