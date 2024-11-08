string = input("Enter a string of lower case characters: ")

count = start = 0

while True:
    start = string.find("bob", start) + 1
    if start == 0:
        break
    count += 1

print("Number of times bob occurs is:", count)