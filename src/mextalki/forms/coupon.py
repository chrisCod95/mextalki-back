from django import forms


class CouponForm(forms.Form):
    promo_code = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'coupon-code',
                'placeholder': 'Enter a promo code',
            },
        ),
    )
