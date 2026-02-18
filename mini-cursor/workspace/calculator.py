# Importing necessary libraries
from abc import ABC, abstractmethod
import operator

# Defining an abstract base class for calculators
class Calculator(ABC):
    @abstractmethod
    def add(self, a, b):
        pass

    @abstractmethod
    def subtract(self, a, b):
        pass

    @abstractmethod
    def multiply(self, a, b):
        pass

    @abstractmethod
    def divide(self, a, b):
        pass


# Implementing the calculator using operator module for simplicity
class SimpleCalculator(Calculator):
    def add(self, a, b):
        return operator.add(a, b)

    def subtract(self, a, b):
        return operator.sub(a, b)

    def multiply(self, a, b):
        return operator.mul(a, b)

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return operator.truediv(a, b)


# Creating an instance of the calculator
def main():
    calculator = SimpleCalculator()

    while True:
        print("\n1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n5. Quit")
        choice = input("Choose an operation: ")

        if choice == "5":
            break

        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == "1":
                print(f"{num1} + {num2} = {calculator.add(num1, num2)}")
            elif choice == "2":
                print(f"{num1} - {num2} = {calculator.subtract(num1, num2)}")
            elif choice == "3":
                print(f"{num1} * {num2} = {calculator.multiply(num1, num2)}")
            elif choice == "4":
                try:
                    print(f"{num1} / {num2} = {calculator.divide(num1, num2)}")
                except ValueError as e:
                    print(e)
            else:
                print("Invalid choice. Please choose a valid operation.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()