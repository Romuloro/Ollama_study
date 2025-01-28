import os
from langchain_community.document_loaders import UnstructuredImageLoader


# Função para carregar imagens
def load_images(image_dir):
    docs = []
    for file in os.listdir(image_dir):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            loader = UnstructuredImageLoader(file_path=os.path.join(image_dir, file), mode="elements")
            docs.extend(loader.load())
    return docs

# Função para carregar imagens
def load_images_path(image_dir):
    docs = []
    for file in os.listdir(image_dir):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            docs.extend(file)
    return docs