def vote(year):
    import datetime

    # Get the current year
    current_year = datetime.datetime.now().year

    # Calculate the age based on the birth year
    age = current_year - year

    # Determine the voting status based on the age
    if 18 <= age <= 70:
        return 'At {} years old: VOTING IS MANDATORY.'.format(age)
    elif age >= 15:
        return 'At {} years old: VOTING IS OPTIONAL.'.format(age)
    else:
        return 'At {} years old: DOES NOT VOTE.'.format(age)


# Prompt the user for their birth year
birth_year = int(input('What year were you born? '))
print(vote(birth_year))

