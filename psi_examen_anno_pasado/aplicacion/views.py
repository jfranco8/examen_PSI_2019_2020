# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from aplicacion.models import receta

from django.http import HttpResponse

# Create your views here.
def show_recetas(request):
    context_dict={}

    receta_list = list(receta.objects.all())
    print receta_list
    if receta_list == []:
        context_dict['error'] = "No hay recetas."
    else:
        context_dict['recetas'] = receta_list[len(receta_list)-3:]

        return render(request, 'aplicacion/receta.html', context_dict)
