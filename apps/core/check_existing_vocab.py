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
input_words =[
    "Integrity", "Accelerate", "Break through", "Empathy", "Allocate", "Monitor", "Apparent",
    "Carry out", "Hypothesis", "Cultivate", "Slip up", "Advocate", "Constraint", "Get ahead",
    "Dramatically", "Abstract", "Implement", "Manipulate", "Drawback", "Engage", "Narrow down",
    "Come across", "Evaluate", "Face up to", "Bias", "Interpret", "Break into", "Adequate",
    "Go along with", "Manifestation", "Deduce", "Sort out", "Controversy", "Minimize",
    "Attribute", "Distort", "Catch on", "Jurisdiction", "Analyze", "Establish", "Wear off",
    "Motivation", "Generate", "Follow through", "Rely on", "Integrate", "Commodity",
    "Explicitly", "Back down", "Invoke", "Dimension", "Actively", "Estimate", "Put forward",
    "Convey", "Derive", "Come about", "Stand out", "Inhibit", "Facilitate", "Dominate",
    "Hand over", "Contribute", "Compatible", "Fall through", "Credible", "Allocate",
    "Justify", "Disrupt", "Work out", "Set aside", "Extract", "Innovation", "Assertive",
    "Emphasize", "Framework", "Get over", "Exploit", "Designate", "Compile", "Constraint",
    "Execute", "Exclude", "Depict", "Adapt", "Assert", "Team up", "Clarify", "Write off",
    "Adversity", "Intervention", "Take over", "Demonstrate", "Fluctuate", "Run into",
    "Clarify", "Coordinate", "Imply", "Point out", "Enhance", "Legislation", "Dismiss",
    "Consistently", "Integrate", "Apparent", "Rule out", "Get by", "Maintain", "Influence",
    "Detect", "Comply", "Eliminate", "Turn down", "Break down", "Expand", "Accommodate",
    "Illustrate", "Stick to", "Induce", "Show up", "Assess", "Modify", "Correspond",
    "Critically", "Motivate", "Draw up", "Distribute", "Clarify", "Stand by", "Exceed",
    "Conceive", "Collaborate", "Distinction", "Come forward", "Exclude", "Sustain",
    "Narrow down", "Come through", "Fall apart", "Hand in", "Go through", "Set forth",
    "Integrate", "Follow up", "Evolve", "Highlight", "Ensure", "Figure out", "Manipulate",
    "Turn up", "Assume", "Infer", "Attribute", "Iron out", "Stick to", "Come down to",
    "Evaluate", "Generate", "Maximize", "Influence", "Put across", "Establish", "Emphasis",
    "Sort out", "Write off", "Explicit", "Hold back", "Consistent", "Engage", "Carry on",
    "Entirely", "Formulate", "Maintain", "Initiate", "Implement", "Integrate", "Work out"
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










# import os
# import django
# import sys

# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
# sys.path.insert(0, PROJECT_ROOT)

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

# django.setup()

# from apps.core.models import Vocabulary

# def renumber_vocabulary():
#     # Fetch all vocab entries ordered in a stable way
#     vocab_entries = Vocabulary.objects.order_by("id")

#     new_number = 1
#     updates = []

#     for vocab in vocab_entries:
#         vocab.word_number = new_number
#         updates.append(vocab)
#         new_number += 1

#     Vocabulary.objects.bulk_update(updates, ['word_number'])

#     print(f"Successfully renumbered {len(updates)} vocabulary words.")

# if __name__ == "__main__":
#     renumber_vocabulary()
