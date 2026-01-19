# apps/accounts/decorators.py
from django.shortcuts import redirect
from django.urls import reverse
from apps.accounts.models import UserAgreement

def check_agreement_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user_agreement,_ = UserAgreement.objects.get_or_create(user=request.user)
                if not user_agreement.agreed:
                    return redirect(f"{reverse('agree_terms')}?next={request.path}")
            except UserAgreement.DoesNotExist:
                return redirect(f"{reverse('agree_terms')}?next={request.path}")
        return view_func(request, *args, **kwargs)
    return wrapper