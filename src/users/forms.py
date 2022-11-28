from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)


class CustomUserSignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
        help_texts = {
            'email': "We'll never share your email with anyone else.",
        }


class SignInForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'profile_picture', 'first_name',
            'last_name', 'location', 'birth_day', 'bio',
        )
