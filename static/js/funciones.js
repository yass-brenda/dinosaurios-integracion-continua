$("#id_estado").change(function(e){
    var token = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax(
        {
            type: "POST",
            url: '/usuarios/obtener_municipios',
            data: {'id': this.value, 'csrfmiddlewaretoken': token},
            success: function(data){
                var html = '';
                $.each(data, function(llave, valor){
                    html += `<option value="${valor.id}">${valor.nombre}</option>`
                });
                $('#id_municipio').html(html)
            }
        }
    );
});