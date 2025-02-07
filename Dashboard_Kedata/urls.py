"""Dashboard_Kedata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from global_login_required import login_not_required
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('',RedirectView.as_view(url='/users/', permanent=False)),
    path('users/', include('users.urls')),
    path('keyword/', include('kedata_keyword.urls')),
    path('schedule/', include('schedule.urls')),

    path('login/', login_not_required(auth_views.LoginView.as_view(template_name='login.html')), name='login'),
    path('logout/', login_not_required(auth_views.LogoutView.as_view()), name='logout'),
    path('admin/', admin.site.urls),
]
