from time import sleep

print('-----' * 8)
print('               AMAZON')
print('-----' * 8)

total_price = product_sum_price = 0
min_price = float ('inf')
min_price_product = ''

while True:
    products = input('Type it the name of the product: ').strip().upper()
    while True:
        try:
            int(products)
            print('Please, type it the name of the one product.')
            products = input('Type it the name of the product again: ').strip().upper()
        except ValueError:
            break
        
    while True:
        try:
            price = float(input('Type it the value of the product: R$'))
            break 
        except ValueError:
            print('Please, type it one value to the product.')

    total_price += price

    if price >= 1000:
        product_sum_price += 1

    if price < min_price:
        min_price = price
        min_price_product = products

    while True:
        question = str(input('\nDo you want to continue [Y or N]? ')).strip().upper()
        question_first_letter = question[0]

        if question_first_letter == 'N':
            print('Total price of all product: R${:.2f}'.format(total_price))
            print('There are {} products greater than R$1000,00. '.format(product_sum_price))
            print('Name of the prodcut with lowest price: {} '.format(min_price_product))
            print('Exiting...')
            sleep(2)
            exit()
        elif question_first_letter == 'Y':
            print('')
            break
        else:
            print('Choose one of the options, YES or NO.')



