import openai
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

loader = PyPDFLoader("test.pdf")
pages = loader.load_and_split()

with get_openai_callback() as cb:
    faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings(model="text-embedding-3-small",deployment="text-embedding-3-small"))
    print(cb)

def chat(input_text):
    docs = faiss_index.similarity_search(input_text, k=1)
    chat = ChatOpenAI(
        openai_api_key=openai.api_key,
        model_name="gpt-4",
        temperature=0.2
    )
    prompt = f''' Provided is an input question along with 4 options and the text related to that question. 
    Read the text clearly, carefully and completely and give the correct option for the input question.
     
    {input_text}
    
    {docs}
    
    '''

    return chat.predict(prompt)