from random import randint
from time import sleep

win = 0
while True:
    
    while True:  
        print('''\nChose one number to play even or odd versus the machine:
        [ 1 ] EVEN
        [ 2 ] ODD
        [ 3 ] Exit Program''')
        try:
            option = int(input('Chose your option: '))
            if 1 <= option <= 3:
                break
            else:
                print('\nType it one number between 1 a 3.\n')
        except ValueError:
            print('\nType it one number between 1 a 3.\n')

    if option == 1:
        machine_option = 2
    elif option == 2:
        machine_option = 1
    elif option == 3:
        print('\nProgram closed.\n')
        break

    while True:        
        try:
            number = int(input('Type it one number: '))
            break
        except ValueError:
            print('Type it one number, to play a game.')


    machine = randint(0, 10)
    print('The number that the machine chose is {}.'.format(machine))

    game = machine + number
    print('The sum of the numbers is {}.'.format(game))


    if option == 1 and machine_option == 2 and game % 2 == 0 or option == 2 and machine_option == 1 and game % 2 == 1:
        print('You win.') 
        win += 1
        print('Victory counter: {}'.format(win))
    else:
        print('You lose.')
        break   
print('Victory total: {}'.format(win))
sleep(3)

    







