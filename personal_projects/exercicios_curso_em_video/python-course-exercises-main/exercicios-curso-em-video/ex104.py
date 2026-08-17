def read_int(msg):
    """
    Prompts the user to enter an integer.

    Args:
        msg (str): The message to display when asking for input.

    Returns:
        int: The integer entered by the user.

    Raises:
        ValueError: If the user does not enter a valid integer.

    Example:
        n = read_int('Enter a number: ')
        print(f'You just entered the number {n}')
    """
    ok = False
    value = 0
    while True:
        n = input(msg)  # Prompt the user for input
        if n.isnumeric():  # Check if the input is numeric
            value = int(n)  # Convert the input to an integer
            ok = True  # Set the flag to True indicating a valid input
        else:
            print('ERROR! Please enter an integer number.')  # Error message for invalid input
        if ok:
            break  # Exit the loop if the input is valid
    return value  # Return the valid integer


# Main Program
n = read_int('Enter a number: ')
print('You just entered the number {}'.format(n))



