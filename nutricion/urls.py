from django.urls import path
from django.contrib import admin
from nutricion import views


nutricion_urlpatterns = [
    path('solicitud_list/',views.solicitud_list,name="solicitud_list"),
    path('solicitud_add/',views.solicitud_add,name="solicitud_add"),
    path('solicitud_save/',views.solicitud_save,name="solicitud_save"),
    path('solicitud_update/<solicitud_id>/',views.solicitud_update,name="solicitud_update"),
    path('solicitud_edit/<solicitud_id>/',views.solicitud_edit,name="solicitud_edit"),
    path('solicitud_delete/<solicitud_id>/',views.solicitud_delete,name="solicitud_delete"),
    #paciente
    path('paciente_add/', views.paciente_add, name="paciente_add"),
    path('paciente_save/', views.paciente_save, name="paciente_save"),
    path('paciente_list/', views.paciente_list, name="paciente_list"),
    path('paciente_edit/<paciente_id>/', views.paciente_edit, name="paciente_edit"),
    path('paciente_update/<paciente_id>/', views.paciente_update, name="paciente_update"),
    path('paciente_delete/<paciente_id>/', views.paciente_delete, name="paciente_delete"),


    path('ficha_add/<paciente_id>/', views.ficha_add, name="ficha_add"),
    path('ficha_save/<paciente_id>/', views.ficha_save, name="ficha_save"),
    path('ficha_edit/<paciente_id>/<ficha_id>/', views.ficha_edit, name="ficha_edit"),
    path('ficha_update/<paciente_id>/<ficha_id>/', views.ficha_update, name="ficha_update"),
    path('ficha_list/',views.ficha_list,name="ficha_list"),
    path('ficha_list/<paciente_id>/',views.ficha_paciente_list,name="ficha_paciente_list"),
    path('ficha_delete/<ficha_id>/',views.ficha_delete,name="ficha_delete"),

    


    #Coordinador
    path('admin_ficha_add/<paciente_id>/',views.admin_ficha_add,name="admin_ficha_add"),
    path('admin_ficha_save/<paciente_id>',views.admin_ficha_save,name="admin_ficha_save"),
    
    
   
    path('admin_ficha_paciente_list/',views.admin_ficha_paciente_list1,name="admin_ficha_paciente_list1"),
    path('admin_ficha_paciente_list/<paciente_id>/',views.admin_ficha_paciente_list2,name="admin_ficha_paciente_list2"),
    path('admin_ficha_paciente_ver/<paciente_id>/<ficha_id>/',views.admin_ficha_paciente_ver,name="admin_ficha_paciente_ver"),
    
    path('admin_ficha_estudiante_list/',views.admin_ficha_estudiante_list1,name="admin_ficha_estudiante_list1"),
    path('admin_ficha_estudiante_list/<estudiante_id>/',views.admin_ficha_estudiante_list2,name="admin_ficha_estudiante_list2"),
    path('admin_ficha_estudiante_ver/<estudiante_id>/<ficha_id>/',views.admin_ficha_estudiante_ver,name="admin_ficha_estudiante_ver"),
    path('admin_calificacion_save1/<estudiante_id>/<ficha_id>/',views.admin_calificacion_save1,name="admin_calificacion_save1"),
    path('admin_calificacion_save2/<paciente_id>/<ficha_id>/',views.admin_calificacion_save2,name="admin_calificacion_save2"),
    
    #alumno
    path('calificacion_ver/',views.calificacion_ver,name="calificacion_ver"),
    path('calificacion_ficha_ver/<ficha_id>/',views.calificacion_ficha_ver,name="calificacion_ficha_ver"),
]

