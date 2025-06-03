from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
LEARNING_MATERIAL_TOPIC = [
    ('grammar', 'grammar'),
    ('vocabulary', 'vocabulary'),
    ('Listning', 'Listning'),
    (5, ''),
    (6, '6 months'),
    (12, '1 year'),
    (24, '2 years')
]



GRAMMAR_TOPICS = [
    ('Simple Sentence', 'Simple Sentences'),
    ('Tense', 'Tense'),
    ('Modal Part 1', 'Modal Part 1'),
    ('Modal Part 2', 'Modal Part 2'),
    ('Causative Verb', 'Causative Verb'),
    ('Voice', 'Voice'),
    ('Other', 'Other'),
]

class GrammarLesson(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(choices=GRAMMAR_TOPICS, max_length=50)
    main_content = CKEditor5Field(config_name="default")
    guidetion = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0) 
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    


PARTS_OF_SPEECH = [
    ('noun', 'Noun'),
    ('pronoun', 'Pronoun'),
    ('verb', 'Verb'),
    ('adjective', 'Adjective'),
    ('adverb', 'Adverb'),
    ('preposition', 'Preposition'),
    ('conjunction', 'Conjunction'),
    ('interjection', 'Interjection'),
    ('phrasal_verb', 'Phrasal Verb'),
    ('phrase', 'Phrase'),
    ('question_word', 'Question_Word')
]

LEVEL = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]

class Vocabulary(models.Model):
    word_number = models.PositiveIntegerField(unique=True)
    word_name = models.CharField(max_length=100, unique=True)
    part_of_speech = models.CharField(choices=PARTS_OF_SPEECH, max_length=20)
    hindi_meaning = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(choices=LEVEL, max_length=50, default='beginner')
    definition = models.CharField(max_length=255)
    example = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.word_name
