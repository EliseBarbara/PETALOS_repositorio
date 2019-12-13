from django.db import models

# Create your models here.
class Estado(models.Model):
    name=models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

class Producto(models.Model):
    name=models.CharField(max_length=100, primary_key=True)
    descripcion=models.TextField()
    valor=models.IntegerField()
    estado=models.ForeignKey(Estado,on_delete=models.CASCADE)
    stock=models.IntegerField()
    foto=models.ImageField(upload_to="flores",null=True)

    def __str__(self):
        return self.name


class Cliente(models.Model):
    name=models.CharField(max_length=15, primary_key=True)
    contrasena=models.TextField()
    correo=models.TextField()

    def __str__(self):
        return self.name