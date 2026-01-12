
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from .sitemaps import StaticSitemap

sitemaps = {
    'static': StaticSitemap,
}

urlpatterns = [
    path('Lemento-admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.core.urls') ),
    path('userdata/', include('apps.user_data.urls') ),
    path('ai-feature/', include('apps.ai_assistant.urls') ),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'), 
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt",
        content_type="text/plain"
    )),
]