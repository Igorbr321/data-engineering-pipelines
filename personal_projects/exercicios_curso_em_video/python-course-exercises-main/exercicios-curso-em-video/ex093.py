# Creating a dictionary to store player's information
player = dict()
goals_per_match = []
total_goals = 0

# Input for the player's name
player['Name'] = str(input("Player's Name: "))

# Input for the number of matches played
matches = int(input('How many matches did {} play? '.format(player['Name'])))

# Collecting the number of goals in each match
for c in range(matches):
    goals = int(input('How many goals in match {}: '.format(c + 1)))
    total_goals += goals
    goals_per_match.append(goals)

# Storing the list of goals and total goals in the player dictionary
player['Goals'] = goals_per_match
player['Total'] = total_goals

# Printing the player dictionary
print('-=' * 30)
print(player)
print('-=' * 30)

# Iterating over the items in the player dictionary and printing them
for k, v in player.items():
    print('The field {} has the value {}.'.format(k, v))
print('-=' * 30)

# Printing a summary of the player's performance
print('Player {} played {} matches.'.format(player['Name'], matches))
for i, v in enumerate(goals_per_match):
    print('   => In match {}, scored {} goals.'.format(i + 1, v))
print('A total of {} goals.'.format(total_goals))
