from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from services import text, vectorstore, chain, image
from infrastructure import prompt

dir_path_pdf = './data/pdf/'
dir_path_image = './data/image/'
MODEL = 'llama3.2-vision'

loader_pdf = PyPDFDirectoryLoader(dir_path_pdf)

def main(question, image_path):
    try:
        data_pdf = text.create_text_chunks(loader_pdf)
        data = data_pdf #+ data_image

        vectorstore_ = vectorstore.create_vectorstore(data, MODEL)

        retriever = vectorstore_.as_retriever()
        model = ChatOllama(model=MODEL, temperature=0)
        parser = StrOutputParser()

        prompt_ = prompt.create_prompt()

        chain_ = chain.create_chain(retriever, prompt_, model, parser)

        print(f"Answer: {chain_.invoke({'question': question, 'image_paths': image_path})}")
    except Exception as e:
        print(f"Erro ao invocar o modelo: {e}")


if __name__ == '__main__':
    question = "Qual é a idade da terra?"
    image_path = image.load_images_path(dir_path_image)
    main(question, image_path)