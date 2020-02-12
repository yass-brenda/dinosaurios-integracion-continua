from django.db import models
from django.contrib.auth.models import User 


class Estado(models.Model):
    nombre = models.CharField(max_length=100,)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    nombre = models.CharField(max_length=100,)
    estado = models.ForeignKey(Estado, verbose_name="Estado", on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    



class Cliente(models.Model):
    rfc = models.CharField("R.F.C.", max_length=15)
    direccion = models.CharField("Dirección", max_length=100)
    telefono = models.CharField("Teléfono", max_length=15)
    usuario = models.OneToOneField(User, verbose_name="Usuario", on_delete=models.CASCADE)
    foto = models.ImageField("Foto", upload_to='usuarios', null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True )

    def __str__(self):
        return self.usuario.first_name
    

