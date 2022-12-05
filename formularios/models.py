from django.db import models
from registro.models import Estudiante, Paciente
from nutricion.models import Detalle_atencion

# Create your models here.

class Formulario_alimentario(models.Model):
    ficha = models.ForeignKey(Detalle_atencion, on_delete=models.CASCADE)
    alimento = models.CharField(max_length=25, null = True, blank = True, verbose_name = 'Nombre alimento', default = None) 
    frecuencia = models.CharField(max_length=25, null = True, blank = True, verbose_name = 'Frecuencia de consumo alimento', default = None)
    cantidad = models.IntegerField(null = True, blank = True, verbose_name = 'Cantidad de consumo', default = 0)
    comentario = models.CharField(max_length=500, null = True, blank = True, verbose_name = 'Comentario del nutricionista', default = None)

    class Meta:
        verbose_name='formulario'
        verbose_name_plural='formularios'
        ordering=['ficha']

class Formulario_satisfaccion(models.Model):
    satisfaccion = models.CharField(max_length=25, null = True, blank = True, verbose_name = 'Satisfaccion', default = None)
    estudiante =  models.ForeignKey(Estudiante, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name='satisfaccion'
        verbose_name_plural='satisfacciones'
        ordering=['estudiante']