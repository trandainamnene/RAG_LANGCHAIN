import torch
from transformers import AutoTokenizer , AutoModelForCausalLM , pipeline
from langchain_community.llms import HuggingFacePipeline

def get_hf_llm(model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B" , max_new_tokens = 1024 , **kwargs) :
    model = AutoModelForCausalLM.from_pretrained(
        model_name
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model_pipline = pipeline(
        "text-generation",
        model = model,
        tokenizer = tokenizer,
        max_new_tokens = max_new_tokens,
        device_map="auto"
    )
    llm = HuggingFacePipeline(
        pipeline = model_pipline
    )
    return llm
