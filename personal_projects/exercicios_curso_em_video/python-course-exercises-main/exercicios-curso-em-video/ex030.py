numero = int(input('\033[1mPar ou impar? Digite seu número:\033[m '))
if numero % 2 == 0:
    print('\033[1;32mPar\033[m')
else:
    print('\033[1;31mImpar\033[m')
