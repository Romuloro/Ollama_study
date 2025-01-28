from operator import itemgetter

def create_chain(retriever, prompt, model, parser):
    chain = (
        {
            "context": itemgetter("question") | retriever,
            "question": itemgetter("question"),
            "image_paths": itemgetter("image_paths"),
        }
        | prompt
        | model
        | parser
    )

    return chain