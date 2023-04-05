from django.urls import path
from .import views

urlpatterns = [

    path('',views.login),
    path('login/',views.login),
    path('signup/',views.signup),
    path('logout/',views.logout),
    path('home/',views.home),

]