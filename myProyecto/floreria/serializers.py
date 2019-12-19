#transferir datos BD a otro lenguaje (JSON) - Tambien se puede pasar de un lenguaje (JSON) a datos y luego a la BD

from rest_framework import serializers
from .models import Producto

#hacer clase que trasnferirá los datos
class FlorSerializers(serializers.ModelSerializer):
    
    #definir el modelo que se basa la clase y los datos que saldrán (los que no tambien)
    class Meta:
        model = Producto
        fiels = ['name', 'descripcion', 'valor','stock','estado', 'foto']
        exclude = []