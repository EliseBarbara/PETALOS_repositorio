#tendrá las urls del sitio web
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name='HOME'),
    path('login/',login,name='LOGIN'),
    path('login_iniciar/',login_iniciar,name='LOGIN_INICIAR'),
    path('cerrar_sesion/',cerrar_sesion,name='CERRAR_SESION'),

]