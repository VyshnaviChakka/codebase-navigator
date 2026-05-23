from dotenv import load_dotenv
import os

load_dotenv()
from langchain_openai import ChatOpenAI
from langsmith import traceable
import os

llm = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")  
)



def generate_answer(query, context, chat_history):
    history_text = "\n".join(
    [f"{msg['role'].upper()}: {msg['content']}" for msg in chat_history]
    )
    prompt = f"""
    You are a helpful AI assistant.

    Use CODE CONTEXT for repository-related answers.
    Use WEB CONTEXT for latest or external information.

    Conversation so far:
    {history_text}

    Use the following code context to answer:

    Context:
    {context}

    Current Question:
    {query}

    Answer clearly with reference to code if possible.
    """

    response = llm.invoke(prompt)
    return response.content
