def cook_book(fail):
    cook_book = {}
    with open(fail, encoding='UTF-8') as f:
       a = []
       for i in f:
           a.append(i)
    b = ''.join(a).strip()
    recepts_list = b.split('\n\n')
    for j in recepts_list:
        q = j.split('\n')
        w = 0
        cook_book[q[0]] = []
        while w < int(q[1]):
            p = q[w+2].split('|')
            ingredient = {'ingredient_name': p[0], 'quantity': p[1], 'measure': p[2]}
            cook_book[q[0]].append(ingredient)
            w += 1
    return cook_book

print(cook_book('Recepts.txt'))