
from django.urls import path
from . import views

urlpatterns = [
    path('',views.lista_periodo, name='lista_periodo'),
    path('agregar',views.agregar_periodo, name='agregar_periodo'),
    path('agregar/dino',views.agregar_dino, name='agregar_dino'),
    path('nuevo/dino',views.NuevoDino.as_view(), name='nuevo_dino'),
    path('dinos/editar/<int:pk>',views.ActualizaDinos.as_view(), name='editar_dinos'),
    path('dinos/eliminar/<int:pk>',views.EliminaDinos.as_view(), name='eliminar_dinos'),
    path('dinos',views.ListaDino.as_view(), name='lista_dinos'),
    path('dinos/votacion',views.ListaDinoVotacion.as_view(), name='lista_dinos_votacion'),
    path('dinos/lista_pdf',views.ListaDinoPdf.as_view(), name='lista_dinos_pdf'),
    path('dinos/grafica',views.Grafica.as_view(), name='dinos_grafica'),

    path('eliminar/<int:id>',views.eliminar_periodo, name='eliminar_periodo'),
    path('editar/<int:id>',views.editar_periodo, name='editar_periodo'),
]
