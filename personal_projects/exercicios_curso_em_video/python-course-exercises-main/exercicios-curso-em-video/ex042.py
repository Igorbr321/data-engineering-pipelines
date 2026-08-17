lado1 = int(input('Primeiro lado do triângulo: '))
lado2 = int(input('Segundo lado do triângulo: '))
lado3 = int(input('Terceiro lado do triângulo: '))

if lado1 == lado2 == lado3:
    print('EQUILÁTERO')
elif lado1 != lado2 != lado3 != lado1:
    print('ESCALENO')
else:
    print('ISÓSCELES')
