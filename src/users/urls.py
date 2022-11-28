from django.urls import path

from src.users.views import (
    EditProfileView,
    ProfileView,
    SignInView,
    SignUpView,
    logout_view,
    resend_verify_view,
    verify_view,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('resend_verify_email/', resend_verify_view, name='resend_verify_email'),
    path('verify_email/<uidb64>/<token>/', verify_view, name='verify_email'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/', ProfileView.as_view(), name='dashboard'),
]
