from django.shortcuts import render,redirect
from registro.models import Profile
from django.contrib.auth.decorators import login_required
from nutricion.models import Solicitud, Detalle_atencion
from registro.models import Coordinador,Docente,Estudiante, Paciente

# Create your views here.
@login_required
def home(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 1:
        if Coordinador.objects.all().count() < 5:
            coordinador_data = Coordinador.objects.all().order_by('-id')
        else:
            coordinador_data = Coordinador.objects.all().order_by('-id')[:5]

        if Docente.objects.all().count() < 5:
            docente_data = Docente.objects.all().order_by('-id')
        else:
            docente_data = Docente.objects.all().order_by('-id')[:5]

        if Estudiante.objects.all().count() < 5:
            estudiante_data = Estudiante.objects.all().order_by('-id')
        else:
            estudiante_data = Estudiante.objects.all().order_by('-id')[:5]
        
        docente_count = Docente.objects.all().count()
        coordinador_count = Coordinador.objects.all().count()
        estudiante_count = Estudiante.objects.all().count()
        template_name = 'paginaweb/inicio.html'
        return render(request,template_name,{'profile':profile,'template_name':template_name,
        'docente_data':docente_data,'estudiante_data':estudiante_data,
        'docente_count':docente_count,'coordinador_data':coordinador_data,
        'estudiante_count':estudiante_count,'coordinador_count':coordinador_count})


    if profile.group_id == 2:
        if Docente.objects.all().count() < 5:
            docente_data = Docente.objects.all().order_by('-id')
        else:
            docente_data = Docente.objects.all().order_by('-id')[:5]

        if Estudiante.objects.all().count() < 5:
            estudiante_data = Estudiante.objects.all().order_by('-id')
        else:
            estudiante_data = Estudiante.objects.all().order_by('-id')[:5]

        if Detalle_atencion.objects.all().count() < 5:
            fichas_data = Detalle_atencion.objects.all().order_by('-id')
        else:
            fichas_data = Detalle_atencion.objects.all().order_by('-id')[:5]

        if Solicitud.objects.all().count() < 5:
            solicitud_data = Solicitud.objects.all().order_by('-id')
        else:
            solicitud_data = Solicitud.objects.all().order_by('-id')[:5]
        
        if Paciente.objects.all().count() < 5:
            paciente_data = Paciente.objects.all().order_by('-id')
        else:
            paciente_data = Paciente.objects.all().order_by('-id')[:5]

        paciente_count = Paciente.objects.all().count()
        docente_count = Docente.objects.all().count()
        estudiante_count = Estudiante.objects.all().count()
        fichas_count = Detalle_atencion.objects.all().count()
        solicitud_count = Solicitud.objects.all().count()

        template_name = 'paginaweb/inicio.html'
        return render(request,template_name,{'profile':profile,'template_name':template_name,
        'docente_data':docente_data,'estudiante_data':estudiante_data,
        'docente_count':docente_count,'estudiante_count':estudiante_count,'fichas_count':fichas_count,
        'fichas_data':fichas_data,'solicitud_data':solicitud_data,'solicitud_count':solicitud_count})


    if profile.group_id == 3:
        if Estudiante.objects.all().count() < 5:
            estudiante_data = Estudiante.objects.all().order_by('-id')
        else:
            estudiante_data = Estudiante.objects.all().order_by('-id')[:5]

        if Detalle_atencion.objects.all().count() < 5:
            fichas_data = Detalle_atencion.objects.all().order_by('-id')
        else:
            fichas_data = Detalle_atencion.objects.all().order_by('-id')[:5]

        if Solicitud.objects.all().count() < 5:
            solicitud_data = Solicitud.objects.all().order_by('-id')
        else:
            solicitud_data = Solicitud.objects.all().order_by('-id')[:5]
        
        if Paciente.objects.all().count() < 5:
            paciente_data = Paciente.objects.all().order_by('-id')
        else:
            paciente_data = Paciente.objects.all().order_by('-id')[:5]


        paciente_count = Paciente.objects.all().count()
        estudiante_count = Estudiante.objects.all().count()
        fichas_count = Detalle_atencion.objects.all().count()
        solicitud_count = Solicitud.objects.all().count()

        template_name = 'paginaweb/inicio.html'
        return render(request,template_name,{'profile':profile,'estudiante_data':estudiante_data,
        'estudiante_count':estudiante_count,'fichas_count':fichas_count,
        'fichas_data':fichas_data,'solicitud_data':solicitud_data,'solicitud_count':solicitud_count,
        'paciente_count':paciente_count,'paciente_data':paciente_data})

        
    if profile.group_id == 4:
        if Detalle_atencion.objects.all().count() < 5:
            fichas_data = Detalle_atencion.objects.all().order_by('-id')
        else:
            fichas_data = Detalle_atencion.objects.all().order_by('-id')[:5]

        if Solicitud.objects.all().count() < 5:
            solicitud_data = Solicitud.objects.all().order_by('-id')
        else:
            solicitud_data = Solicitud.objects.all().order_by('-id')[:5]
        
        if Paciente.objects.all().count() < 5:
            paciente_data = Paciente.objects.all().order_by('-id')
        else:
            paciente_data = Paciente.objects.all().order_by('-id')[:5]

        paciente_count = Paciente.objects.all().count()
        fichas_count = Detalle_atencion.objects.all().count()
        solicitud_count = Solicitud.objects.all().count()

        template_name = 'paginaweb/inicio.html'
        return render(request,template_name,{'profile':profile,
        'fichas_count':fichas_count,'fichas_data':fichas_data,'solicitud_data':solicitud_data,
        'solicitud_count':solicitud_count,'paciente_count':paciente_count,'paciente_data':paciente_data})