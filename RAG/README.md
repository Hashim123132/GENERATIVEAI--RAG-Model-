# RAG Chat

Minimal RAG app.

Backend (Flask) serves frontend and `/api/chat` which queries `chroma_db`.

Quick start:

1. Create virtualenv and install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create embeddings DB:

```bash
python create_database.py
```

3. Run server:

```bash
python api.py
```

4. Open `http://localhost:5000` and chat.
