from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect,HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from .models import *
import pandas as pd
from .forms import *
import sqlite3
from sqlite3 import Error
import urllib.request, json
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse


hoy = date.today()
ahora = hoy.strftime('%Y-%m-%d %H:%M:%S')


database_name = settings.DATABASES['default']['NAME']
con = sqlite3.connect(database_name, check_same_thread=False)
cur = con.cursor()



@login_required(login_url="/login/")
def index(request):
    template_name = 'index.html'
    user = request.user
    grupo = request.user.groups.all()[0].name
    if grupo == 'administradores':
        asesores = Ventas.objects.exclude(scoring__isnull=True).exclude(scoring='')
    else:
        asesores = Ventas.objects.exclude(scoring__isnull=True).exclude(scoring='').filter(asesor_id=user)
    despacho = Ventas.objects.filter(aprobacion_backoffice=1, entrega_sim=0)
    backoffice = Ventas.objects.filter(aprobacion_backoffice=0,supervisor=1,scoring='APROBADO')
    scoring = Ventas.objects.filter(scoring__exact='')  # .filter(scoring='')
    cobertura = Ventas.objects.filter(tipo_venta='FIJA', scoring__isnull=False)  # .filter()
    #aprob_venta = Ventas.objects.filter()
    return render(request, template_name, {'asesores': asesores,
                                           'scoring':scoring,
                                           'cobertura':cobertura,
                                           'grupo':grupo,
                                           'backoffice':backoffice,
                                           'despacho':despacho
                                           }
                  )


"""def index(request):
    context = {}
    context['segment'] = 'index'
    context['asesores'] = Ventas.objects.exclude(scoring__isnull=True).exclude(scoring='')
    context['scoring'] = Ventas.objects.filter(scoring__isnull=True)#.filter(scoring='')
    print(context['scoring'])
    context['cobertura'] = Ventas.objects.filter(tipo_venta='FIJA',scoring=0)#.filter()
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))
"""

def Busqueda_Cedula(request):
    template_name = 'Ventas/Busqueda_Cedula.html'
    Doc_Cliente = request.POST.get('Doc_Cliente')
    if Doc_Cliente:
        if request.method == 'POST' and 'buscarc':
            ventas = Ventas.objects.filter(numero_documento=Doc_Cliente)
            Doc_input = Cliente.objects.filter(numero_documento=Doc_Cliente)
            #Agregar validación de usuarios para solamente mostrar
            print(ventas,Doc_input)
            return render(request, template_name,
                  {
                      'Doc_input': Doc_input,
                      'ventas':ventas
                      }
                      )
    return render(request, template_name)


class Crear_cliente(SuccessMessageMixin,CreateView):
    form_class = ClienteDocForm
    template_name = 'Ventas/crear_cliente.html'
    #success_url = "/Busqueda_Cedula"
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            numero_documento=self.object.calculated_field,
        )

    def form_valid(self, form):
        numero_documento = form.cleaned_data['numero_documento']
        tipo_doc = form.cleaned_data['tipo_documento']
        asesor_id = self.request.user
        print(asesor_id)
        #Doc_Num_Form = form['Doc_Num_Form'].cleaned_data['numero_documento']
        ClienteDocForm = form.save(commit=False)
        ClienteDocForm.numero_documento_id = numero_documento
        ClienteDocForm.asesor_id = asesor_id.id
        doc_num_df = pd.DataFrame({"numero_documento": [numero_documento],
                                   "tipo_documento":[tipo_doc],
                                     "fecha_ingreso": [hoy],
                                  "asesor":asesor_id.id,
                                   #"scoring":''
                                   }
                                  )

        try:
            doc_num_df.to_sql('Ventas_cliente', con, if_exists='append', index=False)
        except Error:
            messages.success(self.request, 'El cliente ya se encuentra ingresado al sistema.')
        else:
            #doc_num_df['numero_documento'].to_sql('Ventas_Ventas_direccion_domicilio', con, if_exists='append', index=False)
            form.asesorid = asesor_id.id
            form.save()
            messages.success(self.request, "Se inicio proceso de venta con el cliente con "+tipo_doc+' '+str(numero_documento)+" satisfactoriamente!")
        #else:
        #print(Doc_Num_Form)
        #ClienteDocForm = form['ClienteDocForm'].save(commit=False)
        #ClienteDocForm.numero_documento_id = numero_documento
        #ClienteDocForm.save()
            return redirect('/cliente/'+str(numero_documento))

        return redirect('/')


class scoring(UpdateView):
    model = Cliente
    second_model = Ventas
    cl_v_update = Ventas
    form_class = scoringform
    #second_form_class = scoringform
    template_name = 'Ventas/scoring.html'
    success_url = "/"
    def get_context_data(self, **kwargs):
        pk = int(self.kwargs.get('pk'))
        context = super(scoring, self).get_context_data(**kwargs)
        context['documento'] = self.second_model.objects.get(numero_documento=pk)  # , scoring=1)
        # context['cl_v_update'] = self.cl_v_update.objects.get(cliente=pk)
        # print(context)
        #if 'form2' not in context:
            #context['form2'] = self.second_form_class(self.request.GET)
        return context


    def form_valid(self, form):
        numero_documento = form.cleaned_data['numero_documento']
        scoring = form.cleaned_data['scoring']
        """if scoring == True:
            scoring = 1
        else:
            scoring = 0"""
        scoring_sql = ("UPDATE Ventas_ventas SET scoring='"+str(scoring)+"' WHERE entrega_sim=0 and numero_documento_id ="+str(numero_documento))
        print(scoring_sql)
        try:
            cur.execute(scoring_sql)
            con.commit()
        except:
            print(Error)
        else:
            form.save()
        return redirect('/')


class ClienteFormView(UpdateView):
    model = Cliente
    second_model = Ventas
    cl_v_update = Ventas
    form_class = ClienteForm
    #second_form_class = ClienteForm#direccion_domicilio_form
    template_name = 'Ventas/cliente_form.html'
    success_url = "/Busqueda_Cedula"
    def get_context_data(self, **kwargs):
        pk = int(self.kwargs.get('pk'))
        context = super(ClienteFormView, self).get_context_data(**kwargs)
        context['documento'] = self.second_model.objects.get(numero_documento=pk)#, scoring=1)
        domicilio = Ventas.objects.filter(tipo_venta='FIJA').filter(numero_documento=pk)#, scoring=1)
        """if domicilio:
            context['form2'] = self.second_form_class(self.request.GET)
        else:
            if 'form' not in context:
                context['form'] = self.second_form_class(self.request.GET)"""
        return context


class VentaView(UpdateView):
    model = Cliente
    second_model = Ventas
    form_class = Cliente_Venta_Form
    second_form_class = VentaForm
    template_name = 'Ventas/venta.html'
    success_url = "/Busqueda_Cedula"
    def get_context_data(self, **kwargs):
        pk = int(self.kwargs.get('pk'))
        context = super(VentaView, self).get_context_data(**kwargs)
        context['documento'] = self.second_model.objects.get(numero_documento_id=pk,celular__isnull=True)
        numero_documento_id = Ventas.objects.get(numero_documento_id=pk, celular__isnull=True)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET,instance=pk)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET,instance=numero_documento_id)
        print(context['form2'])
        return context

    def post(self, request, *args, **kwargs):
        pk = int(self.kwargs.get('pk'))
        venta_id = Ventas.objects.get(numero_documento_id=pk)
        cliente_id = Cliente.objects.get(numero_documento=pk)
        form = self.form_class(request.POST, instance=cliente_id)
        form2 = VentaForm(request.POST or None, instance=venta_id)
        direccion_entrega = self.request.POST.get('direccion_entrega')
        departamento_domicilio = self.request.POST.get('departamento_domicilio')
        municipi_domicilio = self.request.POST.get('municipi_domicilio')
        if form.is_valid() and form2.is_valid():
            fs = form.save(commit=False)
            fs.deptartamento_domicilio_id = departamento_domicilio
            fs.municipi_domicilio_id = municipi_domicilio
            fs.sector_1 = self.request.POST.get('sector_1')
            fs.sector_2 = self.request.POST.get('sector_2')
            fs.detalle_1_opc = self.request.POST.get('detalle_1_opc')
            fs.detalle_1 = self.request.POST.get('detalle_1')
            fs.detalle_2_opc = self.request.POST.get('detalle_2_opc')
            fs.detalle_2 = self.request.POST.get('detalle_2')
            fs.avenida_1 = self.request.POST.get('avenida_1')
            fs.avenida_2 = self.request.POST.get('avenida_2')
            fs.numero_1 = self.request.POST.get('numero_1')
            fs.letra_1 = self.request.POST.get('letra_1')
            fs.numero_2 = self.request.POST.get('numero_2')
            fs.letra_2 = self.request.POST.get('letra_2')
            aprobacion = self.request.POST.get('aprobacion')
            v_token = venta_token.objects.all()[0].venta_token
            fs = form.save()
            #form.save()
            fs2 = form2.save(commit=False)
            fs2.supervisor = 0
            fs2 = form.save()
            """if aprobacion == str(v_token):
                print('aprobacion de supervisor ingresada satisfactoriamente')
                fs = form.save()
            else:
                print('aprobacion de supervisor no valida')
            if direccion_entrega == 'on':
                fs.deptartamento_domicilio_id = departamento_domicilio
                fs.municipi_domicilio_id = municipi_domicilio
                fs.sector_1 = self.request.POST.get('sector_1')
                fs.sector_2 = self.request.POST.get('sector_2')
                fs.detalle_1_opc = self.request.POST.get('detalle_1_opc')
                fs.detalle_1 = self.request.POST.get('detalle_1')
                fs.detalle_2_opc = self.request.POST.get('detalle_2_opc')
                fs.detalle_2 = self.request.POST.get('detalle_2')
                fs.avenida_1 = self.request.POST.get('avenida_1')
                fs.avenida_2 = self.request.POST.get('avenida_2')
                fs.numero_1 = self.request.POST.get('numero_1')
                fs.letra_1 = self.request.POST.get('letra_1')
                fs.numero_2 = self.request.POST.get('numero_2')
                fs.letra_2 = self.request.POST.get('letra_2')
            else:
                aprobacion = self.request.POST.get('aprobacion')
                v_token = venta_token.objects.all()[0].venta_token
                print(v_token)
                if aprobacion == str(v_token):
                    print('aprobacion de supervisor ingresada satisfactoriamente')
                    fs = form.save()
                else:
                    print('aprobacion de supervisor no valida')
                    form.save()
                    form2.save()
            return redirect('/')
            try:
                form.save()
            except:
                print('formulario1 invalido')
            else:
                print('formulario1 guardado')
            """
            messages.success(self.request, 'Venta creada satisfactoriamente')
            return HttpResponseRedirect(self.get_success_url())
        """else:
            try:
                form2.save()
            except:
                print('formulario2 invalido')
            else:
                form2.save()
                print('formulario2 guardado')"""
        return redirect('/')


"""
    def form_valid(self, form):
        dir_dom = form.cleaned_data['direccion_entrega']
        print(dir_dom, 'dfghjiuytrfdfcvbhytfcvbnjytfcvbjytfvhju765rfghjui9876543e4r5t67890o9iuyhgfcghyu')
        if form.is_valid():
            form.save()
        return redirect('/')
        
        
        
        ##################

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        print(request.POST)
        # request.POST['some_key'] = 'some_value'
        return super(VentaView, self).post(request, **kwargs)


    def form2_valid(self, form2):
        if form2.is_valid():
            # print(form2.cleaned_data)
            form2.save()
            sector_1 = form2.cleaned_data['sector_1']
            sector_2 = form2.cleaned_data['sector_2']
            detalle_1_opc = form2.cleaned_data['detalle_1_opc']
            detalle_1 = form2.cleaned_data['detalle_1']
            detalle_2_opc = form2.cleaned_data['detalle_2_opc']
            detalle_2 = form2.cleaned_data['detalle_2']
            avenida_1 = form2.cleaned_data['avenida_1']
            avenida_2 = form2.cleaned_data['avenida_2']
            numero_1 = form2.cleaned_data['numero_1']
            letra_1 = form2.cleaned_data['letra_1']
            numero_2 = form2.cleaned_data['numero_2']
            letra_2 = form2.cleaned_data['letra_2']
            primer_nombre = form2.cleaned_data['primer_nombre']
            segundo_nombre = form2.cleaned_data['segundo_nombre']
            apellidos = form2.cleaned_data['apellidos']
            fecha_nacimiento = form2.cleaned_data['fecha_nacimiento']
            fecha_expedicion = form2.cleaned_data['fecha_expedicion']
            email = form2.cleaned_data['email']
            celular = form2.cleaned_data['celular']
            telefono = form2.cleaned_data['telefono']
            departamento = form2.cleaned_data['departamento']
            municipio = form2.cleaned_data['municipio']
            sector = form2.cleaned_data['sector']
            direccion = form2.cleaned_data['direccion']
            cliente_df = pd.DataFrame({
                'sector_1': [sector_1],
                'sector_2': [sector_2],
                'detalle_1_opc': [detalle_1_opc],
                'detalle_1': [detalle_1],
                'detalle_2_opc': [detalle_2_opc],
                'detalle_2': [detalle_2],
                'avenida_1': [avenida_1],
                'avenida_2': [avenida_2],
                'numero_1': [numero_1],
                'letra_1': [letra_1],
                'numero_2': [numero_2],
                'letra_2': [letra_2],
                'primer_nombre': [primer_nombre],
                'segundo_nombre': [segundo_nombre],
                'apellidos': [apellidos],
                'fecha_nacimiento': [fecha_nacimiento],
                'fecha_expedicion': [fecha_expedicion],
                'email': [email],
                'celular': [celular],
                'telefono': [telefono],
                'sector': [sector],
                'direccion': [direccion],
                'fecha_modificado': [ahora],
                'departamento_id': [departamento],
                'municipio_id': [municipio],
                # 'nombres':[nombres]
            })
            cliente_df['primer_nombre'] = cliente_df['primer_nombre'].str.upper()
            cliente_df['segundo_nombre'] = cliente_df['segundo_nombre'].str.upper()
            cliente_df['nombres'] = cliente_df['primer_nombre'] + ' ' + cliente_df['segundo_nombre']
            cliente_df['nombres'] = cliente_df['nombres'].str.upper()
            cliente_df['apellidos'] = cliente_df['apellidos'].str.upper()
            print(cliente_df)
            # cliente_df['fecha_modificado'] = datetime.now()
            # cliente_df.str.upper()
            print(cliente_df)
            cols = ",".join([str(i) for i in cliente_df.columns.to_list()])
            # cargues_efectivos = []
            for index, row in cliente_df.iterrows():
                try:
                    sql = "INSERT OR REPLACE INTO ventas_cliente (" + cols + ") VALUES " + str(tuple(row))
                    print(sql)
                    con.execute(sql)
                except Error:
                    messages.warning('EL cliente "' + id + '" ya existe en listas blancas')
                else:
                    con.commit()
            # cliente_df.to_sql('Ventas_cliente', con, if_exists='append', index=False)
            # print(request.user.username)
            fs = form2.save(commit=False)
            fs.asesor = self.request.user
            # print(fs.asesor)
            fs.save()
            #
            # print(Error)
            # return HttpResponseRedirect('/Busqueda_Cedula/')
            print(form2.errors)
            print(Error)
        else:
            print('hueputa, porque no guarda?')
            print(Error)
            print(form2.errors)
        # return HttpResponseRedirect('/Busqueda_Cedula/')
        return redirect('/')


###################################
class VentaView(UpdateView):
    model = Cliente
    second_model = Ventas
    form_class = VentaForm1
    second_form_class = VentaForm
    template_name = 'Ventas/venta.html'
    success_url = "/Busqueda_Cedula"

    def get_context_data(self, **kwargs):
        pk = int(self.kwargs.get('pk'))
        context = super(VentaView, self).get_context_data(**kwargs)
        context['documento'] = self.second_model.objects.get(numero_documento_id=pk)
        print(self.second_model.objects.get(numero_documento_id=pk))
        #context['cl_v_update'] = self.cl_v_update.objects.get(cliente=pk)
        return context

    def get_form_kwargs(self):
        print(self.object.numero_documento)
        kwargs = super(VentaView, self).get_form_kwargs()
        kwargs.update(instance={
            'Cliente_Venta_Form': self.object,
            'VentaForm': self.object.numero_documento,
        })
        return kwargs

    def form_valid(self, form):
        dir_dom = form.cleaned_data['direccion_entrega']
        print(dir_dom,'dfghjiuytrfdfcvbhytfcvbnjytfcvbjytfvhju765rfghjui9876543e4r5t67890o9iuyhgfcghyu')
        if form.is_valid():
            form.save()
        return redirect('/')
"""



"""
        if form.is_valid():
            try:
                form.save()
                print('pojwnfvowanvpoin2q9u4gf20i34gb30unof2ivrbfe0iwbn rqwgvun3q0i92¿nm0'+form)
            except:
                print(Error)
                print('ahjbcasbcvhjasbvjbasdvkjbaskjvbaslkjvbaslkjvbjk')
        else:
            print('formulario errado')
            '''celular = form2.cleaned_data['celular']
        numero_documento = form2.cleaned_data['numero_documento']
        venta_df = pd.DataFrame({"cliente_id": [numero_documento],
                                     "fecha_venta": [ahora],
                              "celular":[celular]})
        print(venta_df)
        try:
            venta_df.to_sql('Ventas_ventas', con, if_exists='append', index=False)
        except Error:
            messages.success(self.request, "ya se encuentra un plan asociado al numero de celular:  "+str(celular))
            return redirect('/cliente/'+str(numero_documento))
        else:'''
        #form2.save()
        return redirect('/')



    #########
    def form_valid(self, form2):
        print(form2)
        print('ahjbcasbcvhjasbvjbasdvkjbaskjvbaslkjvbaslkjvbjk')

        if form2.is_valid():
            try:
                print(form2)
                form2.save()
            except:
                print(Error)
        else:
            print(form2)
        celular = form2.cleaned_data['celular']
        numero_documento = form2.cleaned_data['numero_documento']
        venta_df = pd.DataFrame({"cliente_id": [numero_documento],
                                     "fecha_venta": [ahora],
                              "celular":[celular]})
        print(venta_df)
        try:
            venta_df.to_sql('Ventas_ventas', con, if_exists='append', index=False)
        except Error:
            messages.success(self.request, "ya se encuentra un plan asociado al numero de celular:  "+str(celular))
            return redirect('/cliente/'+str(numero_documento))
        else:
            form2.save()
        return redirect('/')


##########################################
class VentaView(CreateView):
    model = Ventas
    form_class = VentaForm
    template_name = 'Ventas/venta.html'

    def form_valid(self, form):
        celular = form.cleaned_data['celular']
        print(celular)
        form.save()
        return redirect('/aprobacionbo/'+str(celular))
"""

"""
def VentaView(request, id):
    template_name = 'Ventas/venta.html'
    context = {}
    obj = get_object_or_404(Cliente.objects.filter(numero_documento=id))
    #obj2 = get_object_or_404(Ventas.objects.filter(numero_documento_id=id).last()) #.filter(celular__isnull=True))
    obj2 = get_object_or_404(Ventas, numero_documento_id=id, celular__isnull=True)
    print(obj)
    print(obj2)
    # pass the object as instance in form
    form = Cliente_Venta_Form(request.POST or None, instance=obj)
    form2 = VentaForm(request.POST or None, instance=obj2)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid() or form2.is_valid():
        #form.save()
        form2.save()
        return HttpResponseRedirect("/")

    # add form dictionary to context
    context["form"] = form
    context["form2"] = form2
    #context["documento"] = Ventas.objects.filter(celular__isnull=True,numero_documento=id)
    for p in Ventas.objects.raw("select * from Ventas_ventas where numero_documento_id="+id+" and celular is NULL"):
        print(p)
    analista = request.user
    #print(context["documento"])
    #context['asignados'] = Cliente.objects.filter(ANALISTA=analista).filter(numero_documento=id)

    return render(request,template_name, context)
"""

class BackOfficeView(UpdateView):
    model = Ventas
    second_model = Cliente
    cl_v_update = Ventas
    form_class = BackofficeForm
    # second_form =
    template_name = 'Ventas/aprobacionbo.html'

    # success_url = "#"

    def get_context_data(self, **kwargs):
        pk = int(self.kwargs.get('pk'))
        context = super(BackOfficeView, self).get_context_data(**kwargs)
        context['documento'] = self.model.objects.get(celular=pk)
        print(context['documento'])
        # context['cl_v_update'] = self.cl_v_update.objects.get(cliente=pk)
        print(context)
        return context

    def form_valid(self, form):
        """celular = form.cleaned_data['celular']
        numero_documento = form.cleaned_data['numero_documento']
        venta = pd.DataFrame({"cliente_id": [numero_documento],
                              "fecha_venta": [ahora],
                              "celular": [celular]})
        try:
            venta.to_sql('Ventas_ventas', con, if_exists='append', index=False)
        except Error:
            messages.success(self.request, "ya se encuentra un plan asociado al numero de celular:  " + str(celular))
            return redirect('/venta/' + str(celular))
        else:
        form.save()
        return redirect('/')
        """

    def form_valid(self, form):
        #celular = form.cleaned_data['celular']
        form.save()
        return redirect('/')
        #return redirect('/despachosim/'+str(celular))


class despachoView(UpdateView):
    model = Ventas
    form_class = MensajeriaDespacho
    template_name = 'Ventas/despachosim.html'
    def form_valid(self, form):
        celular = form.cleaned_data['celular']
        form.save()
        return redirect('/entregasim/'+str(celular))


class entregasimView(UpdateView):
    model = Ventas
    form_class = MensajeriaEntrega
    template_name = 'Ventas/entregasim.html'

    def form_valid(self, form):
        celular = form.cleaned_data['celular']
        form.save()
        return redirect('/')


"""
def ClienteFormView(request, id):
    model = Cliente
    second_model = Cliente_Doc
    form_class = ClienteForm
    #second_form_class = ClienteDocForm2
    template_name = 'Ventas/cliente_form.html'
    context = {}
    obj1 = get_object_or_404(model, pk=id)
    #obj2 = get_object_or_404(Cliente_Doc, pk=id)
    context['documento'] = second_model.objects.get(numero_documento=id)
    #context["cliente"] = model.objects.get(numero_documento=id)

    form = form_class(request.POST or None, instance=obj1)
    context["form"] = form

    if form.is_valid():
        form.save()
        sector_1 = form.cleaned_data['sector_1']
        sector_2 = form.cleaned_data['sector_2']
        detalle_1_opc = form.cleaned_data['detalle_1_opc']
        detalle_1 = form.cleaned_data['detalle_1']
        detalle_2_opc = form.cleaned_data['detalle_2_opc']
        detalle_2 = form.cleaned_data['detalle_2']
        avenida_1 = form.cleaned_data['avenida_1']
        avenida_2 = form.cleaned_data['avenida_2']
        numero_1 = form.cleaned_data['numero_1']
        letra_1 = form.cleaned_data['letra_1']
        numero_2 = form.cleaned_data['numero_2']
        letra_2 = form.cleaned_data['letra_2']
        primer_nombre = form.cleaned_data['primer_nombre']
        segundo_nombre = form.cleaned_data['segundo_nombre']
        apellidos = form.cleaned_data['apellidos']
        fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
        fecha_expedicion = form.cleaned_data['fecha_expedicion']
        email = form.cleaned_data['email']
        celular = form.cleaned_data['celular']
        telefono = form.cleaned_data['telefono']
        departamento = form.cleaned_data['departamento']
        municipio = form.cleaned_data['municipio']
        sector = form.cleaned_data['sector']
        direccion = form.cleaned_data['direccion']
        cliente_df = pd.DataFrame({
            'sector_1': [sector_1],
            'sector_2': [sector_2],
            'detalle_1_opc': [detalle_1_opc],
            'detalle_1': [detalle_1],
            'detalle_2_opc': [detalle_2_opc],
            'detalle_2': [detalle_2],
            'avenida_1': [avenida_1],
            'avenida_2': [avenida_2],
            'numero_1': [numero_1],
            'letra_1': [letra_1],
            'numero_2': [numero_2],
            'letra_2': [letra_2],
            'primer_nombre': [primer_nombre],
            'segundo_nombre': [segundo_nombre],
            'apellidos': [apellidos],
            'fecha_nacimiento': [fecha_nacimiento],
            'fecha_expedicion': [fecha_expedicion],
            'email': [email],
            'celular': [celular],
            'telefono': [telefono],
            'sector': [sector],
            'direccion':[direccion],
            'fecha_modificado':[ahora],
            'departamento_id': [departamento],
            'municipio_id': [municipio],
            #'nombres':[nombres]
        })
        cliente_df['primer_nombre'] = cliente_df['primer_nombre'].str.upper()
        cliente_df['segundo_nombre'] = cliente_df['segundo_nombre'].str.upper()
        cliente_df['nombres'] = cliente_df['primer_nombre']+' '+cliente_df['segundo_nombre']
        cliente_df['nombres'] = cliente_df['nombres'].str.upper()
        cliente_df['apellidos'] = cliente_df['apellidos'].str.upper()
        print(cliente_df)
        #cliente_df['fecha_modificado'] = datetime.now()
        #cliente_df.str.upper()
        print(cliente_df)
        cols = ",".join([str(i) for i in cliente_df.columns.to_list()])
        #cargues_efectivos = []
        for index, row in cliente_df.iterrows():
            try:
                sql = "INSERT OR REPLACE INTO ventas_cliente (" + cols + ") VALUES " + str(tuple(row))
                print(sql)
                con.execute(sql)
            except Error:
                messages.warning(request, ('EL cliente "'+id+'" ya existe en listas blancas'))
            else:
                con.commit()
        #cliente_df.to_sql('Ventas_cliente', con, if_exists='append', index=False)
        #print(request.user.username)
        fs = form.save(commit=False)
        fs.asesor = self.request.user
        #print(fs.asesor)
        fs.save()
        #
        #print(Error)
        #return HttpResponseRedirect('/Busqueda_Cedula/')
        print(form.errors)
        print(Error)
    else:
        print(request.user.username,'hueputa, porque no guarda?')
        print(Error)
        print(form.errors)
    #return HttpResponseRedirect('/Busqueda_Cedula/')
    return render(request, template_name, context)


class PersonUpdateView(UpdateView):
    #model = Cliente
    #form_class = Venta_Form
    success_url = reverse_lazy('home')


class ClienteFormView(UpdateView):
    model = Cliente
    second_model = Cliente_Doc
    form_class = ClienteForm
    second_form_class = ClienteDocForm2
    template_name = 'Ventas/cliente_form.html'
    def get_context_data(self, **kwargs):
        context = super(ClienteFormView, self).get_context_data(**kwargs)
        pk = int(self.kwargs.get('pk'))
        context['documento'] = self.second_model.objects.get(numero_documento=pk)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def get(self, request, *args, **kwargs):
        super(ClienteFormView, self).get(request, *args, **kwargs)
        form = self.form_class
        form2 = self.second_form_class
        return self.render_to_response(self.get_context_data(
            object=self.object, form=form, form2=form2))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            nombre = form.cleaned_data['primer_nombre']
            print(nombre)
            #userdata = form.save(commit=False)
            #userdata.save()
            form2 = form2.save(commit=False)
            form2.save()
            messages.success(self.request, 'Settings saved successfully')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2))
    def get_success_url(self):
        return reverse('client_list')
#############################333
class ClienteFormView(UpdateView):
    model = Cliente
    second_model = Cliente_Doc
    form_class = Clienteform
    template_name = 'Ventas/cliente_form.html'
    success_url = "/Busqueda_Cedula"

    def get_context_data(self, **kwargs):
        pk = int(self.kwargs.get('pk'))
        context = super(ClienteFormView, self).get_context_data(**kwargs)
        context['documento'] = self.second_model.objects.get(numero_documento=pk)
        return context

    def form_valid(self, form):
        try:
            print(form)
            form.save()
        except print(form):
            return redirect('/Busqueda_Cedula/')
        else:
            #if form.is_valid():
            print(form)
            #else:
            print(form,"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        numero_documento = form.cleaned_data['numero_documento']
        documento2 = form.cleaned_data['documento2']
        documento3 = form.cleaned_data['documento3']
        print(numero_documento,documento2,documento3,"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        #Doc_Num_Form.to_sql('Ventas_cliente', con, if_exists='append', index=False)
        return HttpResponseRedirect(reverse('Busqueda_Cedula'))



    
class MyView(UpdateView):
    template_name = 'Ventas/cliente_form.html'
    form_class = Doc_Form
    second_form_class = Form2
    success_url = "/Busqueda_Cedula"

    def get_context_data(self, **kwargs):
        context = super(MyView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(initial={'some_field': context['model'].some_field})
        if 'form2' not in context:
            context['form2'] = self.second_form_class(initial={'another_field': context['model'].another_field})
        return context

    def get_object(self):
        return get_object_or_404(Model, pk=self.request.session['someval'])

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):

        # get the user instance
        self.object = self.get_object()

        # determine which form is being submitted
        # uses the name of the form's submit button
        if 'form' in request.POST:

            # get the primary form
            form_class = self.get_form_class()
            form_name = 'form'

        else:

            # get the secondary form
            form_class = self.second_form_class
            form_name = 'form2'

        # get the form
        form = self.get_form(form_class)

        # validate
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})

#####################################
class ClienteFormView(UpdateView):
    model = Cliente
    form_class = Doc_Form
    template_name = 'Ventas/cliente_form.html'
    success_url = "/Busqueda_Cedula"

    def get_form_kwargs(self):
        kwargs = super(ClienteFormView, self).get_form_kwargs()
        kwargs.update(instance={
            'Doc_Num_Form': self.object,
            'ClienteDocForm': self.object.numero_documento,
        })
        return kwargs









#######################33
class ClienteFormView(UpdateView):
    model = Cliente
    second_model = Cliente_Doc
    form_class = Doc_Form
    template_name = 'Ventas/cliente_form.html'
    success_url = "/Busqueda_Cedula"

    def get_context_data(self, **kwargs):
        pk = int(self.kwargs.get('pk'))
        context = super(ClienteFormView, self).get_context_data(**kwargs)
        context['documento'] = self.second_model.objects.get(numero_documento=pk)
        return context

    def form_valid(self, form):
        try:
            print(form)
            form.save()
        except print(form):
            return redirect('/Busqueda_Cedula/')
        else:
            #if form.is_valid():
            print(form)
            #else:
            print(form,"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        numero_documento = form.cleaned_data['numero_documento']
        documento2 = form.cleaned_data['documento2']
        documento3 = form.cleaned_data['documento3']
        print(numero_documento,documento2,documento3,"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        #Doc_Num_Form.to_sql('Ventas_cliente', con, if_exists='append', index=False)
        return HttpResponseRedirect(reverse('Busqueda_Cedula'))


class Clienteform(UpdateView):
    model = Cliente
    form_class = Clienteform
    template_name = 'Ventas/cliente_form.html'
#######

def Clienteform(request, id):
    obj = get_object_or_404(Cliente, pk=id)
    form = Clienteform(request.POST, instance=obj)
    documento = Cliente_Doc.objects.get(pk=id)
    if request.method == 'POST':
        if form.is_valid():
            #Cliente.objects.filter(documento=id).update(documento='Manzana Fuji')
            form.save()
            return HttpResponseRedirect("/C_search/")

    return render(request, 'Ventas/cliente_form.html',
                  {
        'form':form,
    'documento':documento
    }
                  )


def Ventas_form(request):
    #client = models.Client.objects.get(pk = client_id)
    #notes = client.note_set.all()
    if request.method == 'POST':
        form = Venta_Form(request.POST)
        if form.is_valid():
            form.save(True)
            request.user.message_set.create(message = "Note is successfully added.")
            return render(request, "home")
    else:
        form = Venta_Form()
    return render(request, "home")







    class Ventas_form(CreateView):
    #model = Cliente
    model = Cliente
    form_class = Venta_Form
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(Ventas_form, self).form_valid(form)

def load_cities(request):
    depto_id = request.GET.get('depto')
    tipo_plan_id = request.GET.get('tipo_plan')
    cities = Ciudad.objects.filter(depto_id=depto_id).order_by('nombre')
    planes = Plan.objects.filter(tipo_plan_id=tipo_plan_id).order_by('nombre')

    return render(request, 'Ventas/city_dropdown_list_options.html',
                  {'cities': cities,
                   'planes':planes,
                   })





    else:
        return render(request, 'index.html',
                      {
                          'Doc_Cliente': Doc_Cliente
                      }
                      )


    if request.method=="POST":
        cur.execute("DELETE FROM app_temporal_detalles;")
        cur.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='app_temporal_detalles';")
        cur.execute("DELETE FROM app_temporal_tablas;")
        cur.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='app_temporal_tablas';")

        return render(request, 'index_asesor.html',
                      {
            #####===Backoffice_Fija===#####
            'Backoffice_Fija_Template':Backoffice_Fija_Template,
            'Consulta_GVP': Consulta_GVP,
            'Regularizacion_de_averias_TimeOut': Regularizacion_de_averias_TimeOut,
            'Regularizacion_de_averias_no_agendador':Regularizacion_de_averias_no_agendador,
            'Reintentos_fallidas_de_SOM':Reintentos_fallidas_de_SOM,

            #####===Backoffice_Movil===#####
            'Backoffice_Movil_Template':Backoffice_Movil_Template,
            'Consulta_HLR': Consulta_HLR,
            'Depuracion_XML':Depuracion_XML,

            #####===N1_Fija_Template===#####
            'N1_Fija_Template':N1_Fija_Template,

            #####===N1_Movil_Template===#####
            'N1_Movil_Template':N1_Movil_Template,
            'Cierre_Masivo_Decreto_464': Cierre_Masivo_Decreto_464,

            #####Fechas#####
            'Desde':Desde,
            'Hasta':Hasta
                      }
                      )
        else:
        #bot = Backoffice_Fija.objects.values('bot').order_by('bot').distinct()
        #promedio = Backoffice_Fija.objects.aggregate(average__Transcurrido=Avg('Transcurrido'))
        #Resultados = Backoffice_Fija.objects.all()
        #promedio['average__Transcurrido']
            return render(request, 'index.html',{
            #"bot":bot,
            #"promedio":promedio,
            #"Resultados":Resultados
        }
                      )

 if request.method == 'POST' and 'guardarc':
        form = cliente_Form(request.POST, request.FILES)
        if form.is_valid():
            numero_documento = form.cleaned_data['numero_documento']
            form.save()
            mensaje = ("Cliente con numero de documento '",numero_documento,"'agregado correctamente")
            messages.success(request, mensaje)
            return redirect('/C_search/')
    return render(request, template_name,
                  {
                      'form': form,
                      'Doc_Cliente': Doc_Cliente

"""