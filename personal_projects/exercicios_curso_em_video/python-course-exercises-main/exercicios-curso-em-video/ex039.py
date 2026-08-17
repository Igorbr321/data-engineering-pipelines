import datetime
ano_nasc = int(input('Informe seu ano de nascimento: '))
ano_atual = datetime.date.today().year
idade = ano_atual - ano_nasc

if idade > 18:
    print('Você já passou da idade de se alistar.')
elif idade < 18:
    print('Você ainda não tem idade para se alistar.')
else:
    print('Você pode se alistar esse ano.')

