from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator 

class Ages(models.TextChoices):
    DEFAULT = '18+',
    PF = 'Petit F', 
    PG = 'Petit G', 
    GF = 'Grand F', 
    GG = 'Grand G',

class Status(models.TextChoices):
    C = 'En Cours',
    F = 'Fini',
    N = 'Pas commencé',
    H = 'Hidden',

class Mesurements(models.TextChoices):
    KG = 'KG',
    L = 'L', 
    PIECE = 'PIECE', 
    TRANCHE = 'TRANCHE', 
    CONDIMENT = 'CONDIMENT', 

class Moment(models.TextChoices):
    MATIN = "MATIN",
    MIDI = "MIDI",
    GOUTER = "GOUTER",
    SOUPER = "SOUPER",
    CINQIEME = "5EME",

class TypeCamp(models.TextChoices):
    MENU = "Menu",
    CAMP = "Camp",

"""class Season(models.TextChoices):
    HIVER = "Hiver",
    PRINTEMPS = "Printemps",
    ETE = "Eté",
    AUTOMNE = "Automne",
    ALL = "Toute l'année","""

class Season(models.Model):
    name = models.CharField("Name", null=False,unique=True,max_length=10)

class Section(models.Model):
    name = models.CharField("Nom", null=False,blank=False, max_length=30)
    age = models.CharField("Tranche d'âge", choices=Ages.choices, default=Ages.DEFAULT,max_length=10)

    def __str__(self) -> str:
        return self.name

class Address(models.Model):
    road = models.CharField("Rue", null=False,blank=False, max_length=30)
    town = models.CharField("Ville", null=False,blank=False, max_length=30)
    number = models.CharField("Numéro", null=False,blank=False, max_length=5)
    codePostal = models.CharField("CodePostal", null=False,blank=False, max_length=4)
    country = models.CharField("Pays", null=False,blank=False, max_length=15)

class Camp(models.Model):
    name = models.CharField("Nom", null=False,blank=False, max_length=30)
    location = models.ForeignKey(Address, on_delete=models.RESTRICT,null=True)
    from_date = models.DateField("De", null=True,blank=True)
    to_date = models.DateField("A", null=True,blank=True)
    deadline = models.DateField("Deadline", null=False,blank=False,default='2024-01-01')
    section = models.ForeignKey(Section, on_delete=models.RESTRICT,null=False)
    status= models.CharField("Status", choices=Status.choices, default=Status.C,max_length=20, null=False)
    type = models.CharField("Type",choices=TypeCamp.choices, default=TypeCamp.CAMP,max_length=10, null=False)

class Category(models.Model):
    name = models.CharField("Nom", null=False,blank=False, max_length=30)
    parent_category = models.ForeignKey("self", on_delete=models.RESTRICT,null=True)

    def __str__(self):
        return str(self.name)
    
class Ingredient(models.Model):
    name = models.CharField("Nom", null=False,blank=False, max_length=30)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT,null=True)
    season = models.ManyToManyField(Season)
    mesurement = models.CharField("Mesure", choices=Mesurements.choices, default=Mesurements.KG,max_length=10)
    avg_price = models.DecimalField("Prix moyen",max_digits=5, decimal_places=2,null=True)

    def __str__(self):
        return self.name

class RecipeXEngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.RESTRICT, null=False)
    quantity = models.DecimalField("Quantité",max_digits=15, decimal_places=5)
    age = models.CharField("Tranche d'âge", choices=Ages.choices, default=Ages.DEFAULT,max_length=10)
    vege = models.BooleanField("Vege ?", null=False,blank=False,default=False)
    def __str__(self):
        return str(self.ingredient)+' '+str(self.age)

class Stock(models.Model):
    ingredient = models.CharField("ingredient_name",max_length=150,default='')
    quantity = models.DecimalField("Quantité",max_digits=10, decimal_places=2)
    mesurement = models.CharField("Mesure", choices=Mesurements.choices, default=Mesurements.KG,max_length=10)

class Tag(models.Model):
    name = models.CharField("Nom", null=False,blank=False, max_length=30)
    parent_tag = models.ForeignKey("self", on_delete=models.RESTRICT,null=True,blank=True)

    def __str__(self):
        return str(self.name)

class Recipe(models.Model):
    name = models.TextField("Nom", null=False,blank=False)
    prairie = models.BooleanField("En prairie ?", null=False,blank=False,default=False)
    tags = models.ForeignKey(Tag, on_delete=models.RESTRICT,null=True,blank=True)
    ingredients = models.ManyToManyField(RecipeXEngredient)

    def calculate_total_price(self, age_group):
        total = 0
        for recipe_x_ingredient in self.ingredients.filter(age=age_group):
            ingredient = recipe_x_ingredient.ingredient
            quantity = recipe_x_ingredient.quantity
            total += ingredient.avg_price * quantity
        return total
    
    def __str__(self) -> str:
        return self.name
    

class Menu(models.Model):
    camp = models.ForeignKey(Camp,on_delete=models.RESTRICT, null=False)
    nbr_anim = models.IntegerField("nombre d'animés", null=False,blank=False,validators=[MinValueValidator(0), MaxValueValidator(100)])
    nbr_leaders = models.IntegerField("nombre d'animateurs", null=False,blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    nbr_vege = models.IntegerField("nombre de vege", null=False,blank=False, validators=[MinValueValidator(0), MaxValueValidator(100)])
    date = models.DateField("Jour",null=False, blank=False)
    moment= models.CharField("Moment", choices=Moment.choices, default=Moment.MATIN,max_length=10)
    recipe = models.IntegerField("recipe", null=False,blank=False,validators=[MinValueValidator(0), MaxValueValidator(100)])
    recipe_name = models.CharField("recipe_name",max_length=300,default='')



class IngredientXSU(models.Model):
    ingredient = models.CharField("ingredient_name",max_length=300,default='')
    quantity = models.DecimalField("Quantité",max_digits=20, decimal_places=5,default=0)
    su = models.BooleanField("SU ?", null=False,blank=False,default=False)
    category = models.CharField("category_name",max_length=300,default='')
    mesurement = models.CharField("Mesure", choices=Mesurements.choices, default=Mesurements.KG,max_length=10)

class Producteur(models.Model):
    name = models.CharField("Nom", null=False,blank=False,max_length=100)
    location = models.ForeignKey(Address, on_delete=models.RESTRICT,null=True)
    category = models.ManyToManyField(Category)
