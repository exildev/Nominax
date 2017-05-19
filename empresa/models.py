# -*- coding: utf-8 -*-
from django.db import models


class Configuracion(models.Model):
    nombre = models.CharField(max_length=100)
    dias_anio = models.IntegerField(default=360, verbose_name="Dias del año")
    porc_cesa = models.FloatField(
        default=0.12, verbose_name="Porcentaje de cesantias")
    ango_vaca = models.IntegerField(
        default=2, verbose_name="Años por vacaciones")
    porc_hexd = models.FloatField(
        default=1.25, verbose_name="Porcentaje de horas extras diurnas")
    porc_hnoc = models.FloatField(
        default=1.35, verbose_name="Porcentaje de horas nocturnas")
    porc_hexn = models.FloatField(
        default=1.75, verbose_name="Porcentaje de horas extras nocturnas")
    porc_hord = models.FloatField(
        default=1.75, verbose_name="Porcentaje de horas ordinarias dominicales")
    porc_hxdd = models.FloatField(
        default=2, verbose_name="Porcentaje de horas extras diurnas dominicales")
    porc_hxnd = models.FloatField(
        default=2.5, verbose_name="Porcentaje de horas extras nocturnas dominicales")
    agno_vaca = models.FloatField(
        default=2, verbose_name="Divisor de años por vacaciones")
    dia_cmes = models.IntegerField(default=1, verbose_name="Dia corte mensual")
    dia_cqui = models.IntegerField(
        default=15, verbose_name="Dia corte quinsenal")
    dia_canu = models.IntegerField(
        default=31, verbose_name="Dia de corte anual")
    mes_canu = models.IntegerField(
        default=12, verbose_name="Mes de corte anual")

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configurariones"
    # end class
        
    def __unicode__(self):
        return self.nombre
    # end def
# end class


class Calculos(models.Model):
    nombre = models.CharField(max_length=100)
    cesa = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="Cesantias")
    intc = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="Intereses sobre cesantias")
    prim = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="Primas de servicio")
    vaca = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="Vacaciones")
    hexd = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="Horas extras diurnas")
    hnoc = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="Horas nocturnas")
    hexn = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="Horas extras nocturnas")
    hord = models.CharField(max_length=100, null=True,
                            blank=True, verbose_name="Horas ordinarias dominicales")
    hxdd = models.CharField(max_length=100, null=True, blank=True,
                            verbose_name="Horas extras diurnas dominicales")
    hxnd = models.CharField(max_length=100, null=True, blank=True,
                            verbose_name="Horas extras nocturnas dominicales")

    class Meta:
        verbose_name = "Calculo"
        verbose_name_plural = "Calculos"

    def __unicode__(self):
        return self.nombre
    # end def
# end class


class Anio(models.Model):
    anio = models.IntegerField(verbose_name="año")

    class Meta:
        verbose_name = "Año"
    # end class

    def __unicode__(self):
        return u"%s" % (str(self.anio))
    # end def
# end calss


class Empresa(models.Model):
    codigo = models.CharField(max_length=3)
    razons = models.CharField(max_length=100)
    ident = models.CharField(max_length=30)
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='empresa/', blank=True)
    email = models.EmailField()
    direccion = models.TextField()
    configuracion = models.OneToOneField(Configuracion, null=True)
    calculos = models.ForeignKey(Calculos, null=True)

    def __unicode__(self):
        return u'%s' % (self.razons, )
    # end def
# end class


class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=3)
    activo = models.BooleanField(default=True)
    empresa = models.ForeignKey(Empresa)
    superior = models.ForeignKey(
        'Departamento', blank=True, null=True, default=None)

    def __unicode__(self):
        return u'%s' % (self.nombre, )
    # end def
# end class


class Cargo(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    descripcion = models.TextField()
    departamento = models.ForeignKey(Departamento)
    salario = models.DecimalField(max_digits=20, decimal_places=3)
    #perfil = models.ForeignKey(Perfil)

    def __unicode__(self):
        return u'%s' % (self.nombre, )
    # end def
# end class


class Requisito(models.Model):
    cargo = models.OneToOneField(Cargo, null=True, blank=True)
    educacion = models.TextField(blank=True)
    formacion = models.TextField(blank=True)
    habilidades = models.TextField(blank=True)
    experiencia = models.TextField(blank=True)
# end class


class Empleado(models.Model):
    codigo = models.CharField(max_length=10, blank=True)
    cargo = models.ForeignKey(Cargo, null=True, blank=True)
    empresa = models.ForeignKey(Empresa)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12)
    bonificacion = models.DecimalField(max_digits=20, decimal_places=2)

    def salario(self):
        salario = 0
        if self.cargo:
            return str(self.cargo.salario + self.bonificacion)
        # end if
        return None
    # end def

    def __unicode__(self):
        return u'%s-%s %s' % (self.codigo, self.nombre, self.apellido)
    # end def
# end class


class Jefes(models.Model):
    empleado = models.OneToOneField(Empleado, unique=True)
    departamento = models.OneToOneField(Departamento, unique=True)

    def __unicode__(self):
        return u'%s es jefe del departamento %s ' % (str(self.empleado), str(self.departamento), )
    # end def
# end class


class Contrato(models.Model):
    MODO = (
        (1, 'Mensual'),
        (0, 'Quinsenal'),
    )
    fecha = models.DateField(auto_now_add=True)
    fecha_inicio = models.DateField()
    empleado = models.ForeignKey(Empleado)
    cargo = models.ForeignKey(Cargo)
    documento = models.FileField(upload_to="contratos")
    firmado = models.BooleanField()
    horas_dia = models.IntegerField()
    modalidad = models.IntegerField(choices=MODO)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return u'Contrato de %s' % (self.empleado.nombre, )
    # end def
# end class


class Asistencia(models.Model):
    empleado = models.ForeignKey(Empleado)
    fecha = models.DateTimeField(auto_now_add=True)
    contrato = models.ForeignKey(Contrato)
    periodo = models.IntegerField()
    semestre = models.IntegerField()
# end class


class HorasExtra(models.Model):
    TIPOS = (
        (True, 'Diurna'),
        (False, 'Nocturna')
    )
    empleado = models.ForeignKey(Empleado)
    fecha = models.DateTimeField(auto_now_add=True)
    contrato = models.ForeignKey(Contrato)
    periodo = models.IntegerField()
    semestre = models.IntegerField()
    horas = models.IntegerField()
    tipo = models.BooleanField(default=True, choices=TIPOS)
    dominical = models.BooleanField(default=False)
# end class


class LiquidacionNomina(models.Model):
    periodo = models.IntegerField()
    semestre = models.IntegerField()
    empleado = models.ForeignKey(Empleado)
    contrato = models.ForeignKey(Contrato)
    fecha = models.DateField(auto_now_add=True)
    fecha_corte = models.DateField()

    dias = models.IntegerField(verbose_name="Dias trabajados")
    cesa = models.DecimalField(max_digits=20, decimal_places=2,
                               null=True, blank=True, verbose_name="Cesantias acumuladas $")
    intc = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                               blank=True, verbose_name="Intereses sobre cesantias acumulados $")
    prim = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                               blank=True, verbose_name="Primas de servicio acumuladas $")
    hord = models.DecimalField(max_digits=20, decimal_places=2,
                               null=True, blank=True, verbose_name="Horas ordinarias $")

    hexd = models.DecimalField(max_digits=20, decimal_places=2,
                               null=True, blank=True, verbose_name="Horas extras diurnas $")
    hexn = models.DecimalField(max_digits=20, decimal_places=2,
                               null=True, blank=True, verbose_name="Horas extras nocturnas $")
    hxdd = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                               blank=True, verbose_name="Horas extras diurnas dominicales $")
    hxnd = models.DecimalField(max_digits=20, decimal_places=2, null=True,
                               blank=True, verbose_name="Horas extras nocturnas dominicales $")
    totl = models.DecimalField(max_digits=20, decimal_places=2,
                               null=True, blank=True, verbose_name="Total devengado $")

    def __unicode__(self):
        return u'%s' % (self.empleado,)
    # end def
# end def
