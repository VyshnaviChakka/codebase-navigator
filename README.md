# 🔥 AI Codebase Navigator

An intelligent **multi-agent AI system** that understands any public GitHub repository, answers codebase-related questions, performs real-time web search, and maintains conversational memory.

This project combines **RAG (Retrieval-Augmented Generation)**, **FAISS vector search**, **multi-agent architecture**, and **LLM-powered planning** to help developers explore and understand unfamiliar codebases faster.

---

# 🚀 Problem Statement

Understanding a new codebase is difficult.

Developers often spend hours:

- Searching through files manually
- Understanding architecture
- Tracing authentication flows
- Learning APIs and dependencies
- Finding relevant implementation details

This project solves that problem by allowing users to:

✅ Enter any public GitHub repository URL  
✅ Ask questions in natural language  
✅ Get code-aware explanations  
✅ Perform real-time web search for latest information  
✅ Continue conversations with memory

---

# ✨ Features

### 🔍 Repository Understanding
- Dynamically clones any public GitHub repository
- Reads source code files automatically
- Supports:
  - Python
  - JavaScript
  - TypeScript
  - Java
  - Go
  - C++
  - Markdown docs

### 🧠 Intelligent Multi-Agent System

The system uses specialized agents:

#### 1. Planner Agent
Decides whether the question requires:

- Codebase search
- Web search
- Both

Example:

**"Explain authentication flow"**
→ Code search

**"What are latest FastAPI updates?"**
→ Web search

**"Compare FastAPI routing with latest trends"**
→ Both

---

#### 2. Retriever Agent
Uses **FAISS semantic vector search** to retrieve the most relevant code chunks.

Instead of keyword matching, it uses **embeddings** to understand meaning.

---

#### 3. Web Agent
Uses **Tavily Search API** to fetch:

- Latest documentation
- Trends
- Updates
- External information

---

#### 4. Explainer Agent
Uses an LLM to generate contextual and human-readable answers using:

- Retrieved code context
- Web context
- Conversation history

---

### 💬 Conversational Memory
Maintains chat history to support follow-up questions.

Example:

User:
> Explain routing in FastAPI

User:
> Explain that in detail

The assistant understands that **"that"** refers to routing.

---

### 🌐 Dynamic GitHub Repository Support
Users can enter **any public GitHub repository URL**.

Example repositories:

- FastAPI
- LangChain
- Django
- TensorFlow
- OpenCV

---

# 🏗️ System Architecture

```text
User Question
      ↓
Planner Agent
      ↓
 ┌──────────────┬──────────────┐
 ↓              ↓
Code Search     Web Search
(FAISS)         (Tavily)
 ↓              ↓
Context Aggregation
      ↓
Explainer Agent (LLM)
      ↓
Final Answer