# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from unittest import TestCase
from aplicacion.models import paciente, medico, receta

# python manage.py test aplicacion.tests

#DO NOT MODIFIED ANYTHING BELLOW THIS POINT
#very basic model testing, we just check the new objects exists
class modelsTests(TestCase):

    def test_borrar(self):
        paciente.objects.all().delete()
        medico.objects.all().delete()
        receta.objects.all().delete()

        p = paciente.objects.all()
        m = medico.objects.all()
        r = receta.objects.all()
        self.assertEqual(0, len(p))
        self.assertEqual(0, len(m))
        self.assertEqual(0, len(r))

    def test_medico_paciente(self):
        nombre = 'medico1'
        m = medico.objects.create(nombreM=nombre)
        m.save()
        try:
            m = medico.objects.get(nombreM=nombre)
        except medico.DoesNotExist:
            self.assertTrue(False, "medico %s does not exist" %nombre)
        print("checked: %s" % nombre)

        nombre = 'paciente1'
        p = paciente.objects.create(nombreP=nombre)
        p.save()
        try:
            p = paciente.objects.get(nombreP=nombre)
        except paciente.DoesNotExist:
            self.assertTrue(False, "paciente %s does not exist" %nombre)
        print("checked: %s" % nombre)


    def test_recetas(self):
        try:
            m = medico.objects.get(id = 1)
        except ObjectDoesNotExist:
            print "medico con id 1 inexistente"
        try:
            p = paciente.objects.get(id = 1)
        except ObjectDoesNotExist:
            print "paciente con id 1 inexistente"

        for i in range(0,4):
            r = receta.objects.create(medico = m, paciente = p)
            r.save()

        r = receta.objects.filter(medico=m, paciente=p)
        self.assertEqual(4, len(r))
