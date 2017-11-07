import json # Used to give format at printing dictionaries

class TypeSegment():
    """Represents a segment of the memory for a primitive type"""

    def __init__(self, segment_name, initial_address, final_address):
        """Class constructor"""
        self.name = segment_name
        self.initial_address = initial_address
        self.final_address = final_address
        self.current_address = initial_address
        self.segment = {}

    def __str__(self):
        """The string representation of the class"""
        return ("Segment : " + self.name + "\n" +
                "   Initial address: " + str(self.initial_address) + "\n" +
                "   Final address: " + str(self.final_address) + "\n" +
                "   Current address " + str(self.current_address) + "\n" +
                "   Addresses " + json.dumps(self.segment, indent=4))
