from django.db import models
from django.utils import  timezone


class Direccion(models.Model):
    calle = models.CharField(max_length=60)
    numero = models.IntegerField
    ciudad = models.CharField(max_length=60)


class Vehiculo(models.Model):
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    patente = models.CharField(max_length=60)
    seguro = models.CharField(max_length=60)
    tipo = models.CharField(max_length=60)


class Plan(models.Model):
    fecha_desde = models.DateField
    fecha_hasta = models.DateField
    limite_km = models.FloatField
    precio_km = models.FloatField


class Rastreo(models.Model):
    latitud = models.FloatField
    longitud = models.FloatField


class Calificacion(models.Model):
    puntaje = models.IntegerField
    comentario = models.CharField(max_length=300, null=True)


class Categoria():
    DELIVERY_COMIDA = 'COMIDA'
    DELIVERY_CHICO = 'CHICO'
    DELIVERY_MEDIANO = 'MEDIANO'
    DELIVERY_GRANDE = 'GRANDE'

class Sexo():
    HOMBRE = 'HOMBRE'
    MUJER = 'MUJER'
    OTRO = 'OTRO'

class Estado_Repartidor():
    INACTIVO = 'INACTIVO'
    ACTIVO = 'ACTIVO'
    OCUPADO = 'OCUPADO'

class Estado_Envio ():
    GENERADO = 'GENERADO'
    CANCELADO = 'CANCELADO'
    EN_ESPERA = 'ESPERA'
    CONFIRMADO = 'CONFIRMADO'
    EN_VIAJE = 'VIAJE'
    NO_ENTREGADO = 'NO_ENTREGADO'
    ENTREGADO = 'ENTREGADO'

class Estado_Paquete ():
    EN_VIAJE = 'VIAJE'
    NO_ENTREGADO = 'NO_ENTREGADO'
    ENTREGADO = 'ENTREGADO'



class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=60, unique=True)
    mail = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    telefono = models.CharField(max_length=30, null=True)
    direccion = models.ForeignKey(Direccion, null=True)


class Repartidor(Usuario):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    fecha_Nacimiento = models.DateTimeField
    sexo_choices = ((Sexo.HOMBRE, 'Hombre')(Sexo.MUJER, 'Mujer')(Sexo.OTRO, 'Otro'))
    sexo = models.CharField(max_length=2, choices=sexo_choices)
    dni = models.CharField(max_length=15)
    vehiculo = models.ForeignKey(Vehiculo)
    categoria_choices = ((Categoria.DELIVERY_COMIDA, 'Delivery Comida')(Categoria.DELIVERY_CHICO, 'Delivery Paqueteria Pequeña y Documentos')(Categoria.DELIVERY_MEDIANO, 'Delivery Paqueteria Mediana')(Categoria.DELIVERY_GRANDE, 'Delivery Grandes Objetos'))
    categoria = models.CharField(max_length= 10, choices=categoria_choices)
    estado_choices = ((Estado_Repartidor.INACTIVO, 'Inactivo'), (Estado_Repartidor.ACTIVO, 'Activo'), (Estado_Repartidor.OCUPADO, 'Ocupado'))
    estado = models.CharField(max_length=10, choices=estado_choices, default=Estado_Repartidor.INACTIVO)


class Persona(Usuario):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    fecha_Nacimiento = models.DateTimeField
    sexo_choices = ((Sexo.HOMBRE, 'Hombre')(Sexo.MUJER, 'Mujer')(Sexo.OTRO, 'Otro'))
    sexo = models.CharField(max_length= 7, choices=sexo_choices, null=True)
    dni = models.CharField(max_length=15)

class Empresa(Usuario):
    razon_social = models.CharField(max_length=60)
    cuit = models.CharField(max_length=60)


class Paquete(models.Mcodel):
    fecha_hora_entrega = models.DateTimeField
    destinatario = models.ForeignKey(Usuario)
    direccion = models.ForeignKey(Direccion)
    precio = models.FloatField
    estado_choices = ((Estado_Paquete.ENTREGADO, 'Entregado'), (Estado_Paquete.EN_VIAJE, 'En viaje'), (Estado_Paquete.NO_ENTREGADO, 'No entregado'))
    estado = models.CharField(max_length=10, choices= estado_choices )


class Envio(models.Model):
    fecha_hora_Generado = models.DateTimeField(default= timezone.now())
    fecha_hora_Entregado = models.DateTimeField(null=True)
    estado_choices = ((Estado_Envio.GENERADO, 'Generado'),(Estado_Envio.CANCELADO, 'Cancelado'), (Estado_Envio.EN_ESPERA, 'En espera'), (Estado_Envio.CONFIRMADO, 'Confirmado'), (Estado_Envio.EN_VIAJE, 'En viaje'), (Estado_Envio.ENTREGADO, 'Entregado'), (Estado_Envio.NO_ENTREGADO, 'No entregado') )
    estado = models.CharField(max_length=10, choices= estado_choices )
    repartidor = models.ForeignKey(Repartidor, related_name='repartidor_envio', null=True)
    remitente = models.ForeignKey(Usuario, related_name='remitente_envio', null= True)
    paquetes = models.ForeignKey(Paquete)
    raestreo = models.ForeignKey(Rastreo, null= True)
    categoria = models.CharField(max_length=10, choices=Repartidor.categoria_choices)