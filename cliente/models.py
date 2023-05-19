from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=30, unique=True, null=False, blank=False, primary_key=True)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre
