# Initializing lists to store data
people_list = []  # List to store names and weights
weights = []  # List to store weights only
list_names_max = []  # List to store names with maximum weight
list_names_min = []  # List to store names with minimum weight

# Counter for the number of names
cont_name = 0

# Loop to collect names and weights from the user
while True:
    # Inner loop to ensure the user enters a valid name
    while True:
        name = input('Name: ')
        if name.isdigit():
            print('Please enter a name (text), not a number!')
        else:
            break
    cont_name += 1

    # Inner loop to ensure the user enters a valid weight
    while True:
        try:
            weight = float(input('Weight: '))
            break
        except ValueError:
            print('Please enter a weight (numeric), not text!')
    
    # Append the name and weight to the list
    people_list.append([name, weight])
    weights.append(weight)

    # Prompt the user to continue or stop
    option = input('Do you want to continue [Y/N]? ').upper().strip()
    if option != 'Y':
        break

# Print separator
print('-=' * 30)

# Print the number of people
print("Number of people:", cont_name)

# Find the maximum and minimum weights
max_weight = max(weights)
min_weight = min(weights)

# Loop through the list to find names with maximum weight
for name, weight in people_list:
    if weight == max_weight:
        list_names_max.append(name)
print('The highest weight is {}kg and the people with this weight are {}.'.format(max_weight, list_names_max))

# Loop through the list to find names with minimum weight
for name, weight in people_list:
    if weight == min_weight:
        list_names_min.append(name)
print('The lowest weight is {}kg and the people with this weight are {}.'.format(min_weight, list_names_min))

