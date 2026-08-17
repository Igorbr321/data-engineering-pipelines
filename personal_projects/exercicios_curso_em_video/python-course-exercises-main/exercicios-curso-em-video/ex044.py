print('\033[1;34m=\033[m'*10, end=' ')
print('\033[;1;39mLOJAS IGOR\033[m', end=' ')
print('\033[1;34m=\033[m'*10)
valor = float(input('Preço da compra: R$ '))
print('''FORMAS DE PAGAMENTO
[ 1 ] á vista dinheiro/cheque
[ 2 ] á vista cartão
[ 3 ] 2x no cartão 
[ 4 ] 3x ou mais no cartão''')
opcao = int(input('Qual é a opção: '))

if opcao == 1:
    desconto = valor - (valor * 0.1)
    print('\033[1;39mEscolhendo a opção de pagar a vista/cheque, '
          'desconto de 10% na compra.\033[m')
    print('\033[1;32mSua fatura com desconto: R${:.2f}\033[m'.format(desconto))
elif opcao == 2:
    desconto = valor - (valor * 0.05)
    print('\033[1;39mEscolhendo a opção de pagar a cartão, '
          'desconto de 10% na compra.\033[m')
    print('\033[1;32mSua fatura com desconto: R${:.2f}\033[m'.format(desconto))
elif opcao == 3:
    parcelado = valor / 2
    print('\033[1;39mEscolhendo a opção de parcelar em 2x no cartão, não '
          'possue desconto.\033[m')
    print('\033[1;32mParcelado: (2x){:.2f}\033[m'.format(parcelado))
elif opcao == 4:
    parcelas = int(input('Número de parcelas: '))
    juros = valor + (valor * 0.2)
    parcelado = juros / parcelas
    print('\033[1;39mEscolhendo a opção de parcelar em mais de 3x no cartão, '
          'terá juros de 20%, no preço total da compra.\033[m')
    print('\033[1;34mSua compra com juros será de {:.2f}.\033[m'.format(juros))
    print('\033[1;32mParcelado: ({}x){:.2f}\033[m'.format(parcelas, parcelado))

else:
    print('\033[1;31mDIGITE UMA DAS OPÇÕES!\033[m')
