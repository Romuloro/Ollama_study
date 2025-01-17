import ollama
from read_pdf import read_pdf

def query_rag_model(pdf_text, question):
    # Combine o texto do PDF com a pergunta
    context = pdf_text
    prompt = f"Texto: {context}\nPergunta: {question}\nResposta:"

    # Usando o modelo RAG para gerar uma resposta
    #ollama.api_url = "http://localhost:5000"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response.message.content

# Exemplo de uso
pdf_text = read_pdf("data/Elements Statistical Learning.pdf")
pergunta = "Quantas páginas existem nesse documento? E quantos capitulos existem no documento e quais são eles?"
resposta = query_rag_model(pdf_text, pergunta)
print(resposta)
