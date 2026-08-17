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