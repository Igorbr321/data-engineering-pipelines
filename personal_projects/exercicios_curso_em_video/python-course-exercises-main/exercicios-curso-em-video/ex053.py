for c in range(5):
    frase = str(input('Digite algo: ')).upper().strip()
    juntar = frase.replace(' ', '')
    fraseinv = juntar[::-1]
    if juntar == fraseinv:
        print('Está frase é um PALÍNDROMO.')
    else:
        print('Está frase NÃO É UM PALÍNDROMO.')
    print('')


