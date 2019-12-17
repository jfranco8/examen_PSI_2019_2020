import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','proyecto.settings')

import django
django.setup()

from aplicacion.models import paciente, medico, receta
from django.core.exceptions import ObjectDoesNotExist

#borrar todo:
paciente.objects.all().delete()
medico.objects.all().delete()
receta.objects.all().delete()

# addPaciente
pacientes =["paciente1", "paciente2"]
for i in range(0,2):
    p = paciente.objects.get_or_create(nombreP=pacientes[i])[0]
    p.save()

#addMedico
medicos =["medico1","medico2","medico3","medico4"]
for i in range (0, 4):
    m = medico.objects.get_or_create(nombreM = medicos[i])[0]
    m.save()

# addReceta
L = [[1,1,1],[2,2,1],[3,1,2],[4,2,2],[5,3,2]]
for i in range (0, 5):
    try:
        m = medico.objects.get(id = L[i][1])
    except ObjectDoesNotExist:
        print "medico con id " + str(L[i][1]) + " inexistente"
    try:
        p = paciente.objects.get(id = L[i][2])
    except ObjectDoesNotExist:
        print "paciente con id " + str(L[i][2]) + " inexistente"
    r = receta.objects.get_or_create(medico = m, paciente = p)[0]
    r.save()
