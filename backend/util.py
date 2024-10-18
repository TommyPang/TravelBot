import wikipediaapi # https://pypi.org/project/Wikipedia-API/
from CustomDocumentLoader import *
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import uuid
import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore

load_dotenv()

index_name = "travelbot-attraction-index"
topk = 5

def initialize_vector_db(attraction = 'Palace Museum'):
    wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')
    page_py = wiki_wiki.page(attraction)
    if (page_py.exists()):
        filename= f"./{uuid.uuid1()}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                save_sections(page_py.sections, f)
            
            raw_documents = load_document(filename)
            documents = samantic_split(raw_documents)
            vectordb = insert_embeddings(documents)
            return vectordb
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if os.path.exists(filename):
                os.remove(filename)
            else:
                print("File does not exist.")
    else: 
        return 'Information not available'

def save_sections(sections, file, level = 0):
    for child in sections:
        file.write(f"{' ' * level * 2}- {child.title}: {'N/A' if child.text == '' else child.text}\n")
        save_sections(child.sections, file, level + 1)

def load_document(filename):
    loader = CustomDocumentLoader(filename)
    # raw documents (not splitted/processed are returned as Iterator)
    return loader.lazy_load()

def samantic_split(raw_documents):
    text_splitter = SemanticChunker(OpenAIEmbeddings())
    # docs is an array of documents in chunks
    docs = text_splitter.split_documents(raw_documents)
    return docs

def insert_embeddings(docs):
    embeddings_model = OpenAIEmbeddings()
    # Connect to Pinecone index and insert the chunked docs as contents
    docsearch = PineconeVectorStore.from_documents(docs, embeddings_model, index_name=index_name)
    return docsearch

def getTopKContext(query, vectordb):
    # search for the top k most similar documents to the query
    docs = vectordb.similarity_search(query, k=topk)
    return [ d.page_content for d in docs ]