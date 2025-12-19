"""
URL configuration for nails project.

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
from django.urls import path
from nails_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('contacto/', contacto, name='contacto'),

    path('rol/insert/', insert_rol, name='insert_rol'),
    path('rol/list/', list_rol, name='list_rol'),
    path('rol/reorder/', reorder_roles, name='reorder_roles'),
    path('rol/update-order/', update_rol_order, name='update_rol_order'),
    path('rol/update/<int:id>/', update_rol, name='update_rol'),
    path('rol/delete/<int:id>/', delete_rol, name='delete_rol'),

    path('user/register/', insert_user, name='insert_user'),
    path('user/list/', list_user, name='list_user'),
    path('user/delete/<int:id>/', delete_user, name='delete_user'),
    path('user/update/<int:id>/', update_user, name='update_user'),

    path('user/login/', login_user, name='login_user'),
    path('user/logout/', logout_user, name='logout_user'),
    ]
from django.conf import settings