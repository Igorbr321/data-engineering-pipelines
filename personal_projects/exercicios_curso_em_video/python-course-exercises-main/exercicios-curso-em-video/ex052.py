num = int(input('Digite um número para saber se ele é primo: '))
contador = 0
for c in range(1, num+1):
    if num % c == 0:
        print('\033[33m', end=' ')
        contador += 1
    else:
        print('\033[31m', end=' ')
    print(c, end=' ')
print('\n\033[mO número {} tem {} divisores.'.format(num, contador))
if contador == 2:
    print('E por isso ele é PRIMO!')
else:
    print('E por isso ele NÃO É PRIMO!')
