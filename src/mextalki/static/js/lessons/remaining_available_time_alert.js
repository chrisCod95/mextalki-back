$('.alert').click(function() {
  let element = $(this);
  let tmpClass = element.attr('class');
  element.removeClass();
  setTimeout(function() {
    element.offsetWidth = element.offsetWidth;
    element.addClass(tmpClass).addClass('start-now');
  }, 10);
});

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});
