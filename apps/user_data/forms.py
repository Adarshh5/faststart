from django import forms

class UserDefinitionForm(forms.Form):
    word = forms.CharField()
    definition = forms.CharField(
        label="Add your definition",
        widget=forms.Textarea(attrs={"rows": 2, 'class': 'form-control'})
    )

    def clean_definition(self):
        definition = self.cleaned_data['definition']
        line_count = len(definition.strip().split('\n'))
        if line_count > 5:
            raise forms.ValidationError("Each definition can only have up to 5 lines.")
        return definition


