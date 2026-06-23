# RAG Chat

A minimal **Retrieval-Augmented Generation (RAG)** chat application that answers natural language questions grounded in the content of a PDF document. Uses LangChain to orchestrate ingestion, semantic retrieval, and LLM-based generation.

---

## Architecture

```
User (CLI or Web)
    │
    ▼
┌─────────────────────────────────────────────┐
│          main.py (CLI) / api.py (Web)        │
│  ┌──────────┐    ┌───────────┐  ┌─────────┐ │
│  │Retriever  │───▶│  Prompt   │──▶│  LLM    │ │
│  │(Chroma +  │    │ Template  │  │(Mistral)│ │
│  │   MMR)    │    └───────────┘  └─────────┘ │
│  └──────────┘                                │
└──────────────────────┬──────────────────────┘
                       │
              ┌────────▼────────┐
              │   Chroma DB     │
              │  (vector store) │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │   PDF Document   │
              │ (deeplearning.pdf)│
              └─────────────────┘
```

### Pipeline

| Step | Component | Description |
|------|-----------|-------------|
| **Ingest** | `createDatabase.py` | Loads PDF via `PyPDFLoader`, splits into 1000-char chunks (200 overlap) with `RecursiveCharacterTextSplitter`, embeds with `sentence-transformers/all-mpnet-base-v2`, and persists to Chroma. |
| **Retrieve** | Chroma MMR Retriever | On each query, performs Maximum Marginal Relevance search (`k=4`, `fetch_k=10`, `lambda_mult=0.5`) for diverse, relevant chunks. |
| **Generate** | `ChatMistralAI` | Mistral `mistral-small-2506` receives a prompt with retrieved context and answers strictly from that context — or returns *"I could not find the answer"*. |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3, Flask |
| **LLM Framework** | LangChain (`langchain`, `langchain-mistralai`, `langchain-chroma`) |
| **Vector Store** | Chroma (`langchain_chroma`) |
| **Embeddings** | HuggingFace `sentence-transformers/all-mpnet-base-v2` |
| **LLM** | Mistral AI (`mistral-small-2506`) |
| **Frontend** | React 18, TypeScript, Vite |
| **Document Parsing** | PyPDF, `unstructured` |

---

## Features

- **PDF Ingestion** — Load any PDF, chunk it, embed it, and persist to a local vector database.
- **Semantic Search** — MMR retrieval balances relevance and diversity of results.
- **Grounded Generation** — The LLM is explicitly instructed to answer *only* using the provided context.
- **Dual Interface** — Choose between an interactive CLI (`main.py`) or a modern dark-themed web UI (`api.py` → `localhost:5000`).
- **Graceful Degradation** — If heavy ML dependencies are unavailable, the web server falls back to demo mode so the UI remains testable.

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+ (for frontend development)
- A [HuggingFace access token](https://huggingface.co/settings/tokens)
- A [Mistral AI API key](https://console.mistral.ai/api-keys/)

### Installation

```bash
# 1. Navigate to the project
cd RAG

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your tokens:
#   HUGGINGFACEHUB_ACCESS_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#   MISTRAL_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Build the Vector Database

```bash
# Place your PDF in Document_loaders/ (or edit the path in createDatabase.py)
python createDatabase.py
```

### Run

#### Web Interface (default)

```bash
python api.py
# Open http://localhost:5000
```

#### CLI Interface

```bash
python main.py
```

#### Frontend Development (with backend running)

```bash
cd frontend
npm install
npm run dev    # Vite dev server on :5173 with HMR
```

---

## Project Structure

```
RAG/
├── api.py                  # Flask web server (serves frontend + /api/chat endpoint)
├── main.py                 # CLI-based interactive chat
├── createDatabase.py       # PDF ingestion and vector store creation
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore
├── chroma_db/              # Persisted vector store (gitignored, generated)
├── Document_loaders/       # Source PDF files (gitignored)
└── frontend/               # React + TypeScript + Vite SPA
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig*.json
    ├── index.html
    └── src/
        ├── App.tsx         # Main chat component (state, fetch logic)
        ├── App.css
        ├── index.css        # Global styles / chat UI theme
        ├── main.tsx        # React entry point
        ├── lib/
        │   └── utils.js    # postChat() helper
        ├── components/
        │   ├── ChatWindow.tsx   # Scrollable message list
        │   ├── ChatInput.tsx    # Input form
        │   └── ui/              # Reusable primitives (Button, Input, Card, ScrollArea)
        └── assets/
            ├── hero.png
            ├── react.svg
            └── vite.svg
```

---

## API

### `POST /api/chat`

**Request:**
```json
{
  "question": "What is deep learning?"
}
```

**Response:**
```json
{
  "answer": "Deep learning is a subset of machine learning that uses neural networks with multiple layers..."
}
```

---

## Customization

- **Change the source document** — Edit the `file_path` variable in `createDatabase.py`.
- **Adjust chunking** — Modify `chunk_size` and `chunk_overlap` in `createDatabase.py`.
- **Tune retrieval** — Change `k`, `fetch_k`, or `lambda_mult` in the retriever setup within `main.py` or `api.py`.
- **Swap LLM** — Replace `ChatMistralAI` with any LangChain-supported chat model (`ChatOpenAI`, `ChatAnthropic`, etc.).

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
