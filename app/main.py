from embed import create_embeddings, create_faiss_index, model
from agents import planner_agent, retriever_agent, explainer_agent, web_agent
from ingest import clone_repo, load_code_files, chunk_code
from retrieve import search
from qa import generate_answer

import os
print("LangSmith:", os.getenv("LANGSMITH_API_KEY"))
print("Tracing:", os.getenv("LANGCHAIN_TRACING_V2"))
print("Project:", os.getenv("LANGSMITH_PROJECT"))

# Step 1: Prepare data
repo_url = input("Enter GitHub repo URL: ")
repo = clone_repo(repo_url)
files = load_code_files(repo)
chunks = chunk_code(files)

# Step 2: Embeddings
embeddings = create_embeddings(chunks)
index = create_faiss_index(embeddings)

#  MEMORY STORAGE
chat_history = []

while True:
    query = input("\nAsk your question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    task = planner_agent(query)

    if task == "web":
        print("🌐 Using web search...")
        context = web_agent(query)

    elif task == "both":
        print("🔀 Using BOTH code + web...")

        code_context = retriever_agent(query, model, index, chunks)
        web_context = web_agent(query)

        # Limit both sides
        code_context = "\n\n".join(code_context.split("\n\n")[:2])
        web_context = "\n\n".join(web_context.split("\n\n")[:2])


        context = f"""
        CODE CONTEXT:
        {code_context}

        WEB CONTEXT:
        {web_context}
        """

    else:
        print("📂 Using code search...")
        context = retriever_agent(query, model, index, chunks)

    answer = explainer_agent(query, context, chat_history)
    print("\nAnswer:\n", answer)    

    chat_history.append(f"User: {query}")
    chat_history.append(f"AI: {answer}")