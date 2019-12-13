#tendrá las urls del sitio web
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name='HOME'),
    path('login/',login,name='LOGIN'),
    path('login_iniciar/',login_iniciar,name='LOGIN_INICIAR'),
    path('cerrar_sesion/',cerrar_sesion,name='CERRAR_SESION'),
    path('formulario/',formulario,name='FORMU'),
    path('galeria/',galeria,name='GALE'),
    path('eliminar_producto/<id>/',eliminar_producto,name='ELIMINAR'),
    path('agregar_carro/<id>/',agregar_carro,name='AGREGAR_CARRO'),
    path('carrito/',carrito,name='CARRITO'),
    path('enviar_carrito/',vaciar_carrito,name='VACIARCARRITO'),
    path('nosotros/',nosotros,name='NOSOTROS'),
    path('registrar/',registrar,name='REGISTRAR'),
]