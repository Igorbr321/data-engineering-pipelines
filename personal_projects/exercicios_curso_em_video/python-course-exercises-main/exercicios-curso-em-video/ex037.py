num = int(input('Digite um número inteiro: '))
print('Escolha uma das bases para conversão:')
print('''[ 1 ] Converter para DECIMAL
[ 2 ] Convertar para OCTAL
[ 3 ] Converter para HEXADECIMAL''')
opcao = int(input('Sua opção: '))
if opcao == 1:
    bin = bin(num)
    print('Seu número é {} e a conversão para BINÁRIO é {}'.format(num, bin[2:]))
elif opcao == 2:
    oct = oct(num)
    print('Seu número é {} e a conversão para OCTAL é {}'.format(num, oct[2:]))
elif opcao == 3:
    hex = hex(num)
    print('Seu número é {} e a conversão para HEXADECIMAL é {}'.format(num, hex[2:]))
else:
    print('\033[1;35mDigite um número de 1 a 3 por favor!\033[m')
