frase = input('Digite uma frase: ').upper().strip()
print('Quantas vezes aparece a letra A: {}'.format(frase.count('A')))
print('Em que posição a primeira letra A '
      'aparece: {}'.format(frase.find('A') + 1))
print('Em que posição aparece a '
      'última letra A: {}'.format(frase.rfind('A') + 1))
