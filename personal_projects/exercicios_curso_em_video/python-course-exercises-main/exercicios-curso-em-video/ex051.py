print('=====' * 6)
print('         10 Termos PA')
print('=====' * 6)
p = int(input('Primeiro Termo: '))
r = int(input('Razão: '))
d = p + (10 - 1) * r
for c in range(p, d + r, r):
    print('{} '.format(c), end='--> ')
print('Acabou.')
