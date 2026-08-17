from time import sleep

def counter(start, end, step):
    # Ensure step is positive
    if step < 0:
        step *= -1
    # Ensure step is not zero
    if step == 0:
        step = 1

    print('-=' * 30)
    print('Counting from {} to {} by {}.'.format(start, end, step))

    # Count up if start is less than end
    if start < end:
        count = start
        while count <= end:
            print('{}'.format(count), end=' ', flush=True)
            sleep(0.2)
            count += step
        print('END!')
    # Count down if start is greater than or equal to end
    else:
        count = start
        while count >= end:
            print('{}'.format(count), end=' ', flush=True)
            sleep(0.2)
            count -= step
        print('END!')

# Predefined counts
counter(0, 10, 2)
counter(10, 0, 2)

print('-=' * 30)

# User-defined count
print('Now it\'s your turn to customize the count!')
start = int(input('Start: '))
end = int(input('End: '))
step = int(input('Step: '))

counter(start, end, step)
