from django.shortcuts import render
from django.conf import settings #importa el archivo settings
from django.contrib import messages #habilita la mesajería entre vistas
from django.contrib.auth.decorators import login_required #habilita el decorador que se niega el acceso a una función si no se esta logeado
from django.contrib.auth.models import Group, User # importa los models de usuarios y grupos
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator #permite la paqinación
from django.db.models import Avg, Count, Q #agrega funcionalidades de agregación a nuestros QuerySets
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, HttpResponseRedirect) #Salidas alternativas al flujo de la aplicación se explicará mas adelante
from django.shortcuts import redirect, render #permite renderizar vistas basadas en funciones o redireccionar a otras funciones
from django.template import RequestContext # contexto del sistema
from django.views.decorators.csrf import csrf_exempt #decorador que nos permitira realizar conexiones csrf

from registro.models import Profile #importa el modelo profile, el que usaremos para los perfiles de usuarios


# Create your views here.
def home(request):
    return redirect('login')

@login_required
def pre_check_profile(request):
    pass
        

@login_required
def check_profile(request):  
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()    
    except:
        messages.add_message(request, messages.INFO, 'Hubo un error con su usuario, por favor contactese con los administradores')              
        return redirect('login')
    
    if profile.group_id != 0:
        if profile.first_session == "Si":
            return redirect('password_first_sesion')
        else:
            return redirect('home')
    else:
        return redirect('logout')

@login_required
def check_group_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    
    template_name = 'core/check_group_main.html'
    return render(request,template_name,{'profile':profile})