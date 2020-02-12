from django.test import TestCase, RequestFactory
from dinosaurios.models import Dinosaurio, Periodo, VotacionDino
from django.urls import reverse
from django.contrib.auth.models import User
from django_weasyprint import WeasyTemplateResponse
from dinosaurios.views  import ListaDinoPdf, VistaPdf


class TestViews(TestCase):

    def test_url_dinos_votacion(self):
        self.user_login()
        response = self.client.get('/periodo/dinos/votacion')
        self.assertEqual(response.status_code, 200)

    def test_redireccion_a_login_dinos_votacion(self):
        response = self.client.get('/periodo/dinos/votacion')
        self.assertRedirects(response, '/usuarios/login?next=/periodo/dinos/votacion')

    def test_nombre_url_dinos_votacion(self):
        self.user_login()
        response = self.client.get(reverse('lista_dinos_votacion'))
        self.assertEqual(response.status_code, 200)

    def test_template_dinos_votacion(self):
        self.user_login()
        response = self.client.get('/periodo/dinos/votacion')
        self.assertTemplateUsed(response, 'dinosaurios/dinosaurio_lista_votacion.html')

    def test_envio_datos_dino(self):
        self.user_login()
        self.agrega_dino()
        response = self.client.get('/periodo/dinos/votacion')
        self.assertIn('object_list', response.context)

    def test_envio_t_rex_datos_dino(self):
        self.user_login()
        self.agrega_dino()

        response = self.client.get('/periodo/dinos/votacion')
        self.assertEquals('T-Rex', response.context['object_list'][0]['dino'].nombre)

    def test_t_rex_se_encuentre_en_template(self):
        self.user_login()
        self.agrega_dino()
        response = self.client.get('/periodo/dinos/votacion')
        self.assertContains(response, 'T-Rex')
       
    def test_t_rex_se_encuentre_en_template_en_un_td(self):
        self.user_login()
        self.agrega_dino()
        response = self.client.get('/periodo/dinos/votacion')
        self.assertInHTML('<td>T-Rex</td>',response.rendered_content)


    def test_t_rex_calificacion_4_estrellas(self):
        usuario = self.user_login()
        dino = self.agrega_dino()
        votacion = VotacionDino.objects.create(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 4,
            rollo = 'me pareció muy chido el dino'
        )
        response = self.client.get('/periodo/dinos/votacion')
        self.assertInHTML('<td>4.0 calificación</td>',response.rendered_content)

    def test_t_rex_calificacion_3_estrellas(self):
        usuario = self.user_login()
        dino = self.agrega_dino()
        votacion = VotacionDino.objects.create(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 3.0,
            rollo = 'me pareció muy chido el dino'
        )
        response = self.client.get('/periodo/dinos/votacion')
        self.assertInHTML('<td>3.0 calificación</td>',response.rendered_content)

    def test_t_rex_calificacion_3_estrellas(self):
        usuario = self.user_login()
        dino = self.agrega_dino()
        votacion = VotacionDino.objects.create(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 3,
            rollo = 'me pareció muy chido el dino'
        )
        usuario = User.objects.create(username='juan', password='alex123')
        votacion = VotacionDino.objects.create(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 5,
            rollo = 'me pareció muy chido el dino'
        )
        response = self.client.get('/periodo/dinos/votacion')
        self.assertInHTML('<td>4.0 calificación</td>',response.rendered_content)

    def test_t_rex_calificacion_0_estrellas(self):
        usuario = self.user_login()
        dino = self.agrega_dino()
        response = self.client.get('/periodo/dinos/votacion')
        self.assertInHTML('<td>0 calificación</td>',response.rendered_content)

    def test_t_rex_calificacion_3_estrellas_img(self):
        usuario = self.user_login()
        dino = self.agrega_dino()
        votacion = VotacionDino.objects.create(
            dinosaurio = dino,
            usuario = usuario,
            calificacion = 3.0,
            rollo = 'me pareció muy chido el dino'
        )
        estrellas = '<td><img src="/static/images/star-filled.svg" class="voto-img"><img src="/static/images/star-filled.svg" class="voto-img">'
        estrellas += '<img src="/static/images/star-filled.svg" class="voto-img"><img src="/static/images/star-empty.svg" class="voto-img">'
        estrellas += '<img src="/static/images/star-empty.svg" class="voto-img"></td>'
        response = self.client.get('/periodo/dinos/votacion')
        self.assertInHTML(estrellas,response.rendered_content)

    def test_lista_pdf_status_code_200(self):
        response = self.client.get('/periodo/dinos/lista_pdf')
        self.assertEqual(response.status_code, 200)

    def test_lista_pdf_template_used(self):
        response = self.client.get('/periodo/dinos/lista_pdf')
        self.assertTemplateUsed(response, 'dinosaurios/dinosaurio_pdf.html')

    def test_lista_pdf_view_name(self):
        response = self.client.get(reverse('lista_dinos_pdf'))
        self.assertTemplateUsed(response, 'dinosaurios/dinosaurio_pdf.html')
    
    def test_lista_pdf_es_objeto_de_weasy_template_response(self):
        response = self.client.get(reverse('lista_dinos_pdf'))
        self.assertIsInstance(response, WeasyTemplateResponse)

    def test_envio_datos_dino_pdf(self):
        self.agrega_dino()
        response = self.client.get('/periodo/dinos/lista_pdf')
        self.assertIn('object_list', response.context)

    def test_envio_t_rex_datos_dino_pdf(self):
        self.agrega_dino()

        response = self.client.get('/periodo/dinos/lista_pdf')
        self.assertEquals('T-Rex', response.context['object_list'][0].nombre)

    def test_lista_pdf_se_renderizo(self):
        self.agrega_dino()
        response = self.client.get(reverse('lista_dinos_pdf'))
        self.assertTrue(response.is_rendered)
    
    def test_lista_pdf_content_type(self):
        self.agrega_dino()
        response = self.client.get(reverse('lista_dinos_pdf'))
        self.assertIn("application/pdf", str(response))

    def test_lista_pdf_nombre_archivo(self):
        view_pdf = ListaDinoPdf()
        self.assertEqual('lista_dinos.pdf', view_pdf.pdf_filename)

    def test_lista_pdf_no_se_incluya_como_adjunto(self):
        view_pdf = ListaDinoPdf()
        self.assertFalse(view_pdf.pdf_attachment)

    def test_lista_pdf_modelo_sea_dinosaurio(self):
        view_pdf = ListaDinoPdf()
        self.assertEqual(view_pdf.model, Dinosaurio)
    
    def test_lista_pdf_incluya_el_css_bootstrap(self):
        view_pdf = ListaDinoPdf()
        lista_css = view_pdf.pdf_stylesheets
        bootstrap = lista_css[0].split('/')[-1]
        self.assertEqual('bootstrap.min.css', bootstrap)

    def test_lista_pdf_incluya_el_css_estilos(self):
        view_pdf = ListaDinoPdf()
        lista_css = view_pdf.pdf_stylesheets
        estilos = lista_css[1].split('/')[-1]
        self.assertEqual('estilos.css', estilos)

    def agrega_periodo(self):
        return Periodo.objects.create(nombre = 'Cretacio')

    def agrega_dino(self):
        return Dinosaurio.objects.create(
            nombre = 'T-Rex',
            altura = 5.5,
            periodo = self.agrega_periodo()

        )  
    def user_login(self):
        usuario = User.objects.create_user(username='alex', password='alex123')
        self.client.login(username='alex', password='alex123')
        return usuario
    
