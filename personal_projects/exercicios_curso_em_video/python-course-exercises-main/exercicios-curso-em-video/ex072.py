count = ('One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
         'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen', 'Twenty')

while True:
    choice = input('Choose a number from 1 to 20 or type Exit to exit the program: ')
    if choice.upper() == 'EXIT':
        print('Exiting the program.')
        break

    try:
        num = int(choice)
        if 1 <= num <= 20:
            print('You chose {}: {}'.format(num, count[num - 1]))
        else:
            print('Number out of range. Please choose a number between 1 and 20.')
    except ValueError:
        print('Please type "Exit" to exit the program.')

