from time import sleep
pvalor = int(input('Primeiro valor: '))
svalor = int(input('Segundo valor: '))

opcao = 0
while opcao != 5:
    print('''            [ 1 ] somar
            [ 2 ] multiplicar
            [ 3 ] maior
            [ 4 ] novos números
            [ 5 ] sair do programa''')
    opcao = int(input('>>>>> Qual é a sua opção? '))

    if opcao == 4:
        print('Informe os números novamente.')
        pvalor = int(input('Primeiro valor: '))
        svalor = int(input('Segundo valor: '))
        sleep(1)

    elif opcao == 1:
        soma = pvalor + svalor
        print('A soma dos valores {} + {} '
              '= {}.'.format(pvalor, svalor, soma))
        sleep(1)
        print('\033[1;31m===\033[m' * 12)

    elif opcao == 2:
        mult = pvalor * svalor
        print('A multiplicação dos valores {} x {} '
              '= {}'.format(pvalor, svalor, mult))
        sleep(1)
        print('\033[1;31m===\033[m' * 12)

    elif opcao == 3:
        if pvalor > svalor:
            print('O maior valor é {}.'.format(pvalor))
        else:
            print('O maior valor é {}.'.format(svalor))
        sleep(1)
        print('\033[1;31m===\033[m' * 12)

    elif opcao == 5:
        print('Finalizando...')
        sleep(1)
        print('Volte sempre :)')

    else:
        print('Opção inválida. Tente novamente!')
        print('\033[1;31m===\033[m' * 12)
        sleep(1)









