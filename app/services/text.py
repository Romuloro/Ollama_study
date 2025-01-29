from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader


def create_text_chunks(pdf_docs):

    text_splitter = CharacterTextSplitter(
            separator = '\n',
            chunk_size = 1500,
            chunk_overlap = 300,
            length_function= len
            )
    
    text = ""

    for pdf in pdf_docs:
        loader = PdfReader(pdf)
        for page in loader.pages:
            text += page.extract_text()

    data_slipt = text_splitter.split_text(text)

    return data_slipt
