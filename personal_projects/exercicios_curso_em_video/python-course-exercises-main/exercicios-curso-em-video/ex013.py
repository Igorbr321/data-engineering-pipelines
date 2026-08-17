s = float(input('Digite seu salário atual: R$'))
a = s + (s * 0.15)
print('Seu salário atual é R${:.2f}, com aumento '
      'de 15% é R${:.2f}'.format(s, a))
