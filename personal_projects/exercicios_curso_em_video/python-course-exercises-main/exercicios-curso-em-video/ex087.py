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
print('\nMatrix:')
for row in matrix:
    for element in row:
        print(f'{element:^5}', end='')  # Using center alignment with width of 5 spaces
    print()  # Moving to the next row

# Calculating the sum of all even values
sum_even = 0
for row in matrix:
    for element in row:
        if element % 2 == 0:
            sum_even += element

# Calculating the sum of the values in the third column
sum_third_column = sum(row[2] for row in matrix)

# Finding the maximum value in the second row
max_second_row = max(matrix[1])

# Displaying the results
print('\nSum of all even values:', sum_even)
print('Sum of the values in the third column:', sum_third_column)
print('Maximum value in the second row:', max_second_row)
