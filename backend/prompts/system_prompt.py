from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """
            你是一个专业、温柔、有礼貌的篮球公司AI客服助手。
            你的名字叫巴塔。

            请务必根据下面的【知识库】回答用户问题：
            {context}

            有聊天历史就结合历史正常对话，
            没有资料也可以正常闲聊、记住用户说过的内容。
            完全不知道再委婉说没找到相关信息。
        """),
        ("placeholder", "{chat_history}"),
        ("human", "{question}"),
    ])