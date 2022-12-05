from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    token_app_session = models.CharField(max_length = 240,null=True, blank=True, default='')
    first_session = models.CharField(max_length = 240,null=True, blank=True, default='Si')
    foto_perfil = models.ImageField(upload_to="perfil", null=True, default='no-avatar.jpg')

    class Meta:
        ordering = ['user__username']

class Coordinador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=150, null=True, blank=True, verbose_name='nombre coordinador')
    rut=models.CharField(unique=True,max_length=8, null=True, blank=True, verbose_name='rut coordinador')
    dv=models.CharField(max_length=1, null=True, blank=True, verbose_name='digito verificador coordinador')
    email =models.EmailField(max_length=254, null=True, blank=True, verbose_name='email coordinador')
    estado=models.CharField(max_length=100, null=True, blank=True, default='activo', verbose_name='Estado coordinador')
    created =models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')

    class Meta:
        verbose_name='Coordinador'
        verbose_name_plural='Coordinadores'
        ordering=['nombre']

    def __str__(self):
        return self.nombre

class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=150, null=True, blank=True, verbose_name='nombre docente')
    rut=models.CharField(unique=True,max_length=8, null=True, blank=True, verbose_name='rut docente')
    dv=models.CharField(max_length=1, null=True, blank=True, verbose_name='digito verificador docente')
    email =models.EmailField(max_length=254, null=True, blank=True, verbose_name='email docente')  
    estado=models.CharField(max_length=100, null=True, blank=True, default='activo', verbose_name='Estado docente')
    created =models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')

    class Meta:
        verbose_name='Docente'
        verbose_name_plural='Docentes'
        ordering=['nombre']

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre=models.CharField(max_length=150, null=True, blank=True, verbose_name='nombre estudiante')
    rut=models.CharField(unique=True,max_length=8, null=True, blank=True, verbose_name='rut estudiante')
    dv=models.CharField(max_length=1, null=True, blank=True, verbose_name='digito verificador estudiante')
    email =models.EmailField(max_length=254, null=True, blank=True, verbose_name='email estudiante')  
    estado=models.CharField(max_length=100, null=True, blank=True, default='activo', verbose_name='estado estudiante')
    created =models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')

    class Meta:
        verbose_name='Estudiante'
        verbose_name_plural='Estudiantes'
        ordering=['nombre']

    def __str__(self):
        return self.nombre

class Disciplina(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False, verbose_name='Disciplina')
    class Meta:
        verbose_name='Disciplina'
        verbose_name_plural='Disciplinas'
        ordering=['nombre']

    def __str__(self):
        return self.nombre


class Discapacidad(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False, verbose_name='Discapacidad')
    class Meta:
        verbose_name='Discapacidad'
        verbose_name_plural='Discapacidades'
        ordering=['nombre']

    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    nombre=models.CharField(max_length=150, null=True, blank=True, verbose_name='Nombre Paciente')
    rut=models.CharField(unique=True, max_length=8, null=True, blank=True, verbose_name='Rut paciente')
    dv=models.CharField(max_length=1, null=True, blank=True, verbose_name='Digito verificador Paciente')
    fecha_nacimiento=models.DateField(verbose_name='Fecha nacimiento paciente')
    disciplina= models.ManyToManyField(Disciplina, related_name='disciplina')
    genero= models.CharField(max_length=100, null=True, blank=True, verbose_name='Genero paciente')
    email =models.EmailField(max_length=254, null=True, blank=True, verbose_name='email paciente')
    discapacidades = models.ManyToManyField(Discapacidad, related_name='discapacidad')
    created =models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación paciente')

    class Meta:
        verbose_name='Paciente'
        verbose_name_plural='Pacientes'
        ordering=['nombre']

    def __str__(self):
        return self.nombre

