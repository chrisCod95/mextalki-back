$(function () {
    const csrf_token = Cookies.get('csrftoken');

    function createButton(selector, process_payment_url, paypal_plan_id) {
        let button = paypal.Buttons({
             style: {
              shape: 'rect',
              color: 'gold',
              layout: 'vertical',
              label: 'subscribe'
            },
            fundingSource:  paypal.FUNDING.PAYPAL,
            createSubscription: function (data, actions) {
                return actions.subscription.create({
                    'plan_id': paypal_plan_id
                });
            },
            onApprove: function (data) {
                processPayment(process_payment_url, data);
            }
        })
        button.render(selector);
    }

    function processPayment(process_payment_url, data) {
        const { subscriptionID } = data;
        let payload = {
            'paypal_subscription_id': subscriptionID,
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
            data: JSON.stringify(payload),
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
        let paypal_plan_id = $(this).data('paypal-plan-id');
        createButton(this, process_payment_url, paypal_plan_id);
    })
});
