def draw():
    from random import randint

    # Create an empty list to store the numbers
    list_numbers = []
    
    # Generate 10 random numbers between 1 and 20
    for _ in range(10):
        number = randint(1, 20)
        list_numbers.append(number)

    # Print the generated numbers
    print('Drawing 10 values for the list: {}'.format(', '.join(map(str, list_numbers))))

    # Return the list of generated numbers
    return list_numbers


def sum_even(numbers):
    # Create an empty list to store even numbers
    even_numbers = []

    # Iterate through the list and add even numbers to the even_numbers list
    for number in numbers:
        if number % 2 == 0:
            even_numbers.append(number)

    # Calculate the sum of the even numbers
    sum_of_evens = sum(even_numbers)

    # Print the even numbers and their sum
    print('Summing the even values from {}, we get {}.'.format(even_numbers, sum_of_evens))

    # Return the sum of the even numbers
    return sum_of_evens


# Generate the list of random numbers
drawn_list = draw()

# Calculate the sum of the even numbers from the drawn list
sum_of_even_numbers = sum_even(drawn_list)
