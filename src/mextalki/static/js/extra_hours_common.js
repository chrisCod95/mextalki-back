function setTableHours(hours) {
    tableHours.text(hours);
}

function showTarget(target) {
    target.removeClass('d-none');
    target.addClass('d-block');
}

function hideAllPriceBoxes() {
    priceBoxes.each(function () {
        $(this).removeClass('d-block');
        $(this).addClass('d-none');
    })
}

function handleStripeResult(result) {
    console.error(result.error.message);
}
