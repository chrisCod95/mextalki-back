let billing_cycle_selector = $('#billing-cycle-selector');
let half_year_box = $('#half-year-options');
let monthly_box = $('#monthly-options');

billing_cycle_selector.change(() => {
    if(billing_cycle_selector.is(':checked')){
        half_year_box.removeClass('d-none');
        monthly_box.addClass('d-none');
    } else {
        monthly_box.removeClass('d-none');
        half_year_box.addClass('d-none');
    }
});

