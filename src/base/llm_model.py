import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from transformers import BitsAndBytesConfig

def get_hf_llm(model_name="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", max_new_tokens=512, **kwargs):
    nf4_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        # quantization_config=nf4_config,
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
    )
    model_pipline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens,

    )
    llm = HuggingFacePipeline(
        pipeline=model_pipline,
    )
    return llm

