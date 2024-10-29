from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import chromadb
from langchain_chroma import Chroma
from pandas import read_csv
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings


def setup_client():
    return chromadb.HttpClient(
        host="172.26.0.2",
        port=8000,
        ssl=False,
        headers=None,
        settings=Settings(),
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE
    )


client = setup_client()


def load_and_process_data(file_path: str, num_rows: int = 10):
    df_full = read_csv(file_path)
    return df_full.head(num_rows)


def convert_df_to_text_list(df):
    text_list = []
    for _, row in df.iterrows():
        row_str = ', '.join(map(str, row.tolist()))
        text_list.append(row_str)
    return text_list


"""def create_vectorstore(client, text_list):
    return Chroma.from_texts(
        texts=text_list,
        collection_name="rag-chroma",
        embedding=OpenAIEmbeddings(),
        client=client
    )"""


"""df = load_and_process_data("hf://datasets/keivalya/MedQuad-MedicalQnADataset/medDataset_processed.csv")
text_list = convert_df_to_text_list(df)

vectorstore = create_vectorstore(client, text_list)"""


class VectorStoreManager:
    def __init__(self, client):
        self.client = client
        self.vectorstore = None

    def initialize_vectorstore(self, text_list):
        if not self.vectorstore:
            self.vectorstore = Chroma.from_texts(
                texts=text_list,
                collection_name="rag-chroma",
                embedding=OpenAIEmbeddings(),
                client=self.client
            )

    def get_retriever(self):
        if self.vectorstore:
            return self.vectorstore.as_retriever()
        else:
            raise Exception("Vectorstore has not been initialized")

    def add(self, data):
        if self.vectorstore:
            return self.vectorstore.add_texts([data])
        else:
            raise Exception("Vectorstore has not been initialized")


manager = VectorStoreManager(client)

df = load_and_process_data("hf://datasets/keivalya/MedQuad-MedicalQnADataset/medDataset_processed.csv")
text_list = convert_df_to_text_list(df)
manager.initialize_vectorstore(text_list)

retriever = manager.get_retriever()
