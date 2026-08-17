from random import randint

ge_numbers = [randint(0, 5) for _ in range(5)]

ge_tuple = tuple(ge_numbers)

max_numb = max(ge_tuple)
min_numb = min(ge_tuple)

print(ge_tuple)
print('\nThe largest number is {} and the smallest number is {}.\n'.format(max_numb, min_numb))







