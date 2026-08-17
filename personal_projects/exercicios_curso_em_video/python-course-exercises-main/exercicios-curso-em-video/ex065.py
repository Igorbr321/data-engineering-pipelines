c = 0
s = 0
num_int = 0
menor_numero = float('inf')
maior_numero = float('-inf')

while True:
    num_int = int(input('Digite um número: '))
    c += num_int
    s += 1
    
    menor_numero = min(menor_numero, num_int)
    maior_numero = max(maior_numero, num_int)
        
    question = str(input('Quer continuar [S] ou [N]? ')).strip().upper()
    if question == 'N':
        break

if s == 0:
    print('Nenhum número foi inserido.')
else:
    media = c / s
    print('A soma dos valores é {}, o número de valores inseridos é {}, a média dos valores inseridos é {:.2f}'.format(c, s, media))
    print('O menor número inserido foi {} e o maior número inserido foi {}'.format(menor_numero, maior_numero))
