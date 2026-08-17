import random

#layout
print('\033[1;39mSou seu computador...\033[m')
print('\033[1;36mAcabei de pensar em um número de 0 a 10.')
print('Será que você consegue adivinhar qual foi?\033[m')

#escolha pc
pc = random.randint(1, 10)

#escolha jogador
jogador = int(input('Qual seu palpite? '))

#contador erros
erro = 0

while jogador != pc:
    if jogador > pc:
        print('Menos... Tente mais uma vez.')
        jogador = int(input('Qual seu palpite? '))
        erro += 1
    else:
        print('Mais... Tente mais uma vez.')
        jogador = int(input('Qual seu palpite? '))
        erro += 1
print('Acertou com {} tentativas. Parabéns.'.format(erro))
