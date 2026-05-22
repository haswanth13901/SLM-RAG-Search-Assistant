# 🔍 Local AI Search Bot

> A fully local, CPU-only RAG-powered search assistant — real-time web answers on a budget laptop, no GPU required.

Ask it anything: today's news, live scores, current weather, or your own uploaded documents. It searches the web in real time and uses a local LLM to summarize results in plain English — complete with source citations.

---

## ✨ Key Features

- **Real-time web search** — Tavily API fetches live results for every query, bypassing the model's training cutoff
- **RAG pipeline** — search results are injected directly into the prompt; the model never relies on stale training data
- **Source citations** — every answer links back to the websites it drew from
- **Document Q&A** — upload PDF, TXT, or MD files and ask questions about their content
- **Search toggle** — switch between live web search and raw model knowledge on the fly
- **Chat history** — full session history with one-click export as TXT or PDF
- **Gradio web UI** — clean browser interface at `localhost:7860`, no frontend code needed
- **Runs on CPU only** — optimized for 8GB RAM, no GPU or cloud compute required

---

## 🛠️ Tech Stack

| Layer | Tool | Role |
|---|---|---|
| Local LLM | [Ollama](https://ollama.com) + `qwen2.5:3b` | AI reasoning engine |
| Real-time search | [Tavily API](https://tavily.com) | Live web retrieval |
| UI | [Gradio](https://gradio.app) | Browser-based chat interface |
| Document reading | [PyMuPDF](https://pymupdf.readthedocs.io) | PDF text extraction |
| Chat export | [fpdf2](https://py-fpdf2.readthedocs.io) | PDF generation |
| Secret management | [python-dotenv](https://pypi.org/project/python-dotenv/) | Keeps API keys out of version control |
| Language | Python 3.10+ | — |

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- A free [Tavily API key](https://tavily.com)

### Steps

```bash
# 1. Pull the local model
ollama pull qwen2.5:3b

# 2. Clone the repository
git clone https://github.com/haswanth13901/SLM.git
cd SLM

# 3. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Add your Tavily API key
echo TAVILY_API_KEY=your-key-here > .env
```

---

## 🚀 Usage

Make sure Ollama is running in the background, then launch the app:

```bash
python app.py
```

Open **http://127.0.0.1:7860** in your browser.

| Mode | How to use |
|---|---|
| **Web search** | Type your question with the search toggle **ON** |
| **Model only** | Type your question with the search toggle **OFF** |
| **Document Q&A** | Upload a PDF/TXT/MD file, then ask a question about it |
| **Export history** | Click **Download as TXT** or **Download as PDF** |
| **Clear session** | Click **Clear History** |

### Terminal version

Prefer the command line? Run the terminal-only version instead:

```bash
python searchbot.py
```

---

## 📁 Project Structure

```
SLM/
├── .env                  # API keys (gitignored)
├── .gitignore
├── app.py                # Gradio UI entry point
├── search.py             # Search + AI logic
├── history.py            # Chat history + TXT/PDF export
├── docreader.py          # Document reading (PDF, TXT, MD)
├── searchbot.py          # Terminal version
├── requirements.txt
├── README.md
└── tests/
    └── test.py           # API connection test
```

---

## ⚠️ Limitations

- **CPU inference** — responses take 5–15 seconds; no GPU acceleration
- **3B model cap** — 8GB RAM limits model size; larger, more capable models won't fit
- **~3000 character context** — very large documents are truncated before being sent to the model
- **No multi-turn memory** — each query is independent; the model doesn't remember previous questions
- **Tavily free tier** — capped at 1,000 searches/month
- **No image support** — vision models exceed available RAM; JPG/PNG uploads are not supported
- **2MB document limit** — uploaded files above this size are rejected

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes** with a clear message
   ```bash
   git commit -m "feat: add your feature description"
   ```
4. **Push** to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request** — describe what you changed and why

Please keep PRs focused and include a brief description of the problem being solved. Bug reports and feature requests are also welcome via [GitHub Issues](https://github.com/haswanth13901/SLM/issues).

---

> **Disclaimer:** This is an AI-powered application and can make mistakes. Responses may be incomplete, outdated, or inaccurate. Always verify important information from reliable sources before acting on it.
