import os
from langchain_core.messages import HumanMessage
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from src.base.llm_model import get_hf_llm
from src.rag.main import build_rag_chain, inputQA, outputQA , inputSummarize , outputSummarize
from fastapi.responses import StreamingResponse
from src.rag.utils import Summarize
import asyncio
from typing import Generator
from src.rag.db import *
llm = get_hf_llm()
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using Langchain's Runnable interfaces"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers = ["*"]
)

async def to_async_generator(sync_gen: Generator[str, None, None]):
    try:
        for chunk in sync_gen:
            yield chunk
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"[to_async_generator] Streaming error: {e}")
        yield f"[ERROR] {str(e)}\n"

@app.get("/check")
async def check() :
    return {"status" : "ok"}

@app.post("/summarize")
async def summarize(input: inputQA):
    summarize_chain = Summarize(llm=llm).get_sumary_chain()
    if not input.image:
        result = summarize_chain.invoke({"question": input.question})
    else :
        prompt = input.question
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": f"data:{input.image.type};base64,{input.image.url}"}
            ]
        )
        result = summarize_chain.invoke({"question": message})
    return {"answer": result}
@app.post("/generative_ai/{idChat}" , response_model = outputQA)
async def generative_ai(inputs : inputQA , idChat:int) :
    print("GOOGLE_SEARCH_API_KEY:", os.getenv("GOOGLE_SEARCH_API_KEY"))
    genai_docs = "./data_source/generative_ai"
    memory = load_memory_from_db(idChat)
    genai_chain = build_rag_chain(llm=llm, memory=memory)
    if (not inputs.image) :
        question = inputs.question
        stream_generator = genai_chain(question)  # Đây là generator
    else :
        prompt = inputs.question
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": f"data:{inputs.image.type};base64,{inputs.image.url}"}
            ]
        )
        stream_generator = genai_chain(message)
    return StreamingResponse(
        (chunk async for chunk in to_async_generator(stream_generator)),
        media_type="text/plain"
    )


# add_routes(
#     app,
#     genai_chain,
#     playground_type="default",
#     path="/generative_ai"
# )