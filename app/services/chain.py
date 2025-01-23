from operator import itemgetter

def create_chain(retriever, prompt, model, parser):
    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
        }
        | prompt
        | model
        | parser
    )

    return chain