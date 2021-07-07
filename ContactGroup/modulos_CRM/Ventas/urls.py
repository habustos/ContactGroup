from django.urls import include, path
from django.conf.urls import  url
from django.contrib.auth.decorators import login_required
from django.views import generic
#from material.frontend import urls as frontend_urls
from .views import *

from . import views

urlpatterns = [
    url(r'^chaining/', include('smart_selects.urls')),
    path('Busqueda_Cedula/', views.Busqueda_Cedula, name='Busqueda_Cedula'),
    path('', views.index, name='home'),
    path('documentos/', login_required(views.Crear_cliente.as_view(template_name="Ventas/crear_cliente.html")),name='cliente_add'),
    #path('documentos/', views.Crear_cliente, name='cliente_add'),
    path('scoring/<pk>', scoring.as_view(), name='scoring'),
    path('cliente/<pk>', ClienteFormView.as_view(), name='cliente'),
    path('venta/<pk>', VentaView.as_view(), name='venta'),
    #path('venta/<id>', VentaView, name='venta'),
    path('aprobacionbo/<pk>', BackOfficeView.as_view(), name='aprobacionbo'),
    path('despachosim/<pk>', despachoView.as_view(), name='despachosim'),
    path('entregasim/<pk>', entregasimView.as_view(), name='entregasim'),
]