import django
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "faststart.settings")
django.setup()

from core.models import Vocabulary

# Choose a default level
DEFAULT_LEVEL = 'beginner'
vocab_list = vocab_list = [
   
    

   
 
   
   
    {
        "word_number": 351,
        "word_name": "anybody",
        "part_of_speech": "pronoun",
        "hindi_meaning": "कोई भी व्यक्ति",
        "definition": "Any person, it doesn't matter who",
        "example": "Does anybody here know how to fix this printer?\nक्या यहाँ कोई भी व्यक्ति जानता है कि इस प्रिंटर को कैसे ठीक करें?",
    },
    {
        "word_number": 352,
        "word_name": "anyone",
        "part_of_speech": "pronoun",
        "hindi_meaning": "कोई भी",
        "definition": "Used to refer to any person, without specifying",
        "example": "Anyone can learn to cook with practice.\nकोई भी अभ्यास से खाना बनाना सीख सकता है।",
    },
    {
        "word_number": 353,
        "word_name": "anything",
        "part_of_speech": "pronoun",
        "hindi_meaning": "कुछ भी",
        "definition": "Used to refer to a thing, no matter what",
        "example": "You can ask me anything about computers.\nतुम मुझसे कंप्यूटर्स के बारे में कुछ भी पूछ सकते हो।",
    },
    
 
    {
        "word_number": 359,
        "word_name": "nothing",
        "part_of_speech": "pronoun",
        "hindi_meaning": "कुछ नहीं",
        "definition": "Not anything; no single thing",
        "example": "There's nothing in the fridge - we need to go shopping.\nफ्रिज में कुछ नहीं है - हमें खरीदारी करने जाना होगा।",
    },
    {
        "word_number": 360,
        "word_name": "everybody",
        "part_of_speech": "pronoun",
        "hindi_meaning": "हर कोई",
        "definition": "Every person",
        "example": "Everybody must show their ID card to enter the office.\nहर कोई को कार्यालय में प्रवेश करने के लिए अपना आईडी कार्ड दिखाना होगा।",
    },
    {
        "word_number": 361,
        "word_name": "everyone",
        "part_of_speech": "pronoun",
        "hindi_meaning": "सभी लोग",
        "definition": "Every person (same as 'everybody' but more formal)",
        "example": "Everyone stood up when the principal entered the hall.\nसभी लोग खड़े हो गए जब प्रधानाचार्य हॉल में आए।",
    },
    {
        "word_number": 362,
        "word_name": "everything",
        "part_of_speech": "pronoun",
        "hindi_meaning": "सब कुछ",
        "definition": "All things; all the things of a group or class",
        "example": "She packed everything she needed for the trip.\nउसने यात्रा के लिए आवश्यक सब कुछ पैक कर लिया।",
    },
    {
        "word_number": 363,
        "word_name": "none",
        "part_of_speech": "pronoun",
        "hindi_meaning": "कोई नहीं",
        "definition": "Not any of a group or class",
        "example": "None of the students failed the final exam this year.\nइस वर्ष परीक्षा में छात्रों में से कोई भी फेल नहीं हुआ।",
    },
    {
        "word_number": 364,
        "word_name": "ones",
        "part_of_speech": "pronoun",
        "hindi_meaning": "वे (सामान्य बहुवचन)",
        "definition": "Used to refer to unspecified people or things",
        "example": "The red saris are beautiful, but I prefer the blue ones.\nलाल साड़ियाँ सुंदर हैं, लेकिन मुझे नीली वाली पसंद हैं।",
    },
    {
        "word_number": 365,
        "word_name": "few",
        "part_of_speech": "pronoun",
        "hindi_meaning": "कुछ (सीमित संख्या)",
        "definition": "A small number of people or things",
        "example": "Few understand how difficult farming really is.\nकुछ ही लोग समझते हैं कि खेती वास्तव में कितनी कठिन है।",
    },
    {
        "word_number": 366,
        "word_name": "many",
        "part_of_speech": "pronoun",
        "hindi_meaning": "बहुत से",
        "definition": "A large number of people or things",
        "example": "Many have tried to climb Mount Everest without success.\nबहुत से लोगों ने माउंट एवरेस्ट पर चढ़ने की असफल कोशिश की है।",
    },
    {
        "word_number": 367,
        "word_name": "several",
        "part_of_speech": "pronoun",
        "hindi_meaning": "कई",
        "definition": "More than two but not many",
        "example": "Several of my classmates are going on the school trip.\nमेरे कई सहपाठी स्कूल यात्रा पर जा रहे हैं।",
    },
    {
        "word_number": 368,
        "word_name": "each other",
        "part_of_speech": "pronoun",
        "hindi_meaning": "एक दूसरे",
        "definition": "Used to show that each member does something to the other(s)",
        "example": "The two sisters help each other with homework every day.\nदोनों बहनें हर दिन एक दूसरे की गृहकार्य में मदद करती हैं।",
    },
    {
        "word_number": 369,
        "word_name": "one's",
        "part_of_speech": "pronoun",
        "hindi_meaning": "अपना",
        "definition": "Belonging to or associated with one",
        "example": "One should always do one's best in everything.\nहर किसी को हर काम में अपना सर्वश्रेष्ठ देना चाहिए।",
    },
    {
        "word_number": 370,
        "word_name": "somewhat",
        "part_of_speech": "pronoun",
        "hindi_meaning": "कुछ हद तक",
        "definition": "To a moderate extent or degree",
        "example": "I was somewhat surprised by the test results.\nमैं परीक्षा परिणामों से कुछ हद तक आश्चर्यचकित था।",
    },
]
objects = []

for vocab in vocab_list:
    vocab["level"] = DEFAULT_LEVEL
    obj = Vocabulary(**vocab)
    objects.append(obj)

Vocabulary.objects.bulk_create(objects, ignore_conflicts=True)
print(f"{len(objects)} vocabulary items inserted.")
