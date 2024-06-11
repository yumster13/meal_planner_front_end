from collections import defaultdict
from django.db import transaction
from . import databse_access
from database.models import *
from django.http import HttpResponse

from collections import defaultdict
from django.db import transaction
from . import databse_access
from database.models import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,redirect
from .utils import *
def generate_ingredient_su(request):
    IngredientXSU.objects.all().delete()
    camps = databse_access.getCamps()

    # Global dictionary to track ingredient quantities across all camps
    global_ingredient_dict = defaultdict(lambda: {'quantity': 0, 'measurement': '', 'categories': ''})

    for camp in camps:
        name = camp.section.name
        age = camp.section.age
        menus = databse_access.getMenuCamp(camp)
        
        for menu in menus:
            engredients = get_recipe_id_ingredients(menu.recipe)
            recipe_id = menu.recipe
            for key,engredient in engredients.items():
                quantity_anim = 0
                quantity_lead = 0
                quantity_vege = 0
                ingVege = is_recipe_vege(recipe_id,engredient[0])

                quantity = recipe_quant(recipe_id,age,engredient[0])

                if str(ingVege['vege']) == 'True':

                    quantity_vege = float(quantity['leaders']) * menu.nbr_vege
                else:

                    quantity_anim = float(quantity['anim']) * menu.nbr_anim
                    quantity_lead = float(quantity['leaders']) * menu.nbr_leaders

                categories = str(engredient[2])

                total_quantity = quantity_lead + quantity_anim + quantity_vege

                key = engredient[1]
                
                if key in global_ingredient_dict:
                    global_ingredient_dict[key]['quantity'] += total_quantity
                else:
                    global_ingredient_dict[key] = {
                        'quantity': total_quantity,
                        'mesurement': engredient[3],
                        'categories': categories,
                    }
    from django.shortcuts import get_object_or_404

    for ingredient_name, info in global_ingredient_dict.items():
        print(ingredient_name,"   :",info)
        
        ingredient_xsu,created = IngredientXSU.objects.get_or_create(
            ingredient=ingredient_name
        )
        ingredient_xsu.su = False
        ingredient_xsu.quantity += info['quantity']
        ingredient_xsu.category = info['categories']
        match str(info['mesurement']):
                case 'L':ingredient_xsu.mesurement = Mesurements.L
                case 'KG':ingredient_xsu.mesurement = Mesurements.KG
                case 'PIECE':ingredient_xsu.mesurement = Mesurements.PIECE
                case 'TRANCHE':ingredient_xsu.mesurement = Mesurements.TRANCHE
                case 'CONDIMENT':ingredient_xsu.mesurement = Mesurements.CONDIMENT
        ingredient_xsu.save()

    return redirect('home')

