from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Periodo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField("Descripción", null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    

class Dinosaurio(models.Model):
    nombre = models.CharField(max_length=100)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    periodo = models.ForeignKey(Periodo, verbose_name="Periodo", 
        on_delete=models.CASCADE)
    imagen = models.ImageField("Imágen", upload_to='dinos',null=True, blank=True)

    def __str__(self):
        return self.nombre

class VotacionDino(models.Model):
    dinosaurio = models.ForeignKey(Dinosaurio, verbose_name='Dinosaurio', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, verbose_name='Usuario', on_delete = models.CASCADE)
    calificacion = models.IntegerField("Calificación", default=0, 
        validators=[MaxValueValidator(5,'El valor máximo permitido es 5'), MinValueValidator(1, 'El valor mínimo es 1')])
    rollo = models.TextField("Reseña")

