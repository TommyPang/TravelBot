import wikipediaapi # https://pypi.org/project/Wikipedia-API/
from CustomDocumentLoader import *
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import uuid
import os
import time
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

index_name = "travelbot-attraction-index"
topk = 5
knowledge_file_dir = 'knowledge_base'
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

def get_knowledge_files(directory):
    txt_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    return txt_files

def initialize_vector_db():
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

        index = pc.Index(index_name)

        knowledge_files = get_knowledge_files(knowledge_file_dir)
        docs = []
        for filename in knowledge_files:
            print(f'upserting {filename}')
            try:
                raw_documents = load_document(filename)
                documents = samantic_split(raw_documents)
                docs.extend(documents)
            except Exception as e:
                print(f"An error occurred: {e}")
        vector_store = PineconeVectorStore(index=index, embedding=OpenAIEmbeddings())
        vector_store.add_documents(documents=docs, ids=[str(i) for i in range(len(docs))])
        return vector_store

    index = pc.Index(index_name)
    return PineconeVectorStore(index=index, embedding=OpenAIEmbeddings())

def load_document(filename):
    loader = CustomDocumentLoader(filename)
    # raw documents (not splitted/processed are returned as Iterator)
    return loader.lazy_load()

def samantic_split(raw_documents):
    text_splitter = SemanticChunker(OpenAIEmbeddings())
    # docs is an array of documents in chunks
    docs = text_splitter.split_documents(raw_documents)
    return docs

def getTopKContext(query, vectordb):
    # search for the top k most similar documents to the query
    docs = vectordb.similarity_search(query, k=topk)
    return [ d.page_content for d in docs ]
