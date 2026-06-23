from flask import Flask, request, jsonify
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import mimetypes
import tempfile
import os

load_dotenv()

# ensure Flask serves .jsx/.tsx as JavaScript so browsers accept module scripts
mimetypes.add_type('application/javascript', '.jsx')
mimetypes.add_type('application/javascript', '.tsx')
mimetypes.add_type('application/javascript', '.ts')

app = Flask(__name__, static_folder='frontend', static_url_path='')

# Try to initialise embeddings, vectorstore and LLM. If required packages are missing,
# fall back to a lightweight demo mode so the UI still works.
DEMO_MODE = False
retriever = None
llm = None
prompt = None
embeddings = None
vectorstore = None
try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorstore = Chroma(persist_directory='chroma_db', embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_type='mmr', search_kwargs={'k':4,'fetch_k':10,'lambda_mult':0.5})

    llm = ChatMistralAI(model='mistral-small-2506')

    prompt = ChatPromptTemplate.from_messages([
        ("system","You are a helpful AI assistant. Use ONLY the provided context to answer. If not present, say: I could not find the answer in the document."),
        ("human","Context:\n{context}\n\nQuestion:\n{question}")
    ])
except Exception as e:
    # likely missing heavy ML deps (sentence-transformers / torch). Use demo mode.
    DEMO_MODE = True
    print("[warning] running in DEMO_MODE: ", e)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    question = data.get('question','')
    if DEMO_MODE:
        # simple canned/demo reply so UI works without heavy deps
        demo = f"Demo mode: backend not configured. Example answer for '{question}'."
        return jsonify({'answer': demo})

    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([d.page_content for d in docs])
    final_prompt = prompt.invoke({"context":context, "question": question})
    response = llm.invoke(final_prompt)
    return jsonify({'answer': getattr(response, 'content', str(response))})

@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file sent'}), 400
    file = request.files['file']
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are accepted'}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        global vectorstore, retriever, DEMO_MODE, embeddings

        if vectorstore is None:
            emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
            vs = Chroma.from_documents(documents=chunks, embedding=emb, persist_directory='chroma_db')
            vs.persist()
            embeddings = emb
            vectorstore = Chroma(persist_directory='chroma_db', embedding_function=embeddings)
            retriever = vectorstore.as_retriever(search_type='mmr', search_kwargs={'k':4,'fetch_k':10,'lambda_mult':0.5})
            DEMO_MODE = False
        else:
            vectorstore.add_documents(chunks)
            vectorstore.persist()

        return jsonify({'message': f'Processed {len(chunks)} chunks from {file.filename}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.unlink(tmp_path)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
