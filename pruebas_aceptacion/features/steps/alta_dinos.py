from behave import given, when, then
from selenium import webdriver
from unittest import TestCase

@given(u'Que ingreso al formulario para llenar los datos del dinosaurios')
def step_impl(context):
    context.driver.get('http://192.168.33.10:8000/periodo/nuevo/dino')


@given(u'escribo los datos: nombre "{nombre}", altura: "{altura}", periodo: "{periodo}", imagen: "{imagen}"')
def step_impl(context,nombre, altura, periodo, imagen):
    context.driver.find_element_by_id('id_nombre').send_keys(nombre)
    context.driver.find_element_by_id('id_altura').send_keys(altura)
    context.driver.find_element_by_id('id_periodo').send_keys(periodo)
    context.driver.find_element_by_id('id_imagen').send_keys(imagen)


@when(u'presiono el botón agregar')
def step_impl(context):
    context.driver.find_element_by_class_name('btn-primary').click()
    


@then(u'puedo ver el dinosario "{dino}" en la lista de dinosaurios')
def step_impl(context, dino):
    rows =  context.driver.find_elements_by_tag_name('tr')
    dinos = [row.find_elements_by_tag_name('td')[1].text for row in rows[1:] ]
    
    test = TestCase()
    test.assertIn(dino,dinos)
