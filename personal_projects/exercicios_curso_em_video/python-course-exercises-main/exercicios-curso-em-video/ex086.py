# Creating a 3x3 matrix filled with zeros
matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# Filling the matrix with user input
for i in range(3):
    for j in range(3):
        while True:
            try:
                matrix[i][j] = int(input(f'Enter the value for position [{i+1},{j+1}]: '))
                break
            except ValueError:
                print('Please enter a valid integer.')

# Displaying the matrix with correct formatting
print('Matrix:')
for row in matrix:
    for element in row:
        print(f'{element:^5}', end='')  # Using center alignment with width of 5 spaces
    print()  # Moving to the next row
