from django.shortcuts import render, redirect
from apps.core.models import GrammarLesson, Vocabulary
from django.contrib import messages
from .models import SavedGrammar
from django.http import HttpResponseBadRequest
from .forms import UserDefinitionForm
from .models import UserWordDefinitions, SavedVocabulary
import json
from apps.core.models import Vocabulary
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@login_required
def savegrammar(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    user = request.user
    topic = request.POST.get('topic')  # get topic from POST data

    valid_topics = ['simple_sentence', 'tense', 'modal_part_1', 'modal_part_2', 'causative_verb', 'voice', 'other']
    if topic not in valid_topics:
        return HttpResponseBadRequest("Invalid topic.")

    # Get or create user's SavedGrammar instance
    usergrammar, created = SavedGrammar.objects.get_or_create(user=user)

    # Dynamically update the correct field
    setattr(usergrammar, topic, True)
    usergrammar.save()
    messages.success(request, f"{topic.replace('_', ' ').title()} marked as complete!")

    return redirect('grammar')

@login_required
def saveword(request):
    if request.method == "POST":
        user = request.user
        try:
            data = json.loads(request.body)
            word = data.get('word')

            if not word or not isinstance(word, str) or not word.strip():
                return JsonResponse({"reply": "Invalid word."}, status=400)

            saved_vocab, _ = SavedVocabulary.objects.get_or_create(user=user)

            if word in saved_vocab.words:
                return JsonResponse({"reply": "already_saved"})  # changed
            else:
                saved_vocab.words.insert(0, word)
                saved_vocab.save()
                return JsonResponse({"reply": "added"})  # changed
        except json.JSONDecodeError:
            return JsonResponse({"reply": "Invalid request format."}, status=400)

    return JsonResponse({"reply": "Invalid request method."}, status=405)



@login_required
def saveuserdefinition(request):
    if request.method == "POST":
        form = UserDefinitionForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            definition = form.cleaned_data['definition']

            user_defs, _ = UserWordDefinitions.objects.get_or_create(user=request.user)
            user_defs.definitions[word] = definition
            user_defs.save()

            messages.success(request, "Definition saved.")
        else:
            messages.error(request, "Invalid form: " + str(form.errors))

        obj = Vocabulary.objects.get(word_name=word)
        return redirect(f"/word_detail/{obj.id}")
    
    

@login_required
def deleteuserdefinition(request):
    if request.method == "POST":
       
        word = request.POST.get('word')
        user_defs, created = UserWordDefinitions.objects.get_or_create(user=request.user)

        if word in user_defs.definitions:
            del user_defs.definitions[word]
            user_defs.save()
            messages.success(request, "Definition deleted.")
        else:
            messages.error(request, "Definition not found.")

        obj = Vocabulary.objects.get(word_name=word)
        return redirect(f"/word_detail/{obj.id}")



@login_required
def Profile(request):
    return render(request, "user_data/Profile.html")

@login_required
def savedVocabulary(request):
    user = request.user
    obj, created = SavedVocabulary.objects.get_or_create(user=user)
    VocabularyList = obj.words
    totalwords = len(obj.words)
    return render(request, "user_data/savedvocabulary.html", {'VocabularyList': VocabularyList, "totalwords": totalwords})

@login_required
@csrf_exempt 
def removesavedvocabulary(request):
    if request.method == "POST":
        user = request.user

        try:
            data = json.loads(request.body)
            word = data.get('word')

            if not word:
                return JsonResponse({"reply": "Invalid word provided."}, status=400)

            obj, created = SavedVocabulary.objects.get_or_create(user=user)
            
            cleaned_words = [w for w in obj.words if w is not None]
            obj.words = cleaned_words
            obj.save()

            if word in obj.words:
                obj.words.remove(word)
                obj.save()
                return JsonResponse({"reply": "Removed"})
            else:
                return JsonResponse({"reply": "Word not found in your saved list."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"reply": "Invalid request format."}, status=400)

        except SavedVocabulary.DoesNotExist:
            return JsonResponse({"reply": "No saved vocabulary found."}, status=404)

    return JsonResponse({"reply": "Invalid request method."}, status=405)

@login_required
def savedworddetail(request):
    if request.method == "POST":
        user = request.user
        try:
            data = json.loads(request.body)
            word = data.get('word')

            if not word:
                messages.warning(request, "Invalid word provided.")
                return redirect('savedvocabulary')

            obj = Vocabulary.objects.get(word_name=word)
            return redirect('word_detail', pk=obj.id)

        except Vocabulary.DoesNotExist:
            messages.info(request, "Something is wrong or the word has been removed from the database.")
            return redirect('savedvocabulary')

        except json.JSONDecodeError:
            messages.error(request, "Invalid request format.")
            return redirect('savedvocabulary')

    return redirect('savedvocabulary')

