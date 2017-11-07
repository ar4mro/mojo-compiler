from .type_segment import TypeSegment

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
