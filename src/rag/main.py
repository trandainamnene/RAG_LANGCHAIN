from pydantic import BaseModel, Field
from typing import Optional
from src.rag.vector_store import get_retriever
from src.rag.offline_rag import Offline_RAG

class imageRequest(BaseModel):
    url : str = Field(... , title="Base64 Image URL")
    type : str = Field(... , title="Type of image")
class inputQA(BaseModel) :
    question : str = Field(... , title="Question to ask the model")
    image : Optional[imageRequest] = Field(... , title="Base64 Image")

class outputQA(BaseModel):
    answer : str = Field(... , title="Answer from model")

class inputSummarize(BaseModel):
    question : str = Field(... , title="Question string")
    image: Optional[imageRequest] = Field(..., title="Base64 Image")
class outputSummarize(BaseModel):
    answer : str = Field(... , title="Initial Answer")




def build_rag_chain(llm) :
    # doc_loaded = Loader(file_type = data_type).load_dir(data_dir , workers = 1)
    retriever = get_retriever(collection_name="data_test")
    rag_chain = Offline_RAG(llm).get_chain(retriever=retriever)

    return rag_chain