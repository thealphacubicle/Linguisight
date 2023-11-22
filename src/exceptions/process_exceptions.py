"""
Predefined exceptions for the process module
process_exceptions.py: Predefined exceptions for the process module
"""
__author__ = "Sriya Vuppala"


class UnsupportedProcessTypeError(Exception):
    """
    Exception to be raised when the process type is not supported
    """
    def __init__(self, file_type, message="Process type {} not supported"):
        self.message = message.format(file_type)
        super().__init__(self.message)

    def __str__(self):
        return self.message
