from functions.run_python_file import run_python_file

# Print calculator's usage instructions
print("@" * 25 )
results = run_python_file("calculator", "main.py")
print(results)

# Run the calculator
print("@" * 25 )
results = run_python_file("calculator", "main.py", ["3 + 5"])
print(results)

# Run the calculator's tests successfully
print("@" * 25 )
results = run_python_file("calculator", "tests.py")
print(results)

# Error: Out of working directory
print("@" * 25 )
results = run_python_file("calculator", "../main.py")
print(results)

# Error: Doesn't exist
print("@" * 25 )
results = run_python_file("calculator", "nonexistent.py") 
print(results)

# Error: Not a Python file
print("@" * 25 )
results = run_python_file("calculator", "lorem.txt")
print(results)