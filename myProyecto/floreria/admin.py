from django.contrib import admin
from .models import Producto,Cliente,Estado

# Register your models here.
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Estado)
