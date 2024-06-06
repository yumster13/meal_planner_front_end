from django.contrib import admin
from django.urls import path
from .views import *
from .create_csv import calculate_quantities,generate_ingredient_list
from .addIngredientSu import generate_ingredient_su
urlpatterns = [
    path('admin/home',home,name="home"),
    path('camp/create',CreateCamp,name="createCamp"),
    path('camp/addInfo/<str:camp>/',AddInfoCamp,name="addInfo"),
    path('camps',Camps,name="camps"),
    path('producteurs',DisplayProducteur,name="producteurs"),
    path('producteurs/new',AddProducteur,name="addProducteur"),
    path('camps/menus/<str:camp>',DisplayMenuCamp,name="menus"),
    path('camps/addMenu/<str:camp>',addMenuToCamp,name="addMenu"),
    path('camps/saveMenu/<str:camp>',addMenuToCamp,name="addMenu"),
    path('camps/delete/menu/<str:camp>/<str:menu>/',DeleteMenuCamp,name="deleteMenu"),
    path('camps/setFinished/<str:camp>',FinishCamp,name="setFinished"),
    path('camps/resetStatus/<str:camp>',ResetCampStatus,name="resetStatus"),
    path('recipes',Recipes,name="recipes"),
    path('engredients',Engredients,name="engredients"),
    path('recipe/create',CreateRecipe,name="createRecipe"),
    path('user/create',CreateUserView,name="createUser"),
    path('camps/calculate_quantities',calculate_quantities,name="calculate_quantities"),
    path('camps/generate_ingredient_list',generate_ingredient_list,name="generate_ingredient_list"),
    path('camps/generate_ingredient_su',generate_ingredient_su,name="generate_ingredient_su"),
    path('camps/hideAll',HideCamps,name="hideAll"),

    path('ingredientList/',getIngredientsSu,name="ingredientsSu"),
    path('ingredientList/toggleSu/<str:ingredient>/',toggleSu,name="toggleSu"),

]
