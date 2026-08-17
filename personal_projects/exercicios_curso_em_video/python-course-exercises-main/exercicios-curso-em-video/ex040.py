nota1 = int(input('Informe sua primeira nota: '))
nota2 = int(input('Informe sua segunda nota: '))
nota3 = int(input('Informe sua terceira nota: '))
nota4 = int(input('Informe sua quarta nota: '))
media = (nota1 + nota2 + nota3 + nota4) / 4
if media >= 7:
    print('\033[1;32mAPROVADO\033[m')
elif media >= 5:
    print('\033[1;33mRECUPERAÇÃO\033[m')
else:
    print('\033[1;31mREPROVADO\033[m')
