import math
from typing import Union

def add(x: float, y: float) -> float:
    """Return the sum of two numbers."""
    return x + y

def subtract(x: float, y: float) -> float:
    """Return the difference between two numbers."""
    return x - y

def multiply(x: float, y: float) -> float:
    """Return the product of two numbers."""
    return x * y

def divide(x: float, y: float) -> Union[float, str]:
    """Return the quotient of two numbers or an error message if division by zero."""
    if y == 0:
        return "Error: Division by zero is not allowed."
    else:
        return x / y

def power(base: float, exponent: int) -> float:
    """Return the result of raising a number to a power."""
    return math.pow(base, exponent)

def sqrt(number: float) -> Union[float, str]:
    """Return the square root of a number or an error message if negative."""
    if number < 0:
        return "Error: Square root of negative numbers is not allowed."
    else:
        return math.sqrt(number)