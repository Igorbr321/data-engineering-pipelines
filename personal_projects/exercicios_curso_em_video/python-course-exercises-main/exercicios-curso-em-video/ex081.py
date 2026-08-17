my_list = []

while True:
    values = int(input('Type your numbers or 0 to exit: '))
    my_list.append(values)

    option = input('Do you want to continue (Y/N): ').upper()
    if option == 'N':
        break

print('-=' * 30)
print('You entered {} elements.'.format(len(my_list)))

my_list.sort(reverse=True)
print('The values in descending order: {}'.format(my_list))

if 5 in my_list:
    print('The value 5 is in the list.')
else:
    print('The value 5 is not in the list.')
