from functions.get_file_content import get_file_content

results = get_file_content("calculator", "lorem.txt")
print(f"\nResults for lorem.txt:\n{results}")

results = get_file_content("calculator", "main.py")
print(f"\nResults for main.py:\n{results}")


results = get_file_content("calculator", "pkg/calculator.py")
print(f"\nResults for pkg/calculator:\n{results}")


results = get_file_content("calculator", "/bin/cat")
print(f"\nResults for bin/cat:\n{results}")

results = get_file_content("calculator", "pkg/does_not_exist.py")
print(f"\nResults for pkg/does_not_exist.py:\n{results}")

