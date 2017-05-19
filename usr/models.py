from django.db import models
from django.contrib.auth.models import User, Group
from empresa import models as empresa


class Empresa(User):

    class Meta:
        verbose_name = "Usuario de empresa"
        verbose_name_plural = "Usuarios de empresa"
    # end class
    uempresa = models.ForeignKey(empresa.Empresa)

    def save(self, *args, **kwargs):
        self.is_staff = True
        grupo, ok = Group.objects.get_or_create(name='Empresa')
        super(Empresa, self).save(*args, **kwargs)
        self.groups.add(grupo)
    # end def
# end class


class Auditor(models.Model):
    usuario = models.OneToOneField(User)

    class Meta:
        verbose_name = "Auditor"
        verbose_name_plural = "Auditores"
    # end class
# end class


class Administrador(models.Model):
    usuario = models.OneToOneField(User)

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"
    # end class
# end class


class Empleado(User):

    class Meta:
        verbose_name = "usuario de empleado"
        verbose_name_plural = "usuario de empleado"
    # end class
    uempleado = models.OneToOneField(empresa.Empleado)

    def save(self, *args, **kwargs):
        self.is_staff = True
        grupo, ok = Group.objects.get_or_create(name='Empleado')
        super(Empleado, self).save(*args, **kwargs)
        self.groups.add(grupo)
    # end def
# end class
