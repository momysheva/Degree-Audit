def calculate(expression):
    try:
        operator = None
        for char in expression:
            if char in ['+', '-', '*', '/', '^']:
                operator = char
                break
        
        a, b = expression.split(operator)
        a_float = float(a.strip())
        b_float = float(b.strip())

        if operator == '+':
            result = a_float + b_float
        elif operator == '-':
            result = a_float - b_float
        elif operator == '*':
            result = a_float * b_float
        elif operator == '/':
            if b_float == 0:
                raise ZeroDivisionError("cannot be performed as a number cannot be divided by zero")
            result = a_float / b_float
        elif operator == '^':
            result = a_float ** b_float
        
        print(f"{a} {operator} {b} = {result}")
    except ValueError as ve:
        print(f"{a} {operator} {b} please make sure that operands are in the correct format.")

    except ZeroDivisionError as zde:
        print(f"{a} {operator} {b} {zde}")
    except Exception as e:
        print(f"An error occurred: {e}")

while True:
    file_name = input("Enter the file name (or 'N' to exit): ")
    if file_name == 'N':
        break
    try:
        with open(file_name, 'r') as file:
            for line in file:
                calculate(line.strip())
    except FileNotFoundError:
        print("Error: File does not exist")




    