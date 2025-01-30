import time
import streamlit as st

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