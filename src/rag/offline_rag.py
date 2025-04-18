import re
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.rag.utils import FallBackRetriever
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

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
    def __init__(self, llm):
        self.llm = llm
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",  # Khóa để truy xuất lịch sử trong prompt
            return_messages=True  # Trả về danh sách các tin nhắn (HumanMessage, AIMessage)
        )
        _prompt = self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. Use the following context and chat history to answer the question."),
            MessagesPlaceholder(variable_name="chat_history"),  # Chỗ để chèn lịch sử hội thoại
            ("human", "Context: {context}\n\nQuestion: {question}")
        ])
        self.prompt = _prompt
        self.str_parser = Str_OutputParser()
        self.fallback = FallBackRetriever()


    def get_chain(self, retriever):
        def retriever_with_fallback(question: str):
            initial_docs = retriever.get_relevant_documents(question)
            initial_context = self.format_docs(initial_docs)
            if not self.is_context_relevant(initial_context , question):
                print("Độ dài context không đủ hoặc câu hỏi không liên quan , chuyển sang truy vấn web")
                return self.format_docs(self.fallback.get_relevant_documents(question))
            else :
                return initial_context

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
        def chain_with_memory(input_question: str):
            response = rag_chain.invoke(input_question)
            # Lưu câu hỏi và câu trả lời vào memory
            self.memory.save_context({"input": input_question}, {"output": response})
            return response

        return chain_with_memory

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def is_context_relevant(self , context:str , question:str) -> bool :
        if not context.strip():
            return False
        question_words = set(question.lower().split())
        context_words = set(context.lower().split())
        common_words = question_words.intersection(context_words)
        return len(common_words) > 0