import os
import django

# SETUP DJANGO
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faststart.settings')
django.setup()

from core.models import Vocabulary


# Your input word list (you can replace this each time)
input_words =[
    "fancy", "fare", "uneasy", "gasp", "gather", "lap", "lash", "harbour",
    "deaf", "deal", "rapid", "warm", "bank", "bar", "lazy", "legal", "loud",
    "lucky", "meaningful", "imagine", "wake up", "walk out", "wear out",
    "watch out", "warm up", "write down", "check later", "come early",
    "do your best", "go for it", "have to", "just kidding", "no way", 
    "not really", "on hold", "long time", "in touch"
]


existing_words = set()
for word in input_words:
    if Vocabulary.objects.filter(word_name__iexact=word).exists():
        existing_words.add(word.lower())

# Normalize existing words too
existing_words_normalized = set(word.lower() for word in existing_words)

# Get missing words
missing_words = [word for word in input_words if word.lower() not in existing_words_normalized]

# Print results
print(existing_words_normalized)
print("✅ Missing words (send to DeepSeek):")
# for word in missing_words:
#     print(word)

print(missing_words)