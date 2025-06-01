import pyodbc
from langchain_core.messages import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
def get_db_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=ChatBot;"
        "UID=sa;"
        "PWD=123;"
    )

def load_memory_from_db(conversation_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Question
        WHERE idHistory = ?
    """, conversation_id)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    messages = []
    for row in cursor.fetchall():
        print(row.questiontext)
        print(row.responsetext)
        memory.save_context(
            {"input": f"{row.questiontext}"},
            {"output": f"{row.responsetext}"}
        )
    return memory