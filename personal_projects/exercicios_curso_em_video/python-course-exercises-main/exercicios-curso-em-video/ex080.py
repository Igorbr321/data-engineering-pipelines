my_list = []

for c in range(0, 5):
    value = int(input('Enter a value: '))
    if c == 0 or value > my_list[-1]:
        my_list.append(value)
    else:
        pos = 0
        while pos < len(my_list):
            if value <= my_list[pos]:
                my_list.insert(pos, value)
                print(f'Adding at position {pos} of the list...')
                break
            pos += 1
print('-=' * 30)
print(f'The values entered in order were {my_list}')
