import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.vectorstores import Chroma 
from dotenv import load_dotenv
load_dotenv()

data = PyPDFLoader('Document_loaders/deeplearning.pdf')

docs = data.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


chunks = splitter.split_documents(docs)

embedding_model = HuggingFaceEndpointEmbeddings(
                                        model="sentence-transformers/all-mpnet-base-v2",
                                         huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN"
                                                                            
                            ))


vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db",
)

# ensure data is written to disk
vectorstore.persist()