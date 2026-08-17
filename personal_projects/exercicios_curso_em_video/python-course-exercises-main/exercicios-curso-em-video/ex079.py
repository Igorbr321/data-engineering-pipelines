my_list = []

while True:
    value = int(input('Type your values or 0 to exit: '))
    if value in my_list:
        print('This value has already been stored in the list. Please enter another one!\n')
    else:
        my_list.append(value)

    if value == 0:
        break

    sorted_list = sorted(my_list)

print('Unique values entered: {}'.format(sorted_list))
