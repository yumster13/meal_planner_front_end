from django.conf import settings
from django.shortcuts import redirect
from .views import *
import time
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
import requests


session = requests.Session()
session.verify = settings.VERIFY

class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings by setting a tuple of routes to ignore
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), """
        The Login Required middleware needs to be after AuthenticationMiddleware.
        Also make sure to include the template context_processor:
        'django.contrib.auth.context_processors.auth'."""
        current_route_name = request.path_info
        print(current_route_name)
        headers = {
        'Referer': f'{settings.API_URL}/authenticated',
        "Authorization": f"Bearer {request.session['access_token']}"
        }
        authenticated = session.get(f'{settings.API_URL}/authenticated',data = {},headers=headers)
        authenticated = authenticated.json()
        print(authenticated)
        if not authenticated['value'] == 'True' and current_route_name.find('/admin/') == -1 and current_route_name.find('/o/token') == -1 :
            current_route_name = resolve(request.path_info).url_name
            print(current_route_name)
            if not current_route_name in settings.AUTH_EXEMPT_ROUTES:
                return redirect('login') 


class ValidatedTokenRequiredMiddleware(MiddlewareMixin):

    def process_request(self,request):
        expires_at = request.session.get('expires_at')
        current_route_name = resolve(request.path_info).url_name
        print(expires_at, time.time())
        if not expires_at or time.time() >= expires_at:
            print('passed')
            return redirect('login')
