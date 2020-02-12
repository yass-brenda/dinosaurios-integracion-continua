from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import TemplateView
from .models import Cliente, Municipio
from django.contrib.auth.models import User
from .forms import UserForm, ClienteForm, LoginForm
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .token import token_activacion
from django.contrib.auth.views import LoginView
from django.http import JsonResponse



class NuevoCliente(CreateView):
    model = User
    form_class = UserForm
    extra_context = {'cliente_form': ClienteForm()}
    template_name = 'clientes/cliente_form.html'

    def form_valid(self, form):
        cliente_form = ClienteForm(self.request.POST, self.request.FILES)
        if cliente_form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            cliente = cliente_form.save(commit=False)
            cliente.usuario = user
            cliente.save()

            dominio = get_current_site(self.request)
            mensaje = render_to_string('clientes/confirmar_cuenta.html',
                {
                    'user':user,
                    'dominio':dominio,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': token_activacion.make_token(user)
                }
            )

            email = EmailMessage(
                'Activar cuenta ',
                mensaje,
                to=[user.email]
            )
            email.content_subtype = "html"
            email.send()



        else:
            return self.render_to_response(self.get_context_data(form=form, extra_context=cliente_form))
        return super().form_valid(form)


    def form_invalid(self, form):
        cliente_form = ClienteForm(self.request.POST, self.request.FILES)
        return self.render_to_response(self.get_context_data(form=form, extra_context=cliente_form))
        

    def get_context_data(self, **kwargs):
        if 'extra_context' in kwargs:
            self.extra_context  = {'cliente_form': kwargs['extra_context'] }
        return super().get_context_data(**kwargs)




class ActivarCuenta(TemplateView):
    

    def get(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)

        try:
            uid = urlsafe_base64_decode(kwargs['uidb64'])
            token = kwargs['token']
            user = User.objects.get(pk=uid) 
        except(TypeError, ValueError, User.DoesNotExist):
            user = None
        
        if user is not None and token_activacion.check_token(user, token):
            user.is_active = True
            user.save()
            mensaje = 'Cuenta activada, ingresar datos'
        else:
            mensaje = 'Token inválido, contacta al administrador'

        return render(request, 'clientes/login.html',{'mensaje':mensaje})
        
        # return self.render_to_response(context)


class Login(LoginView):
    template_name = "clientes/login.html"
    form_class = LoginForm


def estados_municpios(request):
    id = request.POST.get('id',None)
    municipios = Municipio.objects.filter(estado_id=id)
    data = [{'id':municipio.id, 'nombre': municipio.nombre} for municipio in municipios]
    return JsonResponse(data, safe=False)



    