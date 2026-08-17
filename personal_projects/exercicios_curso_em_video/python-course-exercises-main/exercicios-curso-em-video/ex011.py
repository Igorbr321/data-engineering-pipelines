l = float(input('Largua da parede: '))
a = float(input('Altura da parede: '))
m2 = l * a
t = m2 / 2
print('Sua parede tem a dimensão de {}x{} e sua área '
      'é de {}m².'.format(l, a, m2))
print('Para pintar essa parede, você precisará '
      'de {}L de tinta.'.format(t))

