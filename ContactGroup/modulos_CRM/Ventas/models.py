from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import valid_extension
#from viewflow.models import Process
import os
from smart_selects.db_fields import ChainedForeignKey,GroupedForeignKey
from django.contrib.auth.models import User



class Depto(models.Model):
    departamento = models.CharField(max_length=30)

    def __str__(self):
        return self.departamento


class Municipio(models.Model):
    municipio = models.CharField(max_length=30)
    departamento = models.ForeignKey(Depto, on_delete=models.CASCADE)

    def __str__(self):
        return self.municipio


class Deptartamento_domicilio(models.Model):
    departamento_domicilio = models.CharField(max_length=30)

    def __str__(self):
        return self.departamento_domicilio


class Municipio_domicilio(models.Model):
    municipio_domicilio = models.CharField(max_length=30)
    departamento_domicilio = models.ForeignKey(Depto, on_delete=models.CASCADE)

    def __str__(self):
        return self.municipio_domicilio


class Categoria_Plan(models.Model):
    categoria = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.categoria


class Tipo_Plan(models.Model):
    categoria = models.ForeignKey(Categoria_Plan, on_delete=models.CASCADE)
    tipo_plan = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.tipo_plan


class Plan(models.Model):
    tipo_plan = models.ForeignKey(Tipo_Plan, on_delete=models.CASCADE)
    plan = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.plan


def generate_path(instance,filename):
    folder = "doc_"+str(instance.numero_documento)
    return os.path.join("media/pdf/",folder,filename)


class Cliente(models.Model):
    t_doc = (
        ('Cédula de ciudadanía','Cédula de ciudadanía'),
        ('Cédula de extranjería', 'Cédula de extranjería'),
        ('Pasaporte', 'Pasaporte'),
        ('PEP','PEP')
    )
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_modificado = models.DateTimeField(auto_now=True)
    asesor = models.CharField(max_length=100,null=True, blank=True,)
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(blank=True, null=True,max_length=100)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=22, choices=t_doc)
    numero_documento = models.BigIntegerField(primary_key=True)
    fecha_expedicion = models.DateField()
    fecha_nacimiento = models.DateField()
    #celular = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(3000000000), MaxValueValidator(3999999999)])
    #celular_alterno = models.IntegerField(blank=True, null=True)
    departamento = models.ForeignKey(Depto, on_delete=models.CASCADE)#,blank=True, null=True,)
    municipio = ChainedForeignKey(
        Municipio,
        chained_field="departamento",
        chained_model_field="departamento",
        show_all=False,
        auto_choose=True,
        #blank=True, null=True,
    )
    departamento_domicilio = models.ForeignKey(Deptartamento_domicilio, on_delete=models.CASCADE,blank=True, null=True,)  # ,blank=True, null=True,)
    municipi_domicilio = ChainedForeignKey(
        Municipio_domicilio,
        chained_field="departamento_domicilio",
        chained_model_field="departamento_domicilio",
        show_all=False,
        auto_choose=True,
        blank=True, null=True,
    )
    opc_sector = (('Barrio', 'Barrio'), ('Zona franca', 'Zona franca'), ('Apartado', 'Apartado'),
                  ('Corregimiento', 'Corregimiento'),
                  ('Caserío', 'Caserío'), ('Parcela', 'Parcela'), ('Vereda', 'Vereda'))
    opc_avenida = (
        ('Calle', 'Calle'), ('Carrera', 'Carrera'), ('Diagonal', 'Diagonal'), ('Transversal', 'Transversal'),
        ('Manzana', 'Manzana'),
        ('Camino', 'Camino'), ('Callejón', 'Callejón'), ('Circunvalar', 'Circunvalar'), ('Autopista', 'Autopista'),
        ('Esquina', 'Esquina'), ('Kilómetro', 'Kilómetro'), ('Carretera', 'Carretera'), ('Variante', 'Variante'),)
    opc_detalle1 = (
        ('Agrupación', 'Agrupación'), ('Edificio', 'Edificio'), ('Interior', 'Interior'), ('Bloque', 'Bloque'),
        ('Unidad residencial', 'Unidad residencial'), ('Urbanización', 'Urbanización'),
        ('Centro comercial', 'Centro comercial'), ('Ciudadela', 'Ciudadela'), ('Agencia', 'Agencia'),
        ('Bodega', 'Bodega'), ('Depósito', 'Depósito'), ('Finca', 'Finca'), ('Hacienda', 'Hacienda'),
        ('Interior', 'Interior'), ('Lote', 'Lote'), ('Muelle', 'Muelle'), ('Parque', 'Parque'),
        ('Pasaje', 'Pasaje'),)
    opc_detalle2 = (
        ('Casa', 'Casa'), ('Consultorio', 'Consultorio'), ('Local', 'Local'), ('Oficina', 'Oficina'),
        ('Piso', 'Piso'),
        ('Almacén', 'Almacén'), ('', ''),)
    letra_opc = (
        ('BIS', 'BIS'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'),
        ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('Ñ', 'Ñ'), ('O', 'O'),
        ('P', 'P'),)
    sector_1 = models.CharField(choices=opc_sector, max_length=50,blank=True, null=True,)
    sector_2 = models.CharField(max_length=300, blank=True, null=True,)
    detalle_1_opc = models.CharField(null=True, blank=True, choices=opc_detalle1, max_length=50)
    detalle_1 = models.CharField(null=True, blank=True, max_length=300)
    detalle_2_opc = models.CharField(null=True, blank=True, choices=opc_detalle2, max_length=50)
    detalle_2 = models.CharField(null=True, blank=True, max_length=300)
    avenida_1 = models.CharField(choices=opc_avenida, null=True, blank=True, max_length=50)
    avenida_2 = models.CharField(null=True, blank=True, choices=opc_avenida, max_length=50)
    numero_1 = models.IntegerField(null=True, blank=True, )
    letra_1 = models.CharField(null=True, blank=True, choices=letra_opc, max_length=50)
    numero_2 = models.IntegerField(null=True, blank=True)
    letra_2 = models.CharField(null=True, blank=True, choices=letra_opc, max_length=50)
    sector = models.CharField(max_length=1000)
    direccion = models.TextField(max_length=1000)
    #direccion_domicilio = models.ForeignKey(direccion_domicilio, on_delete=models.CASCADE)#,blank=True, null=True,)


    def __str__(self):
        return str(self.numero_documento)

    def clean(self):
        self.primer_nombre = self.primer_nombre.upper()
        if self.segundo_nombre is not None:
            self.segundo_nombre = self.segundo_nombre.upper()
        self.apellidos = self.apellidos.upper()
        #self.ocupacion = self.ocupacion.upper()

    def save(self, *args, **kw):
        if self.segundo_nombre is not None:
            self.nombres = '{0} {1}'.format(self.primer_nombre, self.segundo_nombre)
            self.nombres = self.nombres.upper()
        else: self.nombres = self.primer_nombre = self.primer_nombre.upper()
        self.sector = '{0} {1}'.format(self.sector_1, self.sector_2)
        self.sector = self.sector.upper()
        #if self.detalle_2 is not None:
        self.direccion = '{0} {1}{2}#{3}-{4} {5} {6} {7} {8} {9}'.format(self.avenida_1, self.numero_1,self.letra_1, self.avenida_2,self.numero_2, self.letra_2,self.detalle_1_opc,self.detalle_1,self.detalle_2_opc,self.detalle_2)
        self.direccion = self.direccion.replace('None','')
        self.direccion = self.direccion.replace('----','')
        super(Cliente, self).save(*args, **kw)

    """def clean(self):
        try:
            self.primer_nombre = self.primer_nombre.upper()
            self.segundo_nombre = self.segundo_nombre.upper()
            self.apellidos = self.apellidos.upper()
            #self.barrio = self.barrio.upper()
            #self.direccion = self.direccion.upper()
        except:
            self.primer_nombre = self.primer_nombre.upper()
            self.apellidos = self.apellidos.upper()

    def save(self, *args, **kw):
        try:
            self.nombres = '{0} {1}'.format(self.primer_nombre.upper(),self.segundo_nombre.upper())
        except:
            self.nombres = self.primer_nombre.upper()
        else:
            super(Cliente, self).save(*args,**kw)"""


class Cliente_Doc(models.Model):
    #Fecha_Venta = models.DateTimeField(auto_now_add=True)
    #fecha_modificado = models.DateTimeField(auto_now=True)
    #asesor = models.ForeignKey(User, on_delete=models.CASCADE)
    t_doc = (
        ('Cédula de ciudadanía','Cédula de ciudadanía'),
        ('Cédula de extranjería', 'Cédula de extranjería'),
        ('Pasaporte', 'Pasaporte'),
        ('PEP','PEP')
    )
    tipo_documento = models.CharField(max_length=22, choices=t_doc)
    numero_documento = models.OneToOneField(Cliente, on_delete=models.PROTECT,db_constraint=False,primary_key=True)
    documento = models.FileField(upload_to=generate_path, validators=[valid_extension])
    documento2 = models.FileField(blank=True, null=True, upload_to=generate_path, validators=[valid_extension])
    documento3 = models.FileField(blank=True, null=True, upload_to=generate_path, validators=[valid_extension])

    def __str__(self):
        return str(self.numero_documento)


class Ventas(models.Model):
    t_doc = (
        ('Cédula de ciudadanía','Cédula de ciudadanía'),
        ('Cédula de extranjería', 'Cédula de extranjería'),
        ('Pasaporte', 'Pasaporte'),
        ('PEP','PEP')
    )
    t_venta = (
        ('FIJA', 'FIJA'),
        ('MOVIL', 'MOVIL'),
        ('CONVERGENCIA', 'CONVERGENCIA')
    )
    scoring_op = (
        ('APROBADO', 'APROBADO'),
        ('PENDIENTE', 'PENDIENTE'),
        ('ANULADO', 'ANULADO'),
        ('INCUMPLIMIENTO SCORING', 'INCUMPLIMIENTO SCORING'),
    )
    tipo_venta = models.CharField(max_length=22, choices=t_venta,blank=True, null=True,)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    fecha_ingreso = models.DateTimeField(auto_now=True)
    fecha_scoring = models.DateTimeField(auto_now_add=False, auto_now=True)
    numero_documento = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    email = models.EmailField()
    ocupacion = models.CharField(max_length=100)
    #tipo_documento = models.CharField(max_length=22, choices=t_doc)
    foto = models.FileField(upload_to=generate_path)
    documento = models.FileField(upload_to=generate_path, validators=[valid_extension])
    documento2 = models.FileField(blank=True, null=True, upload_to=generate_path, validators=[valid_extension])
    documento3 = models.FileField(blank=True, null=True, upload_to=generate_path, validators=[valid_extension])
    celular = models.PositiveIntegerField(primary_key=True, unique=True,
                                          validators=[MinValueValidator(3000000000), MaxValueValidator(3999999999)])
    celular_alterno = models.IntegerField(blank=True, null=True)
    """
    departamento = models.ForeignKey(Depto, on_delete=models.CASCADE)  # ,blank=True, null=True,)
    municipio = ChainedForeignKey(
        Municipio,
        chained_field="departamento",
        chained_model_field="departamento",
        show_all=False,
        auto_choose=True,
        # blank=True, null=True,
    )
    opc_sector = (('Barrio', 'Barrio'), ('Zona franca', 'Zona franca'), ('Apartado', 'Apartado'),
                  ('Corregimiento', 'Corregimiento'),
                  ('Caserío', 'Caserío'), ('Parcela', 'Parcela'), ('Vereda', 'Vereda'))
    opc_avenida = (
        ('Calle', 'Calle'), ('Carrera', 'Carrera'), ('Diagonal', 'Diagonal'), ('Transversal', 'Transversal'),
        ('Manzana', 'Manzana'),
        ('Camino', 'Camino'), ('Callejón', 'Callejón'), ('Circunvalar', 'Circunvalar'), ('Autopista', 'Autopista'),
        ('Esquina', 'Esquina'), ('Kilómetro', 'Kilómetro'), ('Carretera', 'Carretera'), ('Variante', 'Variante'),)
    opc_detalle1 = (
        ('Agrupación', 'Agrupación'), ('Edificio', 'Edificio'), ('Interior', 'Interior'), ('Bloque', 'Bloque'),
        ('Unidad residencial', 'Unidad residencial'), ('Urbanización', 'Urbanización'),
        ('Centro comercial', 'Centro comercial'), ('Ciudadela', 'Ciudadela'), ('Agencia', 'Agencia'),
        ('Bodega', 'Bodega'), ('Depósito', 'Depósito'), ('Finca', 'Finca'), ('Hacienda', 'Hacienda'),
        ('Interior', 'Interior'), ('Lote', 'Lote'), ('Muelle', 'Muelle'), ('Parque', 'Parque'),
        ('Pasaje', 'Pasaje'),)
    opc_detalle2 = (
        ('Casa', 'Casa'), ('Consultorio', 'Consultorio'), ('Local', 'Local'), ('Oficina', 'Oficina'),
        ('Piso', 'Piso'),
        ('Almacén', 'Almacén'), ('', ''),)
    letra_opc = (
        ('BIS', 'BIS'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'),
        ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('Ñ', 'Ñ'), ('O', 'O'),
        ('P', 'P'),)
    sector_1 = models.CharField(choices=opc_sector, max_length=50)
    sector_2 = models.CharField(max_length=300)
    detalle_1_opc = models.CharField(null=True, blank=True, choices=opc_detalle1, max_length=50)
    detalle_1 = models.CharField(null=True, blank=True, max_length=300)
    detalle_2_opc = models.CharField(null=True, blank=True, choices=opc_detalle2, max_length=50)
    detalle_2 = models.CharField(null=True, blank=True, max_length=300)
    avenida_1 = models.CharField(choices=opc_avenida, null=True, blank=True, max_length=50)
    avenida_2 = models.CharField(null=True, blank=True, choices=opc_avenida, max_length=50)
    numero_1 = models.IntegerField(null=True, blank=True, )
    letra_1 = models.CharField(null=True, blank=True, choices=letra_opc, max_length=50)
    numero_2 = models.IntegerField(null=True, blank=True)
    letra_2 = models.CharField(null=True, blank=True, choices=letra_opc, max_length=50)
    sector = models.CharField(max_length=1000)
    direccion = models.TextField(max_length=1000)
    """
    categoria = models.ForeignKey(Categoria_Plan, on_delete=models.CASCADE, blank=True, null=True)
    tipo_plan = ChainedForeignKey(
        "Tipo_Plan",
        chained_field="categoria",
        chained_model_field="categoria",
        show_all=False,
        auto_choose=True,
        blank=True, null=True, )
    plan = ChainedForeignKey(
        "Plan",
        chained_field="tipo_plan",
        chained_model_field="tipo_plan",
        show_all=False,
        auto_choose=True,
        blank=True, null=True,
    )
    v_movil = models.IntegerField()
    v_fija = models.IntegerField()
    v_total_servicio = models.IntegerField(blank=True, null=True, )
    observaciones = models.TextField(blank=True, null=True, )
    asesor = models.ForeignKey(User, on_delete=models.CASCADE)
    aprobacion_supervisor = models.IntegerField(null=True, blank=True, )
    venta_token = models.IntegerField(null=True, blank=True, )
    supervisor = models.CharField(max_length=100)
    aprobacion_backoffice = models.BooleanField(default=False)
    scoring = models.CharField(choices=scoring_op, max_length=30)
    #scoring = models.BooleanField(default=False)
    cobertura = models.BooleanField(default=False)
    despacho_mensajeria = models.BooleanField(default=False)
    entrega_sim = models.BooleanField(default=False)
    def __str__(self):
        return str(self.celular)

    """def save(self, *args, **kw):
        self.sector = '{0} {1}'.format(self.sector_1, self.sector_2)
        self.sector = self.sector.upper()
        #if self.detalle_2 is not None:
        self.direccion = '{0} {1}{2}#{3}-{4} {5} {6} {7} {8} {9}'.format(self.avenida_1, self.numero_1,self.letra_1, self.avenida_2,self.numero_2, self.letra_2,self.detalle_1_opc,self.detalle_1,self.detalle_2_opc,self.detalle_2)
        self.direccion = self.direccion.replace('None','')
        self.direccion = self.direccion.replace('----','')
        super(Ventas, self).save(*args, **kw)"""


class direccion_entrega(models.Model):
    celular = models.ForeignKey(Ventas, on_delete=models.SET_NULL, null=True)
    departamento = models.ForeignKey(Depto, on_delete=models.CASCADE)  # ,blank=True, null=True,)
    municipio = ChainedForeignKey(
        Municipio,
        chained_field="departamento",
        chained_model_field="departamento",
        show_all=False,
        auto_choose=True,
        # blank=True, null=True,
    )
    opc_sector = (('Barrio', 'Barrio'), ('Zona franca', 'Zona franca'), ('Apartado', 'Apartado'),
                  ('Corregimiento', 'Corregimiento'),
                  ('Caserío', 'Caserío'), ('Parcela', 'Parcela'), ('Vereda', 'Vereda'))
    opc_avenida = (
        ('Calle', 'Calle'), ('Carrera', 'Carrera'), ('Diagonal', 'Diagonal'), ('Transversal', 'Transversal'),
        ('Manzana', 'Manzana'),
        ('Camino', 'Camino'), ('Callejón', 'Callejón'), ('Circunvalar', 'Circunvalar'), ('Autopista', 'Autopista'),
        ('Esquina', 'Esquina'), ('Kilómetro', 'Kilómetro'), ('Carretera', 'Carretera'), ('Variante', 'Variante'),)
    opc_detalle1 = (
        ('Agrupación', 'Agrupación'), ('Edificio', 'Edificio'), ('Interior', 'Interior'), ('Bloque', 'Bloque'),
        ('Unidad residencial', 'Unidad residencial'), ('Urbanización', 'Urbanización'),
        ('Centro comercial', 'Centro comercial'), ('Ciudadela', 'Ciudadela'), ('Agencia', 'Agencia'),
        ('Bodega', 'Bodega'), ('Depósito', 'Depósito'), ('Finca', 'Finca'), ('Hacienda', 'Hacienda'),
        ('Interior', 'Interior'), ('Lote', 'Lote'), ('Muelle', 'Muelle'), ('Parque', 'Parque'),
        ('Pasaje', 'Pasaje'),)
    opc_detalle2 = (
        ('Casa', 'Casa'), ('Consultorio', 'Consultorio'), ('Local', 'Local'), ('Oficina', 'Oficina'),
        ('Piso', 'Piso'),
        ('Almacén', 'Almacén'), ('', ''),)
    letra_opc = (
        ('BIS', 'BIS'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'),
        ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('Ñ', 'Ñ'), ('O', 'O'),
        ('P', 'P'),)
    sector_1 = models.CharField(choices=opc_sector, max_length=50)
    sector_2 = models.CharField(max_length=300)
    detalle_1_opc = models.CharField(null=True, blank=True, choices=opc_detalle1, max_length=50)
    detalle_1 = models.CharField(null=True, blank=True, max_length=300)
    detalle_2_opc = models.CharField(null=True, blank=True, choices=opc_detalle2, max_length=50)
    detalle_2 = models.CharField(null=True, blank=True, max_length=300)
    avenida_1 = models.CharField(choices=opc_avenida, null=True, blank=True, max_length=50)
    avenida_2 = models.CharField(null=True, blank=True, choices=opc_avenida, max_length=50)
    numero_1 = models.IntegerField(null=True, blank=True, )
    letra_1 = models.CharField(null=True, blank=True, choices=letra_opc, max_length=50)
    numero_2 = models.IntegerField(null=True, blank=True)
    letra_2 = models.CharField(null=True, blank=True, choices=letra_opc, max_length=50)
    sector = models.CharField(max_length=1000)
    direccion = models.TextField(max_length=1000)
    observaciones = models.TextField()

    def save(self, *args, **kw):
        self.sector = '{0} {1}'.format(self.sector_1, self.sector_2)
        self.sector = self.sector.upper()
        #if self.detalle_2 is not None:
        self.direccion = '{0} {1}{2}#{3}-{4} {5} {6} {7} {8} {9}'.format(self.avenida_1, self.numero_1,self.letra_1, self.avenida_2,self.numero_2, self.letra_2,self.detalle_1_opc,self.detalle_1,self.detalle_2_opc,self.detalle_2)
        self.direccion = self.direccion.replace('None','')
        self.direccion = self.direccion.replace('----','')
        super(direccion_entrega, self).save(*args, **kw)


class direccion_domicilio(models.Model):
    numero_documento = models.OneToOneField(Cliente, on_delete=models.PROTECT,db_constraint=False,primary_key=True)
    departamento_domicilio = models.ForeignKey(Deptartamento_domicilio, on_delete=models.CASCADE, blank=True,
                                               null=True, )  # ,blank=True, null=True,)
    municipi_domicilio = ChainedForeignKey(
        Municipio_domicilio,
        chained_field="departamento_domicilio",
        chained_model_field="departamento_domicilio",
        show_all=False,
        auto_choose=True,
        blank=True, null=True,
    )
    opc_sector = (('Barrio', 'Barrio'), ('Zona franca', 'Zona franca'), ('Apartado', 'Apartado'),
                  ('Corregimiento', 'Corregimiento'),
                  ('Caserío', 'Caserío'), ('Parcela', 'Parcela'), ('Vereda', 'Vereda'))
    opc_avenida = (
        ('Calle', 'Calle'), ('Carrera', 'Carrera'), ('Diagonal', 'Diagonal'), ('Transversal', 'Transversal'),
        ('Manzana', 'Manzana'),
        ('Camino', 'Camino'), ('Callejón', 'Callejón'), ('Circunvalar', 'Circunvalar'), ('Autopista', 'Autopista'),
        ('Esquina', 'Esquina'), ('Kilómetro', 'Kilómetro'), ('Carretera', 'Carretera'), ('Variante', 'Variante'),)
    opc_detalle1 = (
        ('Agrupación', 'Agrupación'), ('Edificio', 'Edificio'), ('Interior', 'Interior'), ('Bloque', 'Bloque'),
        ('Unidad residencial', 'Unidad residencial'), ('Urbanización', 'Urbanización'),
        ('Centro comercial', 'Centro comercial'), ('Ciudadela', 'Ciudadela'), ('Agencia', 'Agencia'),
        ('Bodega', 'Bodega'), ('Depósito', 'Depósito'), ('Finca', 'Finca'), ('Hacienda', 'Hacienda'),
        ('Interior', 'Interior'), ('Lote', 'Lote'), ('Muelle', 'Muelle'), ('Parque', 'Parque'),
        ('Pasaje', 'Pasaje'),)
    opc_detalle2 = (
        ('Casa', 'Casa'), ('Consultorio', 'Consultorio'), ('Local', 'Local'), ('Oficina', 'Oficina'),
        ('Piso', 'Piso'),
        ('Almacén', 'Almacén'), ('', ''),)
    letra_opc = (
        ('BIS', 'BIS'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'),
        ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('Ñ', 'Ñ'), ('O', 'O'),
        ('P', 'P'),)
    sector_1 = models.CharField(choices=opc_sector, max_length=50)
    sector_2 = models.CharField(max_length=300)
    detalle_1_opc = models.CharField(null=True, blank=True, choices=opc_detalle1, max_length=50)
    detalle_1 = models.CharField(null=True, blank=True, max_length=300)
    detalle_2_opc = models.CharField(null=True, blank=True, choices=opc_detalle2, max_length=50)
    detalle_2 = models.CharField(null=True, blank=True, max_length=300)
    avenida_1 = models.CharField(choices=opc_avenida, null=True, blank=True, max_length=50)
    avenida_2 = models.CharField(null=True, blank=True, choices=opc_avenida, max_length=50)
    numero_1 = models.IntegerField(null=True, blank=True, )
    letra_1 = models.CharField(null=True, blank=True, choices=letra_opc, max_length=50)
    numero_2 = models.IntegerField(null=True, blank=True)
    letra_2 = models.CharField(null=True, blank=True, choices=letra_opc, max_length=50)
    sector = models.CharField(max_length=1000)
    direccion = models.TextField(max_length=1000)
    observaciones = models.TextField()

    def save(self, *args, **kw):
        self.sector = '{0} {1}'.format(self.sector_1, self.sector_2)
        self.sector = self.sector.upper()
        # if self.detalle_2 is not None:
        self.direccion = '{0} {1}{2}#{3}-{4} {5} {6} {7} {8} {9}'.format(self.avenida_1, self.numero_1, self.letra_1,
                                                                         self.avenida_2, self.numero_2, self.letra_2,
                                                                         self.detalle_1_opc, self.detalle_1,
                                                                         self.detalle_2_opc, self.detalle_2)
        self.direccion = self.direccion.replace('None', '')
        self.direccion = self.direccion.replace('----', '')
        super(direccion_domicilio, self).save(*args, **kw)


class venta_token(models.Model):
    venta_token = models.IntegerField(null=True, blank=True, )
    fecha_generacion = models.DateTimeField(auto_now_add=True)

"""
result = MyModel.objects.annotate(
diff=F(int_1)+F(int_2)
).filter(diff__gte=5)


    asesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        to_field='username',
        on_delete=models.CASCADE,
        editable=False
    )

"""