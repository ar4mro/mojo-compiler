from .memory_segment import MemorySegment

class Memory():
    """Represents a memory in a program for global, temporal and
    constant values"""

    def __init__(self):
        """Class constructor"""
        self.global_memory = MemorySegment('Global', 5000, 2000)
        self.temporal_memory = MemorySegment('Temporal', 43000, 2000)
        self.constant_memory = MemorySegment('Constant', 20000, 2000)

    def print_memory(self, memory_type, segment_type = ""):
        """Prints the memory"""
        if memory_type == 'Global':
            self.global_memory.print_segment(segment_type)
        elif memory_type == 'Temporal':
            self.temporal_memory.print_segment(segment_type)
        elif memory_type == 'Constant':
            self.constant_memory.print_segment(segment_type)
