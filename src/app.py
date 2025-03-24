import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from src.base.llm_model import get_hf_llm
from src.rag.main import build_rag_chain, inputQA, outputQA

llm = get_hf_llm()

genai_docs = "./data_source/generative_ai"

genai_chain = build_rag_chain(llm, data_dir=genai_docs, data_type="pdf")
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using Langchain's Runnable interfaces"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers = ["*"]
)

@app.get("/check")
async def check() :
    return {"status" : "ok"}

@app.post("/generative_ai" , response_model = outputQA)
async def generative_ai(inputs : inputQA) :
    answer = genai_chain.invoke(inputs.question)
    return {"answer" : answer}

add_routes(
    app,
    genai_chain,
    playground_type="default",
    path="/generative_ai"
)