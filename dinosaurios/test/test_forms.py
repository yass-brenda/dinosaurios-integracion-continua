from django.test import TestCase
from dinosaurios.models import Dinosaurio, Periodo
from dinosaurios.forms import DinoForm


class TestFormDino(TestCase):

    def test_dino_nombre_vacio(self):
        periodo = Periodo.objects.create(
            nombre = 'cretacio',
            descripcion = 'periodo chido'
        )
        form = DinoForm(
            data={
                'nombre' : '',
                'altura' : '5',
                'periodo' : periodo
            }
        )
        self.assertFalse(form.is_valid())
