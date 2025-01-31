from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from PyPDF2 import PdfReader


def create_text_chunks(pdf_docs):

    text_splitter = CharacterTextSplitter(
            separator = '\n',
            chunk_size = 1500,
            chunk_overlap = 300,
            length_function= len
            )
    
    documents = []

    for pdf in pdf_docs:
        loader = PyPDFLoader(pdf)
        docs = loader.load()
        documents.extend(docs)
    
    data_slipt = text_splitter.split_documents(documents)

    return data_slipt
