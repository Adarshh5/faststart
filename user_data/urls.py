from django.urls import path
from user_data import views



urlpatterns = [
     path('savegrammar/', views.savegrammar, name='savegrammar'),
     path('toggle_save_word/', views.saveword, name='toggle_save_word'),
     path('add_definition/', views.saveuserdefinition, name='add_definition'),
     path('delete_definition/', views.deleteuserdefinition, name='delete_definition'),
     path("Profile/", views.Profile, name ="Profile"),
     path('savedVocabulary/', views.savedVocabulary, name='savedVocabulary'),
     path('removesavedvocabulary/', views.removesavedvocabulary, name='removesavedvocabulary'),
     path('savedworddetail/', views.savedworddetail, name="savedworddetail"),
   
]
