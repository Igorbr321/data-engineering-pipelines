typed = sum = 0
while True:
    num = int(input('Type it one number [Type it 999 to exit]: '))
    if num == 999:
        break
    sum += num
    typed += 1

print('The sum of the valors is {}, and the quantity valors typed is {}.'.format(sum, typed))