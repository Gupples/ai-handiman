from functions import write_file

results = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(results)

results = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(results)

results = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(results)