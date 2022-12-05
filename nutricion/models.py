from django.db import models
from django.contrib.auth.models import Group, User
from registro.models import Paciente,Estudiante
# Create your models here.

class Solicitud(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estado= models.CharField(max_length=100, null=True, blank=True, default='activo', verbose_name='Estado solicitud')
    fecha_eval = models.DateField(null=False, blank=False, verbose_name='Fecha atencion')
    fecha_add = models.DateField(auto_now_add=True, null=False, blank=False, verbose_name='Fecha creacion')
    estudiante = models.ManyToManyField(Estudiante, related_name='estudiante')
    paciente = models.ManyToManyField(Paciente, related_name='paciente')
    
    class Meta:
        verbose_name='Solicitud'
        verbose_name_plural='Solicitudes'
        ordering=['user']

class Detalle_atencion(models.Model):
    estudiante =  models.ForeignKey(Estudiante, blank=True, null=True, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, blank=True, null=True, on_delete=models.CASCADE)
    fecha_eval = models.DateField(auto_now_add=True, null=False, blank=False, verbose_name='Fecha atencion')
    estatura = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    peso_prom = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    prom_circunferencia_cin = models.FloatField(null=False, blank=False)
    prom_circunferencia_braq = models.FloatField(null=False, blank=False)
    prom_pliegue_t = models.FloatField(null=False, blank=False,verbose_name='promedio pliegue triciptal')
    prom_pliegue_b = models.FloatField(null=False, blank=False,verbose_name='promedio pliegue biciptal')
    prom_pliegue_se = models.FloatField(null=False, blank=False,verbose_name='promedio pliegue subescapular')
    prom_pliegue_si = models.FloatField(null=False, blank=False,verbose_name='promedio pliegue suprailiaco')
    sum_pliegues = models.FloatField(null=False, blank=False,verbose_name='suma todos los pliegues')
    porc_grasa = models.FloatField(null=False, blank=False,verbose_name='procentaje de grasa')
    diag_nutri = models.CharField(max_length=1500, null=False, blank=False, verbose_name='comentario')
    prom_pliegue_abd = models.FloatField(null=True, blank=True,verbose_name='promedio pliegue abdominal', default=None)
    prom_pliegue_pant = models.FloatField(null=True, blank=True,verbose_name='promedio pliegue pantorilla', default=None)
    prom_pliegue_media = models.FloatField(null=True, blank=True,verbose_name='promedio pliegue media', default=None)
    prom_pliegue_supra = models.FloatField(null=True, blank=True,verbose_name='promedio pliegue supraespinal', default=None)
    recomendacion = models.CharField(max_length=1500,null=True, blank=True, verbose_name='Recomendación', default=None)

    class Meta:
        verbose_name='Detalle_atencion'
        verbose_name_plural='Detalles_atenciones'

class Calificacion(models.Model):
    ficha = models.ForeignKey(Detalle_atencion, blank=True, null=True, on_delete=models.CASCADE)
    nota = models.FloatField(null=False, blank=False,verbose_name='nota')
    comentario = models.CharField(max_length=1500, null=False, blank=False, verbose_name='comentario')

    class Meta:
        verbose_name='Calificacion'
        verbose_name_plural='Calificaciones'