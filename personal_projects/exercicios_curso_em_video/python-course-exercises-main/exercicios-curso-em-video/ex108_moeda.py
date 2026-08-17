def metade(number = 0):
    n = number / 2

    return n

def dobro(number = 0):
    n = number * 2

    return n 

def aumentar(number = 0, taxa = 0):
    n = (number * taxa/100) + number

    return n

def diminuir(number = 0, taxa = 0):
    n = number - (number * taxa/100) 

    return n

def ajustar_moeda(moeda = 0, cifrao = 'R$'):
    return ('{}{:.2f}'.format(cifrao, moeda)).replace('.', ',')
