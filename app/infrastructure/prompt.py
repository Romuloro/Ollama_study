from langchain.prompts import PromptTemplate

def create_prompt():
    template = """
    You are an assistant that provides answers to questions based on
    a given context. 

    Answer the question based on the context. If you can't answer the
    question, reply "I don't know".

    Be as concise as possible and go straight to the point.

    Context: {context}

    Question: {question}

    Images: {image_paths}
    """

    prompt = PromptTemplate.from_template(template)

    return prompt