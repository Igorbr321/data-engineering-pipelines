def soma(a, b):
    print('A = {} e B = {}.'.format(a, b))
    s = a + b 
    print('A soma de A + B = {}.'.format(s))


def contador(* num):
    tam = len(num)
    print('Recebi os valores {} e são ao todo {} números.'.format(num, tam))

def cont(* num):
    for valor in num:
        print('{}'.format(valor), end=' ')
    print('Fim!')   

def somas(* valores):
    s = 0
    for num in valores:
        s += num
    print('Somando os valores {} temos {}'.format(valores, s))

contador(2, 1, 7)
contador(8, 0)
contador(4, 4, 7, 6, 2)
print()
cont(2, 1, 7)
cont(8, 0)
cont(4, 4, 7, 6, 2)
print()
somas(2, 4, 5)
