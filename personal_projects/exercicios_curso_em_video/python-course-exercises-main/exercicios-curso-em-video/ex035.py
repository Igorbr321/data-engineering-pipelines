print('\033[1;34m-=-=\033[m' * 15)
print('               \033[1;34m Analisador de Triângulos \033[m')
print('\033[1;34m-=-=\033[m' * 15)
a = float(input('Primeiro segmento: '))
b = float(input('Segundo segmento: '))
c = float(input('Terceiro segmento: '))
if a + b > c and a + c > b and a + b > c:
    print('Os segmentos acima PODEM FORMAR um triângulo.')
else:
    print('Os segmentos acima NÃO PODEM FORMAR um triângulo.')
