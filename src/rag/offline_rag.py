import re
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # Xử lý prompt


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
        en_prompt = hub.pull("rlm/rag-prompt")
        self.prompt = en_prompt
        self.str_parser = Str_OutputParser()

    def get_chain(self, retriever):
        input_data = {
            "context": retriever | self.format_docs,
            "question": RunnablePassthrough()
        }
        rag_chain = (
                input_data
                | self.prompt
                | self.llm
                | self.str_parser
        )
        return rag_chain

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
