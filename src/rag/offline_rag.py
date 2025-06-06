import re
from langchain import hub
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.rag.utils import FallBackRetriever
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
import numpy as np
from deep_translator import GoogleTranslator
class Str_OutputParser(StrOutputParser):
    def __init__(self) -> None:
        super().__init__()

    def parse(self, text: str) -> str:
        return self.etract_answer(text)

    def etract_answer(self, text_response: str, pattern: str = r"Answer:\s*(.+)") -> str:
        match = re.search(pattern, text_response, re.DOTALL)
        if match:
            answer_text = match.group(1).strip()
            return answer_text
        else:
            return text_response


class Offline_RAG:
    def __init__(self, llm , memory=None):
        self.llm = llm
        self.memory = memory if memory is not None else ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        _prompt = ChatPromptTemplate.from_messages([
            ("system",
             "Bạn là một trợ lý ảo y khoa, chuyên hỗ trợ bác sĩ trong việc đưa ra chỉ định cận lâm sàng và quyết định lâm sàng. "
             "Dựa trên ngữ cảnh thông tin y học bên dưới và lịch sử hội thoại gần nhất, hãy trả lời rõ ràng , chỉ trả lời những câu liên quan đến y tế và đưa ra chỉ định lâm sàng"
             "Nếu không đủ thông tin, nếu đủ thông tin hãy xem xét câu hỏi đó có liên quan về y tế hoặc có liên quan đến việc giúp bác sĩ đưa chỉ định cận lâm sàng hay liên quan về y tế không rồi mới trả lời , hãy nói rõ và đề xuất các xét nghiệm cận lâm sàng cần thiết."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "Ngữ cảnh: {context}\n\nCâu hỏi: {question}")
        ])
        self.prompt = _prompt
        self.str_parser = Str_OutputParser()
        self.fallback = FallBackRetriever()
        if memory is None:
            self.memory.clear()

    def get_chain(self, retriever):

        def translateVnToEn(text) :
            translated = GoogleTranslator(source='vi', target='en').translate(text)
            return translated
        def retriever_with_fallback(question: str):
            initial_docs = retriever.get_relevant_documents(translateVnToEn(question))
            initial_context = self.format_docs(initial_docs)
            # if not self.is_context_relevant(initial_context, translateVnToEn(question)):
            #     print("Độ dài context không đủ hoặc câu hỏi không liên quan, chuyển sang truy vấn web")
            #     return self.format_docs(self.fallback.get_relevant_documents(question))
            # else:
            web_context = self.format_docs(self.fallback.get_relevant_documents(question))
            print(initial_context)
            return initial_context + web_context

        input_data = {
            "context": retriever_with_fallback,
            "question": RunnablePassthrough(),
            "chat_history": lambda x: self.memory.load_memory_variables({})["chat_history"]
        }
        rag_chain = (
                input_data
                | self.prompt
                | self.llm
                | self.str_parser
        )

        def modify_text_in_human_message(message: HumanMessage, new_text: str) -> HumanMessage:
            new_content = []
            for part in message.content:
                if part["type"] == "text":
                    new_content.append({"type": "text", "text": new_text})  # ✨ thay đổi nội dung tại đây
                else:
                    new_content.append(part)  # giữ nguyên phần image hoặc các phần khác
            return HumanMessage(content=new_content)

        def chain_with_memory(input_question):
            try:
                if isinstance(input_question, HumanMessage):
                    print("is HumanMessage")
                    question_text = self.extract_text_from_message(input_question)
                    # response_from_model = self.llm.invoke([input_question])
                    response = self.llm.invoke([input_question])
                    print(type(response))
                    modify_text_in_human_message(input_question , "")
                    response_text = rag_chain.invoke(
                        f"Tôi đã gửi 1 tấm ảnh cho bạn , và đây là mô tả về hình ảnh : {response.content} . Câu hỏi của tôi là {question_text}")
                elif isinstance(input_question, str):
                    print("is str")
                    question_text = input_question
                    response_text = rag_chain.invoke(question_text)
                else:
                    raise ValueError("Input must be str or HumanMessage")

                # Save chat history
                # print("Lịch sử trước:", self.memory.load_memory_variables({})["chat_history"])
                self.memory.save_context({"input": question_text}, {"output": response_text})
                # print("Lịch sử sau:", self.memory.load_memory_variables({})["chat_history"])

                return response_text
            except Exception as e:
                print(e)

        return chain_with_memory

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # def is_context_relevant(self, context: str, question: str, threshold: float = 0.7) -> bool:
    #
    #     if not context.strip():
    #         return False
    #
    #     try:
    #         question_vec = self.embedding_model.embed_query(question)
    #         context_chunks = context.split("\n\n")
    #         for chunk in context_chunks:
    #             chunk_vec = self.embedding_model.embed_query(chunk)
    #             similarity = self.cosine_similarity(question_vec, chunk_vec)
    #             print(f"Similarity with chunk: {similarity}")
    #             if similarity >= threshold:
    #                 return True
    #         return False
    #     except Exception as e:
    #         print(f"Lỗi khi tính similarity: {str(e)}")
    #         return False

    def cosine_similarity(self, vec1, vec2) -> float:
        a = np.array(vec1)
        b = np.array(vec2)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))



    def extract_text_from_message(self, message: HumanMessage) -> str:
        if isinstance(message, (HumanMessage, AIMessage)):
            if isinstance(message.content, str):
                return message.content
            elif isinstance(message.content, list):
                # Chỉ lấy các phần tử văn bản từ danh sách content
                text_parts = [
                    item["text"] for item in message.content
                    if isinstance(item, dict) and item.get("type") == "text"
                ]
                return " ".join(text_parts)
        return str(message)