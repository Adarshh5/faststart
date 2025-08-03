# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from .models import SavedVocabulary, SavedGrammar, UserWordDefinitions


@receiver(post_save, sender=User)
def create_user_saved_items(sender, instance, created, **kwargs):
    if created:
        SavedGrammar.objects.create(user=instance)
        SavedVocabulary.objects.create(user=instance)
        UserWordDefinitions.objects.create(user=instance)
    