# Memora - AI 智能客服机器人

基于 FastAPI + LangChain + 通义千问 的多轮对话 AI 客服系统，支持知识库 RAG 检索。

## 技术栈

- 后端：Python FastAPI + LangChain
- 前端：Vue3 + Vite + axios
- 大模型：阿里云通义千问（DashScope）
- 向量库：FAISS
- 数据库：SQLite（开发中）

## 功能

- ✅ 多轮对话记忆
- ✅ RAG 知识库检索
- ✅ 角色设定与 Prompt 模板
- ✅ 前后端分离

## 快速启动

### 1. 克隆项目
git clone https://github.com/你的用户名/Memora.git
cd Memora

### 2. 安装后端依赖
pip install -r requirements.txt

### 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的阿里云 API Key

### 4. 准备知识库
# 编辑 docs/knowledge.txt，放入你的知识库内容

### 5. 启动后端
python main.py
# 后端运行在 http://localhost:8000

### 6. 启动前端
cd frontend
npm install
npm run dev
# 前端运行在 http://localhost:5173

## 项目结构

├── main.py              # FastAPI 入口
├── chains/              # LangChain 链逻辑
├── memory/              # 对话记忆管理
├── prompts/             # Prompt 模板
├── rag/                 # RAG 检索模块
├── docs/                # 知识库文件
├── frontend/            # Vue3 前端
└── requirements.txt     # 依赖清单

## 作者

周世豪 - 2026