carro = int(input('Qual a velocidade atual do carro: '))
multa = (carro - 80) * 7
if carro <= 80:
    print('\033[1;32mTenha um bom dia! Dirija com segurança!\033[m')
else:
    print('\033[1;31mVocê foi multado, e ultrapassou os 80km/h.')
    print('Você deve pagar uma multa de\033[m '
          '\033[4;31mR${:.2f}!\033[m'.format(multa))
    print('\033[1;32mTenha um bom dia! Dirija com segurança!\033[m')
