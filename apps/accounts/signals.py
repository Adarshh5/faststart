from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.accounts.models import UserAgreement

User = settings.AUTH_USER_MODEL

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_agreement(sender, instance, created, **kwargs):
    if created:
        UserAgreement.objects.get_or_create(
            user=instance,
            defaults={"agreed": False}
        )
