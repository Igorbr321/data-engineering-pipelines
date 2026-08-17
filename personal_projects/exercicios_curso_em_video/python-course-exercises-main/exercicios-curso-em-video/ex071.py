from test_functions import calculate_notes_withdrawal, print_notes

print('==' * 25)
print('{:^45}'.format('CEV BANK'))
print('==' * 25)

cash = int(input('What amount do you want to withdraw? $'))

notes_50, notes_20, notes_10, notes_1 = calculate_notes_withdrawal(cash)
print_notes(notes_50, notes_20, notes_10, notes_1)
