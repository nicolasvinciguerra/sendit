from django.db import models


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
    comentario = models.CharField(max_length=300)


class Categoria(models.Model):
    nombre = models.CharField(max_length=30)


class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=60)
    mail = models.CharField(max_length=60)
    contrasenia = models.CharField(max_length=300)
    telefono = models.CharField(max_length=30)
    direccion = models.ForeignKey(Direccion)


class Repartidor(Usuario):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    fecha_Nacimiento = models.DateTimeField
    sexo = models.CharField(max_length=10)
    dni = models.CharField(max_length=15)
    vehiculo = models.ForeignKey(Vehiculo)
    categoria = models.CharField(max_length=60)
    estado = models.CharField(max_length=30)


class Persona(Usuario):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    fecha_Nacimiento = models.DateTimeField
    sexo = models.CharField(max_length=10)
    dni = models.CharField(max_length=15)


class Paquete(models.Model):
    fecha_hora_entrega = models.DateTimeField
    destinatario = models.ForeignKey(Usuario)
    direccion = models.ForeignKey(Direccion)
    precio = models.FloatField
    estado = models.CharField(max_length=30)


class Envio(models.Model):
    fecha_hora = models.DateTimeField
    estado = models.CharField(max_length=30)
    repartidor = models.ForeignKey(Repartidor, related_name='repartidor_envio')
    remitente = models.ForeignKey(Usuario, related_name='remitente_envio')
    paquetes = models.ForeignKey(Paquete)
    raestreo = models.ForeignKey(Rastreo)
    categoria = models.ForeignKey(Categoria)