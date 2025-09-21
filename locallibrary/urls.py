"""
URL configuration for locallibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import PasswordsChangeView, password_change_success,logout_user




urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.urls import include

urlpatterns += [
    path('catalog/', include('catalog.urls')),
]

from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
  #  path('login_user', login_user,  name='login'),
    path('logout_user', logout_user,  name='logout_user'),
    
]


urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
     path('password_change/',PasswordsChangeView.as_view(),name='password_change')
]


urlpatterns += [
     path('password_change_success', password_change_success, name="password_change_success")
]