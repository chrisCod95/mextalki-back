from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('src.users.urls')),
    path('subscription/', include('src.subscription.urls')),
    path('paypal/', include('src.paypal.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('src.api.urls')),
    path('accounts/', include('src.allauth_override.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('src.mextalki.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
