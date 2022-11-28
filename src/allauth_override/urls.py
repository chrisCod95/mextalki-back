from django.urls import path

from src.allauth_override.views import login_redirect, logout_redirect, signup_redirect

urlpatterns = [
    path('signup/', signup_redirect),
    path('login/', login_redirect),
    path('logout/', logout_redirect),
]
