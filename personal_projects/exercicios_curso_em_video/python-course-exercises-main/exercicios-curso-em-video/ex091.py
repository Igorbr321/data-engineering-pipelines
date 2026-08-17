from random import randint
from time import sleep
from operator import itemgetter # Importing itemgetter module for sorting dictionaries

game = dict()

# Rolling dice for each player
for c in range(1, 5):
    cube = randint(1, 6)
    game['Player {}'.format(c)] = cube

ranking = dict()

print('Values rolled: ')
# Displaying values rolled for each player
for k, v in game.items():
    print('{} rolled {} on the die.'.format(k, v))
     
print('-=' * 20)
print('{:^33} '.format('=== PLAYERS RANKING ==='))

# Sorting players based on their dice rolls
ranking = sorted(game.items(), key=itemgetter(1), reverse=True)

# Displaying ranking
for i, k in enumerate(ranking):
    print('   {}º Place:  {} with {}.'.format(i + 1, k[0], k[1]))
