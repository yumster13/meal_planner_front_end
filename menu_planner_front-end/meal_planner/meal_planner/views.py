from django.shortcuts import redirect
from .forms import *
from django.shortcuts import render
def RedirectView(request,any_url = None):
    if request.user.is_authenticated:
        print(request.user)
        return redirect('home') 
    else: 
        return redirect('login') 
    


#######################################  API ###############################################

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'email': token.user.email
        })



def LoginView(request):
    pass


from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import requests
from django.middleware.csrf import get_token
import time
requests.packages.urllib3.disable_warnings()
session = requests.Session()
session.verify = False


def CustomLogoutView(request):
        
    # Authenticate via API to get the JWT token
    api_url = settings.API_URL  # Ensure this is set in your settings
    logout = f'{api_url}/logout/'
    csrf_url = f'{api_url}/token/'

    csrf_response = session.get(csrf_url)
    print(csrf_response)
    csrf_token = csrf_response.json().get('csrfToken')
    # Prepare the login data
    data = {
        'csrfmiddlewaretoken': csrf_token,
    }
    headers = {
        'Referer': f'{settings.API_URL}/logout',
        "Authorization": f"Bearer {request.session['access_token']}"
    }
    # Make the login request
    response = session.post(logout, data=data, headers=headers)
    print(response.text)
    if response.status_code == 200:
        return redirect('login')
    else:
        return HttpResponse('Invalid logout', status=401)
    
def CustomLoginView(request):
    if request.method == 'POST':
        # Extract username and password from the request
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        # Authenticate via API to get the JWT token
        api_url = settings.API_URL  # Ensure this is set in your settings
        login_url = f'{api_url}/login/'
        csrf_url = f'{api_url}/token/'

        # Create a session with SSL certificate verification disabled
        

        # Get CSRF token
        csrf_response = session.get(csrf_url)
        print(csrf_response)
        csrf_token = csrf_response.json().get('csrfToken')

        # Prepare the login data
        data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrf_token,
        }

        # Make the login request
        response = session.post(login_url, data=data, headers={'Referer': login_url})
        print(response.text)
        if response.status_code == 200:
            token_data = response.json()
            get_initial_tokens(request,username,password)
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username)

            request.session['group'] = str(user.groups.all()[0].name) if user.groups.all() else 'staff' 
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return HttpResponse('Invalid login', status=401)
    else:
        context = {'form':CustomAuthenticationForm}
        return render(request,'registration/login.html',context)


def get_initial_tokens(request, username, password):
    response = session.post(settings.TOKEN_URL, data={
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
    })
    print(response.json())
    if response.status_code == 200:
        token_data = response.json()
        settings.ACCESS_TOKEN = token_data['access_token']
        request.session['access_token'] = token_data['access_token']
        request.session['refresh_token'] = token_data['refresh_token']
        request.session['expires_at'] = time.time() + token_data['expires_in']
    else:
        raise Exception("Failed to obtain initial tokens: {}".format(response.json()))

def refresh_access_token(request):
    response = session.post(settings.TOKEN_URL, data={
        'grant_type': 'refresh_token',
        'refresh_token': request.session.get('refresh_token'),
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
    })

    if response.status_code == 200:
        token_data = response.json()
        request.session['access_token'] = token_data['access_token']
        request.session['refresh_token'] = token_data['refresh_token']
        request.session['expires_at'] = time.time() + token_data['expires_in']
    else:
        raise Exception("Failed to refresh token: {}".format(response.json()))

