from .memory_segment import MemorySegment
import sys

class Memory():
    """Represents a memory in a program for global, temporal and
    constant values"""

    def __init__(self):
        """Class constructor"""
        self.global_memory = MemorySegment('Global', 5000, 2000)
        self.temporal_memory = MemorySegment('Temporal', 43000, 2000)
        self.constant_memory = MemorySegment('Constant', 20000, 2000)

    def request_global_address(self, value, value_type):
        """Request an address for a global variable"""
        self.global_memory.request_address(value, value_type)

    def request_temporal_address(self, value, value_type):
        """Request an address for a temporal variable"""
        self.temporal_memory.request_address(value, value_type)

    def request_constant_address(self, value, value_type):
        """Request an address for a constant"""
        self.constant_memory.request_address(value, value_type)

    def determines_memory_tpye(self, address):
        """Returns the type of the memory according of the address"""
        if (address >= self.global_memory.initial_address and address <=
            self.global_memory.final_address):
            return 'global'
        elif (address >= self.temporal_memory.initial_address and address <=
            self.temporal_memory.final_address):
            return 'temporal'
        elif (address >= self.constant_memory.initial_address and address <=
            self.constant_memory.final_address):
            return 'constant'
        else:
            print("Invalid address: " + str(address))
            sys.exit()

    def get_value(self, address):
        """Returns a value according of the address"""
        memory_type = determines_memory_tpye(address)
        if memory_type == 'global':
            self.global_memory.get_value(address)
        elif memory_type == 'temporal':
            self.temporal_memory.get_value(address)
        elif memory_type == 'constant':
            self.constant_memory.get_value(address)

    def edit_value(self, address):
        """Edits the value related to an address"""
        memory_type = determines_memory_tpye(address)
        if memory_type == 'global':
            self.global_memory.edit_value(address)
        elif memory_type == 'temporal':
            self.temporal_memory.edit_value(address)
        elif memory_type == 'constant':
            self.constant_memory.edit_value(address)

    def print_memory(self, memory_type, segment_type = ""):
        """Prints the memory"""
        if memory_type == 'global':
            self.global_memory.print_segment(segment_type)
        elif memory_type == 'temporal':
            self.temporal_memory.print_segment(segment_type)
        elif memory_type == 'constant':
            self.constant_memory.print_segment(segment_type)
