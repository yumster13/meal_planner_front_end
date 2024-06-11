from django.conf import settings
import requests
session = requests.Session()
session.verify = settings.VERIFY
from django.conf import settings

def get_recipes_from_api():
    data = {}
    headers = {
        'Referer': f'{settings.API_URL}/api/recipesName',
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
    }
    response = session.get(f'{settings.API_URL}/api/recipesName/', data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_ingredients_from_api():
    data = {}
    headers = {
        'Referer': f'{settings.API_URL}/api/ingredients',
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
    }
    response = session.get(f'{settings.API_URL}/api/ingredients/', data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_ingredients_search(name):
    data = {
        'ingredient': name,
    }
    headers = {
        'Referer': f'{settings.API_URL}/api/ingredientsSearch',
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
    }
    response = session.get(f'{settings.API_URL}/api/ingredientsSearch/', data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_recipes_search(name):
    data = {
        'recipe': name,
    }
    headers = {
        'Referer': f'{settings.API_URL}/api/recipesSearch',
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
    }
    response = session.get(f'{settings.API_URL}/api/recipesSearch/', data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_recipe_id_from_api(recipe_id):
    data = {
        'recipe_id': recipe_id
    }
    headers = {
        'Referer': f'{settings.API_URL}/api/recipe',
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
    }
    response = session.get(f'{settings.API_URL}/api/recipe/', data=data, headers=headers)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_mesurement_from_ingredient(ingredient_name):
    data = {
        'ingredient_name': ingredient_name
    }
    headers = {
        'Referer': f'{settings.API_URL}/api/ingredientsMesure',
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
    }
    response = session.get(f'{settings.API_URL}/api/ingredientsMesure/', data=data, headers=headers)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_recipe_id_ingredients(recipe_id):
    data = {
        'recipe_id': recipe_id
    }
    headers = {
        'Referer': f'{settings.API_URL}/api/ingredientsList',
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
    }
    response = session.get(f'{settings.API_URL}/api/ingredientsList/', data=data, headers=headers)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return []

def is_recipe_vege(recipe_id,ingredient_id):
    data = {
        'recipe_id': recipe_id,
        'ingredient_id': ingredient_id
    }
    headers = {
        'Referer': f'{settings.API_URL}/api/ingredientsVege',
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
    }
    response = session.get(f'{settings.API_URL}/api/ingredientsVege/', data=data, headers=headers)
    #print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return []

def recipe_quant(recipe_id,age,ingredient_id):
    data = {
        'recipe_id': recipe_id,
        'ingredient_id': ingredient_id,
        'age': age,
    }
    headers = {
        'Referer': f'{settings.API_URL}/api/ingredientsQuant',
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
    }
    response = session.get(f'{settings.API_URL}/api/ingredientsQuant/', data=data, headers=headers)
    #print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_categories():
    data = {}
    headers = {
        'Referer': f'{settings.API_URL}/api/categoriesList',
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}"
    }
    response = session.get(f'{settings.API_URL}/api/categoriesList/', data=data, headers=headers)
    #print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return []

