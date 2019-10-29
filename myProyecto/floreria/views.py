from django.shortcuts import render
#importamos las clases del modelo
from .models import Producto,Cliente
#importamos las extensiones para autenticar
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def  login(request):
    return render(request,'core/login.html')

def login_iniciar(request):
    if request.POST:
        u=request.POST.get("txtUsuario")
        p=request.POST.get("txtPass")
        usu=authenticate(request,username=u,password=p)
        if usu is not None and usu.is_active:
            auth_login(request, usu)
            return render(request,'core/index.html')
    return render(request,'core/login.html')

def cerrar_sesion(request):
    logout(request)
    return HttpResponse("<script>alert('cerró sesión');window.location.href='/';</script>")

@login_required(login_url='/login/')
def home(request):
    return render(request,'core/index.html')
    
