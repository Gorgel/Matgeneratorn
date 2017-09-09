# -*- coding: utf-8 -*-
from django.shortcuts import render
from matgeneratorn.models import RecipeType, Recipe
from matgeneratorn.forms import portionsForm
from trello import TrelloClient
import copy

# trello keys
API_KEY = '642dd513d9c2ca3fffc425897e303742'
API_SECRET = 'b9dc91fb518e31715cdd3645fd06c764417ab65384b9472d929a4d1efeaf93ce'
TOKEN = '132abffaab0ef0c9550d573dddf64bf7aa8d0c0304c94877282d0ef110725b67'

# helper functions

# generate matlista data structure
def gen_empty_matlista():
    # create data structure
    matlista = {u'Måndag': {
        'dish': None, 'ingredients': {}
    },
        u'Tisdag': {
            'dish': None, 'ingredients': {}
        },
        u'Onsdag': {
            'dish': None, 'ingredients': {}
        },
        u'Torsdag': {
            'dish': None, 'ingredients': {}
        },
        u'Fredag': {
            'dish': None, 'ingredients': {}
        },
        u'Lördag': {
            'dish': None, 'ingredients': {}
        },
        u'Söndag': {
            'dish': None, 'ingredients': {}
        },
    }

    return matlista

def gen_dish(day, name, matlista):
    dish = Recipe.objects.all().filter(name=name).first()

    matlista[day]['dish'] = dish.name
    matlista[day]['ingredients'] = {}

    ingredients = dish.recipeingredient_set.all()

    for ingredient in ingredients:
        matlista[day]['ingredients'].update(
            {ingredient.ingredient_id.name: {
                'quantity': ingredient.quantity,
                'unit': ingredient.unit.unit}
            })

def multiply_portions(day, portion, matlista):

    for ingredient in matlista[day]['ingredients']:
        matlista[day]['ingredients'][ingredient]['quantity'] *= int(portion)

def gen_random_food(day, food_type, matlista, fast):

    # get the food type object from the form response
    dish_type = RecipeType.objects.filter(name=food_type).first()

    # check if the fast food checkbutton has been checked
    # if it has generate a random dish from dishes labeled fast
    if fast == "True":
        random_dish = Recipe.objects.all().filter(food_type=dish_type).filter(fast=True).order_by('?').first()

    else:
        # get a random recipe using food type response
        random_dish = Recipe.objects.all().filter(food_type=dish_type).order_by('?').first()

    # store name of dish in data structure
    matlista[day]['dish'] = random_dish.name

    if matlista[day]['ingredients']:
        matlista[day]['ingredients'] = {}

    ingredients = random_dish.recipeingredient_set.all()

    for ingredient in ingredients:
        matlista[day]['ingredients'].update(
            {ingredient.ingredient_id.name: {
                'quantity': ingredient.quantity,
                'unit': ingredient.unit.unit}
            })

# Create your views here.

def index(request):


    # get all recepie type objects
    recipe_types = RecipeType.objects.all()

    # store recepie type objects in dictionary
    context_dict = { 'recipe_types' : recipe_types }

    return render(request, 'index.html', context=context_dict)

def show_recipes(request, recipe_type_slug):


    # create context dictionary
    context_dict = {}

    try:
        # get the recipes type corresponding to the slug
        recipe_type = RecipeType.objects.filter(slug=recipe_type_slug)

        # get all recipees in this category.
        recipes = recipe_type.first().recipe_set.all()

        # store every recipe in a dictionary
        context_dict['recipes'] = recipes

    except:

        # if nothing found return nothing
        context_dict['recipes'] = None

    return render(request, 'show_recipes.html', context=context_dict)

def fast_recipes(request):


    # create context dictionary
    context_dict = {}

    try:
        # get all recipees in this category.
        recipes = Recipe.objects.all().filter(fast=True)

        # store every recipe in a dictionary
        context_dict['recipes'] = recipes

    except:

        # if nothing found return nothing
        context_dict['recipes'] = None

    return render(request, 'fast_recipes.html', context=context_dict)

def recipe(request, recipe_slug):

    # get the recipe corresponding to the slug
    recipe = Recipe.objects.filter(slug=recipe_slug)

    # check if the recepie exists
    if recipe:

        # get the form
        form = portionsForm()

        # create context dictionary
        context_dict = {}

        # create number of portinos variable
        portions = 1

        # get recepie ingredients
        recipe_ing = recipe.first().recipeingredient_set.all()

        # if there is a HTML POST object
        # check if the form is valid and save the
        # number of portions if it is. Else print errors
        if request.method == 'POST':

            form = portionsForm(request.POST)

            if form.is_valid():

                portions = int(request.POST['status'])

            else:
                print(form.errors)

        # create an empty list
        recipe_ing_list = []

        # go through all ingredient and muliply ingredient quantity
        # with number of portions, then make sting and append to list
        for ingredient in recipe_ing:
            recipe_ing_list.append(unicode(portions * ingredient.quantity) + unicode(' ')
                + unicode(ingredient.unit) + unicode(' ')
                + unicode(ingredient.ingredient_id.name))


        # store form, recipe and ingredient information in context dictionary
        context_dict['form'] = form
        context_dict['recipes'] = recipe
        context_dict['ingredients'] = recipe_ing_list
        context_dict['portions'] = portions

        # if nothing found return nothing
    else:

        context_dict['recipes'] = None
        context_dict['form'] = None
        context_dict['ingredients'] = None

    return render(request, 'recipe.html', context=context_dict)

def generator(request):

    # create variables
    ingredient_list = {}
    context_dict = {}

    # get ll recipe types from database
    recipe_types = RecipeType.objects.all()
    context_dict['recipe_types'] = recipe_types

    # check if any button has been pushed and a POST object has been created
    if request.method == 'POST':

        print request.POST

        # collect all the food types from the select boxes
        responses = {u'Måndag': request.POST['monday'],
                     u'Tisdag': request.POST['tuesday'],
                     u'Onsdag': request.POST['wednesday'],
                     u'Torsdag': request.POST['thursday'],
                     u'Fredag': request.POST['friday'],
                     u'Lördag': request.POST['saturday'],
                     u'Söndag': request.POST['sunday']}

        # collect number of portions from portions select boxes
        portions = {u'Måndag': request.POST['monday_portions'],
                    u'Tisdag': request.POST['tuesday_portions'],
                    u'Onsdag': request.POST['wednesday_portions'],
                    u'Torsdag': request.POST['thursday_portions'],
                    u'Fredag': request.POST['friday_portions'],
                    u'Lördag': request.POST['saturday_portions'],
                    u'Söndag': request.POST['sunday_portions']}

        fast = {u'Måndag': request.POST['monday_fast'],
                u'Tisdag': request.POST['tuesday_fast'],
                u'Onsdag': request.POST['wednesday_fast'],
                u'Torsdag': request.POST['thursday_fast'],
                u'Fredag': request.POST['friday_fast'],
                u'Lördag': request.POST['saturday_fast'],
                u'Söndag': request.POST['sunday_fast']}

        # if generate button is pushed
        if 'generate' in request.POST:

            # create empty data structure for matlista
            matlista = gen_empty_matlista()

            # loop over each day and generate a random food (if not NONE). Then multiply
            # the quantity of each ingredient with the number of portions selected.
            for day in responses:
                if responses[day] != 'None':

                    gen_random_food(day, responses[day], matlista, fast[day])
                    multiply_portions(day, portions[day], matlista)

        # check if button to generate new dish on monday has been pushed
        elif 'random_monday' in request.POST:

            # fetch matlista object from session
            day = u'Måndag'
            matlista = request.session['matlista']

            # generate a random recepie and update matlista.
            if responses[day] != 'None':
                gen_random_food(day,responses[day], matlista, fast[day])
                multiply_portions(day, portions[day], matlista)

        # check if any of the other days buttons has been pushed
        elif 'random_tuesday' in request.POST:

            day = u'Tisdag'
            matlista = request.session['matlista']

            if responses[day] != 'None':
                gen_random_food(day,responses[day], matlista, fast[day])
                multiply_portions(day, portions[day], matlista)

        elif 'random_wednesday' in request.POST:

            day = u'Onsdag'
            matlista = request.session['matlista']

            if responses[day] != 'None':
                gen_random_food(day,responses[day], matlista, fast[day])
                multiply_portions(day, portions[day], matlista)

        elif 'random_thursday' in request.POST:

            day = u'Torsdag'
            matlista = request.session['matlista']

            if responses[day] != 'None':
                gen_random_food(day,responses[day], matlista, fast[day])
                multiply_portions(day, portions[day], matlista)

        elif 'random_friday' in request.POST:

            day = u'Fredag'
            matlista = request.session['matlista']

            if responses[day] != 'None':
                gen_random_food(day,responses[day], matlista, fast[day])
                multiply_portions(day, portions[day], matlista)

        elif 'random_saturday' in request.POST:

            day = u'Lördag'
            matlista = request.session['matlista']

            if responses[day] != 'None':
                gen_random_food(day,responses[day], matlista, fast[day])
                multiply_portions(day, portions[day], matlista)

        elif 'random_sunday' in request.POST:

            day = u'Söndag'
            matlista = request.session['matlista']

            if responses[day] != 'None':
                gen_random_food(day,responses[day], matlista, fast[day])
                multiply_portions(day, portions[day], matlista)

        # check if any manual dish selection has been done for monday
        elif 'select_monday_btn' in request.POST:

            day = u'Måndag'
            # get the name of the recipe selected from session
            name = request.POST['select_monday']
            # get matlsta sesion object
            matlista = request.session['matlista']
            #update matlista with the new dish
            gen_dish(day,name, matlista)
            multiply_portions(day, portions[day], matlista)

        # check if any of the other days buttons has been pushed
        elif 'select_tuesday_btn' in request.POST:

            day = u'Tisdag'
            name = request.POST['select_tuesday']
            matlista = request.session['matlista']
            gen_dish(day,name, matlista)
            multiply_portions(day, portions[day], matlista)

        elif 'select_wednesday_btn' in request.POST:

            day = u'Onsdag'
            name = request.POST['select_wednesday']
            matlista = request.session['matlista']
            gen_dish(day,name, matlista)
            multiply_portions(day, portions[day], matlista)

        elif 'select_thursday_btn' in request.POST:

            day = u'Torsdag'
            name = request.POST['select_thursday']
            matlista = request.session['matlista']
            gen_dish(day,name, matlista)
            multiply_portions(day, portions[day], matlista)

        elif 'select_friday_btn' in request.POST:

            day = u'Fredag'
            name = request.POST['select_friday']
            matlista = request.session['matlista']
            gen_dish(day,name, matlista)
            multiply_portions(day, portions[day], matlista)

        elif 'select_saturday_btn' in request.POST:

            day = u'Lördag'
            name = request.POST['select_saturday']
            matlista = request.session['matlista']
            gen_dish(day,name, matlista)
            multiply_portions(day, portions[day], matlista)

        elif 'select_sunday_btn' in request.POST:

            day = u'Söndag'
            name = request.POST['select_sunday']
            matlista = request.session['matlista']
            gen_dish(day,name, matlista)
            multiply_portions(day, portions[day], matlista)

        # check if the send to trello button has been pushed.
        elif 'trello' in request.POST:

            # get matlista object and ingredient object from session.
            matlista = request.session['matlista']
            ingredients = request.session['ingredient_strings']

            # if there are any ingredients
            if ingredients:

                # get global trello authentication keys
                global API_KEY
                global API_SECRET
                global TOKEN

                # create a trello client object, connect and authenticate
                trello_client = TrelloClient(
                    api_key=API_KEY,
                    api_secret=API_SECRET,
                    token=TOKEN,
                    token_secret='your-oauth-token-secret'
                )

                # get a trello board
                trello_board = trello_client.get_board(u'58bdc41481b0566eb9890b79')
                # get a trello card
                card = trello_board.get_cards()[0]

                #get checklist in that card
                card.checklists
                checklist = card.checklists[0]

                # make checklist object for each ingredient
                for ingredient in ingredients:
                    checklist.add_checklist_item(ingredient)

        # save matlist object in session
        request.session['matlista'] = matlista

        # loop over each day.
        for day in matlista:
            # For all the ingredients that day
            for ingredient in matlista[day]['ingredients']:
                # check if a ingredient is already in the ingredient list
                if ingredient in ingredient_list:
                    # if the ingredient is in the list and has the same unit. add the
                    # quantity to the ingredient in the ingredient list
                    if matlista[day]['ingredients'][ingredient]['unit'] == ingredient_list[ingredient]['unit']:
                        quant_to_add = matlista[day]['ingredients'][ingredient]['quantity']
                        ingredient_list[ingredient]['quantity'] += quant_to_add

                    # if the ingredient is in the list but the ingredient doe not have the same type of
                    # unit, flag it as a unit conflict for user to resolve.
                    else:
                        ingredient_list.update(copy.deepcopy({ingredient + ' - UNIT CONFLICT' : matlista[day]['ingredients'][ingredient]}))

                # if the ingredient is not in the ingredient list add it to the list
                else:
                    ingredient_list.update(copy.deepcopy({ingredient: matlista[day]['ingredients'][ingredient]}))

        # create a list for storing final ingredients as strings
        # ready to be sent to template.
        ingredient_strings = []
        # loop over ingredients in ingredient list and make string in
        # format "ingredient-quantity ingredient-unit ingredient-name"
        # and save to sting list
        for ingredient in ingredient_list:
            name = ingredient
            quantity = ingredient_list[ingredient]['quantity']
            unit = ingredient_list[ingredient]['unit']
            ingredient_strings.append(unicode(quantity) + ' ' + unit + ' ' + name)

        #save ingredient string list to session
        request.session['ingredient_strings'] = ingredient_strings

        # create lists of manal recepie selction
        dish_type = RecipeType.objects.filter(name=responses[u'Måndag']).first()
        monday_recipes = Recipe.objects.all().filter(food_type=dish_type)
        dish_type = RecipeType.objects.filter(name=responses[u'Tisdag']).first()
        tuesday_recipes = Recipe.objects.all().filter(food_type=dish_type)
        dish_type = RecipeType.objects.filter(name=responses[u'Onsdag']).first()
        wednesday_recipes = Recipe.objects.all().filter(food_type=dish_type)
        dish_type = RecipeType.objects.filter(name=responses[u'Torsdag']).first()
        thursday_recipes = Recipe.objects.all().filter(food_type=dish_type)
        dish_type = RecipeType.objects.filter(name=responses[u'Fredag']).first()
        friday_recipes = Recipe.objects.all().filter(food_type=dish_type)
        dish_type = RecipeType.objects.filter(name=responses[u'Lördag']).first()
        saturday_recipes = Recipe.objects.all().filter(food_type=dish_type)
        dish_type = RecipeType.objects.filter(name=responses[u'Söndag']).first()
        sunday_recipes = Recipe.objects.all().filter(food_type=dish_type)

        # store in context dic and send to template
        context_dict['monday_recipes'] = monday_recipes
        context_dict['tuesday_recipes'] = tuesday_recipes
        context_dict['wednesday_recipes'] = wednesday_recipes
        context_dict['thursday_recipes'] = thursday_recipes
        context_dict['friday_recipes'] = friday_recipes
        context_dict['saturday_recipes'] = saturday_recipes
        context_dict['sunday_recipes'] = sunday_recipes
        context_dict['matlista'] = matlista
        context_dict['ingredient_strings'] = ingredient_strings

    # if no POST data create an empty data structure and save it in session
    else:

        matlista = gen_empty_matlista()
        request.session['matlista'] = matlista


    return render(request, 'generator.html', context=context_dict)