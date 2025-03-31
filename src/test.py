from src.base import llm_model
from src.rag.main import build_rag_chain
from deep_translator import GoogleTranslator
import asyncio
def process_vi_prompt(vi_prompt):
    # Dịch sang tiếng Anh (async)
    translator = GoogleTranslator(source="vi" , target="en")
    en_prompt = translator.translate(vi_prompt)

    # Gọi LLM (giả sử llm.invoke() không phải async)
    llm = llm_model.get_hf_llm()
    en_output = llm.invoke(en_prompt)
    vi_output = GoogleTranslator(source="en", target="vi")
    return vi_output.translate(en_output)

def main():
    vi_prompt = "Question : Thủ đô của Hàn Quốc là gì  Answer :"
    result = process_vi_prompt(vi_prompt)
    print(result)

if __name__ == "__main__":
    main()
