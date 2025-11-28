import os
import django
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

django.setup()
from apps.core.models import Vocabulary

# Choose a default level
DEFAULT_LEVEL = 'intermediate'
vocab_list = [
    
    {
        "word_number": 445,
        "word_name": "Crucial",
        "part_of_speech": "adjective",
        "hindi_meaning": "महत्वपूर्ण",
        "definition": "Extremely important or necessary",
        "example": "Regular practice is crucial for success in competitive exams.\nप्रतियोगी परीक्षाओं में सफलता के लिए नियमित अभ्यास महत्वपूर्ण है।"
    },
    {
        "word_number": 446,
        "word_name": "Inevitable",
        "part_of_speech": "adjective",
        "hindi_meaning": "अपरिहार्य",
        "definition": "Certain to happen; unavoidable",
        "example": "Traffic jams are inevitable during peak hours in cities.\nशहरों में व्यस्त समय के दौरान ट्रैफिक जाम अपरिहार्य हैं।"
    },
    {
        "word_number": 447,
        "word_name": "Versatile",
        "part_of_speech": "adjective",
        "hindi_meaning": "बहुमुखी",
        "definition": "Able to do many different things well",
        "example": "A smartphone is a versatile device for communication and learning.\nस्मार्टफोन संचार और सीखने के लिए एक बहुमुखी उपकरण है।"
    },
    {
        "word_number": 448,
        "word_name": "Robust",
        "part_of_speech": "adjective",
        "hindi_meaning": "मजबूत",
        "definition": "Strong and healthy; unlikely to fail or break",
        "example": "We need a robust internet connection for online classes.\nऑनलाइन कक्षाओं के लिए हमें मजबूत इंटरनेट कनेक्शन की आवश्यकता है।"
    },
    {
        "word_number": 449,
        "word_name": "Subtle",
        "part_of_speech": "adjective",
        "hindi_meaning": "सूक्ष्म",
        "definition": "Not obvious or easy to notice; delicate and precise",
        "example": "There is a subtle difference between these two words in English.\nअंग्रेजी में इन दो शब्दों के बीच सूक्ष्म अंतर है।"
    },
    {
        "word_number": 450,
        "word_name": "Trivial",
        "part_of_speech": "adjective",
        "hindi_meaning": "तुच्छ",
        "definition": "Of little value or importance",
        "example": "Don't waste time on trivial matters during exam preparation.\nपरीक्षा की तैयारी के दौरान तुच्छ मामलों पर समय बर्बाद न करें।"
    },
    {
        "word_number": 451,
        "word_name": "Ubiquitous",
        "part_of_speech": "adjective",
        "hindi_meaning": "सर्वव्यापी",
        "definition": "Present, appearing, or found everywhere",
        "example": "Mobile phones have become ubiquitous in modern life.\nआधुनिक जीवन में मोबाइल फोन सर्वव्यापी हो गए हैं।"
    },
    {
        "word_number": 452,
        "word_name": "Vague",
        "part_of_speech": "adjective",
        "hindi_meaning": "अस्पष्ट",
        "definition": "Not clear or definite; uncertain",
        "example": "The teacher's instructions were vague, so I got confused.\nशिक्षक के निर्देश अस्पष्ट थे, इसलिए मैं उलझन में पड़ गया।"
    },
    {
        "word_number": 453,
        "word_name": "Wary",
        "part_of_speech": "adjective",
        "hindi_meaning": "सतर्क",
        "definition": "Feeling or showing caution about possible dangers or problems",
        "example": "Be wary of strangers offering too much help.\nबहुत अधिक मदद की पेशकश करने वाले अजनबियों से सतर्क रहें।"
    },
    {
        "word_number": 454,
        "word_name": "Zealous",
        "part_of_speech": "adjective",
        "hindi_meaning": "उत्साही",
        "definition": "Showing great energy or enthusiasm for a cause",
        "example": "The zealous volunteers cleaned the entire park.\nउत्साही स्वयंसेवकों ने पूरा पार्क साफ किया।"
    },
    {
        "word_number": 455,
        "word_name": "Ambiguous",
        "part_of_speech": "adjective",
        "hindi_meaning": "अस्पष्ट",
        "definition": "Having more than one possible meaning; unclear",
        "example": "The question was ambiguous, so students answered differently.\nप्रश्न अस्पष्ट था, इसलिए छात्रों ने अलग-अलग उत्तर दिए।"
    },
   

]
objects = []

for vocab in vocab_list:
    vocab["level"] = DEFAULT_LEVEL
    obj = Vocabulary(**vocab)
    objects.append(obj)

Vocabulary.objects.bulk_create(objects, ignore_conflicts=True)
print(f"{len(objects)} vocabulary items inserted.")
