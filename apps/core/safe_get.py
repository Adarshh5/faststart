from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist

def safe_get_or_create(model, **kwargs):
    try:
        with transaction.atomic():
            return model.objects.get_or_create(**kwargs)
    except IntegrityError:
        # If it failed because of a race condition, fallback safely
        instance = model.objects.filter(**kwargs).first()
        if instance:
            return instance, False
        # Extremely rare fallback
        return model.objects.create(**kwargs), True

