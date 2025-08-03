
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('Lemento-admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.core.urls') ),
    path('userdata/', include('apps.user_data.urls') ),
    path('aifeature/', include('apps.ai_assistant.urls') ),
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # 👈 Add this
]
