class SemanticCube():
    """A class that contains the results of the semantic combinations
       between data types """

    def __init__(self):
        """"Class constructor"""
        self.cube = {
            "int" : {
                "int" : {
                    "+" : "int",
                    "-" : "int",
                    "*" : "int",
                    "/" : "int",
                    "=" : "int",
                    "==" : "bool",
                    "<>" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    ">=" : "bool",
                    "<=" : "bool",
                    "and" : "error",
                    "not" : "error"
                },
                "float" : {
                    "+" : "float",
                    "-" : "float",
                    "*" : "float",
                    "/" : "float",
                    "=" : "float",
                    "==" : "bool",
                    "<>" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    ">=" : "bool",
                    "<=" : "bool",
                    "and" : "",
                    "not" : ""
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "=" : "error",
                    "==" : "error",
                    "<>" : "error",
                    ">" : "error",
                    "<" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    "and" : "error",
                    "not" : "error"
                },
                "string": {
                    "+": "error",
                    "-": "error",
                    "*": "error",
                    "/": "error",
                    "=": "error",
                    "==": "error",
                    "<>": "error",
                    ">": "error",
                    "<": "error",
                    ">=": "error",
                    "<=": "error",
                    "and": "error",
                    "not": "error"
                }
            },
            "float" : {
                "int" : {
                    "+" : "float",
                    "-" : "float",
                    "*" : "float",
                    "/" : "float",
                    "=" : "float",
                    "==" : "bool",
                    "<>" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    ">=" : "bool",
                    "<=" : "bool",
                    "and" : "error",
                    "not" : "error"
                },
                "float" : {
                    "+" : "float",
                    "-" : "float",
                    "*" : "float",
                    "/" : "float",
                    "=" : "float",
                    "==" : "bool",
                    "<>" : "bool",
                    ">" : "bool",
                    "<" : "bool",
                    ">=" : "bool",
                    "<=" : "bool",
                    "and" : "error",
                    "not" : "error"
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "=" : "error",
                    "==" : "error",
                    "<>" : "error",
                    ">" : "error",
                    "<" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    "and" : "error",
                    "not" : "error"
                },
                "string": {
                    "+": "error",
                    "-": "error",
                    "*": "error",
                    "/": "error",
                    "=": "error",
                    "==": "error",
                    "<>": "error",
                    ">": "error",
                    "<": "error",
                    ">=": "error",
                    "<=": "error",
                    "and": "error",
                    "not": "error"
                }
            },
            "bool" : {
                "int" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "=" : "error",
                    "==" : "error",
                    "<>" : "error",
                    ">" : "error",
                    "<" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    "and" : "error",
                    "not" : "error"
                },
                "float" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "=" : "error",
                    "==" : "error",
                    "<>" : "error",
                    ">" : "error",
                    "<" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    "and" : "error",
                    "not" : "error"
                },
                "bool" : {
                    "+" : "error",
                    "-" : "error",
                    "*" : "error",
                    "/" : "error",
                    "=" : "bool",
                    "==" : "bool",
                    "<>" : "bool",
                    ">" : "error",
                    "<" : "error",
                    ">=" : "error",
                    "<=" : "error",
                    "and" : "bool",
                    "not" : "bool"
                },
                "string": {
                    "+": "error",
                    "-": "error",
                    "*": "error",
                    "/": "error",
                    "=": "error",
                    "==": "error",
                    "<>": "error",
                    ">": "error",
                    "<": "error",
                    ">=": "error",
                    "<=": "error",
                    "and": "error",
                    "not": "error"
                }
            },
            "string": {
                "int": {
                    "+": "error",
                    "-": "error",
                    "*": "error",
                    "/": "error",
                    "=": "error",
                    "==": "error",
                    "<>": "error",
                    ">": "error",
                    "<": "error",
                    ">=": "error",
                    "<=": "error",
                    "and": "error",
                    "not": "error"
                },
                "float": {
                    "+": "error",
                    "-": "error",
                    "*": "error",
                    "/": "error",
                    "=": "error",
                    "==": "error",
                    "<>": "error",
                    ">": "error",
                    "<": "error",
                    ">=": "error",
                    "<=": "error",
                    "and": "error",
                    "not": "error"
                },
                "bool": {
                    "+": "error",
                    "-": "error",
                    "*": "error",
                    "/": "error",
                    "=": "error",
                    "==": "error",
                    "<>": "error",
                    ">": "error",
                    "<": "error",
                    ">=": "error",
                    "<=": "error",
                    "and": "error",
                    "not": "error"
                },
                "string": {
                    "+": "string",
                    "-": "error",
                    "*": "error",
                    "/": "error",
                    "=": "string",
                    "==": "bool",
                    "<>": "bool",
                    ">": "error",
                    "<": "error",
                    ">=": "error",
                    "<=": "error",
                    "and": "error",
                    "not": "error"
                }
            }
        }

    def get_semantic_type(self, left_tpye, right_type, operator):
        return self.cube[left_tpye][right_type][operator]
