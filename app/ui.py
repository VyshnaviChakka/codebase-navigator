import streamlit as st
from embed import create_embeddings, create_faiss_index, model
from ingest import clone_repo, load_code_files, chunk_code
from agents import planner_agent, retriever_agent, explainer_agent, web_agent

st.title("🔥 AI Codebase Navigator")

repo_url = st.text_input(
    "Enter GitHub Repo URL:",
    "https://github.com/fastapi/fastapi"
)

if "active_repo" not in st.session_state:
    st.session_state.active_repo = repo_url

if "history" not in st.session_state:
    st.session_state.history = []

if repo_url != st.session_state.active_repo:
    st.session_state.active_repo = repo_url
    st.session_state.history = []
    st.cache_resource.clear()
    st.rerun()


@st.cache_resource
def load_system(repo_url):
    repo = clone_repo(repo_url)
    files = load_code_files(repo)
    chunks = chunk_code(files)

    embeddings = create_embeddings(chunks)
    index = create_faiss_index(embeddings)

    return chunks, index


chunks, index = load_system(repo_url)

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

query = st.chat_input("Ask your question:")

if query:
    with st.chat_message("user"):
        st.write(query)

    task = planner_agent(query)

    if task == "web":
        context = web_agent(query)

    elif task == "both":
        code_context = retriever_agent(query, model, index, chunks)
        web_context = web_agent(query)

        code_context = "\n\n".join(code_context.split("\n\n")[:2])
        web_context = "\n\n".join(web_context.split("\n\n")[:2])

        context = f"""
        CODE CONTEXT:
        {code_context}

        WEB CONTEXT:
        {web_context}
        """

    else:
        context = retriever_agent(query, model, index, chunks)

    answer = explainer_agent(query, context, st.session_state.history)

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.history.append({"role": "user", "content": query})
    st.session_state.history.append({"role": "assistant", "content": answer})