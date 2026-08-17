import emoji
from time import sleep
import random
print('\033[1;36m-=--\033[m' * 15)
print(emoji.emojize('\033[1mVou pensar em um número entre 0 a 5, '
                    'adivinhe qual :fire:\033[m'))
print('\033[1;36m-=--\033[m' * 15)
lista = [0, 1, 2, 3, 4, 5]
r = random.choice(lista)  #randint(0,5)
pessoa = int(input('\033[0;30mEm que número eu pensei? \033[m'))
print('\033[0;35mPROCESSANDO...\033[m')
sleep(2)
if pessoa == r:
    print('\033[1;32mGANHOU!!!! Você digitou {}, e eu escolhi {}, '
          'PARABÉNS RUIM!\033[m'.format(pessoa, r))
else:
    print('\033[1;31mPERDEU!!! Você digitou {}, e eu escolhi {}, '
          'HORRÍVEL, TENTE NOVAMENTE.\033[m'.format(pessoa, r))
