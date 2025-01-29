from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import time

import streamlit as st

from services import text, vectorstore, chain, image
from infrastructure import prompt as ppt

dir_path_pdf = './data/pdf/'
dir_path_image = './data/image/'
MODEL = 'llama3.2-vision'

def chat_stream(question,chain_, image_path=None):
    # Prepare os dados de entrada para o chain_
    inputs = {
        "question": question,
        "image_paths": image_path,  # Se necessário, passe o caminho das imagens aqui
    }

    response = f'{chain_.invoke({"question": question, "image_paths": image_path})}'
        
    # Enviando a resposta caractere por caractere, como no exemplo original
    for word in response.split():
        yield word + " "
        time.sleep(0.02)


def save_feedback(index):
    st.session_state.history[index]["feedback"] = st.session_state[f"feedback_{index}"]

def main():
        
    st.set_page_config(page_title='ChatGpt Elis', page_icon=':books:')
    st.header('Olá Elisangela. Converse com seus arquivos da pós')
    #user_question = st.text_input('Faça uma pergunta para mim!')

    if "history" not in st.session_state:
        st.session_state.history = []
    

    for i, message in enumerate(st.session_state.history):
        with st.chat_message(message["role"]):
            st.write(message["content"])

            if message["role"] == "assistant":
                feedback = message.get("feedback", None)
                st.session_state[f"feedback_{i}"] = feedback
                st.feedback(
                    "thumbs",
                    key=f"feedback_{i}",
                    disabled=feedback is not None,
                    on_change=save_feedback,
                    args=[i],
                )
    
    if prompt := st.chat_input("Say something"):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            response = st.write_stream(chat_stream(prompt, st.session_state.conversation))
            st.session_state.history.append({"role": "assistant", "content": response})

            st.feedback(
                "thumbs",
                key=f"feedback_{len(st.session_state.history)}",
                on_change=save_feedback,
                args=[len(st.session_state.history)],
            )
    
    with st.sidebar:
    
        st.subheader('Seus arquivos')
        #precisa colcoar accept_multiple_files = TRue para ele carregar vários arquivos. Caso contrário só carrega um arquivo
        pdf_docs = st.file_uploader("Carregue os seus arquivos em formato PDF", accept_multiple_files=True)

        if st.button('Processar'):

            data_pdf = text.create_text_chunks(pdf_docs)
            data = data_pdf #+ data_image

            vectorstore_ = vectorstore.create_vectorstore(data, MODEL)

            retriever = vectorstore_.as_retriever()
            model = ChatOllama(model=MODEL, temperature=0)
            parser = StrOutputParser()

            prompt_ = ppt.create_prompt()

            st.session_state.conversation = chain.create_chain(retriever, prompt_, model, parser)


if __name__ == '__main__':
    main()