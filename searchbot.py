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

def ask_only(query):
    prompt = f"""You are a polite and professional assistant.
Answer the following question clearly and concisely using your knowledge.
Be formal and straight to the point.
For list questions provide the complete list.

QUESTION: {query}

Formal answer:"""
    return ask(prompt)

def main():
    print("=" * 50)
    print("       Local Search Bot — Terminal Version")
    print("  Powered by qwen2.5:3b + Tavily Search")
    print("=" * 50)
    print("⚠️  Warning: AI can make mistakes.")
    print("   Always double-check important responses.")
    print("=" * 50)
    print("\nCommands:")
    print("  'search on'  — enable web search (default)")
    print("  'search off' — use model knowledge only")
    print("  'quit'       — exit\n")

    use_search = True

    while True:
        query = input("You: ").strip()

        if query.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if not query:
            continue
        if query.lower() == "search on":
            use_search = True
            print("✅ Web search enabled\n")
            continue
        if query.lower() == "search off":
            use_search = False
            print("ℹ️  Web search disabled — using model knowledge only\n")
            continue

        if use_search:
            print("Searching...")
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

Complete and accurate answer based strictly on search results:"""
            answer = ask(prompt)
            print(f"\nBot: {answer}")
            print(f"\n📚 Sources:\n{sources}\n")
        else:
            answer = ask_only(query)
            print(f"\nBot: {answer}")
            print("\nℹ️  Answered from model knowledge (web search disabled)\n")

if __name__ == "__main__":
    main()