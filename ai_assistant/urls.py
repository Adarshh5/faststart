from django.urls import path
from ai_assistant import views



urlpatterns = [
    path('textgeneration/', views.textgeneration.as_view(), name='textgeneration'),
    path('textgenerationresult/', views.textgenerationresult, name='textgenerationresult'),
    path('Chatbot/', views.Chatbot.as_view(), name='Chatbot'),

   
]
