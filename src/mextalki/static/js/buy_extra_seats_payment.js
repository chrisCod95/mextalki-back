const csrf_token = Cookies.get('csrftoken');
const processPaymentModal = $('#processPaymentModal');
const extraSeatsSelector = $('#extraSeatsSelector');
const paypalButtons = $('.paypal-payment-button');
let stripeButtons = $('.stripe-payment-button');
const priceBoxes = $('.price-box');
const tableSeats = $('#tableSeats');
const tableTotal = $('#tableTotal');

$(function () {
    setTableFirstPrice(extra_seat_price);
    onSelectChange(extra_seat_price);
    createPaypalButtons(extra_seat_price, extra_seat_currency);
    createStripeButtons(extra_seat_price);
});

function onSelectChange(extra_seat_price) {
    extraSeatsSelector.change(function () {
        let selected = $('#extraSeatsSelector option:selected');
        let seats = extraSeatsSelector.val();
        let price = (seats * extra_seat_price);
        let target = selected.data('target');
        setTablePrice(price);
        setTableSeats(selected.text());
        hideAllPriceBoxes();
        showTarget($(`#${target}`));
    });
}

function setTableFirstPrice(extra_seat_price) {
    let selected = $('#extraSeatsSelector option:selected');
    let seats = extraSeatsSelector.val();
    let price = (seats * extra_seat_price);
    setTablePrice(price);
    setTableSeats(selected.text());
    let target = selected.data('target');
    showTarget($(`#${target}`));
}

function setTablePrice(price) {
    let message;
    message = `$ ${price} ${extra_seat_currency}`;
    tableTotal.html(message);
}

function createPaypalButtons(extra_seat_price, extra_seat_currency) {
    paypalButtons.each(function () {
        let seats = $(this).data('seats');
        let price = (seats * extra_seat_price);
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
                            currency_code: extra_seat_currency,
                            value: price.toString()
                        }
                    }]
                });
            },
            onApprove: function (data, actions) {
                processPaymentModal.modal('show');
                return actions.order.capture().then(function (details) {
                    processPayment(payment_url, details, seats);
                    processPaymentModal.modal('hide');
                });
            }
        }).render(this);
    });
}

function processPayment(process_payment_url, details, seats) {
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
        'purchased_seats': seats,
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

function createStripeButtons(extra_seat_price) {
    let stripe = Stripe(stripe_public_key);
    stripeButtons.each(function () {
        let seats = $(this).data('seats');
        let price = (seats * extra_seat_price);
        $(this).click(function () {
                createCheckoutSession(price, seats).then(function (data) {
                    stripe.redirectToCheckout({sessionId: data.sessionId}).then(handleStripeResult);
                });
            })
    })
}

function createCheckoutSession(price, seats) {
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
            'product': `${event_type} extra seats`,
            'seats': seats,
        })
    }).then(function (result) {
        return result.json();
    });
}

