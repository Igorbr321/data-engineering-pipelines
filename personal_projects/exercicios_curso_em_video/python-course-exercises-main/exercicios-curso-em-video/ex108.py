import ex108_moeda as moeda

#Programa principal
money = float(input('Digite o preço: R$'))

print('A metade de {} é {}.'.format(moeda.ajustar_moeda(money), moeda.ajustar_moeda(moeda.metade(money))))
print('O dobro de {} é {}.'.format(moeda.ajustar_moeda(money), moeda.ajustar_moeda(moeda.dobro(money))))
print('Aumentando 10% de {} é {}.'.format(moeda.ajustar_moeda(money), moeda.ajustar_moeda(moeda.aumentar(money, 10))))
print('Diminuindo 10% de {} é {}.'.format(moeda.ajustar_moeda(money), moeda.ajustar_moeda(moeda.diminuir(money, 10))))


