from django.shortcuts import render
#importamos las clases del modelo
from .models import Producto,Cliente,Estado
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

#Método para agregar productos y se añadan a la galería de forma automática
@login_required(login_url='/login/')
def formulario(request):
    esta=Estado.objects.all()#Select * from Estado
    if request.POST:
        nombre=request.POST.get("txtNombreFlor")
        valor=request.POST.get("txtValor")
        cantidad=request.POST.get("txtStock")
        descripcion=request.POST.get("txtDescripcion")
        estado=request.POST.get("cboEstado")
        #recupera el objeto con 'name' enviado desde el comboBox (cboEstado)
        obj_estado=Estado.objects.get(name=estado)
        #recuperar la imagen desde el formulario
        imagen=request.FILES.get("txtImagen")
        #crear una instancia de Producto en el modelo
        producto=Producto(
            name=nombre,
            descripcion=descripcion,
            valor=valor,
            estado=obj_estado,
            stock=cantidad,                                
            foto=imagen
        )
        producto.save() #graba el objeto en la BD
        return render(request,'core/formulario.html',{'lista':esta,'msg':'Producto agregado a Galería','sw':True})
    return render(request,'core/formulario.html',{'lista':esta})#pasan los datos a la web

#Método para mostrar la galería
@login_required(login_url='/login/')
def galeria(request):
    flores=Producto.objects.all()# select * from producto     
    return render(request, 'core/galeria.html',{'listaflores':flores})

#Método para eliminar un producto desde la galería
@login_required(login_url='/login/')
def eliminar_producto(request,id):
    mensaje=''    
    producto=Producto.objects.get(name=id)
    try:
        producto.delete()
        mensaje='El producto fue eliminado'
    except:
        mensaje='No se pudo eliminar el producto'
    
    flores=Producto.objects.all()
    return render(request,'core/galeria.html',{'listaflores':flores,'msg':mensaje})
    
