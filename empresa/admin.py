# -*- coding: utf-8 -*-
from django.contrib import admin
import forms
from django.db.models import Q
import models as empresa
from usr import models as usr
from usr import forms as usr_form
from cuser.middleware import CuserMiddleware


class EmpresaUsrInline(admin.StackedInline):
    form = forms.UserForm
    model = usr.Empresa
# end class


class EmpresaAdmin(admin.ModelAdmin):
    model = empresa.Empresa
    form = forms.EmpresaForm
    inlines = [EmpresaUsrInline]
    icon = '<i class="material-icons">domain</i>'
# end class


class CargoStacked(admin.StackedInline):
    model = empresa.Cargo
    form = forms.CargoForm
# end class


class DepartamentoAdmin(admin.ModelAdmin):
    model = empresa.Departamento
    list_display = ('nombre', 'empresa')
    search_fields = ('nombre', )
    list_filter = ('nombre', )
    icon = '<i class="material-icons">domain</i>'

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.form = forms.DepartamentoAdminForm
        else:
            self.form = forms.DepartamentoAdminForm
        # end if
        return super(DepartamentoAdmin, self).get_form(request, obj, **kwargs)
    # end def

    def get_queryset(self, request):
        queryset = super(DepartamentoAdmin, self).get_queryset(request)
        user = CuserMiddleware.get_user()
        if not request.user.is_superuser:
            queryset = queryset.filter(empresa__empresa=user)
        # end if
        return queryset
    # end def
# end class


class RequisitoAdmin(admin.ModelAdmin):
    model = empresa.Requisito
    form = forms.RequisitoForm
# end class


class RequisitoStacked(admin.StackedInline):
    model = empresa.Requisito
    form = forms.RequisitoForm
# end class


class EmpleadoStacked(admin.StackedInline):
    model = empresa.Empleado
    form = forms.EmpleadoForm
# end class


class CargoAdmin(admin.ModelAdmin):
    model = empresa.Cargo
    form = forms.CargoForm
    list_display = ('nombre', 'departamento', 'salario')
    search_fields = ('nombre', 'departamento__nombre')
    list_filter = ('nombre', 'departamento', 'salario')
    inlines = (RequisitoStacked, )
    icon = '<i class="material-icons">person_pin</i>'
    # raw_id_fields = ('departamento', )

    def get_queryset(self, request):
        queryset = super(CargoAdmin, self).get_queryset(request)
        user = CuserMiddleware.get_user()
        if not request.user.is_superuser:
            queryset = queryset.filter(departamento__empresa__empresa=user)
        # end if
        return queryset
    # end def
# end class


class EmpleadoUsrStacked(admin.StackedInline):
    model = usr.Empleado
    form = usr_form.EmpleadoForm
# end def


class EmpleadoAdmin(admin.ModelAdmin):
    model = empresa.Empleado
    inlines = [EmpleadoUsrStacked]
    list_filter = ('cargo',)
    search_fields = ('codigo', 'nombre', 'apellido')
    list_display = ('codigo', 'nombre', 'apellido',
                    'cargo', 'empresa', 'salario')
    icon = '<i class="material-icons">group</i>'

    def get_readonly_fields(self, request, obj=None):
        if obj is not None and obj.cargo is not None:
            return ['cargo', 'empresa']
        # end if
        return []
    # end def

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None and obj.cargo is not None:
            self.form = forms.EmpleadoEditForm
        else:
            self.form = forms.EmpleadoForm
        # end if
        return super(EmpleadoAdmin, self).get_form(request, obj, **kwargs)
    # end def

    def get_queryset(self, request):
        qs = super(EmpleadoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        # end if

        user = CuserMiddleware.get_user()
        empres = empresa.Empresa.objects.filter(empresa=user).first()
        if empres:
            return qs.filter(empresa=empres)
        # end if
        return qs.filter(empleado=user)
    # end def
# end class


class JefesAdmin(admin.ModelAdmin):
    model = empresa.Jefes
    form = forms.JefesForm
    icon = '<i class="material-icons">person</i>'
# end class


class ContratoAdmin(admin.ModelAdmin):
    search_fields = ['empleado__nombre', 'empleado__apellido', 'fecha_inicio']
    list_filter = ('cargo__nombre', 'fecha_inicio')
    list_display = ['empleado', 'cargo', 'fecha_inicio']
    model = empresa.Contrato
    form = forms.ContratoForm
    icon = '<i class="material-icons">content_paste</i>'
# end class


class LiquidacionNominaAdmin(admin.ModelAdmin):
    search_fields = ['empleado__nombre',
                     'empleado__apellido', 'fecha', 'periodo']
    list_filter = ('empleado__cargo__nombre', 'fecha')
    list_display = ['empleado', 'periodo', 'fecha_corte', 'totl']
    model = empresa.LiquidacionNomina
    icon = '<i class="material-icons">attach_money</i>'

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None:
            self.readonly_fields = (
                'dias', 'hord', 'cesa', 'intc', 'prim', 'hexd', 'hexn', 'hxdd', 'hxnd', 'totl')
            self.form = forms.LiquidacionNominaEditForm
        else:
            self.readonly_fields = ()
            self.form = forms.LiquidacionNominaCreateForm
        # end if
        return super(LiquidacionNominaAdmin, self).get_form(request, obj, **kwargs)
    # end def
# end class


class HoraExtraAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">alarm_add</i>'
# end class


class AsistenciaAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">assignment</i>'
# end class


class ConfiguracionAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">settings</i>'
# end class


class CalculosAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">functions</i>'
# end class


admin.site.register(empresa.Asistencia, AsistenciaAdmin)
admin.site.register(empresa.HorasExtra, HoraExtraAdmin)
admin.site.register(empresa.Configuracion, ConfiguracionAdmin)
admin.site.register(empresa.LiquidacionNomina, LiquidacionNominaAdmin)
admin.site.register(empresa.Calculos, CalculosAdmin)
admin.site.register(empresa.Empresa, EmpresaAdmin)
admin.site.register(empresa.Departamento, DepartamentoAdmin)
#admin.site.register(empresa.Requisito, RequisitoAdmin)
admin.site.register(empresa.Cargo, CargoAdmin)
admin.site.register(empresa.Empleado, EmpleadoAdmin)
admin.site.register(empresa.Contrato, ContratoAdmin)
#admin.site.register(empresa.Jefes, JefesAdmin)
