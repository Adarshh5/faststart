from django.urls import path
from account import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
   
]
