from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from services import text, vectorstore, chain
from infrastructure import prompt

dir_path = 'data'
MODEL = 'mistral'

loader = PyPDFDirectoryLoader(dir_path)

def main(question):
    data = text.create_text_chunks(loader)
    vectorstore_ = vectorstore.create_vectorstore(data)

    retriever = vectorstore_.as_retriever()
    model = ChatOllama(model=MODEL, temperature=0)
    parser = StrOutputParser()

    prompt_ = prompt.create_prompt()

    chain_ = chain.create_chain(retriever, prompt_, model, parser)

    print(f"Answer: {chain_.invoke({'question': question})}")


if __name__ == '__main__':
    question = "Please, what is the concept of meta-learning?"
    main(question)