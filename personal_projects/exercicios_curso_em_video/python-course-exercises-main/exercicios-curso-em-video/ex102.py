def factorial(n, show=False):
    """
    Calculates the factorial of a number.
    
    Parameters:
    n (int): The number to calculate the factorial for.
    show (bool): If True, shows the calculation process.
    
    Returns:
    int: The factorial of the number.
    """
    
    result = 1  # Initialize the result to 1
    
    # Loop from n down to 1
    for c in range(n, 0, -1):
        if show:
            print('{}'.format(c), end='')  # Print the current number
            if c > 1:
                print(' x ', end='')  # Print ' x ' if not the last number
            else:
                print(' = ', end='')  # Print ' = ' if it is the last number
        result *= c  # Multiply the result by the current number
    
    return result  # Return the final result

# Testing the function
print(factorial(5, show=True))  # Output: 5 x 4 x 3 x 2 x 1 = 120

