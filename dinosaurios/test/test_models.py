from django.test import TestCase
from dinosaurios.models import Dinosaurio, Periodo, VotacionDino
from dinosaurios.test.test_views import TestViews
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TestHumo(TestCase):

    def test_prueba_humo(self):
        self.assertEqual(2 + 2, 4)

    def test_agrega_dinosaurio(self):
        periodo = Periodo.objects.create(
            nombre='cretacio',
            descripcion='periodo chido'
        )
        dino = Dinosaurio.objects.create(
            nombre='T-REX',
            altura='5',
            periodo=periodo,
        )
        dino_uno = Dinosaurio.objects.first()

        self.assertEqual(dino_uno, dino)
        self.assertEqual(dino_uno.nombre, 'T-REX')
        self.assertEqual(str(dino_uno), 'T-REX')
        self.assertEqual(len(Dinosaurio.objects.all()), 1)

    def test_agrega_votacion(self):
        test_view = TestViews()
        dino = test_view.agrega_dino()
        usuario = User.objects.create(username='alex', password='alex123')
        votacion = VotacionDino.objects.create(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 4,
            rollo = 'me pareció muy chido el dino'
        )
        self.assertEqual(VotacionDino.objects.count(), 1)

    def test_votacion_exede_calificacion_maxima(self):
        test_view = TestViews()
        dino = test_view.agrega_dino()
        usuario = User.objects.create(username='alex', password='alex123')
        votacion = VotacionDino(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 9,
            rollo = 'me pareció muy chido el dino'
        )
        with self.assertRaises(ValidationError):
            votacion.full_clean()

    def test_votacion_exede_calificacion_maxima_mensaje(self):
        test_view = TestViews()
        dino = test_view.agrega_dino()
        usuario = User.objects.create(username='alex', password='alex123')
        votacion = VotacionDino(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 9,
            rollo = 'me pareció muy chido el dino'
        )
        with self.assertRaisesMessage(ValidationError, 'El valor máximo permitido es 5'):
            votacion.full_clean()

    def test_votacion_calificacion_minima(self):
        test_view = TestViews()
        dino = test_view.agrega_dino()
        usuario = User.objects.create(username='alex', password='alex123')
        votacion = VotacionDino(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 0,
            rollo = 'me pareció muy chido el dino'
        )
        with self.assertRaises(ValidationError):
            votacion.full_clean()

    def test_votacion_calificacion_minima_mensaje(self):
        test_view = TestViews()
        dino = test_view.agrega_dino()
        usuario = User.objects.create(username='alex', password='alex123')
        votacion = VotacionDino(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = -1,
            rollo = 'me pareció muy chido el dino'
        )
        with self.assertRaisesMessage(ValidationError, 'El valor mínimo es 1'):
            votacion.full_clean()



    def test_agrega_votacion_verifica_calificacion(self):
        test_view = TestViews()
        dino = test_view.agrega_dino()
        usuario = User.objects.create(username='alex', password='alex123')
        votacion = VotacionDino.objects.create(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 4,
            rollo = 'me pareció muy chido el dino'
        )
        self.assertEqual(VotacionDino.objects.first().calificacion, 4)
    
    def test_agrega_votacion_verifica_dinosaurio(self):
        test_view = TestViews()
        dino = test_view.agrega_dino()
        usuario = User.objects.create(username='alex', password='alex123')
        votacion = VotacionDino.objects.create(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 4,
            rollo = 'me pareció muy chido el dino'
        )
        self.assertEqual(VotacionDino.objects.first().dinosaurio.nombre, 'T-Rex')

    def test_agrega_votacion_verifica_usuario(self):
        test_view = TestViews()
        dino = test_view.agrega_dino()
        usuario = User.objects.create(username='alex', password='alex123')
        votacion = VotacionDino.objects.create(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 4,
            rollo = 'me pareció muy chido el dino'
        )
        self.assertEqual(VotacionDino.objects.first().usuario.username, 'alex')