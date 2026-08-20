import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

def build_knowledge_base(resource_path: str):
    print("Building knowledge base...")

    loader = TextLoader(resource_path, encoding="utf-8")
    documents = loader.load()
    print("Loaded document successfully")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} searchable sections")

    embeddings = OpenAIEmbeddings()
    knowledge_base = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./knowledge_base_db"
    )
    print("Knowledge base built successfully!")
    return knowledge_base

def load_knowledge_base():
    embeddings = OpenAIEmbeddings()
    knowledge_base = Chroma(
        persist_directory="./knowledge_base_db",
        embedding_function=embeddings
    )
    return knowledge_base

def search_resource(knowledge_base, diagnosis: str):
    results = knowledge_base.similarity_search(diagnosis, k=5)

    if not results:
        return None, False

    all_content = " ".join([doc.page_content for doc in results])
    diagnosis_found = diagnosis.lower() in all_content.lower()
    relevant_content = "\n\n".join([doc.page_content for doc in results])

    return relevant_content, diagnosis_found