<template>
  <div class="chat-box">
    <div class="history" ref="historyRef">
      <div class="msg system">你好！我是AI助手，有什么可以帮你的？</div>

      <div v-for="(msg, i) in messages" :key="`msg-${i}`" :class="['msg', msg.role]">
        <!-- 关键改动：用 v-html 渲染 markdown -->
        <div class="message-content" v-html="renderMarkdown(msg.content)"></div>
      </div>

      <div v-if="loading" class="msg ai">AI 正在思考中...</div>
    </div>

    <div class="input-bar">
      <textarea
        v-model="inputText"
        placeholder="输入问题，按回车发送"
        @keyup.enter.exact.prevent="send"
        :disabled="loading"
      ></textarea>
      <button @click="send" :disabled="loading || !inputText.trim()">
        发送
      </button>
      <button @click="clearChat" :disabled="loading">清空对话</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
// import { chat } from '../api/chat'
// 只导入流式方法，删掉旧chat
import { chat } from '../api/chat'
import { marked } from 'marked'  // 引入解析库

const messages = ref([])
const inputText = ref('')
const loading = ref(false)
const historyRef = ref(null)

// 核心：把文本转成带排版的 HTML
const renderMarkdown = (text) => {
  return marked.parse(text || '')
}

const send = async () => {
  const text = inputText.value.trim();
  if (!text || loading.value) return;

  messages.value.push({ role: 'user', content: text });
  inputText.value = '';
  loading.value = true;

  try {
    const reply = await chat(text,"test123");
    // 根据后端统一响应格式取 data.data 或 res.data
    messages.value.push({ role: 'ai', content: reply || '回复为空'});
  } catch (err) {
    messages.value.push({ role: 'ai', content: '连接失败，请检查后端' });
  } finally {
    loading.value = false;
  }
};

watch(messages, async () => {
  await nextTick()
  if (historyRef.value) {
    historyRef.value.scrollTop = historyRef.value.scrollHeight
  }
}, { deep: true })

const clearChat = () => {
  messages.value = []
}
</script>

<style scoped>
.chat-box {
  height: 600px;
  display: flex;
  flex-direction: column;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.history {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background: #fafafa;
}

.msg {
  margin: 8px 0;
  padding: 10px 14px;
  border-radius: 8px;
  max-width: 75%;
  line-height: 1.6; /* 让排版更舒服 */
}

.msg.system {
  background: #e5e5e5;
  color: #666;
  margin: 0 auto 10px;
  max-width: 90%;
  text-align: center;
}

.msg.user {
  background: #0078ff;
  color: white;
  margin-left: auto;
}

.msg.ai {
  background: white;
  color: #333;
  margin-right: auto;
  border: 1px solid #eee;
}

.input-bar {
  display: flex;
  gap: 10px;
  padding: 10px;
  background: white;
}

textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: none;
  height: 50px;
}

button {
  padding: 0 20px;
  background: #0078ff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* 让 AI 回复里的列表、标题、加粗正常显示 */
:deep(.message-content) {
  word-break: break-word;
}
:deep(.message-content p) {
  margin: 0.4em 0;
}
:deep(.message-content ul),
:deep(.message-content ol) {
  padding-left: 1.4em;
  margin: 0.4em 0;
}
:deep(.message-content strong) {
  font-weight: bold;
}
:deep(.message-content h3) {
  font-size: 1.1em;
  font-weight: bold;
  margin: 0.6em 0 0.3em;
}
</style>n