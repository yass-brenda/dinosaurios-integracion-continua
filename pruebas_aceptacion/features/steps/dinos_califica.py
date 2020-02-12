from behave import when, then, given
import time


@given(u'que ingreso al sistema')
def step_impl(context):
    login(context)

@when(u'entro a la sección de dinosaurios calificados')
def step_impl(context):
    context.driver.get(context.url+'periodo/dinos/votacion')

    


@then(u'puede ver el dinosaurio "{dino}" con "{cal}"')
def step_impl(context, dino, cal):
    context.test.assertIn(dino, context.driver.page_source)
    context.test.assertIn(cal, context.driver.page_source)

    


def login(context):
    context.driver.get(context.url+'usuarios/login')
    time.sleep = 1
    context.driver.find_element_by_id('id_username').send_keys('otro')
    context.driver.find_element_by_id('id_password').send_keys('Temporal2019@')
    context.driver.find_element_by_tag_name('button').click()