from pydantic import BaseModel, Field

from src.rag.vector_store import get_retriever
from src.rag.offline_rag import Offline_RAG

class inputQA(BaseModel) :
    question : str = Field(... , title="Question to ask the model")

class outputQA(BaseModel):
    answer : str = Field(... , title="Answer from model")

def build_rag_chain(llm , data_dir , data_type) :
    # doc_loaded = Loader(file_type = data_type).load_dir(data_dir , workers = 1)
    retriever = get_retriever()
    rag_chain = Offline_RAG(llm).get_chain(retriever=retriever)

    return rag_chain