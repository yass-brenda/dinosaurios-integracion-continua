from django.shortcuts import render, redirect
from .models import Periodo, Dinosaurio
from .forms import PeriodoForm, DinoForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count
from django_weasyprint import WeasyTemplateResponseMixin
from django.conf import settings


# class NuevoDino(LoginRequiredMixin, CreateView):
class NuevoDino(CreateView):
    model = Dinosaurio
    form_class = DinoForm
    success_url = reverse_lazy('lista_dinos')

# class ListaDino(PermissionRequiredMixin, ListView):
class ListaDino(ListView):
    model = Dinosaurio
    # permission_required = 'dinosaurios.view_dinosaurio'


class EliminaDinos(DeleteView):
    model = Dinosaurio
    success_url = reverse_lazy('lista_dinos')


class ActualizaDinos(UpdateView):
    form_class = DinoForm
    model = Dinosaurio
    success_url = reverse_lazy('lista_dinos')
    template_name = 'dinosaurios/dinosaurio_edit.html'


class ListaDinoVotacion(LoginRequiredMixin, ListView):
    model = Dinosaurio
    template_name = 'dinosaurios/dinosaurio_lista_votacion.html'
    def get(self, request, *args, **kwargs):
        dinos = Dinosaurio.objects.all()
        dinos_votos = []
        for dino in dinos:
            votos = {5:0, 4:0, 3:0, 2:0, 1:0, 'total':0, 'promedio':0}
            votos_dinos = dino.votaciondino_set.all().values('calificacion').annotate(cuantos=Count('calificacion'))
            if votos_dinos:
                sumatoria = 0
                for dato in votos_dinos:
                    votos[dato['calificacion']] = dato['cuantos']
                    votos['total'] += dato['cuantos']
                    sumatoria += dato['calificacion'] * dato['cuantos']
                votos['promedio'] = sumatoria / votos['total']
            
            dinos_votos.append({'dino':dino, 'votos':votos})  
        self.object_list = dinos_votos
        context = self.get_context_data()
    
        return self.render_to_response(context)

class VistaPdf(ListView):
    model = Dinosaurio
    template_name = 'dinosaurios/dinosaurio_pdf.html'
    suma = 0
    for dino in Dinosaurio.objects.all():
        suma += dino.altura
    
    extra_context = {"suma":suma}

class ListaDinoPdf(WeasyTemplateResponseMixin, VistaPdf):
    pdf_stylesheets = [
        settings.STATICFILES_DIRS[0] + 'css/bootstrap.min.css',
        settings.STATICFILES_DIRS[0] + 'css/estilos.css',
    ]
    pdf_attachment = False
    pdf_filename = 'lista_dinos.pdf'

def agregar_dino(request):
    context = {'app':'Dinosaurio','nuevo':True}
    if request.method == 'POST':
        form = DinoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_periodo')
    else:
        form = DinoForm()
    return render(request, 'nuevo.html',{'form':form})


def agregar_periodo(request):
    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_periodo')
    else:
        form = PeriodoForm()
    return render(request, 'nuevo.html',{'form':form})

def eliminar_periodo(request, id):
    periodo = Periodo.objects.get(pk=id)
    periodo.delete()
    return redirect('lista_periodo')

def editar_periodo(request, id):
    periodo = Periodo.objects.get(pk=id)
    if request.method == 'POST':
        form = PeriodoForm(request.POST, instance=periodo) 
        if form.is_valid():
            form.save()
            return redirect('lista_periodo')
    else:
        form = PeriodoForm(instance=periodo) 
    return render(request, 'editar.html',{'form':form})


def lista_periodo(request):
    periodos = Periodo.objects.all()
    nombre = "T-REX"
    context = {'periodos':periodos, 'nombre':nombre}

    return render(request, 'periodos.html',context)


class Grafica(TemplateView):
    template_name = 'dinosaurios/grafica.html'
    dinos_periodo = Dinosaurio.objects.all().values('periodo').annotate(cuantos=Count('periodo'))
    periodos = Periodo.objects.all()

    datos = []
    for periodo in periodos:
        cuantos = 0
        for dp in dinos_periodo: 
            if dp['periodo'] == periodo.id:
                cuantos = dp['cuantos']
                break
        datos.append({'name':periodo.nombre, 'data':[cuantos]})

    extra_context = {'datos': datos}
    

