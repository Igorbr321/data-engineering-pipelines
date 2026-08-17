from datetime import date
ano = int(input('Qual ano você quer analisar ? Digite 0 para'
                ' verficiar o ano atual. '))
if ano == 0:
    ano = date.today().year
if ano % 4 == 0 and ano % 100 != 0 or ano % 400 == 0:
    print('\033[1;32mO ano de {} é BISSEXTO.\033[m'.format(ano))
else:
    print('\033[1;31mO ano de {} NÃO é BISSEXTO.\033[m'.format(ano))
