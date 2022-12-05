from re import template
from django.urls import path
from django.contrib import admin
from registro import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('perfil/',views.ver_perfil,name='perfil'),
    path('cambiar_foto/', views.cambiar_foto, name="cambiar_foto"),
    path('quitar_foto/', views.quitar_foto, name="quitar_foto"),

    path('password_first/',views.password_first_sesion,name="password_first_sesion"),
    path('password_first_save/',views.password_first_sesion_save,name="password_first_sesion_save"),
    path('password_change/',views.password_change, name='password_change'),
    path('password_change/done/', views.password_change_done, name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset_form'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),

    #coordinador
    path('coordinador_add/', views.coordinador_add, name="coordinador_add"),
    path('coordinador_list/', views.coordinador_list, name="coordinador_list"),
    path('coordinador_save/', views.coordinador_save, name="coordinador_save"),
    path('coordinador_estado/<coordinador_id>/', views.coordinador_estado, name="coordinador_estado"),
    path('coordinador_edit/<coordinador_id>/', views.coordinador_edit, name="coordinador_edit"),
    path('coordinador_update/<coordinador_id>/', views.coordinador_update, name="coordinador_update"),
    path('coordinador_delete/<coordinador_id>/', views.coordinador_delete, name="coordinador_delete"),
    path('coordiandor_load_save/', views.coordinador_load_save, name="coordinador_load_save"),
    
    #docente
    path('docente_add/', views.docente_add, name="docente_add"),
    path('docente_list/', views.docente_list, name="docente_list"),
    path('docente_save/', views.docente_save, name="docente_save"),
    path('docente_estado/<docente_id>/', views.docente_estado, name="docente_estado"),
    path('docente_edit/<docente_id>/', views.docente_edit, name="docente_edit"),
    path('docente_update/<docente_id>/', views.docente_update, name="docente_update"),
    path('docente_delete/<docente_id>/', views.docente_delete, name="docente_delete"),
    path('docente_load_save/', views.docente_load_save, name="docente_load_save"),
    
    #estudiante
    path('estudiante_add/', views.estudiante_add, name="estudiante_add"),
    path('estudiante_list/', views.estudiante_list, name="estudiante_list"),
    path('estudiante_save/', views.estudiante_save, name="estudiante_save"),
    path('estudiante_load_save/', views.estudiante_load_save, name="estudiante_load_save"),
    path('estudiante_estado/<estudiante_id>/', views.estudiante_estado, name="estudiante_estado"),
    path('estudiante_edit/<estudiante_id>/', views.estudiante_edit, name="estudiante_edit"),
    path('estudiante_update/<estudiante_id>/', views.estudiante_update, name="estudiante_update"),
    path('estudiante_delete/<estudiante_id>/', views.estudiante_delete, name="estudiante_delete"),

     #descargar
    path('descargar_estudiante/', views.descargar_estudiante, name="descargar_estudiante"),
    path('descargar_docente/', views.descargar_docente, name="descargar_docente"),
    path('descargar_coordinador/', views.descargar_coordinador, name="descargar_coordinador"),
    
]

