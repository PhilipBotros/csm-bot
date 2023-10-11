from abc import ABC, abstractproperty
import logging
import random

import chromadb
from chromadb import Settings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import AzureSearch, Chroma
import pandas as pd

import config


def get_hf_issues(filepath="data/hf-issues.csv", maxcount=10000, msgminsize=30, msgmaxsize=900):
    df = pd.read_csv(filepath)
    df["comments_clean"] = df["comments"].apply(lambda x: x[1:-1])
    df["embed_text"] = df.apply(lambda x: f"Issue: {x.body}, Comments: {x.comments[1:-1]}", axis=1)
    df = df[df["embed_text"].str.len().between(msgminsize, msgmaxsize)]
    df = df.sample(n=min(len(df), maxcount))
    return list(df["embed_text"])


class ContextManager(ABC):

    @abstractproperty
    def retriever(self):
        pass
    
    def count(self):
        return self.retriever.count()

    def get_relevant_context(self, question):
        return self.retriever.get_relevant_context(question)
 

class AzureSearchContextManager(ContextManager):
    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings(deployment=config.EMBEDDINGS_MODEL)
        self.langchain_azure = AzureSearch(
            azure_search_endpoint=config.COGNITIVE_SEARCH_STORE_ADDRESS,
            azure_search_key=config.COGNITIVE_SEARCH_STORE_PASSWORD,
            index_name=config.COGNITIVE_SEARCH_STORE_INDEX_NAME,
            embedding_function=self.embeddings.embed_query)
        
        self.__handle_db_coldstart()
        self._retriever = self.langchain_azure.as_retriever()
        
    def __handle_db_coldstart(self):
        if self.langchain_azure._collection.count() == 0:
            logging.info("Coldstart: Adding texts to database")
            msgs = get_hf_issues()
            self.langchain_azure.add_texts(msgs, metadatas=[{"source": str(i)} for i in range(len(msgs))])
        else:
            logging.info("Re-instate Cognitive Search DB from disk")

    @property
    def retriever(self):
        return self._retriever


class ChromaContextManager(ContextManager):
    def __init__(self) -> None:
        self.dbclient = chromadb.PersistentClient(config.CHROMADB_PERSIST_DIRECTORY, settings=Settings(allow_reset=True))
        self.embeddings = OpenAIEmbeddings(request_timeout=5, show_progress_bar=True)
        self.langchain_chroma = Chroma(client=self.dbclient, embedding_function=self.embeddings)

        self.__handle_db_coldstart()
        self._retriever = self.langchain_chroma.as_retriever()
        
    def __handle_db_coldstart(self):
        if self.langchain_chroma._collection.count() == 0:
            logging.info("Coldstart: Adding texts to database")
            msgs = get_hf_issues()
            self.langchain_chroma.add_texts(msgs, ids=[str(i) for i in range(len(msgs))])
        else:
            logging.info("Re-instate ChromaDB from disk")

    @property
    def retriever(self):
        return self._retriever
    
    def count(self):
        return self.langchain_chroma._collection.count()

    def sample_dps(self, nr_sample):
        nr_of_elements = self.count()
        random_ids = random.sample(range(nr_of_elements), nr_sample)
        return self.langchain_chroma.get(ids=[str(idx) for idx in random_ids], include=["documents"])["documents"]


def get_context_manager():
    if config.STORAGE_MODE == config.StorageMode.AZURE_SEARCH:
        return AzureSearchContextManager()
    elif config.STORAGE_MODE == config.StorageMode.LOCAL:
        return ChromaContextManager()
    else:
        raise Exception("Unsupported storage mode")


# A single context manager for the whole app
context_manager = get_context_manager()
