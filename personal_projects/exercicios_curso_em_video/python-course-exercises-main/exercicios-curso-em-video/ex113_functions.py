def leia_int(msg):
    while True:
        try:
            n = int(input(msg))
            break
        except (ValueError, TypeError):
            print('\033[0;31mERRO: Digite um número inteiro válido.\033[m')

    return n    


def leia_float(msg):
    while True:
        try:
            n = float(input(msg))
            if n.is_integer():
                print('\033[0;31mERRO: Digite um número decimal válido.\033[m')
            else:
                break
        except (ValueError, TypeError):
            print('\033[0;31mERRO: Digite um número decimal válido.\033[m')

    return n 


