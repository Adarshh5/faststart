from django.urls import path
from apps.user_data import views



urlpatterns = [
     path('savegrammar/', views.savegrammar, name='savegrammar'),
     path('toggle-save-word/', views.saveword, name='toggle_save_word'),
     path('add-definition/', views.saveuserdefinition, name='add_definition'),
     path('delete-definition/', views.deleteuserdefinition, name='delete_definition'),
     path("Profile/", views.Profile, name ="Profile"),
     path('saved-vocabulary/', views.savedVocabulary, name='savedVocabulary'),
     path('remove-saved-vocabulary/', views.removesavedvocabulary, name='removesavedvocabulary'),
     path('saved-word-detail/', views.savedworddetail, name="savedworddetail"),
   
]
