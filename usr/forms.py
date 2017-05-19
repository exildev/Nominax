from django import forms 
from django.contrib.auth.forms import UserCreationForm
import models

class EmpleadoForm(UserCreationForm):
	password1 = forms.CharField(max_length=32, widget=forms.PasswordInput, required=False)
	password2 = forms.CharField(max_length=32, widget=forms.PasswordInput, required=False)
	class Meta:
		model = models.Empleado
		fields = ('username', 'password1', 'password2', 'uempleado')
	#end class
#end class


class EmpresaForm(UserCreationForm):
	password1 = forms.CharField(max_length=32, widget=forms.PasswordInput, required=False)
	password2 = forms.CharField(max_length=32, widget=forms.PasswordInput, required=False)
	class Meta:
		model = models.Empresa
		fields = ('username', 'password1', 'password2', 'uempresa')
	#end class
#end class
