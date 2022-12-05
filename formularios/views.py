from email.headerregistry import Group
from django.shortcuts import render
from registro.models import Paciente,Discapacidad,Profile,User,Estudiante
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date
from formularios.models import Formulario_alimentario,Formulario_satisfaccion
from nutricion.models import Detalle_atencion
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.

@login_required
def encuesta_alimentaria(request,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        Detalle_atencion.objects.get(pk=ficha_id)
        if Formulario_alimentario.objects.filter(ficha_id=ficha_id).count() >= 1:
            return redirect('ficha_list')
        template_name = 'formularios/encuesta_alimentaria.html'
        return render(request,template_name,{'profile':profile,'ficha_id':ficha_id})
    except Detalle_atencion.DoesNotExist:
        return redirect('ficha_list')
    except BaseException:
        return redirect('ficha_list')

@login_required
def encuesta_save(request,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        alimentos = [
            'Pan Corriente',
            'Pan Integral',
            'Arroz',
            'Pastas',
            'Legumbres',
            'Papas cocidas',
            'Papas fritas',
            'Choclo',
            'Verduras',
            'Frutas',
            'Carne de cerdo',
            'Carne de ave y pavo',
            'Carne de vacuno',
            'Pescados',
            'Mariscos',
            'Huevos',
            'Leche entera',
            'Leche semi',
            'Leche descremada',
            'Yogurt',
            'Quesos amarillos', 
            'Queso chacra o Quesillo',
            'Aceite',
            'Aceite de oliva',
            'Embutidos',
            'Cecinas',
            'Enlatados o conservas',
            'Pasteles',
            'Snacks salados',
            'Snacks dulces',
            'Azúcar',
            'Sal',
            'Bebidas azúcaras',
            'Otros que no aparezca']

        i = 0
        
        while i < len(alimentos):
            alimento=alimentos[i]
            frecuencia = 'frecuencia-'+str(i)
            cantidad = 'cantidad-'+str(i)
            comentario = 'comentario-'+str(i)

            if request.POST.get(frecuencia) == None:
                frecuencia = 'Nunca'
            else:
                frecuencia = request.POST.get(frecuencia)
            
            if request.POST.get(cantidad) == None:
                cantidad = '0'
            else:
                cantidad = request.POST.get(cantidad)
            
            if request.POST.get(comentario) == None:
                comentario = 'Sin comentarios'
            else:
                comentario = request.POST.get(comentario)
            
            Formulario_save = Formulario_alimentario(
                ficha_id = ficha_id,
                alimento = alimento,
                frecuencia = frecuencia,
                cantidad = cantidad,
                comentario = comentario,
            )
            Formulario_save.save()
            i = i+1
        
        return redirect('ficha_list')
    else:
        messages.add_message(request,messages.INFO, 'El metodo recibido no es POST')
        return redirect('formularios/encuesta_alimentaria.html')

@login_required
def encuesta_ver(request,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        detalle=Detalle_atencion.objects.get(pk=ficha_id)
        paciente_id = detalle.paciente_id
        formulario_array = Formulario_alimentario.objects.filter(ficha_id=ficha_id).all()
        if len(formulario_array) <= 0:
            return redirect('encuesta_alimentaria',ficha_id)
        template_name = 'formularios/encuesta_alimentaria_ver.html'
        return render(request,template_name, {'profile':profile,'formulario_array':formulario_array,'paciente_id':paciente_id})
    except Detalle_atencion.DoesNotExist:
        return redirect('ficha_list')
    # except BaseException:
    #     return redirect('ficha_list')

def encuesta_satisfaccion_token(request,ficha_id):
    token_generator = PasswordResetTokenGenerator()
    ficha = Detalle_atencion.objects.get(pk=ficha_id)
    paciente = Paciente.objects.get(pk=ficha.paciente_id)
    estudiante = Estudiante.objects.get(pk=ficha.estudiante_id)
    
    user = User.objects.get(pk = estudiante.user_id)
    token = token_generator.make_token(user)

    subject='Encuesta de satisfacción'
    message=str(settings.IP)+":7000/formularios/encuesta_satisfaccion/" + str(token) + "/"
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[paciente.email]
    send_mail(subject,message,email_from,recipient_list)

    Profile.objects.filter(user_id = user.id).update(token_app_session = token)

    return redirect('encuesta_alimentaria',ficha_id)

def validatetoken( token ):
    profile = Profile.objects.all()
    estado = False
    for p in profile:
        if p.token_app_session == token:
            return True
        else:
            pass
    
    if estado == False:
        return False

def encuesta_satisfaccion_add(request,token):
    if validatetoken (token):
        prof = Profile.objects.get(token_app_session = token)
        estudiante = Estudiante.objects.get(user_id=prof.user_id)
        template_name = 'formularios/encuesta_satisfaccion.html'
        return render(request,template_name,{'estudiante_data': estudiante,'token':token})
    else:
        print("token invalido")
        return redirect('login')

def encuesta_satisfaccion_save(request,token):
    if validatetoken (token):
        prof = Profile.objects.get(token_app_session = token)
        estudiante = Estudiante.objects.get(user_id=prof.user_id)
        satisfaccion = request.POST.get('satisfaccion')
        satisfaccion_save = Formulario_satisfaccion(
            estudiante_id = estudiante.id,
            satisfaccion = satisfaccion,
        )
        satisfaccion_save.save()
        Profile.objects.filter(pk = prof.id).update(token_app_session = "No")
        return redirect('encuesta_satisfaccion_add',token)
    else:
        print("token invalido")
        return redirect('login')
        
        
    