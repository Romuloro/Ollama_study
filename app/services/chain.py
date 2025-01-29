from operator import itemgetter
from langchain.memory import ConversationBufferMemory

def create_chain(retriever, prompt, model, parser):

    #memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
            "image_paths": itemgetter("image_paths"),
            #"memory": memory,
        }
        | prompt
        | model
        | parser
    )

    return chain