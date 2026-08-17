# List to store information about all players
info_list = []
partidas = []

while True:
    info_dict = {}
    info_dict['Player'] = str(input('Player Name: '))

    # Number of games played by the player
    games = int(input('How many games did {} play: '.format(info_dict['Player'])))

    # Collect goals for each game
    partidas.clear()  # Clear previous games' goals
    for i in range(games):
        partidas.append(int(input('How many goals in game {}: '.format(i + 1))))

    # Store the goals and total goals in the player's dictionary
    info_dict['Goals'] = partidas[:]
    info_dict['Total'] = sum(partidas)

    # Add the player's information to the list
    info_list.append(info_dict.copy())

    # Ask the user if they want to continue
    option = str(input('Do you want to continue [Y/N]: ')).upper().strip()
    print()
    if option == 'N':
        break
    elif option == 'Y':
        continue
    else:
        print('Please enter Y (YES) or N (NO)!')

# Display the header
print('-=' * 30)
print('cod  ', end='')
for i in info_dict.keys():
    print('{:<15}'.format(i), end='')
print()
print('-' * 40)

# Display the players' data
for k, v in enumerate(info_list):
    print('{:>2} '.format(k), end='')
    for d in v.values():
        print(' {:<15}'.format(str(d)), end='')
    print()
print('-' * 40)

# Allow the user to lookup specific player's data
while True:
    search = int(input('Show data of which player? (999 to exit) '))
    if search == 999:
        break
    if search >= len(info_list):
        print('ERROR! No player with code {}!'.format(search))
    else:
        print(' -- PERFORMANCE OF PLAYER {}'.format(info_list[search]['Player']))
        for i, g in enumerate(info_list[search]['Goals']):
            print('   In game {} scored {} goals.'.format(i + 1, g))
    print('-' * 30)
