from abc import ABC, abstractmethod
from enum import Enum

class Operation(Enum):
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4

class Calculator(ABC):
    @abstractmethod
    def calculate(self, num1, num2, operation):
        pass

class Addition(Calculator):
    def calculate(self, num1, num2, operation):
        if operation == Operation.ADD:
            return num1 + num2
        else:
            raise ValueError("Invalid operation for addition")

class Subtraction(Calculator):
    def calculate(self, num1, num2, operation):
        if operation == Operation.SUBTRACT:
            return num1 - num2
        else:
            raise ValueError("Invalid operation for subtraction")

class Multiplication(Calculator):
    def calculate(self, num1, num2, operation):
        if operation == Operation.MULTIPLY:
            return num1 * num2
        else:
            raise ValueError("Invalid operation for multiplication")

class Division(Calculator):
    def calculate(self, num1, num2, operation):
        if operation == Operation.DIVIDE:
            if num2 == 0:
                raise ValueError("Cannot divide by zero")
            return num1 / num2
        else:
            raise ValueError("Invalid operation for division")

class CalculatorLogic:
    def __init__(self):
        self.calculators = {
            Operation.ADD: Addition(),
            Operation.SUBTRACT: Subtraction(),
            Operation.MULTIPLY: Multiplication(),
            Operation.DIVIDE: Division()
        }

    def calculate(self, num1, num2, operation):
        return self.calculators[operation].calculate(num1, num2, operation)