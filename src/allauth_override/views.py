from django.shortcuts import redirect
from django.urls import reverse_lazy


def signup_redirect(request):
    return redirect(
        reverse_lazy('sign_up'),
    )


def login_redirect(request):
    return redirect(
        reverse_lazy('login'),
    )


def logout_redirect(request):
    return redirect(
        reverse_lazy('logout'),
    )
