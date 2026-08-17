c = 0
s = 0
n = 0
while n != 999:
    n = int(input('Digite um número [999 para parar]: '))
    s += n
    c += 1
print('Você digitou {} números e a soma dele é {}.'.format((c - 1), (s - 999)))
