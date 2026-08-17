n = input('Digite seu nome completo: ').strip()
print('Analisando a sua frase...')
print('Seu nome em maiúsculas é {}'.format(n.upper()))
print('Seu nome em minúsculas é {}'.format(n.lower()))
print('Seu nome tem ao todo {} letras.'.format(len(n) - n.count(' ')))
separa = n.split()
print('Seu primeiro nome é {} e ele tem {} letras'.format(separa[0], len(separa[0])))
      