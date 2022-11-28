$(function () {
    const processPaymentModal = $('#processPaymentModal');
    const csrf_token = Cookies.get('csrftoken');

    function createButton(selector, process_payment_url, price, currency) {
        paypal.Buttons({
            createOrder: function (data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        amount: {
                            currency_code: currency,
                            value: price.toString()
                        }
                    }]
                });
            },
            onApprove: function (data, actions) {
                processPaymentModal.modal('show');
                return actions.order.capture().then(function (details) {
                    processPayment(process_payment_url, details);
                    processPaymentModal.modal('hide');
                });
            }
        }).render(selector);
    }

    function processPayment(process_payment_url, details) {
        const { id , intent, status, payer, create_time, update_time } = details;
        const { name: payer_name } = payer;
        let data = {
            'paypal_id': id,
            'paypal_intent': intent,
            'paypal_status': status,
            'paypal_payer_email': payer.email_address,
            'paypal_payer_id': payer.payer_id,
            'paypal_payer_name': `${payer_name.given_name} ${payer_name.surname}`,
            'paypal_created_at': create_time,
            'paypal_updated_at': update_time
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
            success: function (data){
                const { redirect_url } = data;
                window.location = redirect_url;
            },
            error: function (data){
                const { responseJSON } = data;
                window.location = responseJSON.redirect_url;
            }
        });
    }

    let buttons = $('.paypal-payment-button');
    buttons.each(function () {
        let process_payment_url = $(this).data('payment-url');
        let price = $(this).data('price');
        let currency = $(this).data('currency');
        createButton(this, process_payment_url, price, currency);
    })
});
