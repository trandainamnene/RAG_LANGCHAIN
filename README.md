# 🏥 ỨNG DỤNG CHATBOT Y TẾ HỖ TRỢ CHUẨN ĐOÁN LÂM SÀNG  

**Một giải pháp RAG (Retrieval-Augmented Generation) kết hợp LangChain để hỗ trợ bác sĩ đưa ra chuẩn đoán dựa trên triệu chứng.**  

---

## 🌟 Tổng quan  
Ứng dụng này sử dụng mô hình **Gemini 1.5 Flash** và cơ sở dữ liệu **Milvus** để phân tích triệu chứng lâm sàng, truy xuất thông tin y khoa từ dữ liệu đã crawl, và đưa ra gợi ý chuẩn đoán cho bác sĩ.  

---

## 🛠 Công nghệ sử dụng  
| Thành phần       | Mô tả                                                         |  
|------------------|---------------------------------------------------------------|  
| **Backend**      | LangChain (RAG Pipeline)                                      |  
| **Vector DB**    | Milvus (lưu trữ và tìm kiếm embedding triệu chứng/bệnh án)    |  
| **LLM**         | Gemini 2.0 Flash (Google AI) để phân tích ngữ cảnh và trả lời |  
| **Dữ liệu**     | Crawl từ nguồn y tế đáng tin cậy (HTML → Text → Vector)       |  

---

## 📌 Tính năng chính  
✅ **Nhập triệu chứng lâm sàng** (text/voice)  
✅ **Truy xuất thông tin liên quan** từ cơ sở dữ liệu y khoa  
✅ **Gợi ý chuẩn đoán** dựa trên mô hình Gemini  
✅ **Hỗ trợ bác sĩ** ra quyết định nhanh và chính xác  

---

## 🚀 Cài đặt  
```bash
# Clone dự án
git clone https://github.com/your-repo/medical-chatbot.git

# Cài đặt dependencies
pip install -r requirements.txt

# Khởi chạy ứng dụng
streamlit run ui.py

## 👥 Thành viên dự án
- Trần Đại Nam 
- Huỳnh Thành Tựu