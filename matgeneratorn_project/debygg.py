matlista = {u'Tisdag': {'dish': u'k\xf6ttsoppa', 'ingredients': {u'k\xf6ttf\xe4rs': {'unit': u'gram', 'quantity': 100.0}, u'mor\xf6tter': {'unit': u'st', 'quantity': 14.0}}}, u'M\xe5ndag': {'dish': u'k\xf6ttsoppa', 'ingredients': {u'k\xf6ttf\xe4rs': {'unit': u'gram', 'quantity': 100.0}, u'mor\xf6tter': {'unit': u'st', 'quantity': 14.0}}}}
ingredient_list = []

for day in matlista:
    for ingredient in matlista[day]['ingredients']:
        if ingredient_list:
            for food_item in ingredient_list:
                if food_item.keys()[0] == ingredient:
                    food_item[ingredient]['quantity'] += matlista[day]['ingredients'][ingredient]['quantity']
                else:
                    ingredient_list.append({ingredient: matlista[day]['ingredients'][ingredient]})
        else:
            ingredient_list.append({ingredient: matlista[day]['ingredients'][ingredient]})
