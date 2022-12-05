from django.urls import path
from reportes import views

reportes_urlpatterns = [
    path('ficha_pdf/<ficha_id>/',views.ficha_pdf, name="ficha_pdf"),
    path('dashboard/',views.dashboard_all, name="dashboard"),
]
