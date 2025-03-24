import os

genai_docs = "../data_source/generative_ai"
print(f"Checking data directory: {genai_docs}")
if not os.path.exists(genai_docs):
    raise FileNotFoundError(f"Data directory not found: {genai_docs}")

# Kiểm tra xem có file PDF nào trong thư mục không
pdf_files = [f for f in os.listdir(genai_docs) if f.endswith(".pdf")]
print(f"Found PDF files: {pdf_files}")

if not pdf_files:
    raise ValueError(f"No PDF files found in {genai_docs}")

