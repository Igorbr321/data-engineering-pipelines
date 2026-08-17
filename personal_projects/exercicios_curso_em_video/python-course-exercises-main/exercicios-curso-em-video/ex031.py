viagem = int(input('Qual é a distância da sua viagem: '))
print('Você está prestes a começar uma viagem de {}km'.format(viagem))
if viagem <= 200:
    promo = viagem * 0.5
    print('E o preço da sua passagem será de R${:.2f}'.format(promo))
else:
    normal = viagem * 0.45
    print('E o preço da sua passagem será de R${:.2f}'.format(normal))
