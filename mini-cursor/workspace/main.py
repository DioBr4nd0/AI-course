import sys
from utils import Calculator

def main():
    calculator = Calculator()
    
    while True:
        print("\nSimple Calculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")
        
        choice = input("Choose an operation (1-5): ")
        
        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            
            if choice == '1':
                result = calculator.add(num1, num2)
            elif choice == '2':
                result = calculator.subtract(num1, num2)
            elif choice == '3':
                result = calculator.multiply(num1, num2)
            else:
                result = calculator.divide(num1, num2)
            
            print(f"{num1} {choice.upper()} {num2} = {result}")
        elif choice == '5':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please choose a valid operation.")

if __name__ == "__main__":
    main()