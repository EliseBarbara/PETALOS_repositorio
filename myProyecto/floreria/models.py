from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre=models.CharField(max_length=100, primary_key=True)
    descripcion=models.TextField()
    valor=models.IntegerField()
    estado=models.TextField()
    stock=models.IntegerField()
    foto=models.ImageField(upload_to="flores",null=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre=models.CharField(max_length=15, primary_key=True)
    contrasena=models.TextField()
    correo=models.TextField()

    def __str__(self):
        return self.nombre