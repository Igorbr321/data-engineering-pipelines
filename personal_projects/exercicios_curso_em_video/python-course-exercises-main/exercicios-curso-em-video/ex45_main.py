def jogo():
    #Bibliotecas
    import random
    from time import sleep

    #Info
    lista = ['Pedra', 'Papel', 'Tesoura']
    pc = random.choice(lista)
    jogador = int(input('Qual a sua jogada? '))

    #Timer
    print('\033[1;32mJO\033[m')
    sleep(0.5)
    print('\033[1;32mKEN\033[m')
    sleep(0.5)
    print('\033[1;32mPÔ\033[m')
    sleep(0.5)

    #Game
    if jogador == 1 and pc == 'Papel':
        jogador = 'Pedra'
        print('Você Perdeu, eu escolhi {} e você escolheu {}'.format(pc, jogador))
    elif jogador == 1 and pc == 'Tesoura':
        jogador = 'Pedra'
        print('Você Ganhou, eu escolhi {} e você escolheu {}.'.format(pc, jogador))
    elif jogador == 2 and pc == 'Pedra':
        jogador = 'Papel'
        print('Você Ganhou, eu escolhi {} e você escolheu {}.'.format(pc, jogador))
    elif jogador == 2 and pc == 'Tesoura':
        jogador = 'Papel'
        print('Você Perdeu, eu escolhi {} e você escolheu {}.'.format(pc, jogador))
    elif jogador == 3 and pc == 'Pedra':
        jogador = 'Tesoura'
        print('Você Perdeu, eu escolhi {} e você escolheu {}.'.format(pc, jogador))
    elif jogador == 3 and pc == 'Papel':
        jogador = 'Tesoura'
        print('Você Ganhou, eu escolhi {} e você escolheu {}.'.format(pc, jogador))
    else:
        print('Empate! Tente outra vez.')


