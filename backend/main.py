from fastapi import FastAPI
from pydantic import BaseModel
from chains.chat_chain import chat_with_memory
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    session_id: str


@app.post("/chat")
async def chat(req: ChatRequest):
    result = chat_with_memory(req.question, req.session_id)
    return {"answer": result}


if __name__ == "__main__":
    # # 测试多轮记忆
    # print("🔍 开始测试多轮记忆...")
    #
    # result1 = chat_with_memory("我叫周世豪，我喜欢打篮球，我在自学ai大模型应用开发", "test_memory")
    # print(f"✅ 第一轮回复: {result1}")
    #
    # result2 = chat_with_memory("我叫什么名字？我的爱好是什么？ 另外公司前台电话发一下！", "test_memory")
    # print(f"✅ 第二轮回复: {result2}")
    #
    # result3 = chat_with_memory("你总结一下前面的内容，然后得出我是怎么样的人。", "test_memory")
    # print(f"✅ 第三轮回复: {result3}")
    #
    # print("🔍 测试结束")

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )