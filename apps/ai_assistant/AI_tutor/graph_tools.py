
from langchain.tools.retriever import create_retriever_tool

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from apps.core.models import GrammarLesson
from pydantic import BaseModel, Field
from typing import Literal
from langchain.tools import StructuredTool
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
load_dotenv() 


os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

model = ChatGroq(model="llama3-70b-8192")

VALID_GRAMMAR_TOPICS = Literal[
    "Conditional Sentences",
    "Use of IT",
    "Passive Voice",
    "Causative Verbs",
    "Have to / Need – Compulsory Actions",
    "Modals",
    "Present Tense",
    "Simple Sentence – Part 1",
    "Past Tense",
    "Simple Sentence – Part 2",
    "Future Tense"
]



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DB_PATH = os.path.join(BASE_DIR, "vector_db")

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = FAISS.load_local(
    folder_path=VECTOR_DB_PATH,
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)



retriever = vectorstore.as_retriever(search_kwargs={"k": 2})  # only top 1 chunk
 





class RelevanceCheck(BaseModel):
    relevance: Literal["relevant", "not relevant"]

# ✅ Wrap with structured output
structured_model = model.with_structured_output(RelevanceCheck, strict=True)

# ✅ Use structured_model in function
def document_checker(query, document):
    input_text = f"""
    Given the following user query and document, decide whether the document is relevant to the query.

    Only return "relevant" or "not relevant" under the 'relevance' key.

    User Query:
    {query}

    Document:
    {document}
    """
    result = structured_model.invoke(input_text)
    return result.relevance  # will be exactly "relevant" or "not relevant"

@tool
def retriever_vector_user_query_documents_for_englsihspeaking(query: str) -> str:
    """Given a user query, return the most relevant document chunk from FAISS."""
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant document found."
    
    
    for doc in docs:
        check = document_checker(query, doc.page_content)
        if check == "relevant":
            return doc.page_content

    # 🔄 If no relevant doc found
    return (
        "The retrieved documents were not relevant to the query. "
        "Please attempt to answer the user's question based on general knowledge, in a short and simple way and if you don't know the answer just say 'i don't know about this question'."
    )
    
   


class GrammarTopicInput(BaseModel):
    topic_name:VALID_GRAMMAR_TOPICS  = Field(
            description="Must be exact, e.g.: 'Simple Sentence Part 1' (for is/am/are) or 'Simple Sentence Part 2' (for has/have/had)",
            examples=["Simple Sentence Part 1", "Simple Sentence Part 2"]
    )
def grammar(topic_name:VALID_GRAMMAR_TOPICS) -> str:
     """Fetch grammar notes. Topics:
      - 'Simple Sentence Part 1': Being verbs (is/am/are/was/were/will be)
      - 'Simple Sentence Part 2': Possession verbs (has/have/had/will have)
     """
     try:
        topic = GrammarLesson.objects.get(title=topic_name)

        return topic.main_content
     except GrammarLesson.DoesNotExist:
         return f"Error: Grammar topic '{topic_name}' not found in our database"
     except Exception as e:
         return f"Error retrieving grammar topic: {str(e)}"
    

grammar_tool = StructuredTool.from_function(
    func=grammar,
    name="grammar_notes",
    description="Fetch predefined grammar lessons. Topic must match exactly.",
    args_schema=GrammarTopicInput,
    return_direct=True
)
tools = [grammar_tool, retriever_vector_user_query_documents_for_englsihspeaking]


