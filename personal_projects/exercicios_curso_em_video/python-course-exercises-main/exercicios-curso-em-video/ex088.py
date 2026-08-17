from random import randint
from time import sleep

# Printing the header
print('---' * 11)
print('MEGA SENA'.center(33))
print('---' * 11)

# Asking the user for the number of games to draw
while True:
    try:
        games = int(input('How many games do you want me to draw? '))
        break
    except ValueError:
        print('Please enter a number!')

# Informing the user about the drawing process
print('\n-=-=-=-=', 'DRAWING {} GAMES'.format(games), '-=-=-=-=')

# Loop to draw the games
for i in range(1, games + 1):
    list_games = []
    while len(list_games) < 6:  # Continue until we have 6 unique numbers
        number = randint(1, 60)
        if number not in list_games:  # If the number is not in the list, add it
            list_games.append(number)
        
    # Printing each game's numbers
    print('Game {}: {}'.format(i, list_games))
    sleep(2)  # Pause for 2 seconds between each game

    


