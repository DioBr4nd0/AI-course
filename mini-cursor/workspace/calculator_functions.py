import operator

def add(x, y):
    """Return the sum of two numbers."""
    return x + y

def subtract(x, y):
    """Return the difference of two numbers."""
    return x - y

def multiply(x, y):
    """Return the product of two numbers."""
    return x * y

def divide(x, y):
    """Return the quotient of two numbers."""
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def power(base, exponent):
    """Return the result of raising a number to a power."""
    return base ** exponent

def modulus(base, exponent):
    """Return the remainder of dividing one number by another."""
    if exponent == 0:
        raise ValueError("Cannot divide by zero.")
    return base % exponent

def sqrt(number):
    """Return the square root of a number."""
    import math
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number.")
    return math.sqrt(number)

def sin(angle_in_radians):
    """Return the sine of an angle in radians."""
    import math
    return math.sin(angle_in_radians)

def cos(angle_in_radians):
    """Return the cosine of an angle in radians."""
    import math
    return math.cos(angle_in_radians)

def tan(angle_in_radians):
    """Return the tangent of an angle in radians."""
    import math
    if angle_in_radians == 0:
        raise ValueError("Cannot calculate tangent of zero.")
    return math.tan(angle_in_radians)