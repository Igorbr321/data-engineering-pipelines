while True:
    question = int(input('multiplication table: ')) 
    if question < 0:
        break

    c = 0
    while c != 11:
        print('{} x {} = {} '.format( question ,c, (question * c)))
        c += 1

    



    

