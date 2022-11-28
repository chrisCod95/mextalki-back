from django import forms


class CancelSubscriptionForm(forms.Form):
    CANCEL_REASONS = [
        ('expensive', 'Too expensive'),
        ('other', 'Other'),
    ]
    confirm = forms.BooleanField(required=True)
    reason = forms.ChoiceField(choices=CANCEL_REASONS, label='Reason', required=True)
