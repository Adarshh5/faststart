
from langchain_groq import ChatGroq
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser 


from langchain_core.messages import SystemMessage, HumanMessage, AIMessage



from dotenv import load_dotenv
import os


os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")





load_dotenv()



big_model = ChatGroq(
    model="moonshotai/kimi-k2-instruct",
    max_tokens=200,
   
)
small_model =  ChatGroq(
    model="llama-3.1-8b-instant",
    max_tokens=600,
   
)

system_template = """
You are a helpful English content generation assistant, and you know Indian accent very well:

- ONLY output the final story, article, or response. DO NOT include any internal thoughts, planning, or commentary and any other content.
- Use these grammar rules where possible in your response: {grammar_instructions}.
- Use the following vocabulary words where posssible in your response: {vocabulary_list}.
- User wants to learn vocabulary and grammar rules by seeing them in real context. So your main goal is to use the given grammar and vocabulary where possible.
- Prioritize using the words at the beginning of the list more frequently than those at the end.
- Your response should be engaging, interesting, and easy to understand so that the user must read your full response.
- **Use beginner-friendly English that is easy to understand for new spoken English learners, but it does not mean you will not use given tough vocabulary and grammar rules. **
- Limit responses to under 600 to 800 words.
"""

human_template = """
{user_prompt}
"""

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template(human_template)
])




llm = ChatGroq(
   model="openai/gpt-oss-120b",
   max_tokens=2500,
)

parser = StrOutputParser()
inputwithgrammar = chat_prompt | llm | parser





system_template = """
You are an helpful English content generation assistant.and you know Indian accent very well.

- ONLY output the final story, article, or response. DO NOT include any internal thoughts, planning, or commentary.
- Use the following vocabulary words where possible in your response: {vocabulary_list}.
- User wants to learn vocabulary and by seeing them in real context. So your main goal is to use the given vocabulary where possible.
- Prioritize using the words at the beginning of the list more frequently than those at the end.
- Your response should be engaging, interesting, and easy to understand so that the user must read your full response.
- **Use simple, beginner-friendly English that is easy to understand for new spoken English learners, but it does not mean you will not use given tough vocabulary.**
- Limit responses to under 600 to 800 words.
"""


human_template = """
{user_prompt}
"""

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template(human_template)
])




parser = StrOutputParser()
inputwithoutgrammar = chat_prompt | llm | parser







def build_chat_history_without_vocabulary(request):
    system_msg = SystemMessage(content=f"""You are a helpful English speaker with an Indian accent. Speak only in English and always be friendly.
- Focus on making conversations engaging, clear, and relevant so users enjoy chatting longer.
- Always end with a question to keep the conversation going.
- Speak in simple, beginner-friendly English that new learners can easily follow.

""")

    chat_history = [system_msg]
    all_messages = request.session.get('session_chat_history', [])

    if len(all_messages) <= 6:
        # Use all messages if they're few
        for msg in all_messages:
            if msg['type'] == 'user':
                chat_history.append(HumanMessage(content=msg['content']))
            elif msg['type'] == 'ai':
                chat_history.append(AIMessage(content=msg['content']))
    else:
        # Filter last 3 user and last 3 ai messages separately
        last_user_msgs = [m for m in reversed(all_messages) if m['type'] == 'user'][:3]
        last_ai_msgs = [m for m in reversed(all_messages) if m['type'] == 'ai'][:3]

        # Combine and reverse to maintain order
        trimmed_msgs = sorted(last_user_msgs + last_ai_msgs, key=lambda x: all_messages.index(x))

        for msg in trimmed_msgs:
            if msg['type'] == 'user':
                chat_history.append(HumanMessage(content=msg['content']))
            elif msg['type'] == 'ai':
                chat_history.append(AIMessage(content=msg['content']))

    return chat_history





def build_chat_history(request, grammar_string, vocab_string):
    system_msg = SystemMessage(content=f"""You are a helpful English speaker with an Indian accent. Speak only in English always be friendly.

- Use the given grammar rules: {grammar_string}, and vocabulary words: {vocab_string}. (Vocabulary list ends here.)
  where possible. Make sure they sound natural and fit the flow of the conversation.
- Prioritize the top-listed vocabulary words.
- Focus on making conversations engaging, clear, and relevant so users enjoy chatting longer.
- Always end with a question to keep the conversation going.
- Speak in simple English that new learners can easily follow but it does not mean you will not use given tough vocabulary and grammar rules.

""")

    chat_history = [system_msg]
    all_messages = request.session.get('session_chat_history', [])

    if len(all_messages) <= 6:
        # Use all messages if they're few
        for msg in all_messages:
            if msg['type'] == 'user':
                chat_history.append(HumanMessage(content=msg['content']))
            elif msg['type'] == 'ai':
                chat_history.append(AIMessage(content=msg['content']))
    else:
        # Filter last 3 user and last 3 ai messages separately
        last_user_msgs = [m for m in reversed(all_messages) if m['type'] == 'user'][:3]
        last_ai_msgs = [m for m in reversed(all_messages) if m['type'] == 'ai'][:3]

        # Combine and reverse to maintain order
        trimmed_msgs = sorted(last_user_msgs + last_ai_msgs, key=lambda x: all_messages.index(x))

        for msg in trimmed_msgs:
            if msg['type'] == 'user':
                chat_history.append(HumanMessage(content=msg['content']))
            elif msg['type'] == 'ai':
                chat_history.append(AIMessage(content=msg['content']))

    return chat_history



trans_llm = ChatGroq(
   model="llama-3.1-8b-instant",
   max_tokens=300 
)

   
def translate_to_hindi(text):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional English to Hindi translator. Translate clearly and only return the translated sentence in Hindi, without explanation."),
        ("human", "{text}")
    ])
    
    messages = prompt.format_messages(text=text)

    response = trans_llm.invoke(messages)
    if isinstance(response, str):
        ai_message = AIMessage(content=response)
    else:
        ai_message = response

    return ai_message.content.strip()



