"""
SWITCH CASE
"""
def numbers_to_strings(argument):
    switcher = {
        0: "zero",
        1: "one",
        2: "two",
    }
    return switcher.get(argument, "nothing")

def zero():
    return "zero"

def one():
    return "one"


"""
Dictionary Mapping for Functions
"""
def numbers_to_functions_to_strings(argument):
    switcher = {
        0: zero,
        1: one,
        2: lambda: "two",
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "nothing")
    # Execute the function
    return func()


"""
Dispatch Methods for Classes
"""
class Switcher(object):
    def numbers_to_methods_to_strings(self, argument):
        """Dispatch method"""
        # prefix the method_name with 'number_' because method names
        # cannot begin with an integer.
        method_name = 'number_' + str(argument)
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "nothing")
        # Call the method as we return it
        return method()

    def number_0(self):
        return "zero"

    def number_1(self):
        return "one"

    def number_2(self):
        return "two"

