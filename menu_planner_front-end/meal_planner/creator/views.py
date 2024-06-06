from django.shortcuts import render, redirect
from database.models import *
from .forms import *
# Create your views here.
from django.contrib import messages
from . import databse_access
from django.conf import settings
from django.core.mail import send_mail
from .generate_password import generate_password
from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse,HttpResponseForbidden
from .utils import *
import requests
session = requests.Session()
session.verify = settings.VERIFY


def staff_member_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Access session variables
        my_variable = request.session.get('group')

        # Do something with the session variable
        if my_variable == 'staff':
            return  view_func(request, *args, **kwargs)
        else:
            # Perform another action
            return redirect('/camps/')

        # Call the actual view function
        return view_func(request, *args, **kwargs)

    return _wrapped_view


@staff_member_required
def home(request):

    context = {'home':True, 'user_form':CreateUser}
    return render(request,"home.html",context)

def AddInfoCamp(request, camp):
    instance = get_object_or_404(Camp, pk=camp)
    if request.method == 'POST':
        camp_form = CampFormUpdate(request.POST, instance=instance)
        address_form = AddressForm(request.POST)

        if camp_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            camp = camp_form.save(commit=False)
            camp.location = address
            camp.save()
            Camp.objects.filter(pk=camp.pk).update(status=Status.C)
            messages.success(request, "Données mises à jour")
            return redirect('camps')
        else:
            messages.error(request, "Données mal insérées")

def CreateCamp(request):
    print("passed")
    if request.method == 'POST':
        print("passed")
        camp_form = CreateCamps(request.POST)
        if camp_form.is_valid():
            print("passed")
            section_ids = camp_form.cleaned_data['section']
            recipient_list = []
            for section_id in section_ids:
                print("section",section_id)
                camp = Camp.objects.create(name=str(camp_form.data["name"]+" "+section_id.name),deadline = camp_form.data["deadline"],section = section_id,status = Status.N,type = camp_form.data["type"])
                users = User.objects.filter(groups__name = section_id.name)
                for user in users:
                    recipient_list.append(user.email)
                camp.save()
            subject = 'Camp ajouté'
            message = f'Bonjour, votre camp a été créé. Consultez-le sur le site suivant: https://menuplanner.pythonanywhere.com/. Il faut compléter le menu pour le {camp_form.data['deadline']}'
            email_from = settings.EMAIL_HOST_USER
            send_mail( subject, message, email_from, recipient_list )
            #camp_form.save()
            messages.success(request, "Camp Created")
            return redirect('camps')
        else:
            messages.error(request, "Camp error")
            return render(request, "camp.html", {'camp_form': camp_form})
    else:
        camp_form = CreateCamps()
        return render(request, "camp.html", {'camp_form': camp_form, 'camp': True})

def Camps(request):
    if request.session['group'] == 'staff' :
        camps = databse_access.displayCamps()
    else:
        camps=databse_access.getCampsSection(request.session['group'])
    camp_form = CreateCamps()
    context = {'camps':camps,'camp':True, 'camp_form': camp_form, 'infoCamp':CampFormUpdate(), 'locationCamp':AddressForm()}
    return render(request,'camps.html',context)

def Recipes(request):
    data = {}
    headers = {
        'Referer': f'{settings.API_URL}/api/recipes',
        "Authorization": f"Bearer {request.session['access_token']}"
    }
    response = session.get(f'{settings.API_URL}/api/recipes/', data=data, headers=headers)
    print(response.json())
    if response.status_code == 200:
        recipes = response.json()
        recipe_dict = {}
        for recipe in recipes:
            recipe_dict[recipe['name']] = {
                'prairie': recipe['prairie'],
                'tags': recipe['tags']['name'],
                'avg_price': 0  # You can update this with actual logic if needed
            }
    # print(recipe_dict)
        context = {'recipes':recipe_dict,'recipe':True}
        return render(request,'recipes.html',context)
    else:
        return redirect('login')

def Engredients(request):
    data = {}
    headers = {
        'Referer': f'{settings.API_URL}/api/ingredients',
        "Authorization": f"Bearer {request.session['access_token']}"
    }
    response = session.get(f'{settings.API_URL}/api/ingredients/', data=data, headers=headers)
    if response.status_code == 200:
        ingredients = response.json()
        engredients_dict = {}
        for ingredient in ingredients:
            engredients_dict[ingredient['name']] = {'unit':ingredient['mesurement'],'cat': ingredient['category']['name'],'avg_price':ingredient['avg_price'],'seasons':ingredient['season']}
        context = {'engredients':engredients_dict,'engredient':True}
        return render(request,'engredients.html',context)
    else:
        return redirect('login')
    
def CreateRecipe(request):
    recipeForm = RecipeForm()
    context = {'recipe_form':recipeForm,'recipe':True}
    return render(request,'recipe.html',context)

def CreateUserView(request):
    if request.session['group'] == 'staff' :
        if request.method == 'POST':
            user_form = CreateUser(request.POST)
            if user_form.is_valid():
                email = user_form.data['email']
                section = user_form.data['section']
                subject = 'Bievenue à mealplanner'
                user = email[:email.rfind("@")]
                password = generate_password(15)
                api_url = settings.API_URL  # Ensure this is set in your settings
                addUser = f'{api_url}/addUser/'
                csrfUrl = f'{api_url}/token'
                csrf_response = session.get(csrfUrl)
                print(csrf_response)
                csrf_token = csrf_response.json().get('csrfToken')
                # Prepare the login data
                data = {
                    'csrfmiddlewaretoken': csrf_token,
                    'username' : user,
                    'password' : password,
                    'email' : email,
                }
                headers = {
                    'Referer': f'{settings.API_URL}/addUser',
                    "Authorization": f"Bearer {request.session['access_token']}"
                }
                # Make the login request
                response = session.post(addUser, data=data, headers=headers)
                if response.status_code == 200:
                    user = User.objects.create(username=user,email=email)
                    message = f'Bonjour, voici votre utilisateur et votre mot de passe utilisateur = {user}, mot de passe = {password} \nVoici le site internet pour vous connecter et modifier votre menu: https://menuplanner.pythonanywhere.com/ '
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email, ]
                    user.save()
                    sectionobj = Section.objects.values('name').filter(id=section).first()
                    sectionName = sectionobj['name']
                    group = Group.objects.get_or_create(name=sectionName)
                    group_id = Group.objects.values('id').filter(name=sectionName).first()
                    user.groups.add(group_id['id'])
                    send_mail( subject, message, email_from, recipient_list )
                    messages.success(request, "L'utilisateur a été ajouté")
                    context = {'home':True, 'user_form':CreateUser}
                    return render(request,"home.html",context)
                else:
                    messages.error(request, "Erreur en ajoutant l'utilisateur")
                    context = {'home':True, 'user_form':CreateUser}
                    return render(request,"home.html",context)
            else:
                messages.error(request, "Erreur en ajoutant l'utilisateur")
                context = {'home':True, 'user_form':CreateUser}
                return render(request,"home.html",context)
    else:
        return render(request, '403.html', status=403)
        

def displayRecipes(request):
    databse_access.getRecipes()

from datetime import datetime,timedelta
def get_date_range(start_date, end_date):
    # Convert the input strings to datetime objects if they are strings
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Generate the list of dates
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    return date_list

#or camp_objects.section.name == request.user.groups.all()[0]
def DisplayMenuCamp(request, camp):
    camp_objects = Camp.objects.get(id=camp)
    if request.session['group'] == 'staff' or str(camp_objects.section.name) == str(request.user.groups.all()[0]):
        menus = Menu.objects.filter(camp=camp_objects).order_by('date')
        dates = get_date_range(camp_objects.from_date, camp_objects.to_date)
        menu_dict = {}
        date_dict = {}

        for date in dates:
            matin_menu = databse_access.getMenu(date, Moment.MATIN, camp_objects)
            midi_menu = databse_access.getMenu(date, Moment.MIDI, camp_objects)
            gouter_menu = databse_access.getMenu(date, Moment.GOUTER, camp_objects)
            souper_menu = databse_access.getMenu(date, Moment.SOUPER, camp_objects)
            cinquieme_menu = databse_access.getMenu(date, Moment.CINQIEME, camp_objects)
            #print(matin_menu if matin_menu else None)
            menu_dict[date.day] = [
                MenuForm(initial=matin_menu if matin_menu else {'moment': Moment.MATIN, 'date': date}),
                MenuForm(initial=midi_menu if midi_menu else {'moment': Moment.MIDI, 'date': date}),
                MenuForm(initial=gouter_menu if gouter_menu else {'moment': Moment.GOUTER, 'date': date}),
                MenuForm(initial=souper_menu if souper_menu else {'moment': Moment.SOUPER, 'date': date}),
                MenuForm(initial=cinquieme_menu if cinquieme_menu else {'moment': Moment.CINQIEME, 'date': date}),
            ]
            date_dict[date.day] = date

        section = camp_objects.section
        context = {
            'menus': menus,
            'camp_objects': camp_objects,
            'menu_form': MenuForm(initial={'moment': Moment.MATIN}),
            'search': SearchDate,
            'menu_dict': menu_dict,
            'date_dict': date_dict
        }
        return render(request, "camp_menu.html", context)
    else:
        return render(request, '403.html', status=403)


def addMenuToCamp(request, camp):
    camp_instance = get_object_or_404(Camp, pk=camp)
    if request.method == 'POST':
        menu_form = MenuForm(request.POST)
        if menu_form.is_valid():
            if databse_access.getMenuId(camp=camp, date=menu_form.cleaned_data['date'], moment=menu_form.cleaned_data['moment']) is not None:
                Menu.objects.filter(camp=camp, date=menu_form.cleaned_data['date'], moment=menu_form.cleaned_data['moment']).delete()
            if camp_instance.from_date <= menu_form.cleaned_data['date'] <= camp_instance.to_date:
                menu_instance = menu_form.save(commit=False)
                menu_instance.camp = camp_instance
                menu_instance.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': "Ajout du menu"})
                messages.success(request, "Ajout du menu")
                return DisplayMenuCamp(request, camp)
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': "Mauvaise date"})
                messages.error(request, "Mauvaise date")
                return DisplayMenuCamp(request, camp)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': menu_form.errors})
            messages.error(request, menu_form.errors)
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': "Erreur durant l'exécution"})
        messages.error(request, "Erreur durant l'exécution")
    return DisplayMenuCamp(request, camp)

def DeleteMenuCamp(request,camp,menu):
    Menu.objects.filter(pk=menu).delete()
    return DisplayMenuCamp(request,camp)


def FinishCamp(request,camp):
    Camp.objects.filter(pk=camp).update(status=Status.F)
    return DisplayMenuCamp(request, camp)   

def ResetCampStatus(request,camp):
    Camp.objects.filter(pk=camp).update(status=Status.C)
    return Camps(request)   

def RedirectView(request):
    pass

def getIngredientsSu(request):
    categories = get_categories()
    categories_engredients = {}
    for category in categories:
        if category['name'] == 'produits laitiers':
            categories_engredients['laitiers']  = IngredientXSU.objects.all().filter(category = category['name'])
        else:
            categories_engredients[category['name']]  = IngredientXSU.objects.all().filter(category = category['name'])
    ingredients = databse_access.getIngredientsSu()
    context = {'engredientList':True,'ingredients':categories_engredients}
    print(categories_engredients)
    return render(request,'ingredients_su.html',context)

def toggleSu(request,ingredient):
    print("toggleSu", "ingredient",ingredient)
    ingredient_xsu = get_object_or_404(IngredientXSU, pk=ingredient)
    ingredient_xsu.su = not ingredient_xsu.su  # Toggle the boolean field
    ingredient_xsu.save()
    return JsonResponse({'success':True,'message':'value is updated '})

def HideCamps(request):
    databse_access.HideCamps()
    return redirect('camps')

def AddProducteur(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        producteur_form = ProducteurModelForm(request.POST)
        if address_form.is_valid() and producteur_form.is_valid():
            address = address_form.save()
            producteur = producteur_form.save(commit=False)
            producteur.location = address
            producteur.save()
            producteur_form.save_m2m()
            messages.success(request, "Ajout du producteur")
            return redirect('producteurs')
        else:
            print(address_form.errors,producteur_form.errors)
            messages.error(request, "Erreur dans l'ajout du producteur")
            return redirect('producteurs')
    return redirect('producteurs')

def DisplayProducteur(request):
    producteurs = databse_access.getProducteurs(request)
    context = {'addressForm':AddressForm,'producteurForm':ProducteurModelForm,'producteur_list':producteurs, 'producteurs':True}
    return render(request,"producteurs.html",context)






