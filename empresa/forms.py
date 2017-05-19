from django.db.models import Sum, F, Q
from dateutil import relativedelta
from datetime import date
from django import forms 
from models import Empresa, Departamento, Requisito, Cargo, Empleado, Jefes, Contrato, Asistencia, HorasExtra, LiquidacionNomina
from cuser.middleware import CuserMiddleware
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):

    class Meta:
        fields = ["username", "password1", "password2"]
    #end
    
    def save(self, commit):
        obj = super(UserForm, self).save(commit)
        obj.is_staff = True
        obj.save()
        return obj
    #end def
#end class


class EmpresaForm(forms.ModelForm):
	class Meta:
		exclude = ()
		model = Empresa
	#end class
#end class

class DepartamentoAdminForm(forms.ModelForm):
	class Meta:
		exclude = ('activo',)
		model = Departamento
	#end class
#end def

class DepartamentoForm(forms.ModelForm):
	cargos = forms.ModelMultipleChoiceField(queryset=Cargo.objects, required=False, label="cargos")
	empleados = forms.ModelMultipleChoiceField(queryset=Empleado.objects, required=False, label="empleados")
	def __init__(self, *args, **kwargs):
		super(DepartamentoForm, self).__init__(*args, **kwargs)
		if self.instance.pk:
			self.fields['cargos'].queryset = Cargo.objects.filter(departamento=self.instance)
			self.fields['empleados'].queryset = Empleado.objects.filter(cargo__departamento=self.instance)
		#end if
	#end def
	class Meta:
		exclude = ('empresa', 'activo')
		model = Departamento
	#end class

	def save(self, commit=True):
		obj = super(DepartamentoForm, self).save(False)
		user = CuserMiddleware.get_user()
		obj.empresa = Empresa.objects.filter(empresa__usuario = user).first()
		return super(DepartamentoForm, self).save(commit)
	#end if
#end class

class RequisitoForm(forms.ModelForm):
	class Meta:
		exclude = ()
		model = Requisito
	#end class
#end class

class CargoForm(forms.ModelForm):
	class Meta:
		exclude = ('activo', )
		model = Cargo
	#end class
#end class

class EmpleadoForm(forms.ModelForm):
	class Meta:
		exclude = ('cargo', )
		model = Empleado
	#end class

	def save(self, commit=True):
		obj = super(EmpleadoForm, self).save(False)
		user = CuserMiddleware.get_user()
		#obj.empresa = Empresa.objects.filter(empresa = user).first()
		g, create = Group.objects.get_or_create(name='empleado') 
		if create:
			#configure g
			pass
		# end if
		g.user_set.add(user)
		return super(EmpleadoForm, self).save(commit)
	#end if
#end class


class EmpleadoAdminForm(forms.ModelForm):
	class Meta:
		exclude = ('cargo', )
		model = Empleado
	#end class

#end class

class EmpleadoEditForm(forms.ModelForm):
	class Meta:
		exclude = ()
		model = Empleado
	#end class
#end class

class JefesForm(forms.ModelForm):
	class Meta:
		exclude = ()
		model = Jefes
	#end class
#end class


class ContratoForm(forms.ModelForm):
	class Meta:
		exclude = ('cargos', )
		model = Contrato
	#end class

	def save(self, commit=True):
		obj = super(ContratoForm, self).save(commit)
		obj.empleado.cargo = obj.cargo
		obj.empleado.save()
		return obj
	#end def
#end class

class NominaForm(forms.ModelForm):
	#http://www.gerencie.com/formulas-utilizadas-en-la-liquidacion-de-la-nomina.html
	def save(self, commit):
		obj = super(NominaForm, self).save(commit=False)

		conf = obj.empleado.cargo.departamento.empresa.configuracion
		calc = obj.empleado.cargo.departamento.empresa.calculos

		today = date.today()

		contrato = Contrato.objects.filter(empleado = obj.empleado).last()
		ultima_nomina = LiquidacionNomina.objects.filter(fecha_corte__lt=obj.fecha_corte, empleado=obj.empleado, contrato = contrato).last()
		primera_nomina = LiquidacionNomina.objects.filter(fecha_corte__lt=obj.fecha_corte, empleado=obj.empleado, semestre=obj.semestre, fecha_corte__year = today.year).first()

		if ultima_nomina:
			fecha_anterior = ultima_nomina.fecha_corte			
		else:
			fecha_anterior = contrato.fecha_inicio
		#end def
		
		dias = (obj.fecha_corte - fecha_anterior).days

		if primera_nomina:
			fecha_primera_nomina = primera_nomina.fecha_corte
		else:
			fecha_primera_nomina = contrato.fecha_inicio
		#end def
		dias_semestre = (obj.fecha_corte - fecha_primera_nomina).days

		hexd = HorasExtra.objects.filter(dominical=False, tipo=True, empleado=obj.empleado, semestre = obj.semestre, contrato=contrato).aggregate(total=Sum(F('horas')))['total'] or 0
		hexn = HorasExtra.objects.filter(dominical=False, tipo=False, empleado=obj.empleado, semestre = obj.semestre, contrato=contrato).aggregate(total=Sum(F('horas')))['total'] or 0
		hxdd = HorasExtra.objects.filter(dominical=True, tipo=True, empleado=obj.empleado, semestre = obj.semestre, contrato=contrato).aggregate(total=Sum(F('horas')))['total'] or 0
		hxnd = HorasExtra.objects.filter(dominical=True, tipo=False, empleado=obj.empleado, semestre = obj.semestre, contrato=contrato).aggregate(total=Sum(F('horas')))['total'] or 0

		obj.contrato = contrato

		dias_anio = conf.dias_anio
		porc_cesa = conf.porc_cesa
		ango_vaca = conf.ango_vaca
		corte_anual = date(obj.fecha_corte.year - 1, conf.mes_canu, conf.dia_canu)

		delta = relativedelta.relativedelta(today, fecha_primera_nomina)

		dias_anio_or_dias = [delta.days, dias_anio][delta.months >= 12]

		dias_este_anio = delta.days

		porc_hexd = conf.porc_hexd
		porc_hexn = conf.porc_hexn
		porc_hxdd = conf.porc_hxdd
		porc_hxnd = conf.porc_hxnd
		agno_vaca = conf.agno_vaca

		horas_dia = contrato.horas_dia
		salario = float(obj.empleado.salario())
		valor_hora = (salario/[15, 30][contrato.modalidad])/contrato.horas_dia
		
		obj.dias = dias
		obj.cesa = cesantias = eval(calc.cesa)
		obj.intc = eval(calc.intc)
		obj.prim = eval(calc.prim)

		if fecha_anterior.day >= conf.dia_cqui:
			este_corte = date(obj.fecha_corte.year, obj.fecha_corte.month, conf.dia_cmes)
		elif fecha_anterior.day >= conf.dia_cmes:
			este_corte = date(obj.fecha_corte.year, obj.fecha_corte.month, conf.dia_cmes)
		#end if
		dias_propios = (este_corte - fecha_anterior).days
		pago_ordinario = fecha_anterior.day == [conf.dia_cqui, conf.dia_cmes][contrato.modalidad]

		print 'fecha_anterior', fecha_anterior
		print 'este_corte', este_corte
		print 'dias_propios:', dias_propios
		print 'pago_ordinario', pago_ordinario

		if pago_ordinario and dias_propios > 0 and dias >= dias_propios:
			obj.hord = salario
		else:
			obj.hord = (salario/[15, 30][contrato.modalidad])*dias
		#end def

		obj.hexd = eval(calc.hexd)*hexd
		obj.hexn = eval(calc.hexn)*hexn
		obj.hxdd = eval(calc.hxdd)*hxdd
		obj.hxnd = eval(calc.hxnd)*hxnd
		obj.totl = obj.hord + obj.hexd + obj.hexn + obj.hxdd + obj.hxnd

		obj.save()
		return obj
	#end def
#end def

class LiquidacionNominaEditForm(NominaForm):
	class Meta:
		exclude = ()
	#end class 

#end def

class LiquidacionNominaCreateForm(NominaForm):
	class Meta:
		fields = ('empleado', 'periodo', 'semestre', 'fecha_corte')
	#end class 

#end class