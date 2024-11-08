string = input("Enter a string of lower case characters: ")

start = longest_start = max_length = 0

for i in range(1, len(string) + 1):
    if i < len(string) and string[i] >= string[i - 1]:
        continue
    else:
        if i - start > max_length:
            max_length = i - start
            longest_start = start
        start = i

print(
    "Longest substring in alphabetical order is:",
    string[longest_start : longest_start + max_length],
)
