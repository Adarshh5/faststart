from allauth.account.adapter import DefaultAccountAdapter

class NoUsernameAccountAdapter(DefaultAccountAdapter):
    def clean_username(self, username):
        return ""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model
from allauth.account.utils import user_email

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Email from social login
        email = user_email(sociallogin.user)

        if email:
            User = get_user_model()
            try:
                existing_user = User.objects.get(email=email)
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.is_active = True  # Activate Google users immediately
        user.save()
        return user
