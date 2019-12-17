# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from aplicacion.models import paciente, medico, receta

# Register your models here.

class pacienteAdmin(admin.ModelAdmin):
	list_display = ['nombreP']

class medicoAdmin(admin.ModelAdmin):
	list_display = ['nombreM']

class recetaAdmin(admin.ModelAdmin):
	list_display = ('paciente', 'medico')

admin.site.register(paciente, pacienteAdmin)
admin.site.register(medico,medicoAdmin)
admin.site.register(receta,recetaAdmin)
