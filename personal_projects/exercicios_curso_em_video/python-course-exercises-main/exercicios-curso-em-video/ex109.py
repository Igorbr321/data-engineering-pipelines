import ex109_moeda as moeda

#Programa principal
money = float(input('Digite o preço: R$'))

print('A metade de R${} é R${}.'.format(money, moeda.metade(money, True)))
print('O dobro de R${} é R${}.'.format(money, moeda.dobro(money, True)))
print('Aumentando 10% de R${} é R${}.'.format(money, moeda.aumentar(money, 10, True)))
print('Diminuindo 10% de R${} é R${}.'.format(money, moeda.diminuir(money, 10, True)))

