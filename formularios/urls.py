from django.urls import path
from django.contrib import admin
from formularios import views


formularios_urlpatterns = [
    path('encuesta_alimentaria/<ficha_id>/',views.encuesta_alimentaria,name="encuesta_alimentaria"),
    path('encuesta_save/<ficha_id>/',views.encuesta_save,name="encuesta_save"),
    path('encuesta_ver/<ficha_id>/',views.encuesta_ver,name="encuesta_ver"),

    path('encuesta_satisfaccion_token/<ficha_id>/',views.encuesta_satisfaccion_token,name="encuesta_satisfaccion_token"),
    path('encuesta_satisfaccion/<token>/',views.encuesta_satisfaccion_add,name="encuesta_satisfaccion_add"),
    path('encuesta_satisfaccion_save/<token>/',views.encuesta_satisfaccion_save,name="encuesta_satisfaccion_save"),
]