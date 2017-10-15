class Quadruple():
    """A class that represents a quadruple"""

    def __init__(self, operator, left_operand, right_operand, result):
        """Class constructor"""
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result

    def __str__(self):
        """The string representation of the class"""
        return (str(self.operator) + ", " + str(self.left_operand) + ", "
            + str(self.right_operand) + ", " + str(self.result))
