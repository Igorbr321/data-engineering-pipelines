users = []
ages = []
women = []
registered_people = 0

while True:
    user_info = {}
    user_info['Name'] = str(input('Name: '))
    user_info['Age'] = int(input('Age: '))
    user_info['Gender'] = str(input('Gender [M/F]: ')).upper().strip()

    registered_people += 1

    # Add the age to the ages list and calculate the sum and average age
    ages.append(user_info['Age'])
    sum_age = sum(ages)
    average_age = sum_age / len(ages)

    # Add the name to the women list if the gender is 'F'
    if user_info['Gender'] == 'F':
        women.append(user_info['Name'])

    # Add the user information dictionary to the users list
    users.append(user_info)

    # Ask if the user wants to continue
    option = str(input('Do you want to continue [Y/N]: ')).upper().strip()
    print()
    if option == 'N':
        break
    elif option == 'Y':
        continue
    else:
        print('Please enter Y or N! ')

# Create the women_str based on whether any women were registered
if women:
    women_str = ', '.join(women)
else:
    women_str = 'No women registered.'

# Print the summary information
print('Total number of registered people: {}'.format(registered_people))
print('Average age: {:.2f}'.format(average_age))
print('Registered women: {}\n'.format(women_str))

# Print user information for users older than the average age
print("Users older than the average age:")
for user in users: 
    if user['Age'] > average_age:
        for k, v in user.items():
            print('{:^3}: {:^2}'.format(k, v), end='; ')
        print()
