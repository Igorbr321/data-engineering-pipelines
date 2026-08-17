print('=====' * 6)
print('         10 Termos PA')
print('=====' * 6)

p = int(input('Primeiro Termo: '))
r = int(input('Razão: '))

c = 0
while c != 10:
    print('{} -->'.format(p), end=' ')
    p += r
    c += 1
print('Acabou!')

