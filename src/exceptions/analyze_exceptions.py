"""
Predefined exceptions for the analyze module
analyze_exceptions.py: Predefined exceptions for the process module
"""
__author__ = "Reema Sharma"

class UnsupportedAnalyzeTypeError(Exception):
    """
    Exception to be raised when the analyze type is not supported
    """
    def __init__(self, file_type, message="Analyze type {} not supported"):
        self.message = message.format(file_type)
        super().__init__(self.message)

    def __str__(self):
        return self.message

