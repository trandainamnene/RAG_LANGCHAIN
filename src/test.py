# import os
# import re
# import json
# from langchain_community.document_loaders import RecursiveUrlLoader, WebBaseLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
from src.base.llm_model import get_hf_llm
from src.rag.main import build_rag_chain
from langchain_core.messages import HumanMessage
import base64
#


# def bs4_extractor(html: str) -> str:
#     """
#     Hàm trích xuất và làm sạch nội dung từ HTML
#     Args:
#         html: Chuỗi HTML cần xử lý
#     Returns:
#         str: Văn bản đã được làm sạch, loại bỏ các thẻ HTML và khoảng trắng thừa
#     """
#     soup = BeautifulSoup(html, "html.parser")  # Phân tích cú pháp HTML
#     return re.sub(r"\n\n+", "\n\n", soup.text).strip()  # Xóa khoảng trắng và dòng trống thừa
#
#
# def crawl_web(url_data):
#     """
#     Hàm crawl dữ liệu từ URL với chế độ đệ quy
#     Args:
#         url_data (str): URL gốc để bắt đầu crawl
#     Returns:
#         list: Danh sách các Document object, mỗi object chứa nội dung đã được chia nhỏ
#               và metadata tương ứng
#     """
#     # Tạo loader với độ sâu tối đa là 4 cấp
#     loader = RecursiveUrlLoader(url=url_data, extractor=bs4_extractor, max_depth=4)
#     docs = loader.load()  # Tải nội dung
#     print('length: ', len(docs))  # In số lượng tài liệu đã tải
#
#     # Chia nhỏ văn bản thành các đoạn 10000 ký tự, với 500 ký tự chồng lấp
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=500)
#     all_splits = text_splitter.split_documents(docs)
#     print('length_all_splits: ', len(all_splits))  # In số lượng đoạn văn bản sau khi chia
#     return all_splits


# def web_base_loader(url_data):
#     """
#     Hàm tải dữ liệu từ một URL đơn (không đệ quy)
#     Args:
#         url_data (str): URL cần tải dữ liệu
#     Returns:
#         list: Danh sách các Document object đã được chia nhỏ
#     """
#     loader = WebBaseLoader(url_data)  # Tạo loader cơ bản
#     docs = loader.load()  # Tải nội dung
#     print('length: ', len(docs))  # In số lượng tài liệu
#
#     # Chia nhỏ văn bản tương tự như trên
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=10, chunk_overlap=2)
#     all_splits = text_splitter.split_documents(docs)
#     print(f"all_splits {all_splits} \ndocs : {docs}")
#     return all_splits

#
# def save_data_locally(documents, filename, directory):
#     """
#     Lưu danh sách documents vào file JSON
#     Args:
#         documents (list): Danh sách các Document object cần lưu
#         filename (str): Tên file JSON (ví dụ: 'data.json')
#         directory (str): Đường dẫn thư mục lưu file
#     Returns:
#         None: Hàm không trả về giá trị, chỉ lưu file và in thông báo
#     """
#     # Tạo thư mục nếu chưa tồn tại
#     if not os.path.exists(directory):
#         os.makedirs(directory)
#
#     file_path = os.path.join(directory, filename)  # Tạo đường dẫn đầy đủ
#
#     # Chuyển đổi documents thành định dạng có thể serialize
#     data_to_save = [{'page_content': doc.page_content, 'metadata': doc.metadata} for doc in documents]
#     # Lưu vào file JSON
#     with open(file_path, 'w') as file:
#         json.dump(data_to_save, file, indent=4)
#     print(f'Data saved to {file_path}')  # In thông báo lưu thành công


def main():
    model = get_hf_llm()
    prompt = "Thủ đô của Pháp là ở đâu"
    prompt_2 = "Dân số của Việt Nam là bao nhiêu"
    genai_docs = "./data_source/generative_ai"
    genai_chain = build_rag_chain(model)
    # print(genai_chain(prompt))
    # print(genai_chain(prompt_2))
    # print(genai_chain("bệnh nhân bị đau lưng"))
    # print(genai_chain("vị trí đau ở  trên , thời gian đau tầm 5 phút , mức độ nhẹ , không có triệu chứng khác , không có tiền sử bênh trước đó"))
    # print(genai_chain("Tôi vừa cung cấp cho bạn những thông tin gì"))
    print(genai_chain("Thủ đô của Việt Nam ở đâu ?"))
    print(genai_chain("Dân số nước Pháp là bao nhiêu"))
    print(genai_chain("Tôi vừa hỏi bạn câu gì"))



# Kiểm tra nếu file được chạy trực tiếp
if __name__ == "__main__":
    main()
