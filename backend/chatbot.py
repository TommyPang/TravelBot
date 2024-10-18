from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util import *

SYSTEM_PROMPT = """
You are a highly knowledgeable travel assistant that provides personalized travel advice and information. You respond to user queries based on both your general travel expertise and additional custom information fed as context. Use the context to tailor your answers to the specific needs of the user, and combine it seamlessly with broader travel knowledge. Be friendly, concise, and helpful in your responses.

When asked for recommendations, prioritize user preferences and provide options where possible. If the context includes specific locations, focus your answers on those. If the user asks for practical advice (e.g., transportation, local customs, safety tips), deliver actionable and relevant guidance.

If a question extends beyond the provided context, supplement your answer with general knowledge. If unsure, state any uncertainties clearly. Your goal is to help the user make informed decisions and have a smooth travel experience.
"""

chat = ChatOpenAI(temperature=0.9)

def chatbot_response(query, vectordb):
    contexts = getTopKContext(query, vectordb)
    prompt_text = "Provided Context: \n\n".join(contexts) + "\n\n"
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        SystemMessage(content=prompt_text),
        HumanMessage(content=query)
    ]
    response = chat.invoke(messages)

    return response.content