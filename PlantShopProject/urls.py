"""
URL configuration for PlantShopProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from PlantShopApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('aboutus/', aboutUs, name='aboutUs'),
    path('care/', care, name='care'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('plants/', plants, name='plants'),
    path('shoppingCart/', shoppingCart, name='shoppingCart'),
    path('plants/<int:code>/', singlePlant, name='singlePlant'),
    path('successfulPayment/', successfulPayment, name='success'),
    path('add_to_cart/<int:plant_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('search/', search_plants, name='search_plants'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', payment, name='payment')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

