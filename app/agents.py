from qa import generate_answer
from retrieve import search
from tools import web_search_tool

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

planner_llm = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    base_url="https://openrouter.ai/api/v1"
)
#planner agent(decides which tool to use based on the question and decides intelligently)
def planner_agent(query):
    prompt = f"""
    You are a planner agent.

    Decide which tool to use:
    - "code" → if question is about repository/code
    - "web" → if question is about latest info/news/general knowledge
    - "both" → if question needs both code + web

    Question:
    {query}

    Answer ONLY one word: code / web / both
    """

    response = planner_llm.invoke(prompt)

    return response.content.strip().lower()

# Retriever Agent (finds code)
from langchain_openai import ChatOpenAI

rerank_llm = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    base_url="https://openrouter.ai/api/v1"
)

def retriever_agent(query, model, index, chunks):
    results = search(query, model, index, chunks, top_k=5)

    # Rerank using LLM
    best_chunks = rerank_chunks(query, results, rerank_llm)

    return best_chunks


# Explainer Agent (generates answer)
def explainer_agent(query, context, chat_history):
    return generate_answer(query, context, chat_history)

# Web Agent
def web_agent(query):
    return web_search_tool(query)
     # Split and limit
    split_results = results.split("\n\n")[:3]
    return "\n\n".join(split_results)

#reranking Agent
def rerank_chunks(query, chunks, llm):
    joined_chunks = "\n\n".join(chunks)

    prompt = f"""
    You are an AI assistant.

    From the following chunks, select the 2 most relevant ones for answering the question.

    Question:
    {query}

    Chunks:
    {joined_chunks}

    Return ONLY the most relevant chunks.
    """

    response = llm.invoke(prompt)
    return response.content

planner_llm = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    base_url="https://openrouter.ai/api/v1",
    tags=["planner"]
)

rerank_llm = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    base_url="https://openrouter.ai/api/v1",
    tags=["reranker"]
)