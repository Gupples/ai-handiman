from functions.get_files_info import get_files_info

results = get_files_info("calculator", ".")
print(f"Result for current directory:\n  {results.replace('\n', '\n  ')}")

results = get_files_info("calculator", "pkg")
print(f"\nResult for 'pkg' directory:\n  {results.replace('\n', '\n  ')}")

results = get_files_info("calculator", "/bin")
print(f"\nResult for '/bin' directory:\n  {results.replace('\n', '\n  ')}")

results = get_files_info("calculator", "../")
print(f"\nResult for '../' directory:\n  {results.replace('\n', '\n  ')}")