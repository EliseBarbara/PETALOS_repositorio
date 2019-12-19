from django.shortcuts import render
#importamos las clases del modelo
from .models import Producto,Cliente,Estado
from .forms import CustomUserForm
#importamos las extensiones para autenticar
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login as auth_login
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
#importamos desde el rest_framework
from rest_framework import viewsets
from .serializers import FlorSerializers

#-------------INICIO/CERRAR SESION -------------------------------------------------
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

@login_required(login_url='/login/')
def cerrar_sesion(request):
    logout(request)
    return HttpResponse("<script>alert('cerró sesión');window.location.href='/';</script>")

#-----------NUEVO USUARIO -----------------------------------------
def registrar(request):
    if request.method == 'POST':
        user = request.POST.get("txtUsuario")
        passs = request.POST.get("txtpassword")
        correo = request.POST.get("txtCorreo")

        formulario = CustomUserForm(
            username = user,
            password = passs,
            email = correo,
        )
        formulario.save()
    return render(request,'core/index.html')
    

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
    flores=Producto.objects.all()# select * from Producto     
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

#Método para pagina Nosotros
def nosotros(request):
    return render(request,'core/nosotros.html')

#Métodos para administrar Carro de compras


#Método para agregar productos al carro de compras
@login_required(login_url='/login/')
def agregar_carro(request,id):
    #recuperar el valor del producto (select * from Producto where mane like (%id%))
    producto=Producto.objects.get(name__contains=id)
    precio=producto.valor
    
    #recuperar una sesion llamada 'carro' y de no existir no deja nada ''
    sesion = request.session.get("carro","")
    #buscar el producto en el interior del listado; split: separa elementos del arreglo que van mutando
    arr=sesion.split(";")
    #almacena los registros limpios
    arr2=''
    sw=0
    cant=1
    for f in arr:
        flo=f.split(":")
        if flo[0]==id:
            cant=int(flo[1])+1
            sw=1
            arr2=arr2+str(flo[0])+":"+str(cant)+":"+str(precio)+";"
        elif not flo[0]=="":#para q no recupere el "" como un elemento diferente
            cant=flo[1]
            arr2=arr2+str(flo[0])+":"+str(cant)+":"+str(precio)+";"
    #verifica si el producto existe o no
    if sw==0:
        arr2=arr2+str(id)+":"+str(1)+":"+str(precio)+";"    
    
    #en sesion carro almaceno lo que trae la sesion más el titulo del producto
    request.session["carro"]=arr2
    flores=Producto.objects.all()
    #renderizar la pagina, pasandole el listado de productos
    msg='Se agregó el Producto al carro de compras'
    return render(request,'core/galeria.html',{'listaflores':flores,'msg':msg})

@login_required(login_url='/login/')
def carrito(request):
    lista=request.session.get("carro","")
    arr=lista.split(";")
    return render(request,"core/carrito.html",{'lista':arr})

#Método para vaciar carro de compras
def vaciar_carrito(request):
    request.session["carro"]=""
    lista=request.session.get("carro","")
    msg='Su pedido se está procesando. Le llegará un correo de confirmación del pedido y confirmación metodo pago. Muchas Gracias!!'     
    return render(request,"core/carrito.html",{'lista':lista, 'msg':msg})


#-------------------------Métodos API REST (viewset)
class FlorViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = FlorSerializers #esta clase pasará todo a JSON
