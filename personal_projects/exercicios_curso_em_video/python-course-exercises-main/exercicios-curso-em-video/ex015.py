k = int(input('Kilometros percorridos: '))
d = int(input('Dias alugados: '))
km = k * 0.15
dm = d * 60
total = dm + km
print('Preço de Km percorrido {:.2f}.'.format(km))
print('Preço de dias com o carro alugado {:.2f}'.format(dm))
print('Preço total {:.2f}'.format(total))
