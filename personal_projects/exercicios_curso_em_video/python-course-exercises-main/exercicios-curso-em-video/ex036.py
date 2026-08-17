valor_casa = float(input('Valor da casa: R$'))
salario_comprador = float(input('Salário do comprador: R$'))
anos_pagamento = int(input('Quantos anos de financiamento: '))

prestacao = valor_casa / (anos_pagamento * 12)
emprestimo = salario_comprador * 0.3

if emprestimo > prestacao:
    print('Para pagar uma casa de R${:.2f} em {} anos a prestação'
          ' será de R${:.2f}.'.format(valor_casa, anos_pagamento, prestacao))
    print('\033[1;32mEmpréstimo LIBERADO.\033[m.')
else:
    print('Para pagar uma casa de R${:.2f} em {} anos a prestação'
          ' será de R${:.2f}.'.format(valor_casa, anos_pagamento, prestacao))
    print('\033[1;31mEmpréstimo NEGADO.\033[m.')

