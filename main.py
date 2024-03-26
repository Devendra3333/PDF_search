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

loader = PyPDFLoader("fallen.pdf")
pages = loader.load_and_split()

faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings(model="text-embedding-3-small",deployment="text-embedding-3-small"))

chat = ChatOpenAI(
        openai_api_key=openai.api_key,
        model_name="gpt-4-0125-preview",
        temperature=0.2
    )

def chat_prompt(input_text):
    docs = faiss_index.similarity_search(input_text, k=1)
    prompt = f''' Provided is an input question  and the text related to that question. 
    Read the text clearly, carefully and completely and give the correct answer for the input question.
     
    {input_text}
    
    {docs}
    
    '''

    with get_openai_callback() as cb:
        response = chat.invoke(prompt)
        print(cb)
        return response.content, docs

