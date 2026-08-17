import datetime
ano_nasc = int(input('Ano de Nascimento do atleta: '))
ano_atual = datetime.date.today().year
idade = ano_atual - ano_nasc

if idade <= 9:
    print('Mirim')
elif idade <= 14:
    print('Infantil')
elif idade <= 19:
    print('Júnior')
elif idade <= 25:
    print('Sênior')
else:
    print('Master')
