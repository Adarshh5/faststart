from django.urls import path
from apps.core import views



urlpatterns = [
    path('', views.home, name='home'),
    path('topic/grammar/', views.grammar, name='grammar'),
    path('topic/vocabulary/', views.vocabulary, name='vocabulary'),
    path('word_detail/<int:pk>/', views.WordDetail.as_view(), name='word_detail'),
    path('grammar-topics/', views.grammartopics, name='grammar-topics'),
    path('checkchatvalidation/',views.checkchatvalidation, name='checkchatvalidation'),
    path('Listning/', views.Listning, name ='Listning'),
   
   
]
