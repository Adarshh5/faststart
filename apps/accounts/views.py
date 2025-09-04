from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,  redirect
from django.views import View
from .forms import RegistrationForm, CustomLoginForm, CustomPasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from apps.accounts.models import User, UserAgreement
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import os
from apps.accounts.utils import send_activation_email, send_reset_password_email
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from dotenv import load_dotenv
load_dotenv()
 





def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            # Save agreement info
            UserAgreement.objects.create(
                user=user,
                agreed=form.cleaned_data['agree_to_terms']
            )

            # Send activation email
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
            activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
            send_activation_email(user.email, activation_url)

            messages.success(
                request, "Registration Successful! Please check your email to activate your account.",
            )
            return redirect('login')
        
        else:
            # Form is NOT valid → Show errors on same page
            messages.error(request, "Please correct the errors below.")
            return render(request, 'accounts/registration.html', {'form': form})


    else:
        form = RegistrationForm()
    return render(request, 'accounts/registration.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user.is_active:
            messages.warning(request, "This account has already been activated")
            return redirect('login')
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully!')
            return redirect('login')
        else:
            messages.error(request, 'The activation link is invalid or has expired')
            return redirect('login')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link.")
        return redirect('login')





class CustomLoginView(View):
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
                return redirect('login')

            if not user.is_active:
                messages.error(request, "Your account is inactive. Please activate your account.")
                return redirect('login')

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # redirect to your dashboard/home
            else:
                messages.error(request, "Invalid email or password.")

        return render(request, self.template_name, {'form': form})






@method_decorator(login_required, name='dispatch')
class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'accounts/ChangePassword.html'
    form_class = CustomPasswordChangeForm

    def get(self, request):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request, "Password changed successfully. Please log in with your new password.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

        return render(request, self.template_name, {'form': form})






def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user =  User.objects.filter(email=email).first()
            if user:
                
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                absolute_reset_url = f"{request.build_absolute_uri(reset_url)}"
               
                send_reset_password_email(user.email, absolute_reset_url)
                messages.success(request, (
                    "We have sent you a password reset link. please check your email"

                ))
                return redirect('login')
        return render(request, 'accounts/password_reset.html', {"form": form})

    else:
        form = PasswordResetForm()
        return render(request, 'accounts/password_reset.html', {"form": form})
    


def password_reset_confirm_view(request, uidb64, token):
     try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
           messages.error(request, 'This link has expired or is invalid')
           return redirect('paasword_reset')
        
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success( request, ('Your password has been successfuly reset'))
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
                return render(request, 'accounts/password_reset_confirm.html', {
                    'form': form,
                    'uidb64': uidb64,
                    'token': token
                })
                    
        else:
            form = SetPasswordForm(user)
            return render(request, 'accounts/password_reset_confirm.html', {'form' :form, 'uidb64': uidb64, 'token': token})


     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "An error occurred. Please try again later. ")
        return redirect('password_reset')
     


def privacy_policy_view(request):
    return render(request, 'accounts/privacy_policy.html')


def terms_and_condition(request):
    return render(request, 'accounts/terms_and_condition.html')



def error_view(request):
    raise ValueError("This is a test error")
