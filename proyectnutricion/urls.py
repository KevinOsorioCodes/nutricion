"""proyectnutricion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from core.urls import core_urlpatterns
from reportes.urls import reportes_urlpatterns
from nutricion.urls import nutricion_urlpatterns
from paginaweb.urls import paginaweb_urlpatterns
from formularios.urls import formularios_urlpatterns

urlpatterns = [
    
    path('',include(core_urlpatterns)),
    path('home/',include(paginaweb_urlpatterns)),
    path('cuenta/',include('registro.urls')),
    path('cuenta/',include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('reportes/',include(reportes_urlpatterns)),
    path('nutricion/',include(nutricion_urlpatterns)),
    path('formularios/',include(formularios_urlpatterns)),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)