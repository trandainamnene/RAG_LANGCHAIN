import streamlit as st
from src.rag.main import build_rag_chain
from src.base.llm_model import get_hf_llm

collection_name = "data_test"

# 1. Cấu hình trang
st.set_page_config(
    page_title="RAG APP DEMO",
    page_icon="💬",
    layout="wide"
)


# 2. Cache LLM và RAG chain
@st.cache_resource
def get_llm():
    return get_hf_llm()


@st.cache_resource
def initialize_model():
    llm = get_llm()
    genai_docs = "./data_source/generative_ai"
    return build_rag_chain(llm, data_dir=genai_docs, data_type="pdf")


# 3. Hàm hiển thị chat UI
def display_chat_ui(model):
    # Khởi tạo lịch sử chat trong session_state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Xin chào! Tôi là trợ lý ảo. Bạn muốn hỏi gì về Generative AI?"
        })

    # Tạo placeholder để hiển thị lịch sử chat
    chat_container = st.container()

    # Hàm cập nhật lịch sử chat
    def update_chat_display():
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # Hiển thị lịch sử chat ban đầu
    update_chat_display()

    # Hàm xử lý khi submit form
    def handle_submit():
        user_input = st.session_state.user_input
        if user_input:
            # Thêm câu hỏi vào lịch sử
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Hiển thị câu hỏi ngay lập tức
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(user_input)

            # Xử lý câu trả lời từ model
            with st.spinner("Đang xử lý..."):
                model_response = model(user_input)
                # Thêm câu trả lời vào lịch sử
                st.session_state.messages.append({"role": "assistant", "content": model_response})

                # Hiển thị câu trả lời ngay lập tức
                with chat_container:
                    with st.chat_message("assistant"):
                        st.markdown(model_response)

            # Xóa input sau khi gửi
            st.session_state.user_input = ""

    # Form input với callback
    with st.form("chat_form", clear_on_submit=True):
        st.text_input("Nhập câu hỏi của bạn:", key="user_input",
                      on_change=handle_submit if st.session_state.get("user_input") else None)
        st.form_submit_button("Gửi", on_click=handle_submit)


# 4. Main execution
if __name__ == "__main__":
    model = initialize_model()
    display_chat_ui(model)