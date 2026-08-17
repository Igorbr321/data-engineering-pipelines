words = ('python', 'programming', 'intelligence', 'artificial', 'language', 'model')
vowels = 'aeiou'

for word in words:
    print('Vowels in {}: '.format(word), end='')
    for char in word:
        if char.lower() in vowels:
            print(char, end=' ')
    print()  # Newline to separate the words

