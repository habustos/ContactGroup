from django import forms
from .models import *
from betterforms.multiform import MultiModelForm
from datetime import datetime, timedelta, date



mayordeedad = date.today()-timedelta(days=6570)
#mayordeedad = mayordeedad.strftime("%Y-%m-%d")

hoy = date.today()
#hoy = hoy.strftime("%Y-%m-%d")

class Doc_Num_Form(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['tipo_documento','numero_documento',]


class ClienteDocForm(forms.ModelForm):
    t_doc = (
        ('Cédula de ciudadanía', 'Cédula de ciudadanía'),
        ('Cédula de extranjería', 'Cédula de extranjería'),
        ('Pasaporte', 'Pasaporte'),
        ('PEP', 'PEP')
    )
    tipo_documento = forms.ChoiceField(choices=t_doc)
    numero_documento = forms.IntegerField()
    class Meta:
        model = Ventas
        fields =['tipo_venta','foto','documento','documento2','documento3']#,'numero_documento']


class Doc_Form(MultiModelForm):
    form_classes = {
        'Doc_Num_Form':Doc_Num_Form,
        'ClienteDocForm':ClienteDocForm
    }


class scoringform(forms.ModelForm):
    scoring_op = (
        ('',''),
        ('APROBADO', 'APROBADO'),
        ('PENDIENTE', 'PENDIENTE'),
        ('ANULADO', 'ANULADO'),
        ('INCUMPLIMIENTO SCORING', 'INCUMPLIMIENTO SCORING'),
    )
    scoring = forms.ChoiceField(choices=scoring_op)
    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = ['nombres', 'asesor', 'tipo_documento', 'sector', 'direccion','fecha_nacimiento']
        #aprobacion por lista desplegable (APROBADO,PENDIENTE,ANULADO,INCUMPLIMIENTO_SCORING
        widgets = {

            'fecha_expedicion': forms.DateInput(format=('%Y-%m-%d'),
                                                attrs={'id': 'Fecha_Documento',
                                                       'type': 'date',
                                                       'value': 'false',
                                                       }),
            'fecha_nacimiento': forms.DateInput(format=('%Y-%m-%d'),
                                                attrs={'type': 'date',
                                                       'value': 'false'}
                                                ),
        }


"""class scoringmultipleform(MultiModelForm):
    form_classes = {
        'scoringform':scoringform,
        'ClienteDocForm':ClienteDocForm
    }"""

class ClienteForm(forms.ModelForm):
    """opc_sector = (('---',''),('Barrio','Barrio'),('Zona franca', 'Zona franca'), ('Apartado', 'Apartado'), ('Corregimiento', 'Corregimiento'),
              ('Caserío', 'Caserío'), ('Parcela', 'Parcela'), ('Vereda', 'Vereda'))
    opc_avenida = (('---',''),('Calle','Calle'),('Carrera', 'Carrera'), ('Diagonal', 'Diagonal'), ('Transversal', 'Transversal'), ('Manzana', 'Manzana'),
           ('Camino', 'Camino'), ('Callejón', 'Callejón'), ('Circunvalar', 'Circunvalar'), ('Autopista', 'Autopista'),
           ('Esquina', 'Esquina'), ('Kilómetro', 'Kilómetro'), ('Carretera', 'Carretera'), ('Variante', 'Variante'),)
    opc_detalle1 = (('---',''),('Agrupación', 'Agrupación'), ('Edificio', 'Edificio'), ('Interior', 'Interior'), ('Bloque', 'Bloque'),
                ('Unidad residencial', 'Unidad residencial'), ('Urbanización', 'Urbanización'),
                ('Centro comercial', 'Centro comercial'), ('Ciudadela', 'Ciudadela'), ('Agencia', 'Agencia'),
                ('Bodega', 'Bodega'), ('Depósito', 'Depósito'), ('Finca', 'Finca'), ('Hacienda', 'Hacienda'),
                ('Interior', 'Interior'), ('Lote', 'Lote'), ('Muelle', 'Muelle'), ('Parque', 'Parque'),
                ('Pasaje', 'Pasaje'),)
    opc_detalle2 = (
    ('---',''),('Casa', 'Casa'), ('Consultorio', 'Consultorio'), ('Local', 'Local'), ('Oficina', 'Oficina'), ('Piso', 'Piso'),
    ('Almacén', 'Almacén'), ('', ''),)
    letra_opc = (('---',''),('BIS','BIS'),('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F'),('G','G'),('H','H'),('I','I'),('J','J'),('K','K'),('L','L'),('M','M'),('N','N'),('Ñ','Ñ'),('O','O'),('P','P'),)
    primer_nombre = forms.CharField(max_length=100)
    segundo_nombre = forms.CharField(max_length=100, required=False)
    apellidos = forms.CharField(max_length=100)
    email = forms.EmailField()
    celular = forms.NumberInput()
    telefono = forms.IntegerField(required=False)
    sector_1 = forms.ChoiceField(choices=opc_sector)
    sector_2 = forms.CharField(max_length=300)
    detalle_1_opc= forms.ChoiceField(choices=opc_detalle1)
    detalle_1 = forms.CharField(required=False,max_length=300)
    detalle_2_opc = forms.ChoiceField(required=False,choices=opc_detalle2)
    detalle_2 = forms.CharField(required=False,max_length=300)
    avenida_1 = forms.ChoiceField(choices=opc_avenida)
    avenida_2 = forms.ChoiceField(choices=opc_avenida)
    numero_1= forms.IntegerField(required=False)
    letra_1= forms.ChoiceField(required=False,choices=letra_opc)
    numero_2= forms.IntegerField(required=False)#(widget=forms.IntegerField(attrs={'class': 'check-inline list-unstyled'}))
    letra_2= forms.ChoiceField(required=False,choices=letra_opc)
    #fecha_expedicion= forms.DateInput()"""
    #numero_documento = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Cliente
        fields = ['primer_nombre',
                  'segundo_nombre',
                  'apellidos',
                  'numero_documento',
                  'fecha_expedicion',
                  'fecha_nacimiento',
                  'departamento',
                  'municipio',
                  ]
        exclude = ['nombres','asesor','tipo_documento','sector','direccion',
                  'departamento_domicilio',
                  'municipi_domicilio',
                  'sector_1',
                  'sector_2',
                  'detalle_1_opc',
                  'detalle_1',
                  'detalle_2_opc',
                  'detalle_2',
                  'avenida_1',
                  'avenida_2',
                  'numero_1',
                  'letra_1',
                  'numero_2',
                  'letra_2',
                   ]
        #eliminar fecha nacimiento del formulario
        widgets = {

            'fecha_expedicion': forms.DateInput(format=('%Y-%m-%d'),
                                               attrs={'id':'Fecha_Documento',
                                                      'type':'date',
                                                   'value':'false',
                                                      }),
            'fecha_nacimiento': forms.DateInput(format=('%Y-%m-%d'),
                                                attrs={'type':'date',
                                                       'value':'false'}
                                                ),
        }

        def clean_end_date(self):
            F_Documento = self.cleaned_data['fecha_documento']
            F_Nacimiento = self.cleaned_data['fecha_nacimiento']
            aprobacion = self.cleaned_data['fecha_nacimiento']
            if F_Documento <= F_Nacimiento:
                raise forms.ValidationError(
                    "La fecha de expedición del documento debe ser mayor a la fecha de nacimiento ")




class direccion_domicilio_form(forms.ModelForm):
    """opc_sector = (('---',''),('Barrio','Barrio'),('Zona franca', 'Zona franca'), ('Apartado', 'Apartado'), ('Corregimiento', 'Corregimiento'),
              ('Caserío', 'Caserío'), ('Parcela', 'Parcela'), ('Vereda', 'Vereda'))
    opc_avenida = (('---',''),('Calle','Calle'),('Carrera', 'Carrera'), ('Diagonal', 'Diagonal'), ('Transversal', 'Transversal'), ('Manzana', 'Manzana'),
           ('Camino', 'Camino'), ('Callejón', 'Callejón'), ('Circunvalar', 'Circunvalar'), ('Autopista', 'Autopista'),
           ('Esquina', 'Esquina'), ('Kilómetro', 'Kilómetro'), ('Carretera', 'Carretera'), ('Variante', 'Variante'),)
    opc_detalle1 = (('---',''),('Agrupación', 'Agrupación'), ('Edificio', 'Edificio'), ('Interior', 'Interior'), ('Bloque', 'Bloque'),
                ('Unidad residencial', 'Unidad residencial'), ('Urbanización', 'Urbanización'),
                ('Centro comercial', 'Centro comercial'), ('Ciudadela', 'Ciudadela'), ('Agencia', 'Agencia'),
                ('Bodega', 'Bodega'), ('Depósito', 'Depósito'), ('Finca', 'Finca'), ('Hacienda', 'Hacienda'),
                ('Interior', 'Interior'), ('Lote', 'Lote'), ('Muelle', 'Muelle'), ('Parque', 'Parque'),
                ('Pasaje', 'Pasaje'),)
    opc_detalle2 = (
    ('---',''),('Casa', 'Casa'), ('Consultorio', 'Consultorio'), ('Local', 'Local'), ('Oficina', 'Oficina'), ('Piso', 'Piso'),
    ('Almacén', 'Almacén'), ('', ''),)
    letra_opc = (('---',''),('BIS','BIS'),('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F'),('G','G'),('H','H'),('I','I'),('J','J'),('K','K'),('L','L'),('M','M'),('N','N'),('Ñ','Ñ'),('O','O'),('P','P'),)
    primer_nombre = forms.CharField(max_length=100)
    segundo_nombre = forms.CharField(max_length=100, required=False)
    apellidos = forms.CharField(max_length=100)
    email = forms.EmailField()
    celular = forms.NumberInput()
    telefono = forms.IntegerField(required=False)
    sector_1 = forms.ChoiceField(choices=opc_sector)
    sector_2 = forms.CharField(max_length=300)
    detalle_1_opc= forms.ChoiceField(choices=opc_detalle1)
    detalle_1 = forms.CharField(required=False,max_length=300)
    detalle_2_opc = forms.ChoiceField(required=False,choices=opc_detalle2)
    detalle_2 = forms.CharField(required=False,max_length=300)
    avenida_1 = forms.ChoiceField(choices=opc_avenida)
    avenida_2 = forms.ChoiceField(choices=opc_avenida)
    numero_1= forms.IntegerField(required=False)
    letra_1= forms.ChoiceField(required=False,choices=letra_opc)
    numero_2= forms.IntegerField(required=False)#(widget=forms.IntegerField(attrs={'class': 'check-inline list-unstyled'}))
    letra_2= forms.ChoiceField(required=False,choices=letra_opc)
    #fecha_expedicion= forms.DateInput()"""
    #numero_documento = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = direccion_domicilio
        fields = '__all__'


class VentaForm(forms.ModelForm):
    #celular = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    opc_plan = ((1, 'PLAN MOVIL1'),
                (2, 'PLAN MOVIL2'),
                (3, 'PLAN FIJA1'),
                (4, 'PLAN FIJA1'))
    'supervisor'
    supervisor = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    planes = forms.MultipleChoiceField(choices=opc_plan)
    class Meta:
        model = Ventas
        fields ='__all__'
        exclude = ['primer_nombre',
                  'segundo_nombre',
                  'apellidos',
                  'numero_documento',
                  'fecha_expedicion',
                  'departamento',
                  'municipio',
                  'departamento_domicilio',
                  'municipi_domicilio',
                   'despacho_mensajeria',
                   'entrega_sim',
                   'cliente',
                   'asesor',
                   'numero_documento',
                   'scoring',
                   'cobertura',
                   'venta_token',
                   'aprobacion_supervisor',
                   'aprobacion_backoffice',
                   #'supervisor',
                   'tipo_venta',
                   'foto',
                   'documento',
                   'v_movil',
                   'v_fija',
                   'tipo_plan',
                   'plan',
                   'categoria',
                   'v_total_servicio'
                   ]


class Cliente_Venta_Form(forms.ModelForm):
    """letra_opc = (('---',''),('BIS','BIS'),('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F'),('G','G'),('H','H'),('I','I'),('J','J'),('K','K'),('L','L'),('M','M'),('N','N'),('Ñ','Ñ'),('O','O'),('P','P'),)
    primer_nombre = forms.CharField(max_length=100)
    segundo_nombre = forms.CharField(max_length=100, required=False)
    apellidos = forms.CharField(max_length=100)
    email = forms.EmailField()
    celular = forms.NumberInput()
    telefono = forms.IntegerField(required=False)
    sector_2 = forms.CharField(max_length=300)
    detalle_1 = forms.CharField(required=False,max_length=300)
    detalle_2 = forms.CharField(required=False,max_length=300)
    numero_1= forms.IntegerField(required=False)
    letra_1= forms.ChoiceField(required=False,choices=letra_opc)
    numero_2= forms.IntegerField(required=False)#(widget=forms.IntegerField(attrs={'class': 'check-inline list-unstyled'}))
    letra_2= forms.ChoiceField(required=False,choices=letra_opc)
    #direccion_entrega = forms.BooleanField(widget = forms.BooleanField(attrs = {'onclick' : "Mostrar();"}))"""
    direccion_entrega = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'onclick': "Mostrar();"}))
    #fecha_expedicion= forms.DateInput()
    class Meta:
        model = Cliente
        fields = ['primer_nombre',
                  'segundo_nombre',
                  'apellidos',
                  'numero_documento',
                  'fecha_expedicion',
                  'fecha_nacimiento',
                  'departamento',
                  'municipio',
                  'sector', 'direccion',
                  'departamento_domicilio',
                  'municipi_domicilio',
                  'sector_1',
                  'sector_2',
                  'detalle_1_opc',
                  'detalle_1',
                  'detalle_2_opc',
                  'detalle_2',
                  'avenida_1',
                  'avenida_2',
                  'numero_1',
                  'letra_1',
                  'numero_2',
                  'letra_2',
                  #'supervisor'
                  ]
        exclude = ['nombres','asesor','tipo_documento','direccion'
                   ]
        #eliminar fecha nacimiento del formulario


        widgets = {

            'fecha_expedicion': forms.DateInput(format=('%Y-%m-%d'),
                                               attrs={'id':'Fecha_Documento',
                                                      'type':'date',
                                                   'value':'false',
                                                      }),
            'fecha_nacimiento': forms.DateInput(format=('%Y-%m-%d'),
                                                attrs={'type':'date',
                                                       'value':'false'}
                                                ),
        }


class VentaForm1(MultiModelForm):
    form_classes = {
        'Cliente_Venta_Form': Cliente_Venta_Form,
        'VentaForm': VentaForm
    }



class BackofficeForm(forms.ModelForm):
    #celular = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Ventas
        fields =['aprobacion_backoffice']

        #fields =['aprobacion_backoffice','celular']
        #exclude = ['aprobacion_backoffice','despacho_mensajeria','entrega_sim','numero_docuemnto','celular','asesor']


class BackofficeMultiForm(MultiModelForm):
    form_classes = {
        'BackofficeForm':BackofficeForm,
        'VentaForm':VentaForm
    }


class MensajeriaDespacho(forms.ModelForm):
    #celular = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Ventas
        fields =['despacho_mensajeria','celular']
        #exclude = ['aprobacion_backoffice','despacho_mensajeria','entrega_sim','numero_docuemnto','celular','asesor']


class MensajeriaEntrega(forms.ModelForm):
    #celular = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Ventas
        fields =['entrega_sim','celular']


"""
class ClienteMultiForm(MultiModelForm):
    form_classes = {
        'ClienteForm': ClienteForm,
        'ClienteDocForm2': ClienteDocForm2
    }


elif fecha_expedicion or fecha_nacimiento >= fecha_ingreso:
    raise forms.ValidationError({"fecha_expedicion": "La fecha de expedición del documento debe ser menor a la fecha actual",
                                 "fecha_nacimiento": "La fecha de nacimiento debe ser menor a la fecha actual"})
                                 
####################################################33                                 
class Clienteform(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre1',
                  'nombre2',
                  'apellidos',
                  'fecha_documento',
                  'fecha_nacimiento',
                  'departamento',
                  'municipio',
                  'barrio',
                  'av2',
                  'direccion',
                  'email',
                  'telefono1',
                  #'telefono2',
                  'documento2',
                  'documento3'
                  )

        labels = {'nombre1':'Primer nombre',
                  'nombre2': 'Segundo nombre',
                  'apellidos':'Apellidos',
                  #'tipo_documento':'Tipo de documento',
                  #'numero_documento':'Numero de documento',
                  'fecha_documento':'Fecha de expedición',
                  'fecha_nacimiento':'Fecha de nacimiento',
                  'departamento':'Departamento',
                  'municipio':'Municipio',
                  'barrio':'Barrio',
                  'direccion':'Direccion',
                  'email':'Correo electronico',
                  'telefono_mig':'Linea a migrar',
                  'telefono_2':'Linea secundaria',
                  #'categoria':'Categoría de servicio',
                  'tipo_plan':'Tipo de plan',
                  'plan':'Plan',
                  'v_total_plan':'Valor total',
                  'observaciones':'Observaciones del cliente',
                  'adjunto1':'Cedula',
                  'adjunto2': 'RUT',
                  'adjunto3': 'Otro',
        }
        widgets = {
            'fecha_documento': forms.DateInput(format=('%d-%m-%Y'), attrs={'id':'Fecha_Documento',
                #'class':'form-control'
                                                                                   'type':'date'}),
            'fecha_nacimiento': forms.DateInput(format=('%d-%m-%Y'), attrs={#'class':'form-control',
                                                                            'type':'date'}),
            #'depto': forms.TextInput(attrs={'class':'dropdown-item'}),
            #'ciudad': forms.TextInput(attrs={'class':'dropdown-item'}),

        }



        def __init__(self, *args, **kwargs):
            self.asesor = kwargs.pop('asesor')
            super(Clienteform, self).__init__(*args, **kwargs)

        def clean_end_date(self):
            F_Documento = self.cleaned_data['fecha_documento']
            F_Nacimiento = self.cleaned_data['fecha_nacimiento']

            if F_Documento <= F_Nacimiento:
                raise forms.ValidationError("La fecha de expedición del documento debe ser mayor a la fecha de nacimiento ")
            return F_Documento

        def save(self, *args, **kwargs):
            self.instance.asesor = self.asesor
            meal = super(Clienteform, self).save(*args, **kwargs)
            return meal

'categoria',
                  'tipo_plan',
                  'plan',
                  'v_total_plan',
                  'observaciones',            
            
"""