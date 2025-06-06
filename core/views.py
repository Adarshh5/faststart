from django.shortcuts import render, redirect, get_object_or_404
from .models import GrammarLesson, Vocabulary
from user_data.models import SavedGrammar
from django.http import HttpResponseBadRequest
from .forms import NumberInputForm
from user_data.models import SavedVocabulary, UserWordDefinitions, SavedGrammar, UserVocabulary, UserFreeTierStart, UserDailyMessageUsage, UserDailyStoryUsage
from django.views import View
from django.contrib import messages
from user_data.forms import UserDefinitionForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import logging
from django.utils import timezone
from datetime import timedelta
from django.db import IntegrityError, transaction
from .safe_get import safe_get_or_create
from django.utils.timezone import localtime
from django.http import HttpResponse

import datetime

logger = logging.getLogger(__name__)


def home(request):
    request.session.pop('session_chat_history', None)
    return render(request, 'core/home.html')


def grammar(request):
    return render(request, 'core/grammar.html')

TOPIC_MAP = {
    'simple_sentence': 'Simple Sentence',
    'tense': 'Tense',
    'modal_part_1': 'Modal Part 1',
    'modal_part_2': 'Modal Part 2',
    'causative_verb': 'Causative Verb',
    'voice': 'Voice',
    'other': 'Other',
}

def grammartopics(request):
    user = request.user
    topic_key = request.GET.get('topic')
    if topic_key not in TOPIC_MAP:
        return HttpResponseBadRequest("Invalid topic.")

    # Get the value stored in GrammarLesson.topic
    topic_value = TOPIC_MAP[topic_key]
    grammartopicpart = GrammarLesson.objects.filter(topic=topic_value)

    user = request.user
    data = "anonymous user"

    if user.is_authenticated:
        usergrammar, created = SavedGrammar.objects.get_or_create(user=user)
        topic_completed = getattr(usergrammar, topic_key, False)
        data = "already added" if topic_completed else "not added"

    return render(request, 'core/grammartopics.html', {
        'grammartopicpart': grammartopicpart,
        'data': data,
    })



def vocabulary(request):
    number = request.GET.get('number')
    vocabulary_list = []
    if number:
        try:
            number = int(number)  # convert to int
            vocabulary_list = Vocabulary.objects.filter(
                word_number__gte=number,
                word_number__lte=number + 100
            )
        except ValueError:
            vocabulary_list = Vocabulary.objects.none()  # if number is not valid int
    else:
        vocabulary_list = Vocabulary.objects.filter(word_number__lte=100)

    form = NumberInputForm()
    return render(request, 'core/vocabulary.html', {
        'vocabulary_list': vocabulary_list,
        'form': form,
        'number': number
    })






class WordDetail(View):
    def get(self, request, pk):
        try:
            word = get_object_or_404(Vocabulary, id=pk)

            context = {
                'word': word,
                'form': UserDefinitionForm(),
                'word_added': False,
                'definitionalreadyadded': False,
            }

            if request.user.is_authenticated:
                user = request.user

                saved_vocab, _ = SavedVocabulary.objects.get_or_create(user=user)
                user_defs, _ = UserWordDefinitions.objects.get_or_create(user=user)
                definitions = user_defs.definitions or {}

                if word.word_name in saved_vocab.words:
                    context['word_added'] = True

                if word.word_name in definitions:
                    context['definitionalreadyadded'] = True
                    context['userdefinition'] = definitions[word.word_name]

            return render(request, 'core/word_detail.html', context)

        except Exception as e:
            logger.error(f"Error in WordDetail view for pk={pk}: {str(e)}")
            messages.error(request, "Something went wrong while loading the word details.")
            return redirect('home') 






@login_required
def checkchatvalidation(request):
    user = request.user
    grammarobj, _ = SavedGrammar.objects.get_or_create(user=user)
    vocabularyobj, _ = SavedVocabulary.objects.get_or_create(user=user)

    # Free tier logic
    start_record, _ = UserFreeTierStart.objects.get_or_create(user=user)
    days_used = (timezone.now().date() - start_record.start_date).days
    if days_used >= 10:
        messages.info(request, "Your free tier has expired.")
        return redirect('home')

    # Daily message usage check
    today = localtime(timezone.now()).date()
    message_usage, _ = UserDailyMessageUsage.objects.get_or_create(user=user, date=today)
    if message_usage.message_count >= 20:
        messages.info(request, "You’ve reached today’s message limit.")
        return redirect('home')

  

    return redirect('Chatbot')

 
@login_required
def Listning(request):
    return render(request, 'core/Listning.html')
