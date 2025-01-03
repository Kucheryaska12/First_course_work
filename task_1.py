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
            ingredient = {'ingredient_name': p[0].strip(), 'quantity': p[1].strip(), 'measure': p[2].strip()}
            cook_book[q[0]].append(ingredient)
            w += 1
    return cook_book



def get_shop_list_by_dishes(dishes, person_count):
    ingredients_list = {}
    cook_book1 = cook_book('Recepts.txt')
    for i in dishes:
        if i in cook_book1:
            for j in cook_book1[i]:
                if j['ingredient_name'] not in ingredients_list:
                    ingredients_list[j['ingredient_name']] = {'measure': j['measure'], 'quantity' : int(j['quantity']) * person_count}
                else:
                    ingredients_list[j['ingredient_name']]['quantity'] += int(j['quantity']) * person_count
    return ingredients_list

