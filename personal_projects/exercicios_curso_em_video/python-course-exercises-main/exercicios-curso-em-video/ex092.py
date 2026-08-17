import datetime  # Import datetime to get the current year

year = datetime.date.today().year  # Get the current year

info = dict()  # Create a dictionary to store user information

# Collect user input
info['Name'] = str(input('Name: '))
info['Birth Year'] = int(input('Year of Birth: '))
info['Age'] = year - info['Birth Year']
info['Work Card'] = int(input('Work Card (0 = does not have): '))

if info['Work Card'] == 0:
    # If no work card, print existing info
    for k, v in info.items():
        print('- {} has the value {}.'.format(k, v))
else:
    # If work card exists, collect additional info
    info['Hiring Year'] = int(input('Year of Hiring: '))
    info['Salary'] = float(input('Salary: $'))
    info['Retirement Age'] = info['Age'] + 35

print('-=' * 40)  # Separator
# Print all collected information
for k, v in info.items():
    print('{} has the value {}'.format(k, v))








