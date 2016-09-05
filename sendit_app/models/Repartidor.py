from django.db import models
from sendit_app.models.Categoria import Categoria
from sendit_app.models.Usuario import Usuario
from sendit_app.models.Sexo import Sexo
from sendit_app.models.Vehiculo import Vehiculo
from sendit_app.models.Estado_Repartidor import Estado_Repartidor


class Repartidor(Usuario):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField
    sexo_choices = ((Sexo.HOMBRE, 'Hombre'), (Sexo.MUJER, 'Mujer'))
    sexo = models.BinaryField(choices=sexo_choices, null=True)
    dni = models.CharField(max_length=15)
    vehiculo = models.ForeignKey(Vehiculo)
    categoria_choices = ((Categoria.DELIVERY_COMIDA, 'Delivery Comida'),
                         (Categoria.DELIVERY_CHICO, 'Delivery Paqueteria Pequeña y Documentos'),
                         (Categoria.DELIVERY_MEDIANO, 'Delivery Paqueteria Mediana'),
                         (Categoria.DELIVERY_GRANDE, 'Delivery Grandes Objetos'))
    categoria = models.CharField(max_length=10, choices=categoria_choices)
    estado_choices = ((Estado_Repartidor.INACTIVO, 'Inactivo'), (Estado_Repartidor.ACTIVO, 'Activo'),
                      (Estado_Repartidor.OCUPADO, 'Ocupado'))
    estado = models.CharField(max_length=10, choices=estado_choices, default=Estado_Repartidor.INACTIVO)
    habilitado = models.BinaryField(default=0)
    puntaje_prom = models.FloatField(null=True)
