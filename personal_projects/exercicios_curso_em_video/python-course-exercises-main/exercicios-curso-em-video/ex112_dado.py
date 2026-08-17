def leia_dinheiro(msg):
    valido = False
    while not valido:
        entrada = str(input(msg)).replace(',', '.')
        if entrada.isalpha() or entrada.strip() == '':
            print('\033[0;31mERRO:\"{}\" é um preço válido.\033[m'.format(entrada))
        else:
            valido = True
            return float(entrada)