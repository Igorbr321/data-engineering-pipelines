num = (int(input('\nEnter the first number: ')),
       int(input('Enter the second number: ')),
       int(input('Enter the third number: ')),
       int(input('Enter the fourth number: ')),
       int(input('Enter the fifith number: ')))

print('The numbers entered: {}\n'.format(num))
print('The value nine is typed {} times.'.format(num.count(9)))

if 3 in num:  
       print('The value three is in position {}.'.format(num.index(3) + 1))
else:
       print('The value three did not appear in the tuple.')

even_numbers = tuple(n for n in num if n % 2 == 0)
print('The even values entered were: {}'.format(even_numbers))

