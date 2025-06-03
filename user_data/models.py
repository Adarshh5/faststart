

from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError

class SavedGrammar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    simple_sentence = models.BooleanField(default=False, verbose_name="Simple Sentence")
    tense = models.BooleanField(default=False, verbose_name="Tense")
    modal_part_1 = models.BooleanField(default=False, verbose_name="Modal Part 1")
    modal_part_2 = models.BooleanField(default=False, verbose_name="Modal Part 2")
    causative_verb = models.BooleanField(default=False, verbose_name="Causative Verb")
    voice = models.BooleanField(default=False, verbose_name="Voice")
    other = models.BooleanField(default=False, verbose_name="Other")

    def __str__(self):
        try:
            return f"Grammar progress for {self.user.email}"
        except Exception:
            return f"Grammar progress (user missing)"

    class Meta:
        verbose_name = "Saved Grammar"
        verbose_name_plural = "Saved Grammar"




class SavedVocabulary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    words = models.JSONField(default=list, blank=True)  # Stores words as a list

    def __str__(self):
        return f"Vocabulary of {self.user.email} ({len(self.words)} words)"
    

class UserWordDefinitions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    definitions = models.JSONField(default=dict, blank=True)  # {'word': 'definition text'}

    def clean(self):
        # Ensure max 200 definitions
        if len(self.definitions) > 200:
            raise ValidationError("You can only save up to 200 word definitions.")

        # Check line count for each definition
        for word, definition in self.definitions.items():
            line_count = len(definition.split('\n'))
            if line_count > 5:
                raise ValidationError(
                    f"The definition for '{word}' has {line_count} lines. Max allowed is 5."
                )

    def save(self, *args, **kwargs):
        if self.definitions is None:
            self.definitions = {}  # Fallback in case it's unset
        self.full_clean()
        super().save(*args, **kwargs)

    def update_definition_only(self, word, definition):
        # Check if the word exists in the dictionary
        if word not in self.definitions:
            raise ValidationError("This word does not exist. This function is only for updating existing definitions.")

        # Check line limit
        line_count = len(definition.split('\n'))
        if line_count > 5:
            raise ValidationError("Each definition can be up to 5 lines only.")

        # Update definition
        self.definitions[word] = definition
        self.save()







# Helper function to limit lines in word definition
def validate_definition_lines(value):
    if len(value.strip().splitlines()) > 5:
        raise ValidationError("Definition cannot exceed 5 lines.")

class UserVocabulary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word_name = models.CharField(max_length=30)
    word_definition = models.TextField(validators=[validate_definition_lines])

    def save(self, *args, **kwargs):
        if UserVocabulary.objects.filter(user=self.user).count() >= 100 and not self.pk:
            raise ValidationError("You can save up to 100 vocabulary entries.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.word_name} ({self.user.username})"
    


class UserSavedContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if UserSavedContent.objects.filter(user=self.user).count() >= 10 and not self.pk:
            raise ValidationError("You can save up to 10 content entries.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Content by {self.user.username}"
    




class UserFreeTierStart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)  # The date of first content generation

    def __str__(self):
        return f"{self.user.email} - started on {self.start_date}"
    

class UserDailyStoryUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)  # Updated each day
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.email} - {self.count} stories on {self.date}"
    

class UserDailyMessageUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    message_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.email} - {self.message_count} messages on {self.date}"
