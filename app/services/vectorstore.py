from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

def create_vectorstore(chunks):

    embeddings = OllamaEmbeddings(model='mistral')
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore

