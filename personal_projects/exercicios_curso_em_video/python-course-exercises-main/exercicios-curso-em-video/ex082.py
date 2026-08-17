from time import sleep

my_list = []

while True:
    my_list.append(int(input('Type your value: ')))

    cont = input('Do you want to continue (Y/N)? ').upper()
    if cont == 'N':
        print('Exiting the program...')
        sleep(1)
        break

print('Your list: {}'.format(my_list))

even = [num for num in my_list if num % 2 == 0]
odd = [num for num in my_list if num % 2 != 0]

print('Even List: {}'.format(even))
print('Odd List: {}'.format(odd))
