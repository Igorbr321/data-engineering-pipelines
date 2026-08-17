import ex45_main as sub

for c in range(99999):
    print('\033[1;34m-=\033[m' * 10, end=' ')
    print('\033[1;39mJO-KEN-PÔ\033[m', end=' ')
    print('\033[1;34m-=\033[m' * 10)
    print('''Suas opções:
    [ 1 ] PEDRA
    [ 2 ] PAPEL 
    [ 3 ] TESOURA''')

    sub.jogo()


