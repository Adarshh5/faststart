from django import forms
from apps.accounts.models import User
from django.contrib.auth.forms import PasswordChangeForm


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    agree_to_terms = forms.BooleanField(
        label="I agree to the Terms & Conditions and Privacy Policy",
        required=True
    )

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data




class CustomLoginForm(forms.Form):
    email = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))




class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )



class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'form-control'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "No account is associated with this email address."
            )
        
        return email





from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm

class SetPasswordForm(DjangoSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
