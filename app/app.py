from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import time
import os

import streamlit as st

from services import text, vectorstore, chain, image
from infrastructure import prompt as ppt

base_dir = './data'
dir_path_pdf = os.path.join(base_dir, "pdf")
dir_path_image = os.path.join(base_dir, "image")

# Criar os diretórios caso não existam
os.makedirs(dir_path_pdf, exist_ok=True)
os.makedirs(dir_path_image, exist_ok=True)

MODEL = 'llama3.2-vision'

# Extensões permitidas para imagens e PDFs
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}
PDF_EXTENSION = ".pdf"

def chat_stream(question,chain_, image_path=None):
    # Prepare os dados de entrada para o chain_
    inputs = {
        "question": question,
        "image_paths": image_path,  # Se necessário, passe o caminho das imagens aqui
    }

    response = f'{chain_.invoke(inputs)}'
        
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
    
    
    with st.sidebar:
    
        st.subheader('Seus arquivos PDF', divider=True)
        #precisa colcoar accept_multiple_files = TRue para ele carregar vários arquivos. Caso contrário só carrega um arquivo
        uploaded_files = st.file_uploader("Envie seus arquivos (PDFs ou Imagens)", 
                                    type=["pdf", "png", "jpg", "jpeg", "gif", "bmp"],
                                    accept_multiple_files=True)
        
        pdf_files = []
        image_files = []

        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()

                # Determinar o diretório de destino com base na extensão
                if file_extension == PDF_EXTENSION:
                    save_path = os.path.join(dir_path_pdf, uploaded_file.name)
                    pdf_files.append(save_path)
                elif file_extension in IMAGE_EXTENSIONS:
                    save_path = os.path.join(dir_path_image, uploaded_file.name)
                    image_files.append(save_path)
                else:
                    st.warning(f"Extensão não suportada: {uploaded_file.name}")
                    continue

                # Se o arquivo já existir, apenas armazenamos o caminho
                if os.path.exists(save_path):
                    st.warning(f"Arquivo já existe: {uploaded_file.name}. Apenas registrando o caminho.")
                else:
                    # Salvar o arquivo no diretório apropriado
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"Arquivo salvo: {uploaded_file.name}")

            st.write("Todos os arquivos foram processados!")

        if st.button('Processar'):

            data_pdf = text.create_text_chunks(pdf_files)
            data = data_pdf #+ data_image

            vectorstore_ = vectorstore.create_vectorstore(data, MODEL)

            retriever = vectorstore_.as_retriever()
            model = ChatOllama(model=MODEL, temperature=0)
            parser = StrOutputParser()

            prompt_ = ppt.create_prompt()

            st.session_state.conversation = chain.create_chain(retriever, prompt_, model, parser)
    
    if prompt := st.chat_input("Say something"):
        with st.chat_message("user"):
            st.write(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.status("Pensando...", expanded=False) as status:
                response = st.write_stream(chat_stream(prompt, st.session_state.conversation, image_files))
            
            status.update(label="Concluído!", state="complete")
            st.session_state.history.append({"role": "assistant", "content": response})

            st.feedback(
                "thumbs",
                key=f"feedback_{len(st.session_state.history)}",
                on_change=save_feedback,
                args=[len(st.session_state.history)],
            )


if __name__ == '__main__':
    main()