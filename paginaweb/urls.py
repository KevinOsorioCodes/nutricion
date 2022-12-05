
from django.urls import path,include
from paginaweb import views

paginaweb_urlpatterns = [
    path('',views.home,name="home")
    ]
