teams_brasileirao = (
    "Corinthians", "Flamengo", "Atlético Mineiro", "Palmeiras", "Fortaleza",
    "Bragantino", "Athletico Paranaense", "Ceará", "Santos", "Internacional",
    "Juventude", "Fluminense", "Atlético Goianiense", "América Mineiro",
    "Sport Recife", "Bahia", "São Paulo", "Cuiabá", "Grêmio", "Chapecoense"
)

five_placed = ', '.join(teams_brasileirao[0:5])
four_last_placed = ', '.join(teams_brasileirao[-4:])
order_alphabetic = ', '.join(sorted(teams_brasileirao))

print('\nThe five first teams: {}.'.format(five_placed))
print('\nThe last four teams: {}.'.format(four_last_placed))
print('\nOrder alphabetic: {}.\n'.format(order_alphabetic))

while True:
    choose_team = input('Choose the team to know its position: ').upper()
    teams_brasileirao_maiusc = tuple(team.upper() for team in teams_brasileirao)
    try:
        index = teams_brasileirao_maiusc.index(choose_team)
        print('Your teams place is {}th'.format(index + 1))
        break
    except ValueError:
        print('Team not founded.')
