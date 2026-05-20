# Local AI Search Bot

> ⚠️ **Warning:** This is an AI-powered application and can make mistakes. Responses may be incomplete, outdated, or inaccurate. Always double-check important information from reliable sources before acting on it.

A locally running AI search bot built on a budget laptop — no GPU, no expensive hardware. Designed to squeeze maximum capability out of limited resources.

## Hardware Context

This project was built and runs on:

- **CPU:** Intel Core i7-10510U @ 1.80GHz (4 cores, 8 threads)
- **RAM:** 8GB (no dedicated GPU)
- **OS:** Windows 11 Home

No cloud compute. No GPU. Just a mid-range laptop running a full AI search pipeline.

## What It Does

Ask it anything — current news, today's weather, live sports scores, recent events, or questions about your own documents. It searches the web in real time and uses a local AI model to summarize and answer in plain English.

## How It Works — Architecture

```
User Question
      ↓
[Search Toggle]
      ↓                          ↓
Web Search ON              Web Search OFF
      ↓                          ↓
Tavily Search API          Model Knowledge
      ↓                          ↓
Top 5 results fetched      Direct answer
      ↓                          ↓
Context + Question injected into prompt (RAG)
      ↓
qwen2.5:3b model reasons over the context
      ↓
Answer + Source Citations returned via Gradio UI
```

## RAG — Retrieval Augmented Generation

This project implements RAG at its core. Instead of relying on the model's training data (which has a knowledge cutoff), the bot:

1. **Retrieves** — Tavily fetches live, relevant web results for every query
2. **Augments** — search results are injected directly into the model prompt as context
3. **Generates** — qwen2.5:3b answers strictly based on that retrieved context

This means the bot can answer questions about today's news, live scores, current weather, and recent events — things a standard local model cannot do.

## Features

- **Real-time web search** — Tavily API fetches live results for every query
- **RAG pipeline** — model never relies on stale training data
- **Source citations** — every answer shows which websites it came from
- **Chat history** — full conversation saved during session
- **Download as TXT or PDF** — export your entire chat history
- **Document upload** — upload PDF, TXT, or MD files and ask questions about them
- **Search toggle** — switch between web search and model knowledge on the fly
- **File size validation** — clear error message if uploaded file exceeds 2MB limit
- **Gradio web UI** — runs in browser at localhost:7860
- **Fully modular codebase** — separate files for search, history, and document reading

## Tech Stack

| Component | Tool | Purpose |
|---|---|---|
| Local LLM | Ollama + qwen2.5:3b | AI reasoning engine |
| Real-time search | Tavily API | Live web retrieval |
| UI | Gradio | Browser-based chat interface |
| Document reading | PyMuPDF | PDF text extraction |
| Chat export | fpdf2 | PDF generation |
| Secret management | python-dotenv | Keeps API keys out of GitHub |

## Why qwen2.5:3b

Chosen specifically for this hardware after testing multiple models:

- Only ~2GB RAM usage — fits comfortably in 8GB
- Better instruction following than phi3:mini
- More accurate responses for list and factual queries
- Fast enough for real conversations on CPU

Larger models (7B+) were tested and were too slow for practical use on this hardware.

## Limitations

### Hardware Limitations
- **No GPU** — all inference runs on CPU, so response time is slower than cloud-based solutions (5-15 seconds per query)
- **RAM constraint** — only 8GB RAM limits model size to 3B parameters maximum. Larger, more capable models cannot run on this machine
- **No image support** — vision models like LLaVA require more RAM than available. JPG/PNG uploads are not supported

### Model Limitations
- **Small context window** — qwen2.5:3b can only process ~3000 characters of document text at a time. Very large documents are truncated
- **Occasional inaccuracy** — 3B parameter models sometimes mix training data with search results, leading to partially incorrect answers
- **List completeness** — for long historical lists, the model may miss some entries if they don't appear in the top search results
- **No multi-turn memory** — the model does not remember previous questions within the same session. Each query is independent

### Search Limitations
- **Tavily free tier** — limited to 1000 searches per month. Heavy usage may exhaust the free quota
- **Real-time data gaps** — live scores, stock prices, and breaking news may not always be available depending on Tavily's index freshness
- **Document size limit** — uploaded files must be under 2MB. Large PDFs with many pages will be rejected

### General Limitations
- **Local only** — the bot runs on your machine and is not accessible from other devices on the network by default
- **Ollama dependency** — Ollama must be running in the background before launching the app
- **No persistent memory** — chat history is lost when the app is closed unless downloaded

## Project Structure

```
SLM/
├── .env                  # API keys (gitignored)
├── .gitignore
├── app.py                # Gradio UI entry point
├── search.py             # Search + AI logic
├── history.py            # Chat history + TXT/PDF download
├── docreader.py          # Document reading (PDF, TXT, MD)
├── searchbot.py          # Terminal version
├── requirements.txt
├── README.md
└── tests/
    └── test.py           # API connection test
```

## Setup

### Prerequisites
- Python 3.10+
- Ollama installed from ollama.com

### Installation

```bash
# Pull the model
ollama pull qwen2.5:3b

# Clone the repo
git clone https://github.com/haswanth13901/SLM.git
cd SLM

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your Tavily API key
echo TAVILY_API_KEY=your-key-here > .env
```

### Run

```bash
python app.py
```

Open http://127.0.0.1:7860 in your browser.

## Usage

| Mode | How |
|---|---|
| Web search | Type question, keep search toggle ON |
| Model only | Type question, turn search toggle OFF |
| Document Q&A | Upload PDF/TXT/MD, type question, submit |
| Download history | Click Download as TXT or Download as PDF |
| Clear history | Click Clear History button |

## Key Learnings

- Running LLMs efficiently on CPU-only hardware
- Implementing RAG from scratch without frameworks
- Prompt engineering to override model knowledge cutoff
- Connecting local models to live web data
- Modular Python project structure
- Building a full AI application end to end on a budget machine
