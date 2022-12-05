from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
from registro.models import Profile
from django.contrib import messages
from registro.models import Coordinador,Docente,Estudiante, Paciente,Disciplina,Discapacidad
from nutricion.models import Solicitud, Detalle_atencion
from formularios.models import  Formulario_satisfaccion
from datetime import datetime

@login_required
def export_pdf(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    context = {'profile':profile}
    html = render_to_string("reportes/pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"

    HTML(string=html).write_pdf(response)

    return response

@login_required
def ficha_pdf(request,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    ficha = Detalle_atencion.objects.get(pk=ficha_id)
    estudiante = Estudiante.objects.get(pk=ficha.estudiante_id)
    paciente = Paciente.objects.get(pk=ficha.paciente_id)

    disciplina_all = Disciplina.objects.all()
    discapacidad_all = Discapacidad.objects.all()
    results = Paciente.objects.filter(pk=ficha.paciente_id)

    for paciente_data in results:
        pac_dis = paciente_data.disciplina.all()
        pac_di = paciente_data.discapacidades.all()
    
    disciplina = []
    discapacidad = []
    
    for d in pac_dis:
        for di in disciplina_all:
            if d.disciplina == di.disciplina:
                disciplina_=d.id
        dis = Disciplina.objects.get(pk=disciplina_)
        disciplina.append({'id':dis.id,'nombre':dis.nombre})

    for d in pac_di:
        for di in discapacidad_all:
            if d.discapacidad == di.discapacidad:
                discapacidad_=d.id
        dis = Discapacidad.objects.get(pk=discapacidad_)
        discapacidad.append({'id':dis.id,'nombre':dis.nombre})

    context = {'profile':profile,'estudiante_data':estudiante,'ficha_data':ficha,'paciente_data':paciente,
    'disciplina_data':disciplina,'discapacidad_data':discapacidad}
    html = render_to_string("reportes/ficha_pdf.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; report.pdf"

    HTML(string=html).write_pdf(response)

    return response

@login_required
def dashboard_all(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
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

    Excelete = Formulario_satisfaccion.objects.filter(satisfaccion="Excelente").count()
    Pesima = Formulario_satisfaccion.objects.filter(satisfaccion="Pesima").count()
    Regular = Formulario_satisfaccion.objects.filter(satisfaccion="Regular").count()
    fecha_time = datetime.now()
    if fecha_time.day < 10:
        fecha = str(fecha_time.year) + "-" + str(fecha_time.month) + "-" + "0" + str(fecha_time.day)
    else:
        fecha = str(fecha_time.year) + "/" + str(fecha_time.month) + "/" + str(fecha_time.day)
    ficha_hoy = Detalle_atencion.objects.filter(fecha_eval=fecha).count()
    satisfaccion_count = Formulario_satisfaccion.objects.all().count() 
    paciente_count = Paciente.objects.all().count()
    fichas_count = Detalle_atencion.objects.all().count()
    solicitud_count = Solicitud.objects.all().count()
    docente_count = Docente.objects.all().count()
    coordinador_count = Coordinador.objects.all().count()
    estudiante_count = Estudiante.objects.all().count()
    template_name = 'reportes/dashboard.html'
    return render(request,template_name,{'profile':profile,'template_name':template_name,'paciente_count':paciente_count,
    'satisfaccion_count':satisfaccion_count,'ficha_hoy':ficha_hoy,'coordinador_data':coordinador_data,
    'docente_data':docente_data,'estudiante_data':estudiante_data,'fichas_data':fichas_data,'solicitud_data':solicitud_data,
    'paciente_data':paciente_data,'fichas_count':fichas_count,'solicitud_count':solicitud_count,'docente_count':docente_count,
    'coordinador_count':coordinador_count,'estudiante_count':estudiante_count,'Excelete':Excelete,'Pesima':Pesima,
    'Regular':Regular})