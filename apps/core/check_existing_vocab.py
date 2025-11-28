import os
import django
import sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

django.setup()   # <-- MUST come before model imports

from apps.core.models import Vocabulary   # now safe

# Your input word list (you can replace this each time)
input_words = [
    "Articulate", "Procrastinate", "Delegate", "Facilitate", "Alleviate",
    "Speculate", "Compensate", "Negotiate", "Initiate", "Terminate",
    "Comprehend", "Elaborate", "Anticipate", "Tolerate", "Amplify",
    "Deteriorate", "Rejuvenate", "Manipulate", "Validate", "Imitate",
    "Contemplate", "Venture", "Ascertain", "Refrain", "Perceive",
    "Dilemma", "Priority", "Consensus", "Perks", "Incentive",
    "Accountability", "Autonomy", "Burnout", "Deadline", "Mindset",
    "Nuance", "Setback", "Stakeholder", "Threshold", "Verification",
    "Aftermath", "Bottleneck", "Conscience", "Ethics", "Criteria",
    "Insight", "Morale", "Obligation", "Protocol", "Sanction",
    "Tedious", "Feasible", "Crucial", "Inevitable", "Versatile",
    "Robust", "Subtle", "Trivial", "Ubiquitous", "Vague", "Wary",
    "Zealous", "Ambiguous", "Comprehensive", "Consecutive", "Deficient",
    "Eccentric", "Formidable", "Gregarious", "Hectic", "Indispensable",
    "Jeopardy", "Lucid", "Meticulous", "Notorious", "Accordingly",
    "Consequently", "Conversely", "Ultimately", "Virtually", "Hence",
    "Nonetheless", "Thereby", "Whereas"
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