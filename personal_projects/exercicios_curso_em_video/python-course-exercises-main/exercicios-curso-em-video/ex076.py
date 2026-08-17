school_supplies = (
    'Notebook', 15.99,
    'Pencil', 1.50,
    'Pen', 2.00,
    'Eraser', 0.75,
    'Pencil Case', 5.99,
    'Ruler', 1.25,
    'Backpack', 29.99,
    'Book', 12.99,
    'Planner', 7.50,
    'Calculator', 19.99
)

print('-----' * 8 )
print('{:^40}'.format('PRICE LIST'))
print('-----' * 8 )

for pos in range(0, len(school_supplies)):
    if pos % 2 == 0:
        print('{:.<30}'.format(school_supplies[pos]), end='')
    else:
        print('R${:>7.2f}'.format(school_supplies[pos]))

print('-----' * 8)