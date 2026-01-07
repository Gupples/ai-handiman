from functions.run_python_file import run_python_file

# Print calculator's usage instructions
results = run_python_file("calculator", "main.py")

# Run the calculator
results = run_python_file("calculator", "main.py", ["3 + 5"])

# Run the calculator's tests successfully
results = run_python_file("calculator", "tests.py")

# Error: Out of working directory
results = run_python_file("calculator", "../main.py")

# Error: Doesn't exist
results = run_python_file("calculator", "nonexistent.py") 

# Error: Not a Python file
results = run_python_file("calculator", "lorem.txt")