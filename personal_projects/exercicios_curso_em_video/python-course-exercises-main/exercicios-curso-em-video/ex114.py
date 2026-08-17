import urllib.error
import urllib.request

try: 
    site = urllib.request.urlopen('https://www.instagram.com/')
    print('Consegui acessar o instagram com sucesso.')
except urllib.error.URLError as e:
    print('O site Instagram não está acessível no momento.')
    print(f'Detalhes do erro: {e}')
