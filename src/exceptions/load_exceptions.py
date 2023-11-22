"""
Predefined exceptions for the load module
load_exceptions.py: Predefined exceptions for the load module
"""
__author__ = "Srihari Raman"


class UnsupportedFileTypeError(Exception):
    """
    Exception to be raised when the file type is not supported
    """
    def __init__(self, file_type, message="File type {} not supported"):
        self.message = message.format(file_type)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ArgError(Exception):
    """
    Exception to be raised when the argument is not defined
    """
    def __init__(self, missing_args):
        self.message = ("Are you sure you passed the argument(s) {}? You may have to "
                        "pass it as an optional keyword argument!").format(missing_args)
        super().__init__(self.message)

    def __str__(self):
        return self.message




