import logging

from langchain_openai import OpenAIEmbeddings

import chromadb
from langchain_chroma import Chroma
from pandas import read_csv
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

from app.core.config import settings


def setup_client():
    return chromadb.HttpClient(
        host="172.30.0.2",
        port=8000,
        ssl=False,
        headers=None,
        settings=Settings(),
        tenant=DEFAULT_TENANT,
        database=DEFAULT_DATABASE
    )


client = setup_client()


def load_and_process_data(file_path: str, num_rows: int = 2000):
    df_full = read_csv(file_path)
    return df_full.head(num_rows)


def convert_df_to_text_list(df):
    text_list = []
    for _, row in df.iterrows():
        row_str = ', '.join(map(str, row.tolist()))
        text_list.append(row_str)
    return text_list


class VectorStoreManager:
    def __init__(self, client):
        """Inicializa o gerente de armazenamento de vetores com um cliente."""
        self.client = client
        self.vectorstore = None
        self.persist_directory = "data"

    def initialize_vectorstore(self, text_list, collection_name):
        """Inicializa a loja de vetores com uma lista de textos e um nome de coleção."""
        logging.info("Initializing VectorStore...")
        if not self.vectorstore:
            try:
                chroma_db = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=OpenAIEmbeddings(),
                    collection_name=collection_name
                )
                collection = chroma_db.get()

                if len(collection['ids']) == 0:  # Se a coleção estiver vazia
                    logging.info("Creating new VectorStore...")
                    self.vectorstore = Chroma.from_texts(
                        texts=text_list,
                        collection_name=collection_name,
                        embedding=OpenAIEmbeddings(),
                        client=self.client,
                        persist_directory=self.persist_directory
                    )
                    logging.info("VectorStore initialized successfully.")
                else:
                    logging.info("Using existing VectorStore collection.")
                    self.vectorstore = chroma_db

            except Exception as e:
                logging.error("Failed to initialize VectorStore: " + str(e))
                raise
        else:
            logging.info("VectorStore already initialized.")

    def get_retriever(self):
        """Retorna um objeto de recuperação da loja de vetores."""
        if self.vectorstore:
            return self.vectorstore.as_retriever()
        else:
            logging.error("Attempted to get retriever before initialization.")
            raise RuntimeError("Vectorstore has not been initialized")

    def add(self, data: list):
        """Adiciona uma lista de dados à loja de vetores."""
        if self.vectorstore:
            return self.vectorstore.add_texts(data)
        else:
            raise RuntimeError("Vectorstore has not been initialized")


class VectorStoreHandler:
    def __init__(self, client, url_data, collection_name):
        """Gerencia o processo de inicialização e operação de uma VectorStore."""
        self.client = client
        self.collection_name = collection_name
        self.manager = VectorStoreManager(self.client)
        self.initialized = False

        try:
            text_list = self.load_and_process_data(url_data)
            self.manager.initialize_vectorstore(text_list=text_list, collection_name=self.collection_name)
            self.initialized = True
        except Exception as e:
            logging.error(f"Erro ao inicializar a loja de vetores: {e}")
            raise

    def load_and_process_data(self, url_data):
        """Carrega e processa dados a partir de uma URL."""
        df = load_and_process_data(url_data)
        return convert_df_to_text_list(df)

    def get_retriever(self):
        """Obtém o retriever da VectorStore."""
        if not self.initialized:
            raise RuntimeError("Vectorstore has not been initialized")
        return self.manager.get_retriever()


def create_vector_store(client, url_data, collection_name):
    """Função responsável por criar e inicializar uma VectorStore."""
    handler = VectorStoreHandler(client, url_data, collection_name)
    return handler.manager


def get_retriever_from_manager(manager):
    """Obtém o retriever de um gerente de VectorStore."""
    return manager.get_retriever()


manager = create_vector_store(client, settings.URL_DATA_RAG, "medical_db")
retriever = get_retriever_from_manager(manager)
"""manager = VectorStoreManager(client)
df = load_and_process_data(settings.URL_DATA_RAG)
text_list = convert_df_to_text_list(df)

manager.initialize_vectorstore(text_list=text_list, collection_name="medical_db")

retriever = manager.get_retriever()"""
