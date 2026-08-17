import math
ca = float(input('Cateto adjacente: '))
co = float(input('Cateto oposto: '))
s = (math.pow(ca, 2)) + (math.pow(co, 2))
h = math.sqrt(s)
print('A hipotenusa é {:.2f}'.format(h))
