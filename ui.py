import streamlit as st
from src.rag.main import build_rag_chain
from src.base.llm_model import get_hf_llm
from src.rag.utils import translate

collection_name = "data_test"

# 1. Cấu hình trang - PHẢI là lệnh Streamlit đầu tiên
st.set_page_config(
    page_title="RAG APP DEMO",
    page_icon="💬",
    layout="wide"
)


# 2. Cache các thành phần nặng
@st.cache_resource
def get_llm() :
    llm = get_hf_llm()
    return llm


def initialize_model():
    llm = get_hf_llm()
    genai_docs = "./data_source/generative_ai"
    return build_rag_chain(llm, data_dir=genai_docs, data_type="pdf")


# 3. Hàm hiển thị chat UI
def display_chat_ui():
    # Khởi tạo lịch sử chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Thêm lời chào ban đầu
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Xin chào! Tôi là trợ lý ảo. Bạn muốn hỏi gì về Generative AI?"
        })

    # Hiển thị toàn bộ lịch sử chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Tạo form input và xử lý submit
    with st.form("chat_form"):
        user_input = st.text_input("Nhập câu hỏi của bạn:", key="user_input")
        submitted = st.form_submit_button("Gửi")

        if submitted and user_input:
            # Xử lý khi người dùng nhập và submit
            with st.spinner("Đang xử lý..."):
                # Thêm câu hỏi vào lịch sử
                st.session_state.messages.append({"role": "user", "content": user_input})

                # Dịch và tạo phản hồi
                model_response = model.invoke(user_input)
                # st.write_stream(model_response)
                # Thêm phản hồi vào lịch sử
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": model_response
                })

                # Làm mới UI để hiển thị tin nhắn mới
                st.rerun()


# 4. Main execution
if __name__ == "__main__":
    model = initialize_model()
    display_chat_ui()