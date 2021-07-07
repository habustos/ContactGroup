from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from .models import *
from viewflow import frontend
from os import system
from django.core.files.storage import FileSystemStorage

from django.conf import settings
import shutil
import os

#original = FileSystemStorage(location='/assets/pdf')
#print(original)
#target = r'C:/Users/harold.bustosact/PycharmProjects/pruebas/contact_group/ContactGroup/core/static/assets/pdf'

@frontend.register
class Venta(Flow):
    process_class = Cliente
    adjunto1 = "adjunto1"
    Inicial = (
        flow.Start(
            CreateProcessView,
            fields=[adjunto1,
                    "tipo_documento",
                    "numero_documento",
                    adjunto1]
        ).Permission(
            auto_create=True,
        ).Next(this.Venta_inicial)
    )
    Venta_inicial = (
        flow.View(
            UpdateProcessView,
            fields=["nombre1",
                    "nombre2",
                    "apellidos",
                    "fecha_documento",
                    "fecha_nacimiento",
                    "departamento",
                    "municipio",
                    "barrio",
                    "direccion",
                    "email",
                    "telefono_mig",
                    "telefono_2",
                    "categoria",
                    "tipo_plan",
                    "plan",
                    "v_total_plan",
                    "observaciones",
                    "adjunto2",
                    "adjunto3",
                    ]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_hello_world_request(self, activation):
        print(activation.process.text)