somapar = 0
for c in range(1, 6):
    num = int(input('Digite o {}º número: '.format(c)))
    if num % 2 == 0:
        somapar += num
print('A soma dos números pares é {}.'.format(somapar))

