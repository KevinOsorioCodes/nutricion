from email.headerregistry import Group
from django.shortcuts import render
from registro.models import Paciente,Discapacidad,Disciplina,Profile,User,Estudiante
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect
from registro.views import validarRut,validatename,validateEmail
from django.core.paginator import Paginator
from django.db.models import Q
from nutricion.models import Detalle_atencion,Solicitud,Calificacion
from datetime import date, datetime

# Create your views here.
def fecha_actual():
    fecha_time = datetime.now()
    if fecha_time.day < 10:
        fecha = str(fecha_time.year) + "-" + str(fecha_time.month) + "-" + "0" + str(fecha_time.day)
    else:
        fecha = str(fecha_time.year) + "/" + str(fecha_time.month) + "/" + str(fecha_time.day)
    return fecha

def floats(num):
    try:
        num2 = float(num)
        return num2
    except ValueError: 
        separar = num.split(',',1) 
        juntar = separar[0]+"."+separar[1]
        convert = float(juntar)
        return convert


@login_required
def solicitud_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    fecha = fecha_actual()
    estudiantes = Estudiante.objects.all()
    template_name = 'solicitud/solicitud_add.html'
    return render(request,template_name,{'profile':profile,'estudiantes':estudiantes,'fecha_actual':fecha})

@login_required
def solicitud_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    # try:
    if request.method == 'POST':
        today = date.today()
        fecha_eval = request.POST.get('fecha_eval')
        estudiante = request.POST.getlist('estudiantes')
        fecha = fecha_actual()
        if fecha>fecha_eval:
            #messages.add_message(request, messages.INFO, 'La fecha es anterior a la fecha actual')
            return redirect('solicitud_add')

        solicitud_save = Solicitud(
            user_id = request.user.id,
            fecha_eval = fecha_eval,
        )
        solicitud_save.save()

        if estudiante:
            for e in estudiante:
                solicitud_save.estudiante.add(e)

        return redirect('solicitud_list')
    # except BaseException:
    #     return redirect('solicitud_list')

@login_required
def solicitud_edit(request,solicitud_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        estudiantes_all = Estudiante.objects.all()
        pacientes_all = Paciente.objects.all()
        results = Solicitud.objects.filter(pk=solicitud_id)
        fecha = fecha_actual()

        for solicitud in results:
            sol_e = solicitud.estudiante.all()
            sol_p = solicitud.paciente.all()
        
        estudiante = []
        paciente = []
        
        for e in sol_e:
            for es in estudiantes_all:
                if es.estudiante == e.estudiante:
                    estudiante_=e.id
            estudiante.append(estudiante_)
        
        for s in sol_p:
            for pa in pacientes_all:
                if pa.paciente == s.paciente:
                    paciente_=s.id
            paciente.append(paciente_)
            
        solicitud_data = Solicitud.objects.get(pk = solicitud_id)                   
        template_name = 'solicitud/solicitud_edit.html'
        return render(request,template_name,{'profile':profile,'solicitud_data':solicitud_data,
        'estudiante':estudiante,'estudiantes':estudiantes_all, 
        'paciente':paciente,'pacientes':pacientes_all,'fecha_actual':fecha})
    except Solicitud.DoesNotExist:
        return redirect('solicitud_list')
    except BaseException:
        return redirect('solicitud_list')

@login_required
def solicitud_update(request,solicitud_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        if request.method == 'POST':
            fecha_eval = request.POST.get('fecha_eval')
            fecha = fecha_actual()
            if fecha>fecha_eval:
                #messages.add_message(request, messages.INFO, 'La fecha es anterior a la fecha actual')
                return redirect('solicitud_edit',solicitud_id)
            
            estudiante = request.POST.getlist('estudiantes')
            paciente = request.POST.getlist('pacientes')

            estudiantes_all = Estudiante.objects.all()
            paciente_all = Paciente.objects.all()
            results = Solicitud.objects.filter(pk=solicitud_id)

            for solicitud in results:
                sol_e = solicitud.estudiante.all()
                sol_p = solicitud.paciente.all()
            
            for e in sol_e:
                for es in estudiantes_all:
                    if es.estudiante == e.estudiante:
                        estudiante_=e.id
                solicitud.estudiante.remove(estudiante_)
        
            for solicitud in results:
                if estudiante:
                    for e in estudiante:
                        solicitud.estudiante.add(e)

            for s in sol_p:
                for pa in paciente_all:
                    if pa.paciente == s.paciente:
                        paciente_=s.id
                solicitud.paciente.remove(paciente_)
        
            for solicitud in results:
                if paciente:
                    for p in paciente:
                        solicitud.paciente.add(p)
            
            Solicitud.objects.filter(pk=solicitud_id).update(fecha_eval=fecha_eval)
            return redirect('solicitud_list')         
    except Solicitud.DoesNotExist:
        return redirect('solicitud_edit',solicitud_id)
    except ValueError:
        messages.add_message(request, messages.INFO, 'Error en los datos ingresados Value')
        return redirect('solicitud_edit',solicitud_id)
    except BaseException:
        messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
        return redirect('solicitud_edit',solicitud_id)

@login_required
def solicitud_delete(request,solicitud_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        solicitud = Solicitud.objects.get(pk=solicitud_id)
        Solicitud.objects.filter(pk=solicitud.id).delete()
        return redirect('solicitud_list')
          
    except Solicitud.DoesNotExist:
        return redirect('solicitud_list')
    except BaseException:
        return redirect('solicitud_list')

@login_required
def solicitud_list(request,page=None,initial=None,final=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
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

    if initial == None or final == None:
        initial = request.POST.get('date_initial')
        final = request.POST.get('date_final')
    else:
        initial = initial
        final = final

    if request.POST.get('date_initial') == None or request.POST.get('date_final')== None:
        initial = initial
        final = final
    else:
        initial = request.POST.get('date_initial')
        final = request.POST.get('date_final')

    if request.method == 'POST':
        initial = request.POST.get('date_initial')
        final = request.POST.get('date_final')
        page = None
    
    h_count = Solicitud.objects.all().count()

    
    h_list = []
    h_list_array_count =0
    if initial == None or initial == "" or final == None or final == "":
        h_list_array =Solicitud.objects.order_by('id')
        h_list_array_count =Solicitud.objects.order_by('fecha_eval').count()
        for h in h_list_array:
            user = User.objects.get(pk = h.user_id)
            h_list.append({'id':h.id,'fecha_add':h.fecha_add,'fecha_eval':h.fecha_eval,'nombre':user.first_name})
    else:
        if initial > final:
            inicio = final
            ultimo = initial
            initial = inicio
            final = ultimo
            
        h_list_array_count = Solicitud.objects.filter(fecha_eval__range=(initial,final)).count()

        h_list_array = Solicitud.objects.filter(fecha_eval__range=(initial,final)).order_by('id')

        for h in h_list_array:
            user = User.objects.get(pk = h.user_id)
            h_list.append({'id':h.id,'fecha_add':h.fecha_add,'fecha_eval':h.fecha_eval,'nombre':user.first_name})

    paginator = Paginator(h_list, 5)
    h_list_paginate= paginator.get_page(page)
    template_name = 'solicitud/solicitud_list.html'
    return render(request,template_name,{'profile':profile,'h_count':h_count,'h_list_array_count':h_list_array_count,
    'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'initial':initial,'final':final})

@login_required
def paciente_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    discapacidades = Discapacidad.objects.all()
    disciplinas = Disciplina.objects.all()
    template_name = 'paciente/paciente_add.html'
    return render(request,template_name,{'profile':profile,'discapacidades':discapacidades,'disciplinas':disciplinas})

@login_required
def paciente_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    # try: 
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        dv = request.POST.get('dv')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        email = request.POST.get('email')
        genero = request.POST.get('genero')
        disciplina = request.POST.getlist('disciplina')
        discapacidades = request.POST.getlist('discapacidades')

        rut = rut.replace(".","")
        rutdv= rut+dv
        result=validarRut(rutdv)
        result2=validatename(nombre)
    
        if(validateEmail(email)==False):
            messages.add_message(request, messages.INFO, 'El email: '+ email +' del usuario '+ nombre + ' no es valido')
            return redirect('paciente_add')
        if User.objects.filter(username = email).count()>=1:
            messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el email: '+ email +' ya se encuentra registrado')
            return('paciente_add')
        if Paciente.objects.filter(rut = rut).count()>=1:
            messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el rut: '+ rut +'-'+dv+' ya se encuentra registrado como paciente')
            return('paciente_add')
        if result==False:
            messages.add_message(request, messages.INFO, 'El Rut: '+ rut+'-'+dv +'del usuario '+ nombre + 'no es valido')
            return('paciente_add')
        if result2==False: 
            messages.add_message(request, messages.INFO, 'El Nombre ingresado del usuario: '+ nombre + ' no es valido (solo nombres alfabeticos)')
            return('paciente_add')
    
        paciente_save = Paciente(
            nombre = nombre,
            rut = rut,
            dv = dv,
            fecha_nacimiento = fecha_nacimiento,
            email=email,
            genero=genero,
            )
        paciente_save.save()

        if disciplina:
            for di in disciplina:
                if(validatename(di)==True):
                    if Discapacidad.objects.filter(nombre=di).count()>=1:
                        discapacidad = Discapacidad.objects.get(nombre=di)
                    else:
                        if Disciplina.objects.count()>=1:
                            disciplina_save = Disciplina(id = Disciplina.objects.order_by('-id').first().id+1,nombre = di)
                        else:
                            disciplina_save = Disciplina(id = 1,nombre = di)
                        disciplina_save.save()
                        disciplina = disciplina_save
                else:
                    disciplina = Disciplina.objects.get(pk=di)
                paciente_save.disciplina.add(disciplina.id)
        
        if discapacidades:
            for d in discapacidades:
                if(validatename(d)==True):
                    if Discapacidad.objects.filter(nombre=d).count()>=1:
                        discapacidad = Discapacidad.objects.get(nombre=d)
                    else:
                        if Discapacidad.objects.count()>=1:
                            discapacidad_save = Discapacidad(id = Discapacidad.objects.order_by('-id').first().id+1,nombre = d)
                        else:
                            discapacidad_save = Discapacidad(id = 1,nombre = d)
                        discapacidad_save.save()
                        discapacidad = discapacidad_save
                else:
                    discapacidad = Discapacidad.objects.get(pk=d)
                paciente_save.discapacidades.add(discapacidad.id)

        return redirect('paciente_add')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
    # except ValueError:
    #     return redirect('paciente_add')
      
@login_required
def paciente_list(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
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
    h_count = Paciente.objects.all().count()
    if search == None or search == "None" or search == "":
        h_list_array =Paciente.objects.order_by('nombre')
        for h in h_list_array:
            h_list.append({'id':h.id,'nombre':h.nombre,'email':h.email,'rut':h.rut,'dv':h.dv})
    else:
        h_list_array = Paciente.objects.filter(rut__icontains=search).order_by('nombre')
        h_count = Paciente.objects.filter(rut__icontains=search).count()
        for h in h_list_array:
            h_list.append({'id':h.id,'nombre':h.nombre,'email':h.email,'rut':h.rut,'dv':h.dv})
    paginator = Paginator(h_list, 5)
    h_list_paginate= paginator.get_page(page)
    template_name = 'paciente/paciente_list.html'
    return render(request,template_name,{'profile':profile,'h_count':h_count,
    'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search})
        
@login_required
def paciente_edit(request,paciente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    # try:
    paciente = Paciente.objects.get(pk=paciente_id)
    template_name = 'paciente/paciente_edit.html'
    paciente_data= Paciente.objects.get(pk=paciente_id)

    disciplina_all = Disciplina.objects.all()
    discapacidad_all = Discapacidad.objects.all()
    results = Paciente.objects.filter(pk=paciente_id)

    for paciente in results:
        pac_dis = paciente.disciplina.all()
        pac_disca = paciente.discapacidades.all()
    
    disciplina = []
    discapacidad = []
    
    for d in pac_dis:
        for di in disciplina_all:
            if d.disciplina == di.disciplina:
                disciplina_=d.id
        disciplina.append(disciplina_)

    for d in pac_disca:
        for di in discapacidad_all:
            if d.discapacidad == di.discapacidad:
                discapacidad_=d.id
        discapacidad.append(discapacidad_)
    
    return render(request,template_name,{'profile':profile,'paciente':paciente,'paciente_data':paciente_data,
    'disciplina_all':disciplina_all,'disciplina_data':disciplina,
    'discapacidad_all':discapacidad_all,'discapacidad_data':discapacidad})
    # except Paciente.DoesNotExist:
    #     return redirect('paciente_list')
    # except BaseException:
    #     return redirect('paciente_list')

@login_required
def paciente_update(request,paciente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    paciente = Paciente.objects.get(pk=paciente_id)
    try:
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            genero = request.POST.get('genero')
            email = request.POST.get('email')   


            Paciente.objects.get(pk=paciente_id)


            if(validateEmail(email)==False):
                messages.add_message(request, messages.INFO, 'El email: '+ email +' del usuario '+ nombre + ' no es valido')
                return redirect('paciente_edit')
            if User.objects.filter(username = email).count()>=1:
                messages.add_message(request, messages.INFO, 'El usuario: '+ nombre +' con el email: '+ email +' ya se encuentra registrado')
                return('paciente_edit')

            disciplina = request.POST.getlist('disciplina')
            discapacidad = request.POST.getlist('discapacidad')

            disciplina_all = Disciplina.objects.all()
            discapacidad_all = Discapacidad.objects.all()
            results = Paciente.objects.filter(pk=paciente_id)

            for paciente in results:
                pac_dis = paciente.disciplina.all()
                pac_disca = paciente.discapacidades.all()
         
            for d in pac_dis:
                for di in disciplina_all:
                    if d.disciplina == di.disciplina:
                        disciplina_=d.id
                paciente.disciplina.remove(disciplina_)

            for paciente in results:
                if disciplina:
                    for d in disciplina:
                        paciente.disciplina.add(d)
            
            for d in pac_disca:
                for di in discapacidad_all:
                    if d.discapacidad == di.discapacidad:
                        discapacidad_=d.id
                paciente.discapacidades.remove(discapacidad_)

            for paciente in results:
                if discapacidad:
                    for d in discapacidad:
                        paciente.discapacidades.add(d)

            Paciente.objects.filter(pk=paciente_id).update(nombre=nombre)
            Paciente.objects.filter(pk=paciente_id).update(genero=genero)
            Paciente.objects.filter(pk=paciente_id).update(email=email)
            if (fecha_nacimiento):
                Paciente.objects.filter(pk=paciente_id).update(fecha_nacimiento=fecha_nacimiento)
            return redirect('paciente_list')
    except BaseException():
        return redirect('paciente_edit')

@login_required
def paciente_delete(request,paciente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0 or profile.group_id == 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        paciente = Paciente.objects.get(pk=paciente_id)
        Paciente.objects.filter(pk=paciente.id).delete()
        return redirect('paciente_list')

    except Paciente.DoesNotExist:
        return  redirect('paciente_list')
    except BaseException():
        return redirect('paciente_list')
    
def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    
    ##code
    # separar = fecha_nac.split("-")   ##1997-02-20 #Año-Mes-dia
    # año = separar[0]
    # mes = separar[1]
    # dia = separar[2]
    # edad = calculateAge(date(int(año), int(mes), int(dia)))
    ##code

    return age 

@login_required
def ficha_add(request,paciente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        paciente = Paciente.objects.get(pk=paciente_id)

        template_name = 'ficha/estudiante_ficha_add.html'
        return render(request,template_name,{'profile':profile,'paciente_data':paciente,'paciente_id':paciente_id})

    except ValueError:
        return redirect('ficha')
    except BaseException:
        return redirect('ficha_list')

@login_required
def admin_ficha_add(request,paciente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        paciente = Paciente.objects.get(pk=paciente_id)
        estudiante = Estudiante.objects.all()

        template_name = 'ficha/admin_ficha_add.html'
        return render(request,template_name,{'profile':profile,'estudiante_data':estudiante,'paciente_data':paciente,'paciente_id':paciente_id})

    except ValueError:
         return redirect('ficha_list')
    except BaseException:
         return redirect('ficha_list')

@login_required
def ficha_save(request,paciente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        if request.method == 'POST':
            #Detalle
            estatura = floats(request.POST.get('estatura'))
            prom_circunferencia_cin = floats(request.POST.get('prom_circunferencia_cin'))
            prom_circunferencia_braq = floats(request.POST.get('prom_circunferencia_braq'))
            peso_prom = floats(request.POST.get('peso_prom'))
            prom_pliegue_t = floats(request.POST.get('prom_pliegue_t'))
            prom_pliegue_b = floats(request.POST.get('prom_pliegue_b'))
            prom_pliegue_se = floats(request.POST.get('prom_pliegue_se'))
            prom_pliegue_si = floats(request.POST.get('prom_pliegue_si'))
            sum_pliegues = floats(request.POST.get('sum_pliegues'))
            porc_grasa = floats(request.POST.get('porc_grasa'))
            diag_nutri = request.POST.get('diag_nutri')
            prom_pliegue_abd = request.POST.get('prom_pliegue_abd')
            prom_pliegue_pant = request.POST.get('prom_pliegue_pant')
            prom_pliegue_media = request.POST.get('prom_pliegue_media')
            prom_pliegue_supra = request.POST.get('prom_pliegue_supra')
            recomendacion = request.POST.get('recomendacion')

            if prom_pliegue_abd != '':
                prom_pliegue_abd = floats(prom_pliegue_abd)
            else:
                prom_pliegue_abd = floats(0.0)

            if prom_pliegue_pant != '':
                prom_pliegue_pant = floats(prom_pliegue_pant)
            else:
                prom_pliegue_pant = floats(0.0)

            if prom_pliegue_media != '':
                prom_pliegue_media = floats(prom_pliegue_media)
            else:
                prom_pliegue_media = floats(0.0)
                
            if prom_pliegue_supra != '':
                prom_pliegue_supra = floats(prom_pliegue_supra)
            else:
                prom_pliegue_supra = floats(0.0)

            paciente = Paciente.objects.get(pk=paciente_id)
            
            estudiante = Estudiante.objects.get(user_id=request.user.id)
            ficha_save = Detalle_atencion(
                estudiante_id = estudiante.id,
                paciente_id = paciente.id,
                estatura = estatura,
                peso_prom = peso_prom,
                prom_circunferencia_cin = prom_circunferencia_cin,
                prom_circunferencia_braq = prom_circunferencia_braq,
                prom_pliegue_t = prom_pliegue_t,
                prom_pliegue_b = prom_pliegue_b,
                prom_pliegue_se = prom_pliegue_se,
                prom_pliegue_si = prom_pliegue_si,
                sum_pliegues = sum_pliegues,
                porc_grasa = porc_grasa,
                diag_nutri = diag_nutri,
                prom_pliegue_abd = prom_pliegue_abd,
                prom_pliegue_pant = prom_pliegue_pant,
                prom_pliegue_media = prom_pliegue_media,
                prom_pliegue_supra = prom_pliegue_supra,
                recomendacion = recomendacion,
            )
            
            ficha_save.save()
            messages.add_message(request, messages.INFO, 'Ficha ingresada con éxito')
            return redirect('encuesta_satisfaccion_token',ficha_save.id)
        else:
            messages.add_message(request,messages.INFO, 'El metodo recibido no es POST')
            return redirect('ficha_list')
    except ValueError:
        messages.add_message(request, messages.INFO, 'Value Error')
        return redirect('Ficha_add')
    except BaseException:
        messages.add_message(request, messages.INFO, 'Error')
        return redirect('Ficha_add')

@login_required
def admin_ficha_save(request,paciente_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        if request.method == 'POST':
            #Detalle
            estatura = floats(request.POST.get('estatura'))
            prom_circunferencia_cin = floats(request.POST.get('prom_circunferencia_cin'))
            prom_circunferencia_braq = floats(request.POST.get('prom_circunferencia_braq'))
            peso_prom = floats(request.POST.get('peso_prom'))
            prom_pliegue_t = floats(request.POST.get('prom_pliegue_t'))
            prom_pliegue_b = floats(request.POST.get('prom_pliegue_b'))
            prom_pliegue_se = floats(request.POST.get('prom_pliegue_se'))
            prom_pliegue_si = floats(request.POST.get('prom_pliegue_si'))
            sum_pliegues = floats(request.POST.get('sum_pliegues'))
            porc_grasa = floats(request.POST.get('porc_grasa'))
            diag_nutri = request.POST.get('diag_nutri')
            prom_pliegue_abd = request.POST.get('prom_pliegue_abd')
            prom_pliegue_pant = request.POST.get('prom_pliegue_pant')
            prom_pliegue_media = request.POST.get('prom_pliegue_media')
            prom_pliegue_supra = request.POST.get('prom_pliegue_supra')
            recomendacion = request.POST.get('recomendacion')

            if prom_pliegue_abd != '':
                prom_pliegue_abd = floats(prom_pliegue_abd)
            else:
                prom_pliegue_abd = floats(0.0)

            if prom_pliegue_pant != '':
                prom_pliegue_pant = floats(prom_pliegue_pant)
            else:
                prom_pliegue_pant = floats(0.0)

            if prom_pliegue_media != '':
                prom_pliegue_media = floats(prom_pliegue_media)
            else:
                prom_pliegue_media = floats(0.0)
                
            if prom_pliegue_supra != '':
                prom_pliegue_supra = floats(prom_pliegue_supra)
            else:
                prom_pliegue_supra = floats(0.0)

            paciente = Paciente.objects.get(pk=paciente_id)
            estudiante = request.POST.get('estudiante')
            estudiante = Estudiante.objects.get(pk=estudiante)
            ficha_save = Detalle_atencion(
                estudiante_id = estudiante.id,
                paciente_id = paciente.id,
                estatura = estatura,
                peso_prom = peso_prom,
                prom_circunferencia_cin = prom_circunferencia_cin,
                prom_circunferencia_braq = prom_circunferencia_braq,
                prom_pliegue_t = prom_pliegue_t,
                prom_pliegue_b = prom_pliegue_b,
                prom_pliegue_se = prom_pliegue_se,
                prom_pliegue_si = prom_pliegue_si,
                sum_pliegues = sum_pliegues,
                porc_grasa = porc_grasa,
                diag_nutri = diag_nutri,
                prom_pliegue_abd = prom_pliegue_abd,
                prom_pliegue_pant = prom_pliegue_pant,
                prom_pliegue_media = prom_pliegue_media,
                prom_pliegue_supra = prom_pliegue_supra,
                recomendacion = recomendacion,
            )
            ficha_save.save()
            messages.add_message(request, messages.INFO, 'Ficha ingresada con éxito')
            return redirect('admin_ficha_paciente_list2',paciente_id)
        else:
            messages.add_message(request,messages.INFO, 'El metodo recibido no es POST')
            return redirect('admin_ficha_list')
    except ValueError:
        messages.add_message(request, messages.INFO, 'Value Error')
        return redirect('admin_ficha_estudiante_list')
    except BaseException:
        messages.add_message(request, messages.INFO, 'Error')
        return redirect('admin_ficha_estudiante_list')

@login_required
def admin_calificacion_save1(request,estudiante_id,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    # try:
    if request.method == 'POST':
        nota=request.POST.get('nota')
        comentario=request.POST.get('comentario')

        if Calificacion.objects.filter(ficha_id = ficha_id).count()>=1:
            Calificacion.objects.filter(ficha_id = ficha_id).update(nota=nota)
            Calificacion.objects.filter(ficha_id = ficha_id).update(comentario=comentario)
            return redirect('admin_ficha_estudiante_ver',estudiante_id,ficha_id)

        calificacion_save=Calificacion(
            ficha_id=ficha_id,
            nota=nota,
            comentario=comentario,
            )
        calificacion_save.save()
        
        return redirect('admin_ficha_estudiante_ver',estudiante_id,ficha_id)
    else:
        messages.add_message(request,messages.INFO, 'El metodo recibido no es POST')
        return redirect('admin_ficha_estudiante_ver',estudiante_id,ficha_id)

@login_required
def admin_calificacion_save2(request,paciente_id,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    # try:
    if request.method == 'POST':
        nota=request.POST.get('nota')
        comentario=request.POST.get('comentario')

        if Calificacion.objects.filter(ficha_id = ficha_id).count()>=1:
            Calificacion.objects.filter(ficha_id = ficha_id).update(nota=nota)
            Calificacion.objects.filter(ficha_id = ficha_id).update(comentario=comentario)
            return redirect('admin_ficha_paciente_ver',paciente_id,ficha_id)

        calificacion_save=Calificacion(
            ficha_id=ficha_id,
            nota=nota,
            comentario=comentario,
            )
        calificacion_save.save()
        
        return redirect('admin_ficha_paciente_ver',paciente_id,ficha_id)
    else:
        messages.add_message(request,messages.INFO, 'El metodo recibido no es POST')
        return redirect('admin_ficha_paciente_ver',paciente_id,ficha_id)

#Estudiante
@login_required
def ficha_list(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id !=0 :
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

        pacientes_all = Paciente.objects.all()
        estudiantes = Estudiante.objects.filter(user_id=request.user.id)
        results = Solicitud.objects.filter(fecha_eval=date.today())

        for solicitud in results:
            sol_e = solicitud.estudiante.all()
            sol_p = solicitud.paciente.all()
        
        count = 0
        try:
            for s in sol_e:
                for es in estudiantes:
                    if es.estudiante == s.estudiante:
                        count = count+1

            paciente = []
            
            if search == None or search=="" or search == "None":
                for s in sol_p:
                    for pa in pacientes_all:
                        if pa.paciente == s.paciente:
                            paciente_=s.id
                    pacient = Paciente.objects.get(pk=paciente_)
                    paciente.append({'id':pacient.id,'nombre':pacient.nombre,'rut':pacient.rut,'dv':pacient.dv})

                h_list = paciente
            else:
                for s in sol_p:
                    for pa in pacientes_all:
                        if pa.paciente == s.paciente:
                            paciente_=s.id
                    pacient = Paciente.objects.get(pk=paciente_)
                    pacie = Paciente.objects.all().filter(rut__icontains=search).order_by('nombre')

                    for p in pacie:
                        if p.rut == pacient.rut:
                            paciente.append({'id':pacient.id,'nombre':pacient.nombre,'rut':pacient.rut,'dv':pacient.dv})
                
                h_list=paciente
        except BaseException:
            paciente = 0

        h_list_array_count = len(h_list)

        paginator = Paginator(h_list, 5)
        h_list_paginate= paginator.get_page(page)
        template_name = 'ficha/estudiante_ficha_list.html'
        return render(request,template_name,{'profile':profile,'h_list_array_count':h_list_array_count,
        'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search,'paciente':paciente})

@login_required
def ficha_paciente_list(request,paciente_id,page=None,initial=None,final=None):
    profile = Profile.objects.get(user_id=request.user.id)
    try:
        if profile.group_id !=0 :
            if page == None:
                page = request.GET.get('page')
            else:
                page = page
            if request.GET.get('page') == None:
                page = page
            else:
                page = request.GET.get('page')
            
            if initial == None or final == None:
                initial = request.POST.get('date_initial')
                final = request.POST.get('date_final')
            else:
                initial = initial
                final = final

            if request.POST.get('date_initial') == None or request.POST.get('date_final')== None:
                initial = initial
                final = final
            else:
                initial = request.POST.get('date_initial')
                final = request.POST.get('date_final')

            if request.method == 'POST':
                initial = request.POST.get('date_initial')
                final = request.POST.get('date_final')
                page = None

            h_list = []
            estudiante = Estudiante.objects.get(user_id=request.user.id)
            paciente = Paciente.objects.get(pk= paciente_id)
            h_list_array_count = Detalle_atencion.objects.filter(paciente_id=paciente_id).filter(estudiante_id=estudiante.id).count()
        
            h_list = []
    
            if initial == None or initial == "" or final == None or final == "":
                h_list_array =Detalle_atencion.objects.filter(estudiante_id=estudiante.id).filter(paciente_id=paciente_id).order_by('id')
                for h in h_list_array:
                    h_list.append({'id':h.id,'nombre':paciente.nombre,'fecha_eval':h.fecha_eval})
            else:
                if initial > final:
                    inicio = final
                    ultimo = initial
                    initial = inicio
                    final = ultimo
                    
                h_list_array = Detalle_atencion.objects.filter(estudiante_id=estudiante.id).filter(paciente_id=paciente_id).filter(fecha_eval__range=(initial,final)).order_by('id')

                for h in h_list_array:
                    h_list.append({'id':h.id,'nombre':paciente.nombre,'fecha_eval':h.fecha_eval})

            paginator = Paginator(h_list, 5)
            h_list_paginate= paginator.get_page(page)
            template_name = 'ficha/estudiante_ficha_paciente_list.html'
            return render(request,template_name,{'profile':profile,'h_list_array_count':h_list_array_count,'paciente_data':paciente,
            'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'initial':initial,'final':final})
    except ValueError:
        return redirect('ficha_list')
    except BaseException:
        return redirect('ficha_list')

@login_required
def ficha_edit(request,paciente_id,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        estudiante = Estudiante.objects.get(user_id=request.user.id)
        ficha_data = Detalle_atencion.objects.filter(estudiante_id=estudiante.id).get(pk=ficha_id)
        paciente_data = Paciente.objects.get(pk=ficha_data.paciente_id)

        template_name = 'ficha/estudiante_ficha_edit.html'
        return render(request,template_name,{'profile':profile,'template_name' : 'ficha/ficha_edit.html','paciente_id':paciente_id,
        'ficha_data':ficha_data,'paciente_data':paciente_data,})
    except Detalle_atencion.DoesNotExist:
        return redirect('ficha_list')
    except BaseException:
        return redirect('ficha_list')

@login_required
def ficha_update(request,paciente_id,ficha_id):
    print(paciente_id)
    print(ficha_id)
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        if request.method == 'POST':
            estatura = floats(request.POST.get('estatura'))
            peso_prom = floats(request.POST.get('peso_prom')) 
            prom_circunferencia_cin = floats(request.POST.get('prom_circunferencia_cin'))
            prom_circunferencia_braq = floats(request.POST.get('prom_circunferencia_braq'))
            prom_pliegue_t = floats(request.POST.get('prom_pliegue_t'))
            prom_pliegue_b = floats(request.POST.get('prom_pliegue_b'))
            prom_pliegue_se = floats(request.POST.get('prom_pliegue_se'))
            prom_pliegue_si = floats(request.POST.get('prom_pliegue_si'))
            sum_pliegues = floats(request.POST.get('sum_pliegues'))
            porc_grasa = floats(request.POST.get('porc_grasa'))
            diag_nutri = request.POST.get('diag_nutri')
            prom_pliegue_abd = request.POST.get('prom_pliegue_abd')
            prom_pliegue_pant = request.POST.get('prom_pliegue_pant')
            prom_pliegue_media = request.POST.get('prom_pliegue_media')
            prom_pliegue_supra = request.POST.get('prom_pliegue_supra')
            recomendacion = request.POST.get('recomendacion')
            print ("recomendacion")
            if prom_pliegue_abd != '':
                prom_pliegue_abd = floats(prom_pliegue_abd)
            else:
                prom_pliegue_abd = None

            if prom_pliegue_pant != '':
                prom_pliegue_pant = floats(prom_pliegue_pant)
            else:
                prom_pliegue_pant = None

            if prom_pliegue_media != '':
                prom_pliegue_media = floats(prom_pliegue_media)
            else:
                prom_pliegue_media = None
                
            if prom_pliegue_supra != '':
                prom_pliegue_supra = floats(prom_pliegue_supra)
            else:
                prom_pliegue_supra = None
            #########################################################################
            ##try
            ficha = Detalle_atencion.objects.get(pk=ficha_id)
            estudiante = Estudiante.objects.get(user_id=request.user.id)
            
            if ficha.estudiante_id != estudiante.id:
                return redirect('ficha_list')
                
            ###Update
            Detalle_atencion.objects.filter(pk=ficha_id).update(estatura=estatura)
            Detalle_atencion.objects.filter(pk=ficha_id).update(peso_prom=peso_prom)
            Detalle_atencion.objects.filter(pk=ficha_id).update(prom_circunferencia_cin=prom_circunferencia_cin)
            Detalle_atencion.objects.filter(pk=ficha_id).update(prom_circunferencia_braq=prom_circunferencia_braq)
            Detalle_atencion.objects.filter(pk=ficha_id).update(prom_pliegue_t=prom_pliegue_t)
            Detalle_atencion.objects.filter(pk=ficha_id).update(prom_pliegue_b=prom_pliegue_b)
            Detalle_atencion.objects.filter(pk=ficha_id).update(prom_pliegue_se=prom_pliegue_se)
            Detalle_atencion.objects.filter(pk=ficha_id).update(prom_pliegue_si=prom_pliegue_si)
            Detalle_atencion.objects.filter(pk=ficha_id).update(sum_pliegues=sum_pliegues)
            Detalle_atencion.objects.filter(pk=ficha_id).update(porc_grasa=porc_grasa)
            Detalle_atencion.objects.filter(pk=ficha_id).update(diag_nutri=diag_nutri)
            Detalle_atencion.objects.filter(pk=ficha_id).update(prom_pliegue_abd=prom_pliegue_abd)
            Detalle_atencion.objects.filter(pk=ficha_id).update(prom_pliegue_pant=prom_pliegue_pant)
            Detalle_atencion.objects.filter(pk=ficha_id).update(diag_nutri=diag_nutri)
            Detalle_atencion.objects.filter(pk=ficha_id).update(prom_pliegue_media=prom_pliegue_media)
            Detalle_atencion.objects.filter(pk=ficha_id).update(prom_pliegue_supra=prom_pliegue_supra) 
            Detalle_atencion.objects.filter(pk=ficha_id).update(recomendacion=recomendacion) 
        return redirect('ficha_edit',ficha_id,paciente_id)
    except Detalle_atencion.DoesNotExist:
        return redirect('ficha_edit',ficha_id,paciente_id)
    except ValueError:
        messages.add_message(request, messages.INFO, 'Error en los datos ingresados Value')
        return redirect('ficha_edit',ficha_id,paciente_id)
    except BaseException:
        messages.add_message(request, messages.INFO, 'Error en los datos ingresados Base')
        return redirect('ficha_edit',ficha_id,paciente_id)

@login_required
def ficha_delete(request,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 4:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        detalle = Detalle_atencion.objects.get(pk=ficha_id)
        Detalle_atencion.objects.filter(pk=detalle.id).delete()
        return redirect('ficha_list')
    except Detalle_atencion.DoesNotExist:
        return redirect('ficha_list')
    except BaseException:
        return redirect('ficha_list')

@login_required
def ficha_estudiante_list(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id !=0 :
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
        if search == None or search == "None":
            h_list_array =Estudiante.objects.order_by('nombre')
            for h in h_list_array:
                h_list.append({'id':h.id,'nombre':h.nombre})

        else:
            h_list_array = Estudiante.objects.filter(Q(fecha_eval__icontains=search)).order_by('nombre')
            for h in h_list_array:
                h_list.append({'id':h.id,'nombre':h.nombre})

        paginator = Paginator(h_list, 5)
        h_list_paginate= paginator.get_page(page)
        template_name = 'ficha/ficha_estudiante_list.html'
        return render(request,template_name,{'profile':profile,'h_count':h_count,
        'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search})
	
#Estudiante
@login_required
def admin_ficha_paciente_list1(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id !=0 :
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

        pacientes_all = Paciente.objects.all()

        paciente = []
        try:
            if search == None or search=="" or search == "None":
                for pa in pacientes_all:
                    pacient = Paciente.objects.get(pk=pa.id)
                    paciente.append({'id':pacient.id,'nombre':pacient.nombre,'rut':pacient.rut,'dv':pacient.dv})

                h_list = paciente
            else:
                pacie = Paciente.objects.filter(rut__icontains=search).order_by('nombre')

                for pa in pacientes_all:
                    for p in pacie:
                        pac = Paciente.objects.get(pk=p.id)
                        if pa.rut == pac.rut:
                            paciente.append({'id':pa.id,'nombre':pa.nombre,'rut':pa.rut,'dv':pa.dv})

                h_list=paciente
        except BaseException:
            paciente = 0
            pass

        h_list_array_count = len(h_list)

        paginator = Paginator(h_list, 5)
        h_list_paginate= paginator.get_page(page)
        template_name = 'ficha/admin_ficha_paciente_list1.html'
        return render(request,template_name,{'profile':profile,'h_list_array_count':h_list_array_count,
        'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search,'paciente':paciente})

@login_required
def admin_ficha_paciente_list2(request,paciente_id,page=None,initial=None,final=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id !=0 :
        if page == None:
            page = request.GET.get('page')
        else:
            page = page
        if request.GET.get('page') == None:
            page = page
        else:
            page = request.GET.get('page')
        
        if initial == None or final == None:
            initial = request.POST.get('date_initial')
            final = request.POST.get('date_final')
        else:
            initial = initial
            final = final

        if request.POST.get('date_initial') == None or request.POST.get('date_final')== None:
            initial = initial
            final = final
        else:
            initial = request.POST.get('date_initial')
            final = request.POST.get('date_final')

        if request.method == 'POST':
            initial = request.POST.get('date_initial')
            final = request.POST.get('date_final')
            page = None

        h_list = []
        paciente = Paciente.objects.get(pk= paciente_id)
        h_list_array_count = Detalle_atencion.objects.filter(paciente_id=paciente).count()

        if initial == None or initial == "" or final == None or final == "":
            h_list_array = Detalle_atencion.objects.filter(paciente_id=paciente).order_by('id')
            for h in h_list_array:
                estudiante= Estudiante.objects.get(pk=h.estudiante_id)
                h_list.append({'id':h.id,'nombre_paciente':paciente.nombre,'nombre_estudiante':estudiante.nombre,'fecha_eval':h.fecha_eval})
        else:
            if initial > final:
                inicio = final
                ultimo = initial
                initial = inicio
                final = ultimo
                
            h_list_array = Detalle_atencion.objects.filter(paciente_id=paciente).filter(fecha_eval__range=(initial,final)).order_by('id')
            h_list_array_count = Detalle_atencion.objects.filter(paciente_id=paciente).filter(fecha_eval__range=(initial,final)).count()
            for h in h_list_array:
                estudiante= Estudiante.objects.get(pk=h.estudiante_id)
                h_list.append({'id':h.id,'nombre_paciente':paciente.nombre,'nombre_estudiante':estudiante.nombre,'fecha_eval':h.fecha_eval})

        paginator = Paginator(h_list, 5)
        h_list_paginate= paginator.get_page(page)
        template_name = 'ficha/admin_ficha_paciente_list2.html'
        return render(request,template_name,{'profile':profile,'h_list_array_count':h_list_array_count,'paciente_data':paciente,
        'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'initial':initial,'final':final})

@login_required
def admin_ficha_paciente_ver(request,paciente_id,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        ficha_data = Detalle_atencion.objects.get(pk=ficha_id)
        paciente_data = Paciente.objects.get(pk=paciente_id)
        estudiante_data = Estudiante.objects.get(pk = ficha_data.estudiante_id)
        calificacion_data = Calificacion.objects.get(ficha_id=ficha_data.id)

        disciplina_all = Disciplina.objects.all()
        discapacidad_all = Discapacidad.objects.all()
        results = Paciente.objects.filter(pk=paciente_id)

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

        template_name = 'ficha/admin_ficha_paciente_ver.html'
        return render(request,template_name,{'profile':profile,'template_name' : 'ficha/ficha_edit.html','calificacion_data':calificacion_data,
        'ficha_data':ficha_data,'paciente_data':paciente_data,'estudiante_data':estudiante_data,'disciplina_data':disciplina,'discapacidad_data':discapacidad})
    except Detalle_atencion.DoesNotExist:
        return redirect('admin_ficha_paciente_list2',paciente_id)
    except Calificacion.DoesNotExist:
        disciplina_all = Disciplina.objects.all()
        discapacidad_all = Discapacidad.objects.all()
        results = Paciente.objects.filter(pk=ficha_data.paciente_id)

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

        template_name = 'ficha/admin_ficha_estudiante_ver.html'
        return render(request,template_name,{'profile':profile,'template_name' : 'ficha/ficha_edit.html',
        'ficha_data':ficha_data,'paciente_data':paciente_data,'disciplina_data':disciplina,'discapacidad_data':discapacidad,
        'estudiante_data':estudiante_data})

@login_required
def admin_ficha_estudiante_list1(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id !=0 :
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
        estudiantes_all = Estudiante.objects.all()

        try:
            estudiante = []
            if search == None or search=="" or search == "None":
                for es in estudiantes_all:
                    estudiant = Estudiante.objects.get(pk=es.id)
                    perfil = Profile.objects.get(user_id= estudiant.user_id)
                    estudiante.append({'id':es.id,'nombre':es.nombre,'rut':es.rut,'dv':es.dv,'perfil':perfil})
                
                h_list = estudiante
            else:
                estudia = Estudiante.objects.filter(rut__icontains=search).order_by('nombre')
                for es in estudiantes_all:
                    for e in estudia:
                        if es.rut == e.rut:
                            perfil = Profile.objects.get(user_id= e.user_id)
                            estudiante.append({'id':e.id,'nombre':e.nombre,'rut':e.rut,'dv':e.dv,'perfil':perfil})
                h_list = estudiante
    
        except BaseException:
            estudiante=0
            pass
        
        h_list_array_count = len(h_list)

        paginator = Paginator(h_list, 5)
        h_list_paginate= paginator.get_page(page)
        template_name = 'ficha/admin_ficha_estudiante_list1.html'
        return render(request,template_name,{'profile':profile,'h_list_array_count':h_list_array_count,
        'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search,'estudiante':estudiante})

@login_required
def admin_ficha_estudiante_list2(request,estudiante_id,initial=None,final=None,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)

    if profile.group_id !=0 :
        if page == None:
            page = request.GET.get('page')
        else:
            page = page
        if request.GET.get('page') == None:
            page = page
        else:
            page = request.GET.get('page')
        
        if initial == None or final == None:
            initial = request.POST.get('date_initial')
            final = request.POST.get('date_final')
        else:
            initial = initial
            final = final

        if request.POST.get('date_initial') == None or request.POST.get('date_final')== None:
            initial = initial
            final = final
        else:
            initial = request.POST.get('date_initial')
            final = request.POST.get('date_final')

        if request.method == 'POST':
            initial = request.POST.get('date_initial')
            final = request.POST.get('date_final')
            page = None

        h_list = []

        estudiante = Estudiante.objects.get(pk=estudiante_id)
        h_list_array_count = Detalle_atencion.objects.filter(estudiante_id=estudiante).count()

        if initial == None or initial == "" or final == None or final == "":
            h_list_array = Detalle_atencion.objects.filter(estudiante_id=estudiante).order_by('id')
            for h in h_list_array:
                paciente= Paciente.objects.get(pk=h.paciente_id)
                h_list.append({'id':h.id,'nombre_paciente':paciente.nombre,'nombre_estudiante':estudiante.nombre,'fecha_eval':h.fecha_eval})
        else:
            if initial > final:
                inicio = final
                ultimo = initial
                initial = inicio
                final = ultimo
                
            h_list_array = Detalle_atencion.objects.filter(estudiante_id=estudiante_id).filter(fecha_eval__range=(initial,final)).order_by('id')
            h_list_array_count = Detalle_atencion.objects.filter(estudiante_id=estudiante_id).filter(fecha_eval__range=(initial,final)).count()
            for h in h_list_array:
                paciente= Paciente.objects.get(pk=h.paciente_id)
                h_list.append({'id':h.id,'nombre_paciente':paciente.nombre,'nombre_estudiante':estudiante.nombre,'fecha_eval':h.fecha_eval})

        paginator = Paginator(h_list, 5)
        h_list_paginate= paginator.get_page(page)
        template_name = 'ficha/admin_ficha_estudiante_list2.html'
        return render(request,template_name,{'profile':profile,'h_list_array_count':h_list_array_count,'estudiante_data':estudiante,
        'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'initial':initial,'final':final})

@login_required
def admin_ficha_estudiante_ver(request,estudiante_id,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        ficha_data = Detalle_atencion.objects.get(pk=ficha_id)
        
        estudiante_data = Estudiante.objects.get(pk = estudiante_id)
        paciente_data = Paciente.objects.get(pk= ficha_data.paciente_id)
        calificacion_data = Calificacion.objects.get(ficha_id=ficha_data.id)

        disciplina_all = Disciplina.objects.all()
        discapacidad_all = Discapacidad.objects.all()
        results = Paciente.objects.filter(pk=ficha_data.paciente_id)

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

        template_name = 'ficha/admin_ficha_estudiante_ver.html'
        return render(request,template_name,{'profile':profile,'template_name' : 'ficha/ficha_edit.html',
        'ficha_data':ficha_data,'paciente_data':paciente_data,'disciplina_data':disciplina,'discapacidad_data':discapacidad,
        'estudiante_data':estudiante_data,'calificacion_data':calificacion_data})
    except Detalle_atencion.DoesNotExist:
        return redirect('admin_ficha_estudiante_list2',estudiante_id)
    except Calificacion.DoesNotExist:
        disciplina_all = Disciplina.objects.all()
        discapacidad_all = Discapacidad.objects.all()
        results = Paciente.objects.filter(pk=ficha_data.paciente_id)

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

        template_name = 'ficha/admin_ficha_estudiante_ver.html'
        return render(request,template_name,{'profile':profile,'template_name' : 'ficha/ficha_edit.html',
        'ficha_data':ficha_data,'paciente_data':paciente_data,'disciplina_data':disciplina,'discapacidad_data':discapacidad,
        'estudiante_data':estudiante_data})
        
@login_required
def calificacion_ver(request,page=None,search=None):
   profile = Profile.objects.get(user_id=request.user.id)
   if profile.group_id !=0:
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
        estudiantes = Estudiante.objects.get(user_id=request.user.id)

        h_count = Detalle_atencion.objects.filter(estudiante_id=estudiantes.id).count()
        if search == None or search == "None":
            h_list_array = Detalle_atencion.objects.filter(estudiante_id=estudiantes.id).order_by('id')
            for h in h_list_array:
                paciente = Paciente.objects.get(pk=h.paciente_id)
                try:
                    calificacion = Calificacion.objects.get(ficha_id=h.id)
                    h_list.append({'id':h.id,'nombre_paciente':paciente.nombre,'fecha_eval':h.fecha_eval,'calificacion':calificacion.nota})
                except Calificacion.DoesNotExist:
                    h_list.append({'id':h.id,'nombre_paciente':paciente.nombre,'fecha_eval':h.fecha_eval})
        else:
            h_list_array = Detalle_atencion.objects.filter(estudiante_id=estudiantes.id).order_by('id')
            for h in h_list_array:
                paciente = Paciente.objects.get(pk=h.paciente_id)
                pacie = Paciente.objects.all().filter(nombre__icontains=search).order_by('nombre')
                for p in pacie:
                    if p.rut == paciente.rut:
                        try:
                            calificacion = Calificacion.objects.get(ficha_id=h.id)
                            h_list.append({'id':h.id,'nombre_paciente':paciente.nombre,'fecha_eval':h.fecha_eval,'calificacion':calificacion.nota})
                        except Calificacion.DoesNotExist:
                            h_list.append({'id':h.id,'nombre_paciente':paciente.nombre,'fecha_eval':h.fecha_eval})
                
        h_list_array_count = len(h_list)

        paginator = Paginator(h_list, 5)
        h_list_paginate= paginator.get_page(page)
        template_name = 'ficha/calificaciones.html'
        return render(request,template_name,{'profile':profile,'h_list_array_count':h_list_array_count,
        'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search,'estudiantes':estudiantes,'h_count':h_count})

@login_required
def calificacion_ficha_ver(request,ficha_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id == 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    try:
        estudiante = Estudiante.objects.get(user_id=request.user.id)
        ficha_data = Detalle_atencion.objects.filter(estudiante_id=estudiante.id).get(pk=ficha_id)
        paciente_data = Paciente.objects.get(pk=ficha_data.paciente_id)
        calificacion = Calificacion.objects.get(ficha_id=ficha_data.id)
        template_name = 'ficha/calificaciones_ficha_ver.html'
        return render(request,template_name,{'profile':profile,'template_name' : 'ficha/calificaciones_ficha_ve',
        'ficha_data':ficha_data,'paciente_data':paciente_data,'calificacion_data':calificacion})
    except Detalle_atencion.DoesNotExist:
        return redirect('ficha_list')
    except BaseException:
        return redirect('ficha_list')