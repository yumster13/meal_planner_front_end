"""
URL configuration for meal_planner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth import views

from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('admin/', admin.site.urls),
    path('creator/',include("creator.urls")),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('login',CustomLoginView,name='login'),
    path('logout',CustomLogoutView,name='logout'),
    path('<str:any_url>/',RedirectView ),
    path('',RedirectView ),
    path('session_security/', include('session_security.urls')),
    path('api-token-auth/', csrf_exempt(CustomAuthToken.as_view()), name='api_token_auth'),
]
