list_even = []  # List to store even numbers
list_odd = []   # List to store odd numbers
users_all = []  # List to store all numbers entered

# Loop to prompt the user to input numbers
for number in range(1, 8):
    while True:
        try:
            users = int(input('Enter your {}º value: '.format(number)))
            users_all.append(users)  # Add the entered number to the list of all numbers
            break
        except ValueError:  # If the input is not a valid integer, prompt the user again
            print('Please enter a value!')

    if users % 2 == 0:  # Check if the number is even
        list_even.append(users)
        list_even = list(set(list_even))  # Remove duplicates from the even numbers list
        list_even.sort()  # Sort the even numbers list
    else:  # If the number is odd
        list_odd.append(users)
        list_odd = list(set(list_odd))  # Remove duplicates from the odd numbers list
        list_odd.sort()  # Sort the odd numbers list

# Convert lists of even and odd numbers to strings
str_even = ', '.join(map(str, list_even))
str_odd = ', '.join(map(str, list_odd))

# Print the results
print('\nThe numbers entered were: {}.'.format(users_all))
print('The even numbers are: {}.'.format(str_even))
print('The odd numbers are: {}.'.format(str_odd))
