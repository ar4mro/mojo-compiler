import json # Used to give format at printing dictionaries
import sys # Prints segment in a dictionary format, booleans are min caps

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

    def available_space(self, total_addresses=0):
        """Determines if the segment is not full"""
        if self.current_address + total_addresses <= self.final_address:
            return True
        else:
            return False

    def valid_address(self, address):
        """Determines if an address is a valid one"""
        if address in self.segment:
            return True
        else:
            return False

    def request_address(self, value):
        """Allocates an address for a variable or constant"""
        if self.available_space():
            address = self.current_address
            self.segment[address] = value
            self.current_address += 1
            return address
        else:
            print("There is no available space in the " + self.name + " memory segment")
            sys.exit()

    def request_sequential_addresses(self, total_addresses, value):
        """Allocates a bunch of addresses"""
        if self.available_space(total_addresses):
            base_address = self.current_address

            # Request a unique address for each element
            for i in range(total_addresses):
                self.segment[self.current_address] = value
                self.current_address += 1

            return base_address
        else:
            print("There is no available space in the " + self.name + " memory segment")
            sys.exit()

    def get_value(self, address):
        """Returns a value related to an address"""
        if self.valid_address(address):
            return self.segment[address]
        else:
            print("The address you requested a value is not valid")
            return None

    def check_existing_value(self, existing_value):
        """Checks if the value exists in the segment"""
        for address, value in self.segment.items():
            # Constant values are unique, there's only one address per value
            if value == existing_value:
                return address
        # Returns nothing if the value doesn't exists
        return None

    def edit_value(self, address, value):
        """Edits the value related to an address"""
        if self.valid_address(address):
            self.segment[address] = value
        else:
            print("The address: " + str(address) + " you are trying to change" +
                " its value is not valid")
            sys.exit()

    def reset(self):
        """Clears all the addresses, starts at its initial adress"""
        self.segment.clear()
        self.current_address = self.initial_address
