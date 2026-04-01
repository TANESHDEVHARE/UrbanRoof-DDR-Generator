from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_vectorstore(docs):

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore