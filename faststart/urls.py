
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('Lemento-admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls') ),
    path('userdata/', include('user_data.urls') ),
    path('aifeature/', include('ai_assistant.urls') ),
    path('ckeditor5/', include('django_ckeditor_5.urls')),  # 👈 Add this
]
