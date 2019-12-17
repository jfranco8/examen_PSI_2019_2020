# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class paciente(models.Model):
    nombreP = models.CharField(max_length=128)

    def __str__(self):
		return self.nombreP

class medico(models.Model):
    nombreM = models.CharField(max_length=128)

    def __str__(self):
		return self.nombreM

class receta(models.Model):
    medico = models.ForeignKey(medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.medico.nombreM + ' ' + self.paciente.nombreP
