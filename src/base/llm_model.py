import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from transformers import BitsAndBytesConfig
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI


def get_hf_llm(model_name="gemini-2.0-flash", max_new_tokens=512, **kwargs):
    # Load API key
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    print(google_api_key)
    # nf4_config = BitsAndBytesConfig(
    #     load_in_4bit=True,
    #     bnb_4bit_quant_type="nf4",
    #     bnb_4bit_use_double_quant=True,
    #     bnb_4bit_compute_dtype=torch.float16,
    # )
    #
    # model = AutoModelForCausalLM.from_pretrained(
    #     model_name,
    #     # quantization_config=nf4_config,
    #     device_map="auto"
    # )
    #
    # tokenizer = AutoTokenizer.from_pretrained(
    #     model_name,
    # )
    # model_pipline = pipeline(
    #     "text-generation",
    #     model=model,
    #     tokenizer=tokenizer,
    #     max_new_tokens=max_new_tokens,
    #
    # )
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
        max_tokens=max_new_tokens,
        timeout=None,
        max_retries=2,
        google_api_key=google_api_key
        # other params...
    )
    return llm
