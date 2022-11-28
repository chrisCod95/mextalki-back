const csrf_token = Cookies.get('csrftoken');
const processPaymentModal = $('#processPaymentModal');
const extraHourSelect = $('#extraHourSelector');
const paypalButtons = $('.paypal-payment-button');
let stripeButtons = $('.stripe-payment-button');
const priceBoxes = $('.price-box');
const tableHours = $('#tableHours');
const tableTotal = $('#tableTotal');

$(function () {
    setTableFirstPrice(extra_hour_price, discount_percentage);
    onSelectChange(extra_hour_price, discount_percentage);
    createStripeButtons(extra_hour_price, discount_percentage);
    createPaypalButtons(extra_hour_price, discount_percentage, extra_hour_currency);
});

function onSelectChange(extra_hour_price, discount_price) {
    extraHourSelect.change(function () {
        let selected = $('#extraHourSelector option:selected');
        let hours = extraHourSelect.val();
        let normal_price = (hours * extra_hour_price);
        let price = normal_price - (normal_price * discount_percentage);
        let target = selected.data('target');
        setTablePrice(normal_price, price);
        setTableHours(selected.text());
        hideAllPriceBoxes();
        showTarget($(`#${target}`));
    });
}

function createPaypalButtons(extra_hour_price, discount_percentage, extra_hour_currency) {
    paypalButtons.each(function () {
        let hours = $(this).data('hours');
        let normal_price = (hours * extra_hour_price);
        let price = normal_price - (normal_price * discount_percentage);
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
                    processPayment(payment_url, details, hours, coupon_code);
                    processPaymentModal.modal('hide');
                });
            }
        }).render(this);
    });
}

function createStripeButtons(extra_hour_price, discount_percentage) {
    let stripe = Stripe(stripe_public_key);
    stripeButtons.each(function () {
        let hours = $(this).data('hours');
        let normal_price = (hours * extra_hour_price);
        let price = normal_price - (normal_price * discount_percentage);
        $(this).click(function () {
                createCheckoutSession(price, hours, coupon_code).then(function (data) {
                    stripe.redirectToCheckout({sessionId: data.sessionId}).then(handleStripeResult);
                });
            })
    })
}

function setTableFirstPrice(extra_hour_price, discount_percentage) {
    let selected = $('#extraHourSelector option:selected');
    let hours = extraHourSelect.val();
    let normal_price = (hours * extra_hour_price);
    let price = normal_price - (normal_price * discount_percentage);
    setTablePrice(normal_price, price);
    setTableHours(selected.text());
    let target = selected.data('target');
    showTarget($(`#${target}`));
}

function setTablePrice(normal_price, price) {
    let message;
    let parsePrice = price.toFixed(2);
    if (normal_price > price) {
        message = `<s>$ ${normal_price} ${extra_hour_currency}</s> $ ${parsePrice} ${extra_hour_currency}`;
    } else {
        message = `$ ${normal_price} ${extra_hour_currency}`;
    }
    tableTotal.html(message);
}

function processPayment(process_payment_url, details, hours, coupon_code) {
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
        'coupon_code': valid_coupon ? coupon_code : null,
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

function createCheckoutSession(price, hours, coupon_code) {
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
            'coupon_code': valid_coupon ? coupon_code : null,
        })
    }).then(function (result) {
        return result.json();
    });
}

