# -*- encoding: utf8 -*-
from django.contrib import admin
import forms
from models import Empresa, Auditor, Administrador, Empleado


class AuditorAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">done_all</i>'
# end class


class AdministradorAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">star</i>'
# end class


class EmpleadoAdmin(admin.ModelAdmin):
    model = Empleado
    form = forms.EmpleadoForm
    icon = '<i class="material-icons">work</i>'
# end class


class EmpresaAdmin(admin.ModelAdmin):
    model = Empresa
    form = forms.EmpresaForm
    icon = '<i class="material-icons">business_center</i>'
# end class


admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Auditor, AuditorAdmin)
admin.site.register(Administrador, AdministradorAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
