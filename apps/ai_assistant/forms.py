from django import forms


INCLUDE_CHOICES = [
    ('include', 'Include'),
    ('not_include', 'Do not Include'),
]

STORY_TONE_CHOICES = [
    ('Twist Ending', 'Twist Ending'),
    ('Moral Lesson', 'Moral Lesson'),
    ('Emotional Journey', 'Emotional Journey'),
    ('Humorous Style', 'Humorous Style'),
]

class UserStoryStylingForm(forms.Form):
    grammar = forms.ChoiceField(choices=INCLUDE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    add_my_added_vocabulary = forms.ChoiceField(choices=INCLUDE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    story_tone = forms.ChoiceField(choices=STORY_TONE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


class UserContentStylingForm(forms.Form):
    grammar = forms.ChoiceField(choices=INCLUDE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    add_my_added_vocabulary = forms.ChoiceField(choices=INCLUDE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    prompt = forms.CharField(
        label="Enter your custom prompt",
        widget=forms.Textarea(attrs={"rows": 3, 'class': 'form-control'})
    )