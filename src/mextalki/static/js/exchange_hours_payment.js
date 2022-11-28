const csrf_token = Cookies.get('csrftoken');
const processPaymentModal = $('#processPaymentModal');
const extraHourSelect = $('#extraHourSelector');
const paypalButtons = $('.paypal-payment-button');
let stripeButtons = $('.stripe-payment-button');
let swapButtons = $('.swap-payment-button');
const priceBoxes = $('.price-box');
const tableHours = $('#tableHours');
const tableTotal = $('#tableTotal');

$(function () {
    setTableFirstPrice(extra_hour_price, discount);
    onSelectChange(extra_hour_price, discount);
    createStripeButtons(extra_hour_price, discount);
    createPaypalButtons(extra_hour_price, discount, extra_hour_currency);
    createSwapButtons(extra_hour_price, discount);
});

function setTableFirstPrice(extra_hour_price, discount) {
    let selected = $('#extraHourSelector option:selected');
    let hours = extraHourSelect.val();
    let price = (hours * extra_hour_price);
    let discountPrice = (price - discount);
    setTablePrice(price, discountPrice);
    setTableHours(selected.text());
    let target = selected.data('target');
    showTarget($(`#${target}`));
}

function onSelectChange(extra_hour_price, discount) {
    extraHourSelect.change(function () {
        let selected = $('#extraHourSelector option:selected');
        let price = (extraHourSelect.val() * extra_hour_price);
        let discountPrice = (price - discount);
        let target = selected.data('target');
        setTablePrice(price, discountPrice);
        setTableHours(selected.text());
        hideAllPriceBoxes();
        showTarget($(`#${target}`));
    });
}

function createPaypalButtons(extra_hour_price, discount, extra_hour_currency) {
    paypalButtons.each(function () {
        let hours = $(this).data('hours');
        let normal_price = (hours * extra_hour_price);
        let price =  normal_price - discount;
        if (price >= 1) {
            paypal.Buttons({
                style: {
                    shape: 'rect',
                    color: 'gold',
                    layout: 'vertical',
                },
                fundingSource: paypal.FUNDING.PAYPAL,
                createOrder: function (data, actions) {
                    return actions.order.create({
                        purchase_units: [{
                            amount: {
                                currency_code: extra_hour_currency,
                                value: price.toString()
                            }
                        }]
                    });
                },
                onApprove: function (data, actions) {
                    processPaymentModal.modal('show');
                    return actions.order.capture().then(function (details) {
                        processPayment(payment_url, details, hours, discount);
                        processPaymentModal.modal('hide');
                    });
                }
            }).render(this);
        } else {
            $(this).remove();
        }
    });
}

function createStripeButtons(extra_hour_price, discount) {
    let stripe = Stripe(stripe_public_key);
    stripeButtons.each(function () {
        let hours = $(this).data('hours');
        let normal_price = (hours * extra_hour_price);
        let price =  normal_price - discount;
        if (price >= 1) {
            $(this).click(function () {
                createCheckoutSession(price, hours, discount).then(function (data) {
                    stripe.redirectToCheckout({sessionId: data.sessionId}).then(handleStripeResult);
                });
            })
        } else {
            $(this).remove();
        }
    })
}

function createSwapButtons(extra_hour_price, discount) {
    swapButtons.each(function () {
        let hours = $(this).data('hours');
        let normal_price = (hours * extra_hour_price);
        let price = normal_price - discount;
        if (price <= 0) {
            $(this).click(function (_) {
                processSwap(swap_url, hours, normal_price)
            })
        } else {
            $(this).remove();
        }
    })
}

function setTablePrice(price, discountPrice) {
    let message;
    if (discountPrice >= 1) {
        message = `<s>$ ${price} ${extra_hour_currency}</s> $ ${discountPrice} ${extra_hour_currency}`;
    } else {
        message = `<s>$ ${price} ${extra_hour_currency}</s>`;
    }
    tableTotal.html(message);
}

function processPayment(process_payment_url, details, hours, discount) {
    const {id, intent, status, payer, create_time, update_time} = details;
    const {name: payer_name} = payer;
    let data = {
        'paypal_id': id,
        'paypal_intent': intent,
        'paypal_status': status,
        'paypal_payer_email': payer.email_address,
        'paypal_payer_id': payer.payer_id,
        'paypal_payer_name': `${payer_name.given_name} ${payer_name.surname}`,
        'paypal_created_at': create_time,
        'paypal_updated_at': update_time,
        'purchased_hours': hours,
        'credits': discount,
    }
    $.ajax({
        method: 'post',
        url: process_payment_url,
        headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        dataType: "json",
        data: JSON.stringify(data),
        success: function (data) {
            const {redirect_url} = data;
            window.location = redirect_url;
        },
        error: function (data) {
            const {responseJSON} = data;
            window.location = responseJSON.redirect_url;
        }
    });
}

function processSwap(process_swap_url, hours, discount) {
    let data = {
        'purchased_hours': hours,
        'credits': discount,
    }
    $.ajax({
        method: 'post',
        url: process_swap_url,
        headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        dataType: "json",
        data: JSON.stringify(data),
        success: function (data) {
            const {redirect_url} = data;
            window.location = redirect_url;
        },
        error: function (data) {
            const {responseJSON} = data;
            window.location = responseJSON.redirect_url;
        }
    });
}

function createCheckoutSession(price, hours, discount) {
    let parsePrice = price.toFixed(2);
    return fetch(stripe_checkout_url, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            'price': parsePrice,
            'product': `${event_type} extra hours`,
            'hours': hours,
            'event_type': event_type,
            'credits': discount,
        })
    }).then(function (result) {
        return result.json();
    });
}
