from django.urls import path
from apps.ai_assistant import views



urlpatterns = [
    path('textgeneration/', views.textgeneration.as_view(), name='textgeneration'),
    path('textgenerationresult/', views.textgenerationresult, name='textgenerationresult'),
    path('chatbot/', views.Chatbot.as_view(), name='Chatbot'),
    path('ai-tutor/',views.AItutor.as_view(), name="Ai_tutor"),

   
]
