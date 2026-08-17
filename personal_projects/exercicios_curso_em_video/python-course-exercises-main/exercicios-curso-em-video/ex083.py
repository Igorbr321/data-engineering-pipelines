expr = str(input('Enter the expression: '))
stack = []
for char in expr:
    if char == '(':
        stack.append('(')
    elif char == ')':
        if len(stack) > 0:
            stack.pop()
        else:
            stack.append(')')
            break

if len(stack) == 0:
    print('Your expression is valid!')
else:
    print('Your expression is invalid!')

