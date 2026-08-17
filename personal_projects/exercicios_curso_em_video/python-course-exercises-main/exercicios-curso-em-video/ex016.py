from math import trunc
n = float(input('Digite um número: '))
real = trunc(n)  # pega somente o primeiro número
print('Seu valor é {}, sua porção inteira é {} '.format(n, real))
