from . import databse_access

import pandas as pd
from django.http import HttpResponse
import os
import zipfile
from io import BytesIO
from database.models import *
from .utils import *
from database.models import *
class Ages(models.TextChoices):
    DEFAULT = '18+',
    PF = 'Petit F', 
    PG = 'Petit G', 
    GF = 'Grand F', 
    GG = 'Grand G',

def calculate_quantities(request):
    camps = databse_access.getCamps()
    temp_dir = 'temp_files'

    excel_files = []
    print(camps)
    for camp in camps:
        engredient_dict = []
        name = camp.section.name
        age = camp.section.age
        menus = databse_access.getMenuCamp(camp)
        for menu in menus:
            #print('recipe', menu.recipe.id)
            engredients = get_recipe_id_ingredients(menu.recipe)
            recipe_id = menu.recipe

            # Filter RecipeXEngredient related to the specific recipe and age
            """filtered_ingredient_ids = RecipeXEngredient.objects.filter(
                recipe__id=recipe_id,
                age=Ages.GG
            ).values_list('ingredient_id', flat=True).distinct()
            print(filtered_ingredient_ids)"""
            #print(engredients)
            for key,engredient in engredients.items():
                #print('engredient',key,engredient)
                quantity_anim = 0
                quantity_lead = 0
                quantity_vege = 0
                ingVege = is_recipe_vege(recipe_id,engredient[0])
                #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = engredient['ingredients__ingredient__id']).values('vege').distinct()
                if not IngredientXSU.objects.filter(ingredient = engredient[1],su = 1):
                    #print(ingVege)
                    quantity = recipe_quant(recipe_id,age,engredient[0])
                    #print(quantity)
                    if str(ingVege['vege']) == 'True':
                        #quantity_leaders = recipe_quant(recipe_id,Ages.GG,engredient['ingredients__ingredient__id'])
                        #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = engredient['ingredients__ingredient__id']).values('quantity').distinct()
                        #print(quantity['leaders'], menu.nbr_vege)
                        quantity_vege = float(quantity['leaders']) * menu.nbr_vege
                    else:
                        #quantity_anim = quantity_leaders = recipe_quant(recipe_id,age,engredient['ingredients__ingredient__id'])
                        #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=age,ingredient__id = engredient['ingredients__ingredient__id']).values('quantity').distinct()
                        #quantity_leaders = quantity_leaders = recipe_quant(recipe_id,Ages.GG,engredient['ingredients__ingredient__id'])
                        #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = engredient['ingredients__ingredient__id']).values('quantity').distinct()
                        quantity_anim = float(quantity['anim']) * menu.nbr_anim
                        quantity_lead = float(quantity['leaders']) * menu.nbr_leaders
                    #print(quantity_anim,"||",quantity_lead,"||",quantity_vege)
                    categories = str(engredient[2])
                    engredient_dict.append([menu.date, menu.recipe_name, str(engredient[1]), (quantity_lead + quantity_anim + quantity_vege),str(engredient[3]), categories])
                """print("id: ->",engredient.ingredient.id)
                engredient_info = databse_access.getIngredient(engredient.ingredient.id)
                quantity_anim = 0
                quantity_lead = 0
                quantity_vege = 0
                categories = ""
                print(engredient_info)
                if engredient_info:
                    if engredient_info.vege:
                        if engredient.age == 'Grand G':
                            quantity_vege = engredient.quantity * menu.nbr_vege 
                    if engredient.age == age:
                        print('engredient\n', engredient.quantity)
                        quantity_anim = engredient.quantity * menu.nbr_anim

                    if engredient.age == 'Grand G':
                        quantity_lead = engredient.quantity * menu.nbr_leaders
                    else:
                        quantity_lead = 0
                        quantity_vege = 0
                    print(recipe)
                    categories = str(engredient_info.category.name)
                engredient_dict.append([menu.date, recipe[0].name, engredient_info.name, (quantity_lead + quantity_anim + quantity_vege), categories])"""
        #print('menu\n', menus)
        #print(engredient_dict)

        # Write to Excel file
        df = pd.DataFrame(engredient_dict, columns=['Date', 'Recipe Name', 'Ingredient Name', 'Total Quantity', 'Mesurement', 'Categories'])
        excel_file_path = os.path.join(temp_dir, f'ingredients_{camp.name}.xlsx')
        df.to_excel(excel_file_path, index=False,engine='xlsxwriter',engine_kwargs={'options': {'strings_to_numbers': True}})
        excel_files.append(excel_file_path)

    # Create a zip file containing all the Excel files
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file_path in excel_files:
            zip_file.write(file_path, os.path.basename(file_path))

    # Serve the zip file as a download
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="ingredients.zip"'

    return response


import os
import pandas as pd
import zipfile
from io import BytesIO
from django.http import HttpResponse
from collections import defaultdict

def generate_ingredient_list(request):
    camps = databse_access.getCamps()
    temp_dir = 'temp_files'

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Global dictionary to track ingredient quantities across all camps
    global_ingredient_dict = defaultdict(lambda: {'quantity': 0, 'measurement': '', 'categories': ''})

    for camp in camps:
        name = camp.section.name
        age = camp.section.age
        menus = databse_access.getMenuCamp(camp)
        
        for menu in menus:
            engredients = get_recipe_id_ingredients(menu.recipe)
            recipe_id = menu.recipe

            # Filter RecipeXEngredient related to the specific recipe and age
            """filtered_ingredient_ids = RecipeXEngredient.objects.filter(
                recipe__id=recipe_id,
                age=Ages.GG
            ).values_list('ingredient_id', flat=True).distinct()
            print(filtered_ingredient_ids)"""
            #print(engredients)
            for key,engredient in engredients.items():
                #print('engredient',key,engredient)
                quantity_anim = 0
                quantity_lead = 0
                quantity_vege = 0
                ingVege = is_recipe_vege(recipe_id,engredient[0])
                #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = engredient['ingredients__ingredient__id']).values('vege').distinct()
                
                #print(ingVege)
                quantity = recipe_quant(recipe_id,age,engredient[0])
                #print(quantity)
                if str(ingVege['vege']) == 'True':
                    #quantity_leaders = recipe_quant(recipe_id,Ages.GG,engredient['ingredients__ingredient__id'])
                    #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = engredient['ingredients__ingredient__id']).values('quantity').distinct()
                    #print(quantity['leaders'], menu.nbr_vege)
                    quantity_vege = float(quantity['leaders']) * menu.nbr_vege
                else:
                    #quantity_anim = quantity_leaders = recipe_quant(recipe_id,age,engredient['ingredients__ingredient__id'])
                    #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=age,ingredient__id = engredient['ingredients__ingredient__id']).values('quantity').distinct()
                    #quantity_leaders = quantity_leaders = recipe_quant(recipe_id,Ages.GG,engredient['ingredients__ingredient__id'])
                    #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = engredient['ingredients__ingredient__id']).values('quantity').distinct()
                    quantity_anim = float(quantity['anim']) * menu.nbr_anim
                    quantity_lead = float(quantity['leaders']) * menu.nbr_leaders
                #print(quantity_anim,"||",quantity_lead,"||",quantity_vege)
                categories = str(engredient[2])

                total_quantity = quantity_lead + quantity_anim + quantity_vege

                key = engredient[1]
                
                if key in global_ingredient_dict:
                    global_ingredient_dict[key]['quantity'] += total_quantity
                else:
                    global_ingredient_dict[key] = {
                        'quantity': total_quantity,
                        'measurement': engredient[3],
                        'categories': categories,
                    }

    # Prepare the list for DataFrame
    global_ingredient_list = [
        [ingredient_name, info['quantity'], info['measurement'], info['categories']]
        for ingredient_name, info in global_ingredient_dict.items()
    ]

    # Write to Excel file
    df = pd.DataFrame(global_ingredient_list, columns=['Ingredient Name', 'Total Quantity', 'Measurement', 'Categories'])
    excel_file_path = os.path.join(temp_dir, 'total_ingredients.xlsx')
    df.to_excel(excel_file_path, index=False,engine='xlsxwriter',engine_kwargs={'options': {'strings_to_numbers': True}})

    # Create a zip file containing the Excel file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.write(excel_file_path, os.path.basename(excel_file_path))

    # Serve the zip file as a download
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="ingredients.zip"'

    # Clean up temporary files

    return response


def generateCsvMeal(request):
    camps = databse_access.getCamps()
    temp_dir = 'temp_files'

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    excel_files = []
    engredient_list_notneeded = []
    engredients = databse_access.IngredientsSU()
    for engredient in engredients:
        engredient_list_notneeded.append(engredient.name)
    for camp in camps:
        engredient_dict = []
        name = camp.section.name
        age = camp.section.age
        menus = databse_access.getMenuCamp(camp)
        for menu in menus:
            #print('recipe', menu.recipe.id)
            engredients = get_recipe_id_ingredients(menu.recipe)
            recipe_id = menu.recipe

            # Filter RecipeXEngredient related to the specific recipe and age
            """filtered_ingredient_ids = RecipeXEngredient.objects.filter(
                recipe__id=recipe_id,
                age=Ages.GG
            ).values_list('ingredient_id', flat=True).distinct()
            print(filtered_ingredient_ids)"""
            #print(engredients)
            for key,engredient in engredients.items():
                #print('engredient',key,engredient)
                quantity_anim = 0
                quantity_lead = 0
                quantity_vege = 0
                ingVege = is_recipe_vege(recipe_id,engredient[0])
                #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = engredient['ingredients__ingredient__id']).values('vege').distinct()
                if IngredientXSU.objects.filter(ingredient = engredient[1]) is None:
                    #print(ingVege)
                    quantity = recipe_quant(recipe_id,age,engredient[0])
                    #print(quantity)
                    if str(ingVege['vege']) == 'True':
                        #quantity_leaders = recipe_quant(recipe_id,Ages.GG,engredient['ingredients__ingredient__id'])
                        #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = engredient['ingredients__ingredient__id']).values('quantity').distinct()
                        #print(quantity['leaders'], menu.nbr_vege)
                        quantity_vege = float(quantity['leaders']) * menu.nbr_vege
                    else:
                        #quantity_anim = quantity_leaders = recipe_quant(recipe_id,age,engredient['ingredients__ingredient__id'])
                        #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=age,ingredient__id = engredient['ingredients__ingredient__id']).values('quantity').distinct()
                        #quantity_leaders = quantity_leaders = recipe_quant(recipe_id,Ages.GG,engredient['ingredients__ingredient__id'])
                        #RecipeXEngredient.objects.filter(recipe__id=recipe_id,age=Ages.GG,ingredient__id = engredient['ingredients__ingredient__id']).values('quantity').distinct()
                        quantity_anim = float(quantity['anim']) * menu.nbr_anim
                        quantity_lead = float(quantity['leaders']) * menu.nbr_leaders
                    #print(quantity_anim,"||",quantity_lead,"||",quantity_vege)
                    categories = str(engredient[2])
                    engredient_dict.append([menu.date, menu.recipe_name, str(engredient[1]), (quantity_lead + quantity_anim + quantity_vege),str(engredient[3]), categories])
                """print("id: ->",engredient.ingredient.id)
                engredient_info = databse_access.getIngredient(engredient.ingredient.id)
                quantity_anim = 0
                quantity_lead = 0
                quantity_vege = 0
                categories = ""
                print(engredient_info)
                if engredient_info:
                    if engredient_info.vege:
                        if engredient.age == 'Grand G':
                            quantity_vege = engredient.quantity * menu.nbr_vege 
                    if engredient.age == age:
                        print('engredient\n', engredient.quantity)
                        quantity_anim = engredient.quantity * menu.nbr_anim

                    if engredient.age == 'Grand G':
                        quantity_lead = engredient.quantity * menu.nbr_leaders
                    else:
                        quantity_lead = 0
                        quantity_vege = 0
                    print(recipe)
                    categories = str(engredient_info.category.name)
                engredient_dict.append([menu.date, recipe[0].name, engredient_info.name, (quantity_lead + quantity_anim + quantity_vege), categories])"""
        #print('menu\n', menus)
        #print(engredient_dict)

        # Write to Excel file
        df = pd.DataFrame(engredient_dict, columns=['Date', 'Recipe Name', 'Ingredient Name', 'Total Quantity', 'Mesurement', 'Categories'])
        excel_file_path = os.path.join(temp_dir, f'ingredients_{camp.name}.xlsx')
        df.to_excel(excel_file_path, index=False,engine='xlsxwriter',engine_kwargs={'options': {'strings_to_numbers': True}})
        excel_files.append(excel_file_path)

    # Create a zip file containing all the Excel files
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file_path in excel_files:
            zip_file.write(file_path, os.path.basename(file_path))

    # Serve the zip file as a download
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="ingredients.zip"'

    return response

