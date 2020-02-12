from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # path('',views.lista_periodo, name='lista_periodo'),
    path('nuevo',views.NuevoCliente.as_view(), name='nuevo_usuario'),
    path('login',views.Login.as_view(), name='login'),
    path('logout',LogoutView.as_view(), name='logout'),
    path('obtener_municipios',views.estados_municpios, name='obtener_municipios'),
    # path('dinos/editar/<int:pk>',views.ActualizaDinos.as_view(), name='editar_dinos'),
    # path('dinos/eliminar/<int:pk>',views.EliminaDinos.as_view(), name='eliminar_dinos'),
    path('activar/<slug:uidb64>/<slug:token>', views.ActivarCuenta.as_view(), name='activar')
]
