$(function () {
    const csrf_token = Cookies.get('csrftoken');
    let stripe = Stripe(stripe_public_key);

    let createCheckoutSession = function (priceId) {
        return fetch(stripe_checkout_url, {
            method: "POST",
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({'price_id': priceId})
        }).then(function (result) {
            return result.json();
        });
    }
    let handleResult = function (result){
        console.error(result.error.message);
    }
    let buttons = $('.stripe-payment-button');
    buttons.each(function () {
        let button = $(this);
        button.click(function () {
            let priceId = button.data('price-id');
            createCheckoutSession(priceId).then(function (data) {
                stripe.redirectToCheckout({sessionId: data.sessionId}).then(handleResult);
            });
        })
    })
});
