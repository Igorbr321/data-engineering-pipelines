def titulo(t):
    print('-=' * 20)
    print('{:^40}'.format(t))
    print('-=' * 20)

def area(larg, comp):
    a = larg * comp
    print('A área de um terreno {}x{} é de {}m².'.format(larg, comp, a))



titulo('Controle de Terrenos')

l = float(input('LARGURA (m): '))
c = float(input('COMPRIMENTO (m): '))
area(l, c)

