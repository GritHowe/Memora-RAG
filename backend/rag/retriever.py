from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from rag.splitter import get_splitter
from typing import List
import os
from dotenv import load_dotenv
import dashscope

load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")
embed_model = os.getenv("EMBED_MODEL", "text-embedding-v2")


class AliyunEmbeddings(Embeddings):
    """阿里云 DashScope 文本向量模型（企业标准封装）"""

    def _call_api(self, texts: List[str]) -> List[List[float]]:
        all_embeddings = []

        for text in texts:
            resp = dashscope.TextEmbedding.call(
                model=embed_model,
                input=[text],
                api_key=api_key
            )

            if resp.status_code != 200:
                raise Exception(f"向量生成失败：{resp.message}")

            embedding = resp.output["embeddings"][0]["embedding"]
            all_embeddings.append(embedding)

        return all_embeddings

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._call_api(texts)

    def embed_query(self, text: str) -> List[float]:
        return self._call_api([text])[0]


def get_retriever():
    embeddings = AliyunEmbeddings()

    if os.path.exists("./faiss_index"):
        vector_store = FAISS.load_local(
            "./faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        loader = TextLoader("./docs/knowledge.txt", encoding="utf-8")
        docs = loader.load()
        splits = get_splitter().split_documents(docs)
        vector_store = FAISS.from_documents(splits, embeddings)
        vector_store.save_local("./faiss_index")

    # 返回检索器
    return vector_store.as_retriever(search_kwargs={"k": 3})
