def metade(number = 0, formato = False):
    n = number / 2

    return n if not formato else ajustar_moeda(n)

def dobro(number = 0, formato = False):
    n = number * 2

    return n if not formato else ajustar_moeda(n)

def aumentar(number = 0, taxa = 0, formato = False):
    n = (number * taxa/100) + number

    return n if not formato else ajustar_moeda(n)

def diminuir(number = 0, taxa = 0, formato = False):
    n = number - (number * taxa/100) 

    return n if not formato else ajustar_moeda(n)

def ajustar_moeda(moeda = 0, cifrao = 'R$'):
    return ('{}{:.2f}'.format(cifrao, moeda)).replace('.', ',')


def resumo(price = 0, aumento = 0, redução = 0):
    print('-' * 35)
    print('RESUMO DO VALOR'.center(35))
    print('-' * 35)

    print('Preço analisado: \t{}'.format(ajustar_moeda(price), True))
    print('Dobro do preço: \t{}'.format(dobro(price, True)))
    print('Metade do preço: \t{}'.format(metade(price, True)))
    print('{}% de aumento: \t{}'.format(aumento, aumentar(price, aumento, True)))
    print('{}% de redução: \t{}'.format(redução, diminuir(price, redução, True)))
    print('-' * 35)
