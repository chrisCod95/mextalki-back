$(function () {
    let collapse_list = $('#faqAccordion').find('.collapse');
    collapse_list.each(function (){
        let collapse = $(this);
        let icon = collapse.parent().find('i.fas');
        collapse.on('hidden.bs.collapse', function () {
            icon.removeClass('fa-chevron-up');
            icon.addClass('fa-chevron-down');
        });
        collapse.on('show.bs.collapse', function () {
            icon.removeClass('fa-chevron-down');
            icon.addClass('fa-chevron-up');
        });
    });
});
