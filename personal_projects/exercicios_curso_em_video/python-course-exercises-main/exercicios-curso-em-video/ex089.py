# Creating an empty list to store student information
records = list()

while True:
    # Loop for inputting student information
    while True:
        name = input('Name: ')
        if name.isdigit():
            print('Please enter a name (text), not a number.')
        else:
            break
            
    # Inputting student's grades
    note_1 = int(input('Grade 1: '))
    note_2 = int(input('Grade 2: '))
    average_grade = (note_1 + note_2) / 2

    # Appending student information to the list
    records.append([name, [note_1, note_2], average_grade])

    # Asking if the user wants to continue
    option_one = input('Do you want to continue [Y/N]: ').upper().strip()
    if option_one != 'Y':
        break

# Displaying student records
print('-=' * 25)
print('{:<8} {:<12} {:<10}'.format('No.', 'NAME', 'AVERAGE'))
print('-' * 30)

for index, record in enumerate(records):
    print('{:<8} {:<12} {:<10}'.format(index, record[0], record[2]))

# Loop to display individual student's grades
while True:
    print('-' * 30)
    notes = int(input('Show grades of which student? [999 to stop] '))
    if notes == 999:
        break
    if notes <= len(records) - 1:
        print("Grades of {} are {}.".format(records[notes][0], records[notes][1]))


