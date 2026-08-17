print('\033[1;31m ===== \033[m' * 9)
print('                    \033[1;39mAnalisador De Dados\033[m')
print('\033[1;31m ===== \033[m' * 9)
print('')

quant = int(input('Quantidades de pessoas para análise: '))
contm = 0
maiorh = 0
menorm = 0
for p in range(1, quant + 1):
    nome = str(input('Nome da {}ª pessoa: '.format(p))).strip()
    idade = int(input('Idade da {}ª pessoa: '.format(p)))
    sexo = str(input('Sexo da {}ª pessoa [M] [F]: '.format(p))).upper().strip()
    print('\033[1;31m----------\033[m' * 5)
    contm += idade
    if sexo == 'M':
        if p == 1:
            maiorh = idade
        else:
            if idade > maiorh:
                maiorh = nome
    if sexo == 'F':
        if idade <= 20:
            menorm += 1
media = contm / quant
print('A média de idade do grupo é {} anos.'.format(media))
print('O nome do homem mais velho é {}.'.format(maiorh))
print('A idade de mulheres com menos de 20 anos é {}.'.format(menorm))
