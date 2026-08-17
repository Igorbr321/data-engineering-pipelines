import datetime
atual = datetime.date.today().year
contadormaior = 0
contadormenor = 0
for c in range(1, 8):
    pessoa = int(input('{}º ano de nascimento: '.format(c)))
    idade = atual - pessoa
    if idade >= 18:
        contadormaior += 1
    else:
        contadormenor += 1
print('Existem {} pessoas maiores de idade.'.format(contadormaior))
print('Existem {} pessoas menores de idade.'.format(contadormenor))

