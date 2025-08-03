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
from langchain_groq import ChatGroq
from .graph_tools import tools
from .graph_tools import VALID_GRAMMAR_TOPICS

def agent(state):
    messages = state['messages']
    model = ChatGroq(model="llama3-8b-8192")
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    
    
    return {"messages": [response]}

