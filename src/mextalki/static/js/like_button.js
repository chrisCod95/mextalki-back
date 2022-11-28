localStorage.setItem('{{ object.slug }}', '{{ request.path }}');


$('.like-form').submit(function(e) {
    e.preventDefault();
    const url = $(this).attr('action');

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(response) {
            $('.likes-count').text(`${response.likes_count}`);
            $('#like-button').attr('disabled', true);
        },
        error: function (response) {
            console.error('error', response);
        },
    })
})
