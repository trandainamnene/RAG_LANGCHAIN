from typing import List, Any, Optional
from langchain.schema.retriever import BaseRetriever
from langchain.schema import Document
from langchain.retrievers.web_research import WebResearchRetriever
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.output_parsers import StrOutputParser

from src.base.llm_model import get_hf_llm
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
import numpy as np
load_dotenv()


class FallBackRetriever(BaseRetriever):
    """
    Lớp retriever chỉ sử dụng web retriever để tìm kiếm thông tin.
    """
    # Cài đặt google_search_api_key và google_cse_id trong env
    google_api_key: Optional[str] = os.getenv("GOOGLE_SEARCH_API_KEY")
    google_cse_id: Optional[str] = os.getenv("GOOGLE_SEARCH_CSE_ID")
    def __init__(self,
                 *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._web_retriever = None
        # Thông tin của search engine

    @property
    def web_retriever(self) -> BaseRetriever:
        """
        Khởi tạo web retriever theo kiểu lazy loading
        """
        if not self._web_retriever:
            try:
                self._web_retriever = self._create_web_retriever()
            except Exception as e:
                print(f"Lỗi khi khởi tạo web retriever: {str(e)}")
                return None
        return self._web_retriever

    def _create_search_engine(self):
        """
        Tạo search engine
        """
        return GoogleSearchAPIWrapper(
            google_api_key=self.google_api_key,
            google_cse_id=self.google_cse_id
        )

    def _create_web_retriever(self) -> BaseRetriever:
        """
        Tạo và trả về một retriever tìm kiếm thông tin trên web.
        """
        # Khởi tạo search engine
        search = self._create_search_engine()
        if not search:
            return None

        # Tạo vectorstore tạm thời
        vectorstore = self._create_temporary_vectorstore()
        if not vectorstore:
            return None

        # Lấy LLM
        llm = get_hf_llm()
        if not llm:
            return None

        # Tạo WebResearchRetriever
        web_retriever = WebResearchRetriever.from_llm(
            vectorstore=vectorstore,
            search=search,
            llm=llm, allow_dangerous_requests=True
            , num_search_results=3
        )
        return web_retriever

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> list[Document]:
        """
        Tìm kiếm thông tin chỉ từ web và lọc những document liên quan đến query.
        """
        print("Tìm kiếm từ web.")
        try:
            embedding_model = HuggingFaceEmbeddings()
            web_results = self.web_retriever.get_relevant_documents(query)
            if not web_results:
                # print("Không tìm thấy kết quả web.")
                return []

            # Tính vector truy vấn
            query_vec = embedding_model.embed_query(query)

            # Lọc kết quả theo độ tương đồng
            filtered_results = []
            for doc in web_results:
                doc_vec = embedding_model.embed_query(doc.page_content)
                similarity = self.cosine_similarity(query_vec, doc_vec)
                # print(f"Similarity with doc: {similarity}")
                if similarity >= 0.85:  # threshold có thể điều chỉnh
                    filtered_results.append(doc)

            if not filtered_results:
                print("Không có context đủ liên quan sau khi lọc.")
            return filtered_results

        except Exception as e:
            # print(f"Lỗi khi tìm kiếm web: {str(e)}")
            return []

    def cosine_similarity(self, vec1, vec2) -> float:
        a = np.array(vec1)
        b = np.array(vec2)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    @staticmethod
    def _create_temporary_vectorstore():
        """
        Tạo một vectorstore tạm thời để lưu trữ kết quả tìm kiếm web.
        Sử dụng HuggingFace embeddings.
        """
        try:
            embeddings = HuggingFaceEmbeddings()
        except Exception as e:
            print(f"Lỗi khi khởi tạo HuggingFace embeddings: {str(e)}")
            # Fallback đến mô hình nhẹ hơn nếu có lỗi
            embeddings = HuggingFaceEmbeddings()

        # Khởi tạo FAISS vectorstore trống
        vectorstore = FAISS.from_texts(
            texts=["Temporary initialization text"],
            embedding=embeddings
        )
        return vectorstore

class Summarize :
    def __init__(self , llm):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(
            "Tóm tắt câu hỏi này thành một đoạn ngắn gọn, rõ ràng:\n\n{question}"
        )
    def get_sumary_chain(self):
        summary_chain = self.prompt | self.llm | StrOutputParser()
        return summary_chain




if __name__ == "__main__":
    # Tạo đối tượng FallBackRetriever
    retriever = FallBackRetriever()
    # Query truy vấn trên web
    QUERY_STRING = "Dân số của Pháp"
    documents = retriever.get_relevant_documents(QUERY_STRING)
    print(documents)
