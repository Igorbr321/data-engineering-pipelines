print('=====' * 6)
print('         10 Termos PA')
print('=====' * 6)

p = int(input('Primeiro Termo: '))
r = int(input('Razão: '))

termo = p
cont = 1
total = 0
mais = 10

while mais != 0:
    total += mais
    while cont <= total:
        print('{} -->'.format(termo), end=' ')
        termo += r
        cont += 1
    print('Pausa')
    mais = int(input('Quantos termos você quer mostrar a mais? '))
print('Projeto finalizado com {} termos mostrados.'.format(termo))
