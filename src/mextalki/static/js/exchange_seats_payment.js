const csrf_token = Cookies.get('csrftoken');
const processPaymentModal = $('#processPaymentModal');
const extraSeatsSelect = $('#extraSeatsSelector');
const paypalButtons = $('.paypal-payment-button');
let stripeButtons = $('.stripe-payment-button');
let swapButtons = $('.swap-payment-button');
const priceBoxes = $('.price-box');
const tableSeats = $('#tableSeats');
const tableTotal = $('#tableTotal');

$(function () {
    setTableFirstPrice(extra_seat_price, discount);
    onSelectChange(extra_seat_price, discount);
    createStripeButtons(extra_seat_price, discount);
    createPaypalButtons(extra_seat_price, discount, extra_seat_currency);
    createSwapButtons(extra_seat_price, discount);
});

function setTableFirstPrice(extra_seat_price, discount) {
    let selected = $('#extraSeatsSelector option:selected');
    let seats = extraSeatsSelect.val();
    let price = (seats * extra_seat_price);
    let discountPrice = (price - discount);
    setTablePrice(price, discountPrice);
    setTableSeats(selected.text());
    let target = selected.data('target');
    showTarget($(`#${target}`));
}

function onSelectChange(extra_seat_price, discount) {
    extraSeatsSelect.change(function () {
        let selected = $('#extraSeatsSelector option:selected');
        let price = (extraSeatsSelect.val() * extra_seat_price);
        let discountPrice = (price - discount);
        let target = selected.data('target');
        setTablePrice(price, discountPrice);
        setTableSeats(selected.text());
        hideAllPriceBoxes();
        showTarget($(`#${target}`));
    });
}

function createPaypalButtons(extra_seat_price, discount, extra_seat_currency) {
    paypalButtons.each(function () {
        let seats = $(this).data('seats');
        let normal_price = (seats * extra_seat_price);
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
                                currency_code: extra_seat_currency,
                                value: price.toString()
                            }
                        }]
                    });
                },
                onApprove: function (data, actions) {
                    processPaymentModal.modal('show');
                    return actions.order.capture().then(function (details) {
                        processPayment(payment_url, details, seats, discount);
                        processPaymentModal.modal('hide');
                    });
                }
            }).render(this);
        } else {
            $(this).remove();
        }
    });
}

function createStripeButtons(extra_seat_price, discount) {
    let stripe = Stripe(stripe_public_key);
    stripeButtons.each(function () {
        let seats = $(this).data('seats');
        let normal_price = (seats * extra_seat_price);
        let price =  normal_price - discount;
        if (price >= 1) {
            $(this).click(function () {
                createCheckoutSession(price, seats, discount).then(function (data) {
                    stripe.redirectToCheckout({sessionId: data.sessionId}).then(handleStripeResult);
                });
            })
        } else {
            $(this).remove();
        }
    })
}

function createSwapButtons(extra_seat_price, discount) {
    swapButtons.each(function () {
        let seats = $(this).data('seats');
        let normal_price = (seats * extra_seat_price);
        let price = normal_price - discount;
        if (price <= 0) {
            $(this).click(function (_) {
                processSwap(swap_url, seats, normal_price)
            })
        } else {
            $(this).remove();
        }
    })
}

function setTablePrice(price, discountPrice) {
    let message;
    if (discountPrice >= 1) {
        message = `<s>$ ${price} ${extra_seat_currency}</s> $ ${discountPrice} ${extra_seat_currency}`;
    } else {
        message = `<s>$ ${price} ${extra_seat_currency}</s>`;
    }
    tableTotal.html(message);
}

function processPayment(process_payment_url, details, seats, discount) {
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

function processSwap(process_swap_url, seats, discount) {
    let data = {
        'purchased_seats': seats,
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

function createCheckoutSession(price, seats, discount) {
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
            'event_type': event_type,
            'credits': discount,
        })
    }).then(function (result) {
        return result.json();
    });
}
