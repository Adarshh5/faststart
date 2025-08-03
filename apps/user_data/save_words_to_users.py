import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "faststart.settings")
django.setup()

from accounts.models import User
from core.models import Vocabulary
from user_data.models import SavedVocabulary

def save_words_to_users():
    # Get all word names from Vocabulary model
    all_word_names = list(Vocabulary.objects.values_list('word_name', flat=True))

    # Iterate over all users
    for user in User.objects.all():
        saved_vocab, created = SavedVocabulary.objects.get_or_create(user=user)
        saved_vocab.words = all_word_names  # Save only word names
        saved_vocab.save()

    print("All words saved to every user's SavedVocabulary.")

if __name__ == "__main__":
    save_words_to_users()
