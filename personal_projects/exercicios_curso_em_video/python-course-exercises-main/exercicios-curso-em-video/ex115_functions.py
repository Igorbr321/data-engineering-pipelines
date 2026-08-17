info_list = list()

def menu():
    print('-' * 45)
    print('MENU PRINCIPAL'.center(45))
    print('-' * 45)

    print('''1 - Ver pessoas cadastradas
2 - Cadastrar nova pessoa
3 - Sair do sistema''')
    
    print('-' * 45)

    while True:
        n = erros('Digite sua opção: ')
        if n >= 1 and n <= 3:
            condicoes_opcoes(n)
        else:
            print('Digitar um número entre 1 e 3, por favor!')


def pessoas_cadastradas():
    print('-' * 45)
    print('OPÇÃO 1'.center(45))
    print('-' * 45)

    print('{:<20} {:>5}'.format('Name', 'Age'))
    print('-' * 27)
    for pessoa in info_list:
        print('{:<20} {:>5}'.format(pessoa['name'], pessoa['idade']))
    print('-' * 45)

    
def cadastrar_nova_pessoa():
    print('-' * 45)
    print('OPÇÃO 2'.center(45))
    print('-' * 45)

    info_dict = dict()
    
    info_dict['name'] = input('Digite o nome: ').upper().strip()
    info_dict['idade'] = int(input('Digite sua idade: '))

    info_list.append(info_dict)
    print('-' * 45)

def sair_do_sistema():
    from time import sleep
    print('-' * 45)
    print('OPÇÃO 3'.center(45))
    print('-' * 45)

    print('Saindo do Programa...')
    print('-' * 45)
    sleep(2)
    exit()


def condicoes_opcoes(i = 0):
    while True:
        if i == 1:
            pessoas_cadastradas()
            break
        elif i == 2:
            cadastrar_nova_pessoa()
            break
        elif i == 3:
            sair_do_sistema()
            break

def erros(msg):
    while True:
        try:
            option_int = int(input(msg))
            break
        except (ValueError, TypeError):
            print('ERRO! Digite uma das opções.')

    return option_int
