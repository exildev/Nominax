from supra import views as supra
import models

class EmpleadoListView(supra.SupraListView):
	model = models.Empleado
	list_display = ['id', 'value']

	def value(self, obj, dict):
		return obj.nombre
	# end def
# end class