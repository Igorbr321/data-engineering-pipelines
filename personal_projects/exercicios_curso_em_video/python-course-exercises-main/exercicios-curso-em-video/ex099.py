def collect_data():
    max_values = []  # List to store entered values
    cont_values = 0  # Counter for the number of entered values
    while True:
        try:
            values = int(input('Enter values (0 to stop): '))  # Prompt user for input
        except ValueError:
            print('Please enter an integer!')  # Error message for non-integer input
            continue
        
        if values == 0:  # If user enters 0, stop collecting values
            break
        
        cont_values += 1  # Increment the counter for each entered value

        max_values.append(values)  # Add entered value to the list
        
    print('Analyzing the entered values...')
    # Convert list of values to a comma-separated string for printing
    norm = ', '.join(map(str, max_values))
    print('{}. In total, {} numbers were entered.'.format(norm, cont_values))  # Print entered values and total count

    return max_values  # Return the list of entered values


def find_largest_value(lista):
    if not lista:
        return None  # If the list is empty, return None
    
    max_value = lista[0]  # Initialize max_value with the first element of the list
    for value in lista:  # Iterate through the list
        if value > max_value:  # If current value is greater than max_value, update max_value
            max_value = value

    
    return max_value  # Return the largest value found


values = collect_data()  # Call the collect_data function to collect values
largest_value = find_largest_value(values)  # Call the find_largest_value function to find the largest value

print('The largest value in the list is {}.'.format(largest_value))  # Print the largest value found
