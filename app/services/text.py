from langchain.text_splitter import CharacterTextSplitter


def create_text_chunks(loader):

    text_splitter = CharacterTextSplitter(
            separator = '\n',
            chunk_size = 1500,
            chunk_overlap = 300,
            length_function= len
            )

    data_slipt = loader.load_and_split(text_splitter)

    return data_slipt
