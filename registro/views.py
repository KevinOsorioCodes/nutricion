from .forms import UserCreationFormWithEmail, EmailForm
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render,redirect,get_object_or_404
from django import forms
from .models import Profile
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.db import DataError
from django.contrib.auth.hashers import make_password
from itertools import cycle
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from registro.models import Coordinador,Docente,Estudiante
from nutricion.models import Detalle_atencion
import os
import pandas

#descargar archivo
import mimetypes
import os
from django.http.response import HttpResponse

def password_change(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 0:
        template_name = 'registration/password_change.html'
        return render(request,template_name,{'profile':profile})
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

def password_change_done(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 0:
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = User.objects.get(pk=profile.user_id)
        password=user.password

        if check_password(old_password,password) == False:
            messages.add_message(request, messages.INFO, 'Contraseña antigua incorrecta')
            return redirect('password_change')

        if new_password1 != new_password2:
            messages.add_message(request, messages.INFO, 'Las contraseñas nueva y la confirmación deben ser iguales')
            return redirect('password_change')

        if new_password1 == password:
            messages.add_message(request, messages.INFO, 'Las contraseñas antigua y la nueva no deben ser iguales')
            return redirect('password_change')

        new_password = make_password(new_password1)

        User.objects.filter(pk=profile.user_id).update(password=new_password)
        messages.add_message(request, messages.INFO, 'Contraseña cambiada con exito')
        return redirect('login')
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

def validarRut(rut):
    rut = rut.upper()
    rut = rut.replace("-","")
    rut = rut.replace(".","")
    aux = rut[:-1]
    dv = rut[-1:]

    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2,8))
    s = sum(d * f for d, f in zip(revertido,factors))
    res = (-s)%11

    if str(res) == dv:
        return True
    elif dv=="K" and res==10:
        return True
    else:
        return False

def validatename(name):
    namevalid = name.replace(" ","")
    return namevalid.isalpha()

    
def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

@login_required
def ver_perfil(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 0:
        template_name = 'registration/profile.html' #TEST
        return render(request,template_name,{'profile':profile})
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def cambiar_foto(request,format=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    try:
        imagen = request.FILES['input-file']

    except ValueError:
        messages.add_message(request, messages.INFO, 'Error en los datos recibidos')
        return redirect('perfil')
    except BaseException:
        imagenAnt=profile.foto_perfil
        Profile.objects.filter(user_id=request.user.id).update(foto_perfil=imagenAnt)
        messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
        return redirect('perfil')

    if profile.foto_perfil!="no-avatar.jpg":
        if os.path.isfile(profile.foto_perfil.path):
            os.remove(profile.foto_perfil.path)

    fs = FileSystemStorage()
    fs.save(imagen.name,imagen)
    Profile.objects.filter(user_id=request.user.id).update(foto_perfil=imagen)
    return redirect('perfil')

@login_required
def quitar_foto(request,format=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try: 
        if profile.foto_perfil!="no-avatar.jpg":
            if os.path.isfile(profile.foto_perfil.path):
                os.remove(profile.foto_perfil.path)

    except BaseException:
        messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
    Profile.objects.filter(user_id=request.user.id).update(foto_perfil="no-avatar.jpg")
    return redirect('perfil')

@login_required
def password_first_sesion(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'registration/password_first_sesion.html'
    user = User.objects.get(id=request.user.id)
    return render(request,template_name,{'user':user,'profile':profile})

@login_required
def password_first_sesion_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    user_id = profile.user_id
    user = User.objects.get(pk=user_id)
    password=user.password

    old_password = request.POST.get('old_password')
    new_password1 = request.POST.get('new_password1')
    new_password2 = request.POST.get('new_password2')

    if check_password(old_password,password) == False:
        messages.add_message(request, messages.INFO, 'Contraseña antigua incorrecta')
        return redirect('password_first_sesion')

    if new_password1 != new_password2:
        messages.add_message(request, messages.INFO, 'Las contraseñas nueva y la confirmación deben ser iguales')
        return redirect('password_first_sesion')

    if new_password1 == password:
        messages.add_message(request, messages.INFO, 'Las contraseñas antigua y la nueva no deben ser iguales')
        return redirect('password_first_sesion')

    new_password = make_password(new_password1)

    Profile.objects.filter(user_id=user_id).update(first_session="No")
    User.objects.filter(pk=user_id).update(password=new_password)

    messages.add_message(request, messages.INFO, 'Contraseña cambiada correctamente')
    return redirect('login')

#Coordinador
@login_required
def coordinador_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'usuarios/coordinador_add.html'
    return render(request,template_name,{'profile':profile,'template_name' : 'usuarios/coordinador_add.html'})

@login_required
def descargar_coordinador(request):
    pass
    BASE_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nombre_archivo = "excel_coordinadores.xlsx"
    ruta_archivo = BASE_dir + "/registro/templates/excel/" + nombre_archivo
    archivo = open(ruta_archivo, 'rb')
    tipo_mimetype = mimetypes.guess_type(ruta_archivo)
    response = HttpResponse(archivo, content_type=tipo_mimetype)
    response['Content-Disposition'] = "attachment; filename=%s" % nombre_archivo
    return response

@login_required
def coordinador_list(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page')
    if search == None:
        search = request.GET.get('search')
    else:
        search = search
    if request.GET.get('search') == None:
        search = search
    else:
        search = request.GET.get('search')
    if request.method == 'POST':
        search = request.POST.get('search')
        page = None
    h_list = []
    h_count = Coordinador.objects.all().count()
    if search == None or search == "None" or search=="":
        h_list_array =Coordinador.objects.order_by('nombre')
        for h in h_list_array:
            perfil = Profile.objects.get(user_id=h.user_id)
            h_list.append({'id':h.id,'nombre':h.nombre,'email':h.email,'rut':h.rut,'dv':h.dv,'estado':h.estado,'perfil':perfil})
    else:
        h_list_array = Coordinador.objects.filter(rut__icontains=search).order_by('nombre')
        h_count = Coordinador.objects.filter(rut__icontains=search).count()
        for h in h_list_array:
            perfil = Profile.objects.get(user_id=h.user_id)
            h_list.append({'id':h.id,'nombre':h.nombre,'email':h.email,'rut':h.rut,'dv':h.dv,'estado':h.estado,'perfil':perfil})
    paginator = Paginator(h_list, 5)
    h_list_paginate= paginator.get_page(page)
    template_name = 'usuarios/coordinador_list.html'
    return render(request,template_name,{'profile':profile,'h_count':h_count,
    'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search,'template_name' : 'usuarios/coordinador_list.html'})

@login_required
def coordinador_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        if request.method == 'POST':
            cantidad = int(request.POST.get('cantidad'))
            t = int(1)
            usuarios1 = Coordinador.objects.all().count()
            while t <= cantidad:
                nombre = 'nombre-'+str(t)
                rut = 'rut-'+str(t)
                dv = 'dv-'+str(t)
                email = 'email-'+str(t)

                nombre = request.POST.get(nombre)
                rut = request.POST.get(rut)
                dv = request.POST.get(dv)
                email = request.POST.get(email)   
            
                rutdv= rut+dv
                validation=rutdv
                result=validarRut(validation)
                result2=validatename(nombre)

                if User.objects.filter(username = email).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el email: '+ email +' ya se encuentra registrado')
                    t = t+1
                    continue
                if Coordinador.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como coordinador')
                    t = t+1
                    continue
                if Docente.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como docente')
                    t = t+1
                    continue
                if Estudiante.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como estudiante')
                    t = t+1
                    continue
                if result==False: #Resultado de rut
                    messages.add_message(request, messages.INFO, 'El Rut: '+ rut+'-'+dv +' del usuario '+ nombre + ' no es valido')
                    t = t+1
                    continue
                if result2==False: 
                    messages.add_message(request, messages.INFO, 'El Nombre ingresado del usuario: '+ nombre + ' no es valido (solo nombres alfabeticos)')
                    t = t+1
                    continue
                
                contraseña=list(rut)
                contraseña2=list(reversed(contraseña))
                semipassw=[]
                for i in range (4):
                    semipassw.append(contraseña2[i])
                lpassw=list(reversed(semipassw))
                passw = "".join(lpassw)

                User_save = User(
                    first_name = nombre,
                    password = make_password(passw),
                    username=email,
                    email=email,
                    )

                User_save.save()
                user_id = User.objects.get(email=email)
                
                Profile_save = Profile(
                    token_app_session= "No",
                    group_id = 2,
                    user_id=user_id.id,
                )
                Profile_save.save()

                Coordinador_save = Coordinador(
                    user_id = user_id.id,
                    nombre = nombre,
                    rut = rut,
                    dv = dv,
                    email=email,
                )
                Coordinador_save.save()

                subject='Usuario creado en '+ settings.IP
                message="Se ha creado el usuario para " + str(nombre) + " \nPara iniciar sesión debe ingresar lo siguiente: \n1)Usuario: "+ email +"\n2)Clave: ultimos 4 digitos antes del dv\nPara iniciar sesión ingrese al siguiente enlace: "+str(settings.IP)+":7000/"
                email_from=settings.EMAIL_HOST_USER
                recipient_list=[email]
                send_mail(subject,message,email_from,recipient_list)

                t = t+1
            usuarios2 = Coordinador.objects.all().count()
            if usuarios2>usuarios1:
                messages.add_message(request, messages.INFO, 'Usuarios ingresados: ' + str(usuarios2-usuarios1))
            return redirect('coordinador_add')
        else:
            messages.add_message(request, messages.INFO, 'Error en el método de envío')
            return redirect('check_group_main')
    except ValueError:
        messages.add_message(request, messages.INFO, 'Error en los datos ingresados Value')
        return redirect('coordinador_add')
    except BaseException:
        messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
        return redirect('coordinador_add')

@login_required
def coordinador_load_save(request):
    from django.contrib.auth.hashers import make_password,check_password
    from registro.models import Coordinador,Docente,Estudiante
    from django.core.mail import send_mail
    
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id==2:
        try:
            usuarios1 = Coordinador.objects.all().count()

            if len(request.FILES) == 0:
                messages.add_message(request, messages.INFO, 'Sin archivo excel')
                return redirect('coordinador_add')
            file = request.FILES['coordinador_excel']
                
            datos = pandas.read_excel(file)
            filas = len(datos)

            estudiante = []

            for i in range(filas):
                estudiante.append({'nombre':datos.iat[i,0],'correo':datos.iat[i,1],'rut':datos.iat[i,2],'dv':datos.iat[i,3]})

            for e in estudiante:
                nombre = e['nombre']
                email = e['correo']
                rut = str(e['rut'])
                dv = str(e['dv'])
                if (nombre == None or nombre == 'None' or nombre == 'nan' or 
                    email == None or email == 'None' or email == 'nan'or
                    rut == None or rut == 'None' or rut == 'nan' or 
                    dv == None or dv == 'None' or dv == 'nan'):
                    messages.add_message(request, messages.INFO, 'No se aceptan espacios ni campos vacios en el archivo Excel')
                    return redirect('coordinador_add')  
            
            for e in estudiante:
                nombre = e['nombre']
                email = e['correo']
                rut = str(e['rut'])
                dv = str(e['dv'])
                validation = rut+dv
                result=validarRut(validation)
                result2=validatename(nombre)

                if(validateEmail(email)==False):
                    messages.add_message(request, messages.INFO, 'El email: '+ email +' del usuario '+ nombre + ' no es valido')
                    continue
                if User.objects.filter(username = email).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el email: '+ email +' ya se encuentra registrado')
                    continue
                if Coordinador.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como coordinador')
                    continue
                if Docente.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como docente')
                    continue
                if Estudiante.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como estudiante')
                    continue
                
                if result==False:
                    messages.add_message(request, messages.INFO, 'El Rut: '+ rut+'-'+dv +' del usuario '+ nombre + ' no es valido')
                    continue
                if result2==False: 
                    messages.add_message(request, messages.INFO, 'El Nombre ingresado del usuario: '+ nombre + ' no es valido (solo nombres alfabeticos)')
                    continue

                contraseña=list(rut)
                contraseña2=list(reversed(contraseña))
                semipassw=[]
                for i in range (4):
                    semipassw.append(contraseña2[i])
                lpassw=list(reversed(semipassw))
                passw = "".join(lpassw)

                User_save = User(
                    first_name = nombre,
                    password = make_password(passw),
                    username=email,
                    email=email,
                    )

                User_save.save()
                user_id = User.objects.get(email=email)
                
                Profile_save = Profile(
                    token_app_session= "No",
                    group_id = 2,
                    user_id=User_save.id,
                )
                Profile_save.save()

                Coordinador_save = Coordinador(
                    user_id = user_id.id,
                    nombre = nombre,
                    rut = rut,
                    dv = dv,
                    email=email,
                )
                Coordinador_save.save()

                
                subject='Usuario creado en '+ settings.IP
                message="Se ha creado el usuario para " + str(nombre) + " \nPara iniciar sesión debe ingresar lo siguiente: \n1)Usuario: "+ email +"\n2)Clave: ultimos 4 digitos antes del dv\nPara iniciar sesión ingrese al siguiente enlace: "+str(settings.IP)+":7000/"
                email_from=settings.EMAIL_HOST_USER 
                recipient_list=[email]
                send_mail(subject,message,email_from,recipient_list)
            usuarios2 = Coordinador.objects.all().count()
            if usuarios2>usuarios1:
                messages.add_message(request, messages.INFO, 'Usuarios ingresados: ' + str(usuarios2-usuarios1))
            return redirect('coordinador_add')
        except ValueError:
                messages.add_message(request, messages.INFO, 'Error en los datos ingresados Value')
                return redirect('coordinador_add')
        except DataError:
            messages.add_message(request, messages.INFO, 'No se aceptan espacios ni campos vacios en el archivo Excel')
            return redirect('coordinador_add')
        except BaseException:
            messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
            return redirect('coordinador_add')
    else: 
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def coordinador_edit(request,coordinador_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        coordinador_data = Coordinador.objects.get(pk=coordinador_id)
        coordinador_user = User.objects.get(pk=coordinador_data.user_id)
        template_name = 'usuarios/coordinador_edit.html'
        return render(request,template_name,{'profile':profile,'template_name' : 'usuarios/coordinador_edit.html',
        'coordinador_data':coordinador_data,'coordinador_user':coordinador_user})
    except Coordinador.DoesNotExist:
        return redirect('coordinador_list')
    except BaseException:
        return redirect('coordinador_list')

@login_required
def coordinador_update(request,coordinador_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            email = request.POST.get('email')
        Coordinador.objects.get(pk=coordinador_id)
        coordinador=Coordinador.objects.get(pk=coordinador_id); 
        if (validatename(nombre)):
            Coordinador.objects.filter(pk=coordinador_id).update(nombre=nombre)
            User.objects.filter(pk=coordinador.user.id).update(first_name=nombre)
        else:
            messages.add_message(request, messages.INFO, 'Nombre no actualizado, no es un nombre valido')   
        if (validateEmail(email)):
            Coordinador.objects.filter(pk=coordinador_id).update(email=email)
            User.objects.filter(pk=coordinador.user.id).update(email=email)
            User.objects.filter(pk=coordinador.user.id).update(username=email)
        else:
            messages.add_message(request, messages.INFO, 'Correo no actualizado, no es un correo valido')
        return redirect('coordinador_edit',coordinador_id)
    except Coordinador.DoesNotExist:
        return redirect('coordinador_edit',coordinador_id)
    except ValueError:
        messages.add_message(request, messages.INFO, 'Error en los datos ingresados Value')
        return redirect('coordinador_edit',coordinador_id)
    # except BaseException:
    #     messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
    #     return redirect('coordinador_edit',coordinador_id)
        
@login_required
def coordinador_estado(request,coordinador_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:  
        coordinador = Coordinador.objects.get(pk=coordinador_id)
        state=User.objects.get(pk=coordinador.user_id) 
        if state.is_active == True:
            estado=False
            estado_des="desactivado"
            User.objects.filter(pk=coordinador.user_id).update(is_active=estado)
            Coordinador.objects.filter(pk=coordinador_id).update(estado=estado_des)
            messages.add_message(request, messages.INFO, 'coordinador desactivada(o)')
            return redirect('coordinador_edit',coordinador_id)
        elif state.is_active == False:
            estado=True
            estado_act="activo"
            User.objects.filter(pk=coordinador.user_id).update(is_active=estado)
            Coordinador.objects.filter(pk=coordinador_id).update(estado=estado_act)
            messages.add_message(request, messages.INFO, 'coordinador activada(o)')
            return redirect('coordinador_edit',coordinador_id)
        else: 
            messages.add_message(request, messages.INFO, 'Hubo un error en el proceso')
            return redirect('coordinador_edit',coordinador_id)
    except User.DoesNotExist: 
        messages.add_message(request, messages.INFO, 'El Usuario no existe')
        return redirect('coordinador_edit',coordinador_id)
    except Coordinador.DoesNotExist: 
        messages.add_message(request, messages.INFO, 'El Coordinador no existe')
        return redirect('coordinador_edit',coordinador_id)
    except BaseException: 
        messages.add_message(request, messages.INFO, 'Error, contacte con el administrador')
        return redirect('coordinador_edit',coordinador_id)

@login_required
def coordinador_delete(request,coordinador_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        coordinador = Coordinador.objects.get(pk=coordinador_id)
        user = User.objects.get(pk = coordinador.user_id)
        perfil =  Profile.objects.get(user_id = user.id)

        if profile.foto_perfil!="no-avatar.jpg":
            if os.path.isfile(profile.foto_perfil.path):
                os.remove(profile.foto_perfil.path)

        Coordinador.objects.filter(pk=coordinador.id).delete()
        Profile.objects.filter(user_id=request.user.id).update(foto_perfil="no-avatar.jpg")
        User.objects.filter(pk=user.id).delete()
        Profile.objects.filter(pk=perfil.id).delete()
        return redirect('coordinador_list')
    except Coordinador.DoesNotExist:
        return redirect('coordinador_list')

#Profesor
@login_required
def docente_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id==2:
        template_name = 'usuarios/docente_add.html'
        return render(request,template_name,{'profile':profile,'template_name' : 'usuarios/docente_add.html'})
    else: 
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def descargar_docente(request):
    pass
    BASE_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nombre_archivo = "excel_docentes.xlsx"
    ruta_archivo = BASE_dir + "/registro/templates/excel/" + nombre_archivo
    archivo = open(ruta_archivo, 'rb')
    tipo_mimetype = mimetypes.guess_type(ruta_archivo)
    response = HttpResponse(archivo, content_type=tipo_mimetype)
    response['Content-Disposition'] = "attachment; filename=%s" % nombre_archivo
    return response

@login_required
def docente_list(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id== 2:
        if page == None:
            page = request.GET.get('page')
        else:
            page = page
        if request.GET.get('page') == None:
            page = page
        else:
            page = request.GET.get('page')
        if search == None:
            search = request.GET.get('search')
        else:
            search = search
        if request.GET.get('search') == None:
            search = search
        else:
            search = request.GET.get('search')
        if request.method == 'POST':
            search = request.POST.get('search')
            page = None
        h_list = []
        h_count = Docente.objects.all().count()
        if search == None or search == "None" or search=="":
            h_list_array =Docente.objects.order_by('nombre')
            for h in h_list_array:
                perfil = Profile.objects.get(user_id=h.user_id)
                h_list.append({'id':h.id,'nombre':h.nombre,'rut':h.rut,'dv':h.dv,'email':h.email,'estado':h.estado,'perfil':perfil})
        else:
            h_list_array =Docente.objects.filter(rut__icontains=search).order_by('nombre')
            h_count = Docente.objects.filter(rut__icontains=search).count()
            for h in h_list_array:
                perfil = Profile.objects.get(user_id=h.user_id)
                h_list.append({'id':h.id,'nombre':h.nombre,'email':h.email,'rut':h.rut,'dv':h.dv,'estado':h.estado,'perfil':perfil})
        paginator = Paginator(h_list, 5)
        h_list_paginate= paginator.get_page(page)
        template_name = 'usuarios/docente_list.html'
        return render(request,template_name,{'profile':profile,'h_count':h_count,
        'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search,'template_name' : 'usuarios/docente_list.html'})
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def docente_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id== 2:
        try:
            usuarios1 = Docente.objects.all().count()
            if request.method == 'POST':
                cantidad = int(request.POST.get('cantidad'))
                t = int(1)
                while t <= cantidad:
                    nombre = 'nombre-'+str(t)
                    rut = 'rut-'+str(t)
                    dv = 'dv-'+str(t)
                    email = 'email-'+str(t)

                    nombre = request.POST.get(nombre)
                    rut = request.POST.get(rut)
                    dv = request.POST.get(dv)
                    email = request.POST.get(email)   
                
                    rutdv= rut+dv
                    validation=rutdv
                    result=validarRut(validation)
                    result2=validatename(nombre)

                    if User.objects.filter(username = email).count()>=1:
                        messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el email: '+ email +' ya se encuentra registrado')
                        t = t+1
                        continue
                    if Coordinador.objects.filter(rut = rut).count()>=1:
                        messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como coordinador')
                        t = t+1
                        continue
                    if Docente.objects.filter(rut = rut).count()>=1:
                        messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como docente')
                        t = t+1
                        continue
                    if Estudiante.objects.filter(rut = rut).count()>=1:
                        messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como estudiante')
                        t = t+1
                        continue
                    if result==False: #Resultado de rut
                        messages.add_message(request, messages.INFO, 'El Rut: '+ rut+'-'+dv +' del usuario '+ nombre + ' no es valido')
                        t = t+1
                        continue
                    if result2==False: 
                        messages.add_message(request, messages.INFO, 'El Nombre ingresado del usuario: '+ nombre + ' no es valido (solo nombres alfabeticos)')
                        t = t+1
                        continue

                    contraseña=list(rut)
                    contraseña2=list(reversed(contraseña))
                    semipassw=[]
                    for i in range (4):
                        semipassw.append(contraseña2[i])
                    lpassw=list(reversed(semipassw))
                    passw = "".join(lpassw)

                    User_save = User(
                        first_name = nombre,
                        password = make_password(passw),
                        username=email,
                        email=email,
                        )

                    User_save.save()
                    user_id = User.objects.get(email=email)

                    Profile_save = Profile(
                        token_app_session= "No",
                        group_id = 3,
                        user_id=user_id.id,
                    )
                    Profile_save.save()
                    
                    Docente_save = Docente(
                        user_id = user_id.id,
                        nombre = nombre,
                        rut = rut,
                        dv = dv,
                        email=email,
                    )
                    Docente_save.save()

                    subject='Usuario creado en '+ settings.IP
                    message="Se ha creado el usuario para " + str(nombre) + " \nPara iniciar sesión debe ingresar lo siguiente: \n1)Usuario: "+ email +"\n2)Clave: ultimos 4 digitos antes del dv\nPara iniciar sesión ingrese al siguiente enlace: "+str(settings.IP)+":7000/"
                    email_from=settings.EMAIL_HOST_USER 
                    recipient_list=[email]
                    send_mail(subject,message,email_from,recipient_list)

                    t = t+1
                usuarios2 = Docente.objects.all().count()
                if usuarios2>usuarios1:
                    messages.add_message(request, messages.INFO, 'Usuarios ingresados: ' + str(usuarios2-usuarios1))
                return redirect('docente_add')
            else:
                messages.add_message(request, messages.INFO, 'Error en el método de envío')
                return redirect('check_group_main')
        except ValueError:
            messages.add_message(request, messages.INFO, 'Error en los datos ingresados Value')
            return redirect('docente_add')
        except BaseException:
            messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
            return redirect('docente_add')
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def docente_load_save(request):
    from django.contrib.auth.hashers import make_password,check_password
    from registro.models import Coordinador,Docente,Estudiante
    from django.core.mail import send_mail
    
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id==2:
        try:
            usuarios1 = Docente.objects.all().count()
            
            if len(request.FILES) == 0:
                messages.add_message(request, messages.INFO, 'Sin archivo excel')
                return redirect('docente_add')
            file = request.FILES['docente_excel']
            datos = pandas.read_excel(file)
            filas = len(datos)

            estudiante = []

            for i in range(filas):
                estudiante.append({'nombre':datos.iat[i,0],'correo':datos.iat[i,1],'rut':datos.iat[i,2],'dv':datos.iat[i,3]})
            for e in estudiante:
                nombre = e['nombre']
                email = e['correo']
                rut = str(e['rut'])
                dv = str(e['dv'])
                if (nombre == None or nombre == 'None' or nombre == 'nan' or 
                    email == None or email == 'None' or email == 'nan'or
                    rut == None or rut == 'None' or rut == 'nan' or 
                    dv == None or dv == 'None' or dv == 'nan'):
                    messages.add_message(request, messages.INFO, 'No se aceptan espacios ni campos vacios en el archivo Excel')
                    return redirect('coordinador_add')          
            for e in estudiante:
                nombre = e['nombre']
                email = e['correo']
                rut = str(e['rut'])
                dv = str(e['dv'])
                validation = rut+dv
                result=validarRut(validation)
                result2=validatename(nombre)

                if(validateEmail(email)==False):
                    messages.add_message(request, messages.INFO, 'El email: '+ email +' del usuario '+ nombre + ' no es valido')
                    continue
                if User.objects.filter(username = email).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el email: '+ email +' ya se encuentra registrado')
                    continue
                if Coordinador.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como coordinador')
                    continue
                if Docente.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como docente')
                    continue
                if Estudiante.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como estudiante')
                    continue
                
                if result==False:
                    messages.add_message(request, messages.INFO, 'El Rut: '+ rut+'-'+dv +' del usuario '+ nombre + ' no es valido')
                    continue
                if result2==False: 
                    messages.add_message(request, messages.INFO, 'El Nombre ingresado del usuario: '+ nombre + ' no es valido (solo nombres alfabeticos)')
                    continue

                contraseña=list(rut)
                contraseña2=list(reversed(contraseña))
                semipassw=[]
                for i in range (4):
                    semipassw.append(contraseña2[i])
                lpassw=list(reversed(semipassw))
                passw = "".join(lpassw)

                User_save = User(
                    first_name = nombre,
                    password = make_password(passw),
                    username=email,
                    email=email,
                    )

                User_save.save()
                user_id = User.objects.get(email=email)

                Profile_save = Profile(
                    token_app_session= "No",
                    group_id = 3,
                    user_id=user_id.id,
                )
                Profile_save.save()
                
                Docente_save = Docente(
                    user_id = user_id.id,
                    nombre = nombre,
                    rut = rut,
                    dv = dv,
                    email=email,
                )
                Docente_save.save()

                subject='Usuario creado en '+ settings.IP
                message="Se ha creado el usuario para " + str(nombre) + " \nPara iniciar sesión debe ingresar lo siguiente: \n1)Usuario: "+ email +"\n2)Clave: ultimos 4 digitos antes del dv\nPara iniciar sesión ingrese al siguiente enlace: "+str(settings.IP)+":7000/"
                email_from=settings.EMAIL_HOST_USER 
                recipient_list=[email]
                send_mail(subject,message,email_from,recipient_list)
            usuarios2 = Docente.objects.all().count()
            if usuarios2>usuarios1:
                messages.add_message(request, messages.INFO, 'Usuarios ingresados: ' + str(usuarios2-usuarios1))
            return redirect('docente_add')
        except ValueError:
                messages.add_message(request, messages.INFO, 'Error en los datos ingresados Value')
                return redirect('docente_add')
        except DataError:
            messages.add_message(request, messages.INFO, 'No se aceptan espacios ni campos vacios en el archivo Excel')
            return redirect('docente_add')
        except BaseException:
            messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
            return redirect('docente_add')
    else: 
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def docente_edit(request,docente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    try:
        if profile.group_id == 1 or profile.group_id== 2:
            template_name = 'usuarios/docente_edit.html'
            docente_data = Docente.objects.get(pk=docente_id)
            docente_user = User.objects.get(pk=docente_data.user_id)
            return render(request,template_name,{'profile':profile,'template_name' : 'usuarios/docente_edit.html',
            'docente_data':docente_data,'docente_user':docente_user})
        else:
            messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
            return redirect('check_group_main')
    except Docente.DoesNotExist:
        return redirect('docente_list')
    except BaseException:
        return redirect('docente_list')

@login_required
def docente_update(request,docente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    try:
        if profile.group_id == 1 or profile.group_id== 2:
            if request.method == 'POST':
                nombre = request.POST.get('nombre')
                email = request.POST.get('email')
            Docente.objects.get(pk=docente_id)
            docente = Docente.objects.get(pk=docente_id)
            if (validatename(nombre)):
                Docente.objects.filter(pk=docente_id).update(nombre=nombre)
                User.objects.filter(pk=docente.user.id).update(first_name=nombre)
            else:
                messages.add_message(request, messages.INFO, 'Nombre no actualizado, no es un nombre valido')   
            if (validateEmail(email)):
                Docente.objects.filter(pk=docente_id).update(email=email)
                User.objects.filter(pk=docente.user.id).update(email=email)
                User.objects.filter(pk=docente.user.id).update(username=email)
            else:
                messages.add_message(request, messages.INFO, 'Correo no actualizado, no es un correo valido')
            return redirect('docente_edit',docente_id)
        else:
            messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
            return redirect('check_group_main')
    except Docente.DoesNotExist:
        return redirect('docente_edit',docente_id)
    except ValueError:
        return redirect('docente_edit',docente_id)
    except BaseException:
        return redirect('docente_edit',docente_id)


@login_required
def docente_estado(request,docente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id== 2:
        try:  
            docente = Docente.objects.get(pk=docente_id)
            state=User.objects.get(pk=docente.user_id) 
            if state.is_active == True:
                estado=False
                estado_des="desactivado"
                User.objects.filter(pk=docente.user_id).update(is_active=estado)
                Docente.objects.filter(pk=docente_id).update(estado=estado_des)
                messages.add_message(request, messages.INFO, 'docente desactivada(o)')
                return redirect('docente_edit',docente_id)
            elif state.is_active == False:
                estado=True
                estado_act="activo"
                User.objects.filter(pk=docente.user_id).update(is_active=estado)
                Docente.objects.filter(pk=docente_id).update(estado=estado_act)
                messages.add_message(request, messages.INFO, 'docente activada(o)')
                return redirect('docente_edit',docente_id)
            else: 
                messages.add_message(request, messages.INFO, 'Hubo un error en el proceso')
                return redirect('docente_edit',docente_id)
        except User.DoesNotExist:
            messages.add_message(request, messages.INFO, 'El Usuario no existe')
            return redirect('docente_edit',docente_id)
        except Docente.DoesNotExist:
            messages.add_message(request, messages.INFO, 'El Docente no existe')
            return redirect('docente_edit',docente_id)
        except BaseException: 
            messages.add_message(request, messages.INFO, 'Error, contacte con el administrador')
            return redirect('docente_edit',docente_id)
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def docente_delete(request,docente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    try:
        if profile.group_id == 1 or profile.group_id== 2:
            docente = Docente.objects.get(pk=docente_id)
            user = User.objects.get(pk = docente.user_id)
            perfil =  Profile.objects.get(user_id = user.id)

        
            if profile.foto_perfil!="no-avatar.jpg":
                if os.path.isfile(profile.foto_perfil.path):
                    os.remove(profile.foto_perfil.path)

            Docente.objects.filter(pk=docente.id).delete()
            Profile.objects.filter(user_id=request.user.id).update(foto_perfil="no-avatar.jpg")
            User.objects.filter(pk=user.id).delete()
            Profile.objects.filter(pk=perfil.id).delete()
            return redirect('docente_list')
        else:
            messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
            return redirect('check_group_main')
    except Docente.DoesNotExist:
        return redirect('docente_list')
    except BaseException:
        return redirect('docente_list')
        

#Estudiante
@login_required
def estudiante_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id== 2:
        template_name = 'usuarios/estudiante_add.html'
        pythonfile = 'excel_estudiantes.xlsx'
        excel_estudiantes = os.path.abspath(pythonfile)
        
        return render(request,template_name,{'profile':profile,'template_name' : 'usuarios/estudiante_add.html','excel_estudiantes':excel_estudiantes})
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def descargar_estudiante(request):
    pass
    BASE_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nombre_archivo = "excel_estudiantes.xlsx"
    ruta_archivo = BASE_dir + "/registro/templates/excel/" + nombre_archivo
    archivo = open(ruta_archivo, 'rb')
    tipo_mimetype = mimetypes.guess_type(ruta_archivo)
    response = HttpResponse(archivo, content_type=tipo_mimetype)
    response['Content-Disposition'] = "attachment; filename=%s" % nombre_archivo
    return response

@login_required
def estudiante_list(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id== 2:
        if page == None:
            page = request.GET.get('page')
        else:
            page = page
        if request.GET.get('page') == None:
            page = page
        else:
            page = request.GET.get('page')
        if search == None:
            search = request.GET.get('search')
        else:
            search = search
        if request.GET.get('search') == None:
            search = search
        else:
            search = request.GET.get('search')
        if request.method == 'POST':
            search = request.POST.get('search')
            page = None
        h_list = []
        h_count = Estudiante.objects.all().count()
        if search == None or search == "None" or search=="":
            h_list_array =Estudiante.objects.order_by('nombre')
            for h in h_list_array:
                perfil = Profile.objects.get(user_id=h.user_id)
                h_list.append({'id':h.id,'nombre':h.nombre,'email':h.email,'rut':h.rut,'dv':h.dv,'perfil':perfil})
        else:
            h_list_array = Estudiante.objects.filter(rut__icontains=search).order_by('nombre')
            h_count =Estudiante.objects.filter(rut__icontains=search).count()
            for h in h_list_array:
                perfil = Profile.objects.get(user_id=h.user_id)
                h_list.append({'id':h.id,'nombre':h.nombre,'email':h.email,'rut':h.rut,'dv':h.dv,'perfil':perfil})
        paginator = Paginator(h_list, 5)
        h_list_paginate= paginator.get_page(page)
        template_name = 'usuarios/estudiante_list.html'
        return render(request,template_name,{'profile':profile,'h_count':h_count,
        'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search,'template_name' : 'usuarios/estudiante_list.html'})
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def estudiante_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id== 2:
        try:
            usuarios1 = Estudiante.objects.all().count()
            if request.method == 'POST':
                cantidad = int(request.POST.get('cantidad'))
                t = int(1)
                
                while t <= cantidad:
                    nombre = 'nombre-'+str(t)
                    rut = 'rut-'+str(t)
                    dv = 'dv-'+str(t)
                    email = 'email-'+str(t)

                    nombre = request.POST.get(nombre)
                    rut = request.POST.get(rut)
                    dv = request.POST.get(dv)
                    email = request.POST.get(email)   
                
                    validation = rut+dv
                    result=validarRut(validation)
                    result2=validatename(nombre)

                    if(validateEmail(email)==False):
                        messages.add_message(request, messages.INFO, 'El email: '+ email +' del usuario '+ nombre + ' no es valido')
                        t = t+1
                        continue
                    if User.objects.filter(username = email).count()>=1:
                        messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el email: '+ email +' ya se encuentra registrado')
                        t = t+1
                        continue
                    if Coordinador.objects.filter(rut = rut).count()>=1:
                        messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como coordinador')
                        t = t+1
                        continue
                    if Docente.objects.filter(rut = rut).count()>=1:
                        messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como docente')
                        t = t+1
                        continue
                    if Estudiante.objects.filter(rut = rut).count()>=1:
                        messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como estudiante')
                        t = t+1
                        continue
                    if result==False: #Resultado de rut
                        messages.add_message(request, messages.INFO, 'El Rut: '+ rut+'-'+dv +' del usuario '+ nombre + ' no es valido')
                        t = t+1
                        continue
                    if result2==False: 
                        messages.add_message(request, messages.INFO, 'El Nombre ingresado del usuario: '+ nombre + ' no es valido (solo nombres alfabeticos)')
                        t = t+1
                        continue

                    contraseña=list(rut)
                    contraseña2=list(reversed(contraseña))
                    semipassw=[]
                    for i in range (4):
                        semipassw.append(contraseña2[i])
                    lpassw=list(reversed(semipassw))
                    passw = "".join(lpassw)

                    User_save = User(
                        first_name = nombre,
                        password = make_password(passw),
                        username=email,
                        email=email,
                        )

                    User_save.save()
                    user_id = User.objects.get(email=email)
   
                    Profile_save = Profile(
                        token_app_session= "No",
                        group_id = 4,
                        user_id=user_id.id,
                    )
                    Profile_save.save()
                    
                    Estudiante_save = Estudiante(
                        user_id = user_id.id,
                        nombre = nombre,
                        rut = rut,
                        dv = dv,
                        email=email,
                    )

                    Estudiante_save.save()

                    subject='Usuario creado en '+ settings.IP
                    message="Se ha creado el usuario para " + str(nombre) + " \nPara iniciar sesión debe ingresar lo siguiente: \n1)Usuario: "+ email +"\n2)Clave: ultimos 4 digitos antes del dv\nPara iniciar sesión ingrese al siguiente enlace: "+str(settings.IP)+":7000/"
                    email_from=settings.EMAIL_HOST_USER 
                    recipient_list=[email]
                    send_mail(subject,message,email_from,recipient_list)

                    t = t+1
                usuarios2 = Estudiante.objects.all().count()
                if usuarios2>usuarios1:
                    messages.add_message(request, messages.INFO, 'Usuarios ingresados: ' + str(usuarios2-usuarios1))
                return redirect('estudiante_add')
            else:
                messages.add_message(request, messages.INFO, 'Error en el método de envío')
                return redirect('check_group_main')
        except ValueError:
            messages.add_message(request, messages.INFO, 'Error en los datos ingresados Value')
            return redirect('estudiante_add')
        except BaseException:
            messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
            return redirect('estudiante_add')
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def estudiante_load_save(request):
    from django.contrib.auth.hashers import make_password,check_password
    from registro.models import Coordinador,Docente,Estudiante
    from django.core.mail import send_mail
    
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id==2:
        try:
            usuarios1 = Estudiante.objects.all().count()
            if len(request.FILES) == 0:
                messages.add_message(request, messages.INFO, 'Sin archivo excel')
                return redirect('estudiante_add')

            file = request.FILES['estudiante_excel']
            
            datos = pandas.read_excel(file)
            filas = len(datos)

            estudiante = []

            for i in range(filas):
                estudiante.append({'nombre':datos.iat[i,0],'correo':datos.iat[i,1],'rut':datos.iat[i,2],'dv':datos.iat[i,3]})

            for e in estudiante:
                nombre = e['nombre']
                email = e['correo']
                rut = str(e['rut'])
                dv = str(e['dv'])
                if (nombre == None or nombre == 'None' or nombre == 'nan' or 
                    email == None or email == 'None' or email == 'nan'or
                    rut == None or rut == 'None' or rut == 'nan' or 
                    dv == None or dv == 'None' or dv == 'nan'):
                    messages.add_message(request, messages.INFO, 'No se aceptan espacios ni campos vacios en el archivo Excel')
                    return redirect('estudiante_add') 

            for e in estudiante:
                nombre = e['nombre']
                email = e['correo']
                rut = str(e['rut'])
                dv = str(e['dv'])
                validation = rut+dv
                result=validarRut(validation)
                result2=validatename(nombre)

                if(validateEmail(email)==False):
                    messages.add_message(request, messages.INFO, 'El email: '+ email +' del usuario '+ nombre + ' no es valido')
                    continue
                if User.objects.filter(username = email).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el email: '+ email +' ya se encuentra registrado')
                    continue
                if Coordinador.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como coordinador')
                    continue
                if Docente.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como docente')
                    continue
                if Estudiante.objects.filter(rut = rut).count()>=1:
                    messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como estudiante')
                    continue
                
                if result==False:
                    messages.add_message(request, messages.INFO, 'El Rut: '+ rut+'-'+dv +' del usuario '+ nombre + ' no es valido')
                    continue
                if result2==False: 
                    messages.add_message(request, messages.INFO, 'El Nombre ingresado del usuario: '+ nombre + ' no es valido (solo nombres alfabeticos)')
                    continue

                contraseña=list(rut)
                contraseña2=list(reversed(contraseña))
                semipassw=[]
                for i in range (4):
                    semipassw.append(contraseña2[i])
                lpassw=list(reversed(semipassw))
                passw = "".join(lpassw)

                User_save = User(
                    first_name = nombre,
                    password = make_password(passw),
                    username=email,
                    email=email,
                    )

                User_save.save()
                user_id = User.objects.get(email=email)

                Profile_save = Profile(
                    token_app_session= "No",
                    group_id = 4,
                    user_id=user_id.id,
                )
                Profile_save.save()
                
                Estudiante_save = Estudiante(
                    user_id = user_id.id,
                    nombre = nombre,
                    rut = rut,
                    dv = dv,
                    email=email,
                )

                Estudiante_save.save()

                subject='Usuario creado en '+ settings.IP
                message="Se ha creado el usuario para " + str(nombre) + " \nPara iniciar sesión debe ingresar lo siguiente: \n1)Usuario: "+ email +"\n2)Clave: ultimos 4 digitos antes del dv\nPara iniciar sesión ingrese al siguiente enlace: "+str(settings.IP)+":7000/"
                email_from=settings.EMAIL_HOST_USER 
                recipient_list=[email]
                send_mail(subject,message,email_from,recipient_list)
            usuarios2 = Estudiante.objects.all().count()
            if usuarios2>usuarios1:
                messages.add_message(request, messages.INFO, 'Usuarios ingresados: ' + str(usuarios2-usuarios1))
            return redirect('estudiante_add')
        except ValueError:
            messages.add_message(request, messages.INFO, 'Error en los datos ingresados Value')
            return redirect('estudiante_add')
        except DataError:
            messages.add_message(request, messages.INFO, 'No se aceptan espacios ni campos vacios en el archivo Excel')
            return redirect('estudiante_add')
        except BaseException:
            messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
            return redirect('estudiante_add')
    else: 
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def estudiante_edit(request,estudiante_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id== 2: 
        try:
            template_name = 'usuarios/estudiante_edit.html'
            estudiante_data = Estudiante.objects.get(pk=estudiante_id)
            estudiante_user = User.objects.get(pk=estudiante_data.user_id)
            return render(request,template_name,{'profile':profile,'template_name' : 'usuarios/estudiante_edit.html',
            'estudiante_data':estudiante_data,'estudiante_user':estudiante_user})
        except Estudiante.DoesNotExist:
            return redirect('estudiante_list')
        except BaseException: 
            messages.add_message(request, messages.INFO, 'Error, contacte con el administrador')
            return redirect('estudiante_list')
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')  

@login_required
def estudiante_update(request,estudiante_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id== 2:
        try:
            if request.method == 'POST':
                nombre = request.POST.get('nombre')
                email = request.POST.get('email')
                estado = request.POST.get('estado')
            Estudiante.objects.get(pk=estudiante_id)
            estudiante = Estudiante.objects.get(pk=estudiante_id)
            if (validatename(nombre)):
                Estudiante.objects.filter(pk=estudiante_id).update(nombre=nombre)
                User.objects.filter(pk=estudiante.user.id).update(first_name=nombre)
            else:
                messages.add_message(request, messages.INFO, 'Nombre no actualizado, no es un nombre valido')   
            if (validateEmail(email)):
                Estudiante.objects.filter(pk=estudiante_id).update(email=email)
                User.objects.filter(pk=estudiante.user.id).update(email=email)
                User.objects.filter(pk=estudiante.user.id).update(username=email)
            else:
                messages.add_message(request, messages.INFO, 'Correo no actualizado, no es un correo valido')
            return redirect('estudiante_edit',estudiante_id)
        except Estudiante.DoesNotExist: 
            return redirect('estudiante_list')
        except BaseException: 
            messages.add_message(request, messages.INFO, 'Error, contacte con el administrador')
            return redirect('estudiante_list')
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def estudiante_estado(request,estudiante_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1 or profile.group_id== 2:
        try:  
            estudiante = Estudiante.objects.get(pk=estudiante_id)
            state=User.objects.get(pk=estudiante.user_id) 
            if state.is_active == True:
                estado=False
                estado_des="desactivado"
                User.objects.filter(pk=estudiante.user_id).update(is_active=estado)
                Estudiante.objects.filter(pk=estudiante_id).update(estado=estado_des)
                messages.add_message(request, messages.INFO, 'Estudiante desactivada(o)')
                return redirect('estudiante_edit',estudiante_id)
            elif state.is_active == False:
                estado=True
                estado_act="activo"
                User.objects.filter(pk=estudiante.user_id).update(is_active=estado)
                Estudiante.objects.filter(pk=estudiante_id).update(estado=estado_act)
                messages.add_message(request, messages.INFO, 'Estudiante activada(o)')
                return redirect('estudiante_edit',estudiante_id)
            else: 
                messages.add_message(request, messages.INFO, 'Hubo un error en el proceso')
                return redirect('estudiante_edit',estudiante_id)
        except Estudiante.DoesNotExist: 
            messages.add_message(request, messages.INFO, 'El Usuario no existe')
            return redirect('estudiante_edit',estudiante_id)
        except BaseException: 
            messages.add_message(request, messages.INFO, 'Error, contacte con el administrador')
            return redirect('estudiante_edit',estudiante_id)
    else:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

@login_required
def estudiante_delete(request,estudiante_id):
    profile = Profile.objects.get(user_id=request.user.id)
    try:
        if profile.group_id == 1 or profile.group_id== 2:
            estudiante = Estudiante.objects.get(pk=estudiante_id)
            user = User.objects.get(pk = estudiante.user_id)
            perfil =  Profile.objects.get(user_id = user.id)

            if profile.foto_perfil!="no-avatar.jpg":
                if os.path.isfile(profile.foto_perfil.path):
                    os.remove(profile.foto_perfil.path)

            Estudiante.objects.filter(pk=estudiante.id).delete()
            Profile.objects.filter(user_id=request.user.id).update(foto_perfil="no-avatar.jpg")
            User.objects.filter(pk=user.id).delete()
            Profile.objects.filter(pk=perfil.id).delete()
            return redirect('estudiante_list')
        else:
            messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
            return redirect('check_group_main')
    except Estudiante.DoesNotExist:
        return redirect('estudiante_list')

'''
def admin_dash(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.id != 1:
        messages.add_message(request,messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    docente_data = Docente.objects.all().order_by('-id')[5]
    coordinador_data = Coordinador.objects.all().order_by('-id')[5]
    estudiante_data = Estudiante.objects.all().orden_by('-id')[5]

    docente_count = Docente.objects.all().count()
    coordinador_count = Coordinador.objects.all().count()
    estudiante_count = Estudiante.objects.all().count()
    return redirect(request,template_name,{'profile':profile,'template_name':template_name,'docente_data':docente_data,'estudiante_data':estudiante_data,
    'docente_count':docente_count,'coordinador_data':coordinador_data,'estudiante_count':estudiante_count,'coordinador_count':coordinador_count})

def coordinador_dash(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.id != 2:
        messages.add_message(request,messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    docente_data = Docente.objects.all().order_by('-id')[5]
    estudiante_data = Estudiante.objects.all().orden_by('-id')[5]

    docente_count = Docente.objects.all().count()
    estudiante_count = Estudiante.objects.all().count()

    fichas_count = Detalle_atencion.objects.all().count()
    fichas_data = Detalle_atencion.objects.all().order_by('-id')[-5]
    
    return render(request,template_name,{'profile':profile,'template_name':template_name,'docente_data':docente_data,'estudiante_data':estudiante_data,
    'docente_count':docente_count,'estudiante_count':estudiante_count,'fichas_count':fichas_count,'fichas_data':fichas_data})



def docente_dash(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.id != 3:
        messages.add_message(request,messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    template_name = ''
    return render(request,template_name,{'profile':profile,'template_name':template_name})




def alumnos_dash(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.id != 4:
        messages.add_message(request,messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    template_name = ''
    return render(request,template_name,{'profile':profile,'template_name':template_name})

'''