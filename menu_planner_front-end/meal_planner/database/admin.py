from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    pass
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass
@admin.register(RecipeXEngredient)
class RecipeXEngridientAdmin(admin.ModelAdmin):
    pass
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass