from django import forms
from database.models import *

DATE_INPUT_FORMATS = ['%Y-%m-%d']
class DateInput(forms.DateInput):
    input_type = 'date'
    input_formats = DATE_INPUT_FORMATS


class SearchDate(forms.Form):
    date = forms.DateField(widget=DateInput())

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = []

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['road', 'town', 'number', 'codePostal', 'country']

class CampForm(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ['name','section','deadline', 'from_date','to_date','type']
        widgets = {
            'deadline': DateInput(),
            'from_date': DateInput(),
            'to_date': DateInput(),
        }

class CreateUser(forms.Form):
    email = forms.EmailField()
    section = forms.ModelChoiceField(queryset=Section.objects.all())

class MenuForm(forms.ModelForm):
    recipe = forms.ChoiceField(choices=[], label="Recipe")

    class Meta:
        model = Menu
        fields = ['date', 'moment','nbr_anim', 'nbr_vege', 'nbr_leaders']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['recipe'].choices = self.get_recipe_choices()
        self.fields['nbr_anim'].widget.attrs.update({'min': '0'})

    def get_recipe_choices(self):
        recipes = get_recipes_from_api()
        choices = [(recipe['id'], recipe['name']) for recipe in recipes]
        return choices
        #return []
    def save(self, commit=True):
        menu = super().save(commit=False)
        recipe_id = self.cleaned_data['recipe']
        values = get_recipe_id_from_api(recipe_id)
        menu.recipe = values['menu']
        menu.recipe_name = values['recipe_name']
        if commit:
            menu.save()
        return menu

"""class MenuFormNoDate(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nbr_anim','nbr_leaders','nbr_vege','moment','recipe']"""

# forms.py
from django import forms
from .utils import *

class MenuFormNoDate(forms.ModelForm):
    recipe = forms.ChoiceField(choices=[], label="Recipe")

    class Meta:
        model = Menu
        fields = ['nbr_anim', 'nbr_leaders', 'nbr_vege', 'moment']

    def __init__(self, *args, **kwargs):
        super(MenuFormNoDate, self).__init__(*args, **kwargs)
        self.fields['recipe'].choices = self.get_recipe_choices(self)

    def get_recipe_choices(self):
        recipes = get_recipes_from_api()
        choices = [(recipe['id'], recipe['name']) for recipe in recipes]
        return choices
    
    def save(self, commit=True):
        menu = super().save(commit=False)
        recipe_id = self.cleaned_data['recipe']
        menu.recipe = get_recipe_id_from_api(recipe_id)
        if commit:
            menu.save()
        return menu
    
class MenuFormNoDate(forms.ModelForm):
    ingredient = forms.ChoiceField(choices=[], label="Ingredient")

    class Meta:
        model = Stock
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super(MenuFormNoDate, self).__init__(*args, **kwargs)
        self.fields['ingredient'].choices = self.get_ingredient_choices(self)

    def get_ingredient_choices(self):
        ingredients = get_ingredients_from_api()
        choices = [(ingredient['name']) for ingredient in ingredients]
        return choices
    
    def save(self, commit=True):
        stock = super().save(commit=False)
        ingredient = self.cleaned_data['ingredient']
        print(ingredient)
        stock.ingredient = ingredient
        stock.mesurement = get_mesurement_from_ingredient(ingredient)
        if commit:
            stock.save()
        return stock


class CampFormUpdate(forms.ModelForm):
    class Meta:
        model = Camp
        fields = ['from_date','to_date']
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput(),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if from_date and to_date:
            if from_date >= to_date:
                raise forms.ValidationError("The 'from_date' must be before the 'to_date'.")

        return cleaned_data

class CreateCamps(forms.Form):
    section = forms.ModelMultipleChoiceField(
        queryset=Section.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    name = forms.CharField(label="Nom du Camp",max_length=50)
    deadline = forms.DateField(widget=DateInput(), input_formats=DATE_INPUT_FORMATS)
    type = forms.ChoiceField(choices=TypeCamp.choices,required=True)


class ProducteurModelForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Producteur
        fields = ['name','category']