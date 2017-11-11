from .type_segment import TypeSegment
import sys

class MemorySegment():
    """Represents a memory that is divided in type segments"""

    def __init__(self, memory_name, initial_address, total_addresses):
        """Class constructor"""
        self.name = memory_name
        self.type_segment_size = int(total_addresses / 4)
        self.initial_address = initial_address
        self.final_address= initial_address + total_addresses - 1

        # Calculates the initial and final addresses for each type segment
        self.int_initial_address = initial_address
        self.int_final_address = initial_address + self.type_segment_size - 1
        self.float_initial_address = initial_address + self.type_segment_size
        self.float_final_address = initial_address + self.type_segment_size * 2 - 1
        self.string_initial_address = initial_address + self.type_segment_size * 2
        self.string_final_address = initial_address + self.type_segment_size * 3 - 1
        self.bool_initial_address = initial_address + self.type_segment_size * 3
        self.bool_final_address = initial_address + self.type_segment_size * 4 - 1

        # Creates the type segments
        self.int_segment = TypeSegment('Integer', self.int_initial_address,
            self.int_final_address)
        self.float_segment = TypeSegment('Float', self.float_initial_address,
            self.float_final_address)
        self.string_segment = TypeSegment('String', self.string_initial_address,
            self.string_final_address)
        self.bool_segment = TypeSegment('Boolean', self.bool_initial_address,
            self.bool_final_address)

    def request_address(self, value, value_type):
        """Requests an address according of the type"""
        if segment_type == 'int':
            return self.int_segment.request_address(value)
        elif segment_type == 'float':
            return self.float_segment.request_address(value)
        elif segment_type == 'string':
            return self.string_segment.request_address(value)
        elif segment_type == 'bool':
            return self.bool_segment.request_address(value)

    def determines_segment_tpye(self, address):
        """Returns the type of the segment according of the address"""
        if (address >= self.int_initial_address and address <=
            self.int_final_address):
            return 'int'
        elif (address >= self.float_initial_address and address <=
            self.float_final_address):
            return 'float'
        elif (address >= self.string_initial_address and address <=
            self.string_final_address):
            return 'string'
        elif (address >= self.bool_initial_address and address <=
            self.bool_final_address):
            return 'bool'
        else:
            print("Invalid address in the " + self.name + " memory")
            sys.exit()

    def get_value(self, address):
        """Returns a value according of the address"""
        segment_type = determines_segment_tpye(address)
        if segment_type == 'int':
            self.int_segment.get_value(address)
        elif segment_type == 'float':
            self.float_segment.get_value(address)
        elif segment_type == 'string':
            self.string_segment.get_value(address)
        elif semantics == 'bool':
            self.bool_segment.get_value(address)

    def edit_value(self, address):
        """Edits the value related to an address"""
        segment_type = determines_segment_tpye(address)
        if segment_type == 'int':
            self.int_segment.edit_value(address)
        elif segment_type == 'float':
            self.float_segment.edit_value(address)
        elif segment_type == 'string':
            self.string_segment.edit_value(address)
        elif semantics =='bool':
            self.bool_segment.edit_value(address)

    def print_segment(self, segment_type = ""):
        """Prints the segments with all its atributes"""
        print("Memory : " + self.name + "\n" +
              "   Initial address : " + str(self.initial_address) + "\n" +
              "   Final address : " + str(self.final_address))

        if segment_type == 'int':
            print(self.int_segment)
        elif segment_type == 'float':
            print(self.float_segment)
        elif segment_type == 'string':
            print(self.string_segment)
        elif segment_type == 'bool':
            print(self.bool_segment)
        else:
            print(self.int_segment)
            print(self.float_segment)
            print(self.string_segment)
            print(self.bool_segment)
