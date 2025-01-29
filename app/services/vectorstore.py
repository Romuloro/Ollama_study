from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

def create_vectorstore(chunks, model_name):

    embeddings = OllamaEmbeddings(model=model_name)
    vectorstore = FAISS.from_texts(chunks, embeddings)

    return vectorstore

