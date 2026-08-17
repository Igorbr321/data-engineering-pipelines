p = float(input('Digite o valor do produto: R$'))
d = p - (p * 0.05)
print('Seu produto custa R${:.2f}, e com desconto de 5%'
      ' sai pelo preço de R${:.2f}'.format(p, d))
