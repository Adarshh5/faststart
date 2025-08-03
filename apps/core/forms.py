from django import forms

class NumberInputForm(forms.Form):
    number = forms.IntegerField(
        label="Word Number",
        min_value=0,
        max_value=1000,
        error_messages={
            'min_value': 'Number cannot be less than 0.',
            'max_value': 'Number cannot be greater than 1000.',
            'invalid': 'Enter a valid number.'
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a number between 0 and 1000'
        })
    )



