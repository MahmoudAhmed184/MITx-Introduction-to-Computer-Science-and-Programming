VOWELS = 'aeiou'

string = input("Enter a string of lower case characters: ")

num_of_vowels = 0

for character in string:
    if character in VOWELS:
        num_of_vowels += 1

print("Number of vowels:", num_of_vowels)