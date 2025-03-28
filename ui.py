import streamlit as st
from src.rag.main import build_rag_chain
from src.base.llm_model import get_hf_llm
from multiprocessing import freeze_support
import torch


if __name__ == "__main__":
    PYTORCH_CUDA_ALLOC_CONF = True
    torch.cuda.empty_cache()
    torch.cuda.memory_summary(device=0)

    st.set_page_config(
        page_title="RAG APP DEMO",  # Tiêu đề tab trình duyệt
        page_icon="💬",  # Icon tab
        layout="wide"  # Giao diện rộng
    )
    def generate_response(input_text):
        genai_docs = "./data_source/generative_ai"
        llm = get_hf_llm()
        model = build_rag_chain(llm, data_dir=genai_docs, data_type="pdf")
        st.info(model.invoke(input_text))


    with st.form("my_form"):
        text = st.text_area(
            "Nhập câu hỏi :",
            "Video-to-Speech",
        )
        submitted = st.form_submit_button("Submit")
        generate_response(text)
