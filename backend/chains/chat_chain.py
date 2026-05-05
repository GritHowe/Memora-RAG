from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv
from prompts.system_prompt import get_prompt

from memory.chat_memory import get_message_history

# 【新增：导入你的检索器】
from rag.retriever import get_retriever

load_dotenv()

# 存储 session 对应的消息历史
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = get_message_history()
    return store[session_id]


def create_chat_chain():
    llm = ChatOpenAI(
        model=os.getenv("LLM_MODEL_NAME", "qwen-plus"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        temperature=0.3
    )

    parser = StrOutputParser()

    # # 【修改：加入 {context} 知识库内容】
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", """
    #         你是一个专业、温柔、有礼貌的篮球公司AI客服助手。
    #         你的名字叫巴塔。
    #
    #         请务必根据下面的【知识库】回答用户问题：
    #         {context}
    #
    #         有聊天历史就结合历史正常对话，
    #         没有资料也可以正常闲聊、记住用户说过的内容。
    #         完全不知道再委婉说没找到相关信息。
    #     """),
    #     ("placeholder", "{chat_history}"),
    #     ("human", "{question}"),
    # ])
    prompt = get_prompt()

    chain = prompt | llm | parser

    return chain


def chat_with_memory(question: str, session_id: str) -> str:
    """带记忆 + RAG 知识库的聊天函数"""
    chain = create_chat_chain()
    history = get_session_history(session_id)

    # ========================
    # 【核心：RAG 知识库检索】
    # ========================
    retriever = get_retriever()
    docs = retriever.invoke(question)
    context = "\n".join([doc.page_content for doc in docs])

    result = chain.invoke({
        "chat_history": history.messages,
        "question": question,
        "context": context,  # 把检索结果传入
    })

    # 保存消息
    history.add_user_message(question)
    history.add_ai_message(result)

    return result