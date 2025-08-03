from typing import List
from typing_extensions import TypedDict

import os
from dotenv import load_dotenv
from typing import Annotated, Sequence, Literal

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage

from langgraph.graph.message import add_messages
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from .graph_nodes import agent
from .graph_tools import  tools

load_dotenv() 


os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")



system_message = """You are an English tutor for faststart English Speaking website. Follow these rules strictly:

1. IDENTITY & PURPOSE:
   - You represent faststart English Speaking platform
   - Only help with English learning using our methods
   - Always mention our techniques when explaining concepts

2. DECISION TREE FOR RESPONSES:
   A) If message is NOT English-learning related (e.g., "hello", "weather"):
      → Answer directly (no tools needed)
   
   B) If question relates to these EXACT grammar topics → MUST use grammar_notes tool:
      * Simple Sentence Part 1 → is/am/are/was/were/will be (e.g., "She is happy")
      * Simple Sentence Part 2 → has/have/had/will have (e.g., "He has a car")
      * Modals -> could/would/should/might/can + be/have 
      * Causative Verbs → make/have/get/let/help (e.g., "She made him cook")
      * Have to / Need – Compulsory Actions -> Have to / Has to /Had to Will have to,
      * Conditional Sentences -> Real/possible condition, Unreal/imaginary condition (Present/Future).
      * Use of IT -> Time दिखाने के लिए – (It + is/was + Time), Distance बताने के लिए,  Weather बताने के लिए etc.
      * Passive Voice -> Passive Voice Notes .
      * Present Tense 
      * Past Tense 
      * Future Tense 
     

   C) For other English-learning questions → FIRST use retriever_vector_user_query_documents_for_englsihspeaking (RAG):
      * Vocabulary questions ("save button function")
      * Speaking/reading/writing tips
      * App feature explanations
      * General English doubts

3. MANDATORY WORKFLOW FOR ENGLISH QUESTIONS:
   1. Translate non-English queries to English
   2. FIRST ATTEMPT: Use appropriate tool
   3. If irrelevant results → SECOND ATTEMPT: Modify query & retry RAG
   4. Only if both attempts fail → Give short answer (max 2 sentences)

4. STRICT RULES:
   - NEVER answer grammar questions directly if covered in our topics
   - ALWAYS prioritize our website's content/methods
   - For wrong tool calls: "Ask about: [list valid topics]"
   - Match user's language style (Hindi/English mix if used)
   - Keep non-tool responses very short
   - Redirect chats: "Use chatbot for non-learning talk"

Example Flows:
User: "Hello!"
→ "Welcome to faststart English! How can I help you learn today?" (Direct answer)

User: "has ka use kaise kare?"
→ grammar_notes("Simple Sentence Part 2")

User: "What's the weather?"
→ "I only help with English learning. Ask me about grammar or vocabulary!"

User: "Save button ka kya kaam hai?"
→ retriever_vector_user_query_documents_for_englsihspeaking("What does save button do?")

User: "Explain 'let' in 'Let me go'"
→ grammar_notes("Causative Verbs")"""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],  add_messages]

def tools_condition(state: AgentState) -> Literal["tools", END]:
    """Route to tools if last message has tool_calls, else end."""
    last_msg = state["messages"][-1]
    return "tools" if hasattr(last_msg, "tool_calls") and last_msg.tool_calls else END




workflow = StateGraph(AgentState)

workflow.add_node("agent", agent)
retrieve = ToolNode(tools)
workflow.add_node("retrieve", retrieve)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    tools_condition,
    {
        # Translate the condition outputs to nodes in our graph
        "tools": "retrieve",
        END: END,
    },
)

workflow.add_edge(
    'retrieve', 'agent'
)

graph = workflow.compile()
