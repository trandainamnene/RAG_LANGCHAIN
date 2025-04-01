from src.base import llm_model
from src.rag.main import build_rag_chain
from deep_translator import GoogleTranslator
import asyncio
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
def process_vi_prompt(vi_prompt):
    llm = llm_model.get_hf_llm()
    en_output = llm.invoke(vi_prompt)
    print("English Output from LLM:", en_output)  # Debug



def main():
    vi_prompt = "Bạn là ai"
    result = process_vi_prompt(vi_prompt)
    print(result)

if __name__ == "__main__":
    main()
    # load_dotenv()
    # google_api_key = os.getenv("GOOGLE_API_KEY")
    # print(google_api_key)
    # print(dotenv_values())
