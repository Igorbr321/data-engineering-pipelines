def player_profile(name, goals=0):
    # Check if the name is empty and set to '<unknown>' if it is
    if not name:
        name = '<unknown>'
    
    # Try to convert goals to an integer
    try:
        goals = int(goals)
    except (ValueError, TypeError):
        # If conversion fails, set goals to 0
        goals = 0
    
    # Print the player's profile
    print('The player {} scored {} goal(s) in the championship.'.format(name, goals))


# Get player name from user input
player_name = input('Player name: ')
# Get number of goals from user input
player_goals = input('Number of goals: ')

# Call the function with the user inputs
player_profile(player_name, player_goals)
