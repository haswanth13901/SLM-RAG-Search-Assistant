import requests
import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def ask(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "qwen2.5:3b", "prompt": prompt, "stream": False}
    )
    return r.json()["response"]

def search(query):
    # Detect list-based questions and search more aggressively
    list_keywords = ["list", "all", "every", "history", "from start", "beginning", "till", "complete"]
    is_list_query = any(word in query.lower() for word in list_keywords)
    
    if is_list_query:
        enhanced_query = f"complete full list {query} all years"
        max_results = 8
    else:
        enhanced_query = f"{query} 2025 2026"
        max_results = 5

    result = client.search(enhanced_query, max_results=max_results)
    context = "\n\n".join([f"{r['title']}: {r['content']}" for r in result['results']])
    sources = "\n".join([f"- {r['title']}: {r['url']}" for r in result['results']])
    return context, sources

def search_and_ask(query):
    context, sources = search(query)
    prompt = f"""You are a professional search assistant.
IMPORTANT: The search results below are more up to date than your training data.
Always trust the search results over your own knowledge.
For list questions, extract and combine ALL names/items mentioned across ALL search results.
Do not skip any entry. Present as a complete numbered list.
Do not add information that contradicts the search results.

SEARCH RESULTS:
{context}

QUESTION: {query}

Complete list extracted from all search results:"""
    answer = ask(prompt)
    full_response = f"{answer}\n\n---\n📚 Sources:\n{sources}"
    return answer, sources, full_response

def doc_and_ask(query, doc_text):
    doc_context = doc_text[:3000]
    prompt = f"""You are a polite and professional assistant.
Using the document below, answer the question clearly and concisely in 2-3 sentences.
Be formal, accurate, and straight to the point.
Only use the document content to answer.

DOCUMENT:
{doc_context}

QUESTION: {query}

Formal answer:"""
    answer = ask(prompt)
    full_response = f"{answer}\n\n---\n📄 Source: Uploaded document"
    return answer, "Uploaded document", full_response

def ask_only(query):
    prompt = f"""You are a polite and professional assistant.
Answer the following question clearly and concisely in 2-3 sentences using your knowledge.
Be formal and straight to the point.

QUESTION: {query}

Formal answer:"""
    answer = ask(prompt)
    full_response = f"{answer}\n\n---\nℹ️ Answered from model knowledge (web search disabled)"
    return answer, "Model knowledge", full_response