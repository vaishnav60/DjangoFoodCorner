"""FoodCorner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from FoodApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('addfood/',views.addFood),
    path('menu/',views.menu),
    path('update/<int:id>', views.updateFood),
    path('delete/<int:id>',views.deleteFood),
    path('signup/',views.signup),
    path('login/',views.loginUser),
    path('logout/',views.logoutUser),
    path("",views.index),
    path("addtocart/",views.addCart),
    path('profile/', views.userProfile),
    path('updatecust/', views.updateProfile),
    path('cart/', views.showCart),
    path('updatecart/', views.updateCart),
    path('deleteCart/<int:id>',views.deleteCart),
    path('placeOrder',views.placeOrder),
    path('myorders/', views.showOrders),
    path('allorders/', views.allOrders)


]
if settings.DEBUG:
    print(static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT))

    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


