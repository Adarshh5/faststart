from django.shortcuts import render, redirect
from user_data.models import SavedGrammar, UserVocabulary, SavedVocabulary,UserDailyStoryUsage, UserDailyMessageUsage, UserFreeTierStart, UserDailyDoubtSolving
from .forms import UserContentStylingForm
from django.views import View
from django.http import JsonResponse
from .textgnerationtemplate import inputwithgrammar, inputwithoutgrammar, llm, build_chat_history, translate_to_hindi, build_chat_history_without_vocabulary
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from django.utils import timezone
from datetime import timedelta
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import localtime
from django.http import HttpResponse

from core.safe_get import safe_get_or_create
import logging
from .AI_tutor.Agentic import system_message, AgentState, graph
from .AI_tutor.message_convert import serialize_message, deserialize_message
from dotenv import load_dotenv
import os
load_dotenv()



logger = logging.getLogger(__name__)


def get_user_grammar_list(user):
    grammar_list = [
        "simple sentences where the subject doesn't do any work such as -> Ram is good man, raju was in school, we will/would be on the space in the future, shetal had two sister,  class 5th student don't have laptop , my friend will/would have car   ",
        "use tense ",
        "modal verbs: can/could/might/would, can/could/would be + obj, can/could/would have + obj, has/have to, will have to, need to"
    ]
    
    usergrammar = SavedGrammar.objects.get(user=user)
    if usergrammar.causative_verb:
        grammar_list.append("use causative verbs (make/get)")
    if usergrammar.voice:
        grammar_list.append("use passive voice")
    if usergrammar.other:
        grammar_list.append("use of 'It', 'use of Let', and conditional sentences")
    
    return grammar_list

def includevocabulary(user):
    sendingvocabulary = []

    # Get user vocabulary (max 100 assumed)
    user_vocab_qs = UserVocabulary.objects.filter(user=user)
    user_vocab_list = [word.word_name for word in user_vocab_qs]
    sendingvocabulary.extend(user_vocab_list)

    # Total we want
    total_allowed = 100
    remaining = total_allowed - len(sendingvocabulary)

    # Get saved vocabulary
    try:
        saved_vocab_obj = SavedVocabulary.objects.get(user=user)
        saved_vocab_list = saved_vocab_obj.words
    except SavedVocabulary.DoesNotExist:
        saved_vocab_list = []

    if remaining != 0 or remaining > 0:
        # Ensure no IndexError if not enough vocab available
        if len(saved_vocab_list) >= remaining:
            sendingvocabulary.extend(saved_vocab_list[:remaining])
        else:
            sendingvocabulary.extend(saved_vocab_list)

    return sendingvocabulary


def notincludevocabulary(user):
    sendingvocabulary = []

    try:
        saved_vocab_obj = SavedVocabulary.objects.get(user=user)
       
        saved_vocab_list = saved_vocab_obj.words
    except SavedVocabulary.DoesNotExist:
        saved_vocab_list = []
   
    total_allowed = 100
    if len(saved_vocab_list) >= total_allowed:
        sendingvocabulary.extend(saved_vocab_list[:total_allowed])
    else:
        sendingvocabulary.extend(saved_vocab_list)

    return sendingvocabulary


@method_decorator(login_required, name='dispatch')
class textgeneration(View):
    def get(self, request):
        user = request.user
        try:
            grammarobj = SavedGrammar.objects.filter(user=user).first()
            if not grammarobj:
                grammarobj = SavedGrammar(user=user)
                grammarobj.save()
        except Exception as e:
            return HttpResponse(f"Manually created grammar object failed: {e}")


        vocabularyobj,_ = SavedVocabulary.objects.get_or_create(user=user)
        start_record, _ = UserFreeTierStart.objects.get_or_create(user=user)
        days_used = (timezone.now().date() - start_record.start_date).days

        if days_used >= 10:
            messages.info(request, "Your free tier has expired.")
            return redirect('home')

        today = localtime(timezone.now()).date()
        
        story_usage, _ = UserDailyStoryUsage.objects.get_or_create(user=user, date=today)
        if story_usage.count >= 2:
            messages.info(request, "You’ve reached today’s story generation limit.")
            return redirect('home')
        if not (grammarobj.simple_sentence or grammarobj.tense or grammarobj.modal_part_1 or grammarobj.modal_part_2):
            messages.info(request, 'You have to complete at least Simple Sentences, Tense, or Modals to generate text.')
            return redirect('home')

        if len(vocabularyobj.words) < 20:
            messages.info(request, 'You have to add at least 20 words to generate text content.')
            return redirect('home')
      
        form1  = UserContentStylingForm()
        context = {
            'form1': form1,
        }
        return render(request, 'ai_assistant/textgeneration.html', context)
    
    def post(self, request):
        user = request.user
        form1 = UserContentStylingForm(request.POST)
        context = {
            'form1': form1,
        }
        
        if form1.is_valid():
            grammar_option = form1.cleaned_data['grammar']
            vocab_option = form1.cleaned_data['add_my_added_vocabulary']
            user_prompt = form1.cleaned_data['prompt']
            try:
                 # 🧠 Get grammar list and vocab list
                grammar_list = get_user_grammar_list(user) if grammar_option == "include" else []
                vocab_list = includevocabulary(user) if vocab_option == "include" else notincludevocabulary(user)
                  # 🛡️ Safe join - handle None, wrong types, etc.
                grammar_string = ", ".join(grammar_list) if isinstance(grammar_list, list) else ""
                vocab_string = ", ".join(vocab_list) if isinstance(vocab_list, list) else ""


                if grammar_option == "include":
                    llmresponse = inputwithgrammar.invoke({
                        "grammar_instructions": grammar_string,
                        "vocabulary_list": vocab_string,
                        "user_prompt": user_prompt
                    })
                else:
                    llmresponse = inputwithoutgrammar.invoke({
                        "vocabulary_list": vocab_string,
                        "user_prompt": user_prompt
                    })
                today = localtime(timezone.now()).date()
                countobj, _ = safe_get_or_create(UserDailyStoryUsage, user=user, date=today)
                countobj.count+=1
                countobj.save()

                request.session['llm_response'] = llmresponse
                return redirect('textgenerationresult')
            except Exception as e:
                logger.error("LLM error occurred: %s", str(e))  # Logs error for YOU
                messages.error(request, "Something went wrong. Please try again.") 
                return redirect('home')
                
        else:
            return render(request, 'ai_assistant/textgeneration.html', context)

            
                   

@login_required
def textgenerationresult(request):
    llm_response = request.session.get('llm_response', None)
    if llm_response:
       return render(request, 'ai_assistant/textgenerationresult.html', {'llm_response':llm_response})
    else:
        return redirect('textgeneration') 

                   
                   

    

@method_decorator(login_required, name='dispatch')
class Chatbot(View):
    def get(self, request):
        user = request.user
        start_record, _ = UserFreeTierStart.objects.get_or_create(user=user)
        days_used = (timezone.now().date() - start_record.start_date).days
        if days_used >= 10:
            messages.info(request, "Your free tier has expired.")
            return redirect('home')
        if 'session_chat_history' not in request.session:
            request.session['session_chat_history'] = []

        grammar_list = get_user_grammar_list(user)
        vocab_list = notincludevocabulary(user)

        if len(vocab_list) > 20:
            _ = build_chat_history_without_vocabulary(request)
        else:
            grammar_string = ", ".join(grammar_list)
            vocab_list = [w for w in vocab_list if isinstance(w, str) and w.strip()]
            vocab_string = ", ".join(vocab_list)
            _ = build_chat_history(request, grammar_string, vocab_string)

       
        return render(request, 'ai_assistant/chatbot.html', {
            'chat_history': request.session['session_chat_history'],
        })
    
    def post(self, request):
     
        try:
            user = request.user
            data = json.loads(request.body)
            user_message = data.get('user_message')

            if not user_message:
                return JsonResponse({'error': 'No message provided.'})

            today = localtime(timezone.now()).date()
            message_usage, _ = UserDailyMessageUsage.objects.get_or_create(user=user, date=today)

            if message_usage.message_count >= int(os.getenv("Message_limit")):
                return JsonResponse({'reply': "⛔ You have sent 20 messages. Limit reached!"})

            # Build context
            grammar_list = get_user_grammar_list(user)
            vocab_list = notincludevocabulary(user)
            

            if len(vocab_list) < 20:
                  print("inside")
                  chat_history = build_chat_history_without_vocabulary(request)
            else:
                 grammar_string = ", ".join(grammar_list)
                 vocab_string = ", ".join(vocab_list)
                 chat_history = build_chat_history(request, grammar_string, vocab_string)
            
            request.session['session_chat_history'].append(
                {'type': 'user', 'content': user_message}
            )

            
            chat_history.append(HumanMessage(content=user_message))
            print(chat_history)

          
            response = llm.invoke(chat_history)

            if isinstance(response, str):
                ai_message = AIMessage(content=response)
            else:
                ai_message = response
            chat_history.append(ai_message)

           
            message_usage.message_count += 1
            message_usage.save()

            
            hindi_translation = translate_to_hindi(ai_message.content)

           
            request.session['session_chat_history'].append(
                {
                    'type': 'ai',
                    'content': ai_message.content,
                    'translation': hindi_translation
                }
            )
            request.session.modified = True
           
            return JsonResponse({
                'reply': ai_message.content,
                'translation': hindi_translation
            })

        except Exception as e:
            logger.error("Chatbot error: %s", str(e))
            
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'})
        



@method_decorator(login_required, name='dispatch')
class AItutor(View):
    def get(self, request):
        user = request.user
        start_record, _ = UserFreeTierStart.objects.get_or_create(user=user)
        days_used = (timezone.now().date() - start_record.start_date).days
        if days_used >= 10:
            messages.info(request, "Your free tier has expired.")
            return redirect('home')

        request.session.setdefault('session_AItutor_history', [])
        request.session.setdefault('session_user_chat_history', [])
        
        return render(request, 'ai_assistant/AItutor.html', {
            'chat_history': request.session['session_user_chat_history'],
        })
    
    def post(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            user_message = data.get('user_message')

            if not user_message:
                return JsonResponse({'error': 'No message provided.'}, status=400)
            
            today = localtime(timezone.now()).date()
            message_usage, _ = UserDailyDoubtSolving.objects.get_or_create(user=user, date=today)

            if message_usage.message_count >= int(os.getenv("Doubt_soling_chatlimit")):
                return JsonResponse({'reply': "⛔ You have sent 5 messages. Limit reached!"})

            # Add user message to history (frontend format)
            request.session['session_user_chat_history'].append(
                {"role": "user", "content": user_message}
            )
            
            # Deserialize stored messages
            stored_messages = [
                deserialize_message(msg) 
                for msg in request.session.get('session_AItutor_history', [])
            ]
            # print(stored_messages)
            
            # Prepare agent state
            initial_messages = [
                SystemMessage(content=system_message),
                *stored_messages,
                HumanMessage(content=user_message)
            ]
            
            # Invoke graph
            agent_state = {"messages": initial_messages}
            LLM_response = graph.invoke(agent_state)
            
            # Get only new messages
            new_messages = LLM_response["messages"][len(initial_messages):]
            
            
            # Serialize and store full history
            request.session['session_AItutor_history'] = [
                serialize_message(msg) 
                for msg in initial_messages[1:] + new_messages  # Exclude system message
            ][-10:]  
            
            # Get final response
            final_response = new_messages[-1].content
            message_usage.message_count += 1
            message_usage.save()
            
         
            request.session['session_user_chat_history'].append(
                {"role": "assistant", "content": final_response}
            )
            
            request.session.modified = True
            return JsonResponse({'reply': final_response})

        except Exception as e:
            logger.error("Chatbot error: %s", str(e), exc_info=True)
            return JsonResponse(
                {'error': 'An unexpected error occurred. Please try again.'},
                status=500
            )