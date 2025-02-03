
# RAG

Este projeto é um **Retrieval-Augmented Generation (RAG)** processo de otimizar a saída de um grande modelo de linguagem, de forma que ele faça referência a uma base de conhecimento confiável fora das suas fontes de dados de treinamento antes de gerar uma resposta. Usando como base documentos **PDF** e **futuramente (Imagens, Tabelas e Dados cadastrais)**.

## Requisitos ⚠️
1. Ter o [wsl](https://learn.microsoft.com/pt-br/windows/wsl/install) caso seu sistema seja Windows.
2. Ter o docker instalado, sendo o mais indicado a sua [CLI](https://docs.docker.com/engine/install/ubuntu/), juntamente com o [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
3. Ter uma placa de video com 8GB de VRAM.
    - Caso não tenha uma GPU o formato compativel para CPU está em desenvolvimento.
    - Caso a sua GPU não tenha 8BG de VRAM, [Veja aqui](#gpu-com--8-vram)



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
```

Já dentro do container docker rode no seu terminal:

#### GPU com 8 VRAM

```bash
ollama pull llama3.2-vision
```

#### GPU com > 8 VRAM

```bash
ollama pull ministral
```
Além disso modifique a variavel **MODEL** para mistral no arquivo **app.py**

**Finalmente rode o projeto com o comando**
```bash
streamlit run app.py --server.port 8777
```