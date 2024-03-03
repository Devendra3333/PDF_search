import openai
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

loader = PyPDFLoader("fallen.pdf")
pages = loader.load_and_split()

faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings(model="text-embedding-3-small",deployment="text-embedding-3-small"))

def chat(input_text):
    results = []
    docs = faiss_index.similarity_search(input_text, k=10)
    for doc in docs:
        result = {
            "page_number": doc.metadata["page"],
            "text": doc.page_content
        }
        results.append(result)
    return results