from database.models import *
from django.db.models import F

def getCamps():
    return Camp.objects.all().filter(status = Status.F)
def displayCamps():
    return Camp.objects.all().filter(status__in=[Status.F,Status.C,Status.N])

def HideCamps():
    Camp.objects.filter(status=Status.F).update(status = Status.H)

def getCampsSection(section_name):
    return Camp.objects.filter(section__name = section_name)

def getRecipes():
    return Recipe.objects.select_related('tags').order_by('name')

def getIngredients():
    return Ingredient.objects.all()

def getMenu(date, moment, camp):
    return Menu.objects.filter(date=date, moment=moment, camp=camp).values('id', 'camp_id', 'nbr_anim', 'nbr_leaders', 'nbr_vege', 'date', 'moment', 'recipe').first()

def getMenuId(date, moment, camp):
    return Menu.objects.filter(date=date, moment=moment, camp=camp).values('id').first()

def getMenuCamp(camp):
    return Menu.objects.filter(camp=camp).order_by('date')

def getEngredientsFromRecipe(recipe):
    return Recipe.objects.prefetch_related('ingredients').all().filter(pk=recipe)

def getIngredient(engredient):
    return Ingredient.objects.filter(pk=engredient).first()

def isvege(engredient):
    return Ingredient.objects.all().filter(pk=engredient)

def getRecipesMoment(tag):
    return Recipe.objects.filter(tags__name = tag)

def getIngredientsSu():
    return IngredientXSU.objects.all()

def getIngredientByName(name):
    return Ingredient.objects.filter(name=name)


def IngredientsSU(request):
    return IngredientXSU.objects.all()

def getProducteurs(request):
    return Producteur.objects.all()
