from .function_directory import FunctionDirectory

class Program():
    """A class that represents the program"""

    def __init__(self, global_scope = "", current_scope = ""):
        """Class constructor"""
        self.global_scope = global_scope
        self.current_scope = current_scope
        self.function_directory = FunctionDirectory()
        self.temporal_variables = []
        self.temporal_parameters = []
