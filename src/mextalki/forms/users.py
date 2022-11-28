from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254)


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': 'The two password fields didn’t match.',
    }
    new_password1 = forms.CharField(
        label='New password',
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='New password confirmation',
        strip=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
