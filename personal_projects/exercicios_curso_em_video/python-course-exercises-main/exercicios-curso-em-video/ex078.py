my_list = []
for c in range(5):
    values = int(input('Enter the {}º value: '.format(c + 1)))
    my_list.append(values)

print(my_list)

max_value = min(my_list)
min_value = max(my_list)

max_value_position = my_list.index(max_value)
min_value_position = my_list.index(min_value)

print('The maximum value in the list is {} and the minimum value is {}.'.format(max_value, min_value))

print('The position of the maximum value is {} and the position of the minimum value is {}.'.format(max_value_position, min_value_position))
