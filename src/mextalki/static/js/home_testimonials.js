let animation_elements = $.find('.animation-element');
let web_window = $(window);

function check_if_in_view() {
    let window_height = web_window.height();
    let window_top_position = web_window.scrollTop();
    let window_bottom_position = (window_top_position + window_height);
    $.each(animation_elements, function () {
        let element = $(this);
        let element_height = $(element).outerHeight();
        let element_top_position = $(element).offset().top;
        let element_bottom_position = (element_top_position + element_height);
        if ((element_bottom_position >= window_top_position) && (element_top_position <= window_bottom_position)) {
            element.addClass('in-view');
        } else {
            element.removeClass('in-view');
        }
    });
}

$(window).on('scroll resize', function () {
    check_if_in_view()
})
$(window).trigger('scroll');