
# RAG

Este projeto é um **Retrieval-Augmented Generation (RAG)** processo de otimizar a saída de um grande modelo de linguagem, de forma que ele faça referência a uma base de conhecimento confiável fora das suas fontes de dados de treinamento antes de gerar uma resposta. Usando como base documentos **PDF** e **futuramente (Imagens, Tabelas e Dados cadastrais)**.


## Instalação

Instale o projeto

### Faça o clone do projeto

```bash
    git clone https://github.com/Romuloro/Ollama_study.git
```

### Rodar o projeto
Nesta parte da instalação é nescessário o uso de **docker** e ter instalado o docker habilitado para o uso de **GPU's**.
No mesmo diretório onde o projeto foi clonado faça os comandos no terminal.

```bash
    docker compose up --build
```

Sai do container com **Ctrl + C**

```bash
    docker compose up -d && docker compose exec ollamaapp /bin/bash
    ollama pull llama3.2-vision
    streamlit run app.py
```
    