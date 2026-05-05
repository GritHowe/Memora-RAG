// api/chat.js
import axios from 'axios'

export async function chat(question, sessionId) {
  const res = await axios.post('http://localhost:8000/chat', {question: question,session_id: sessionId });
  return res.data.answer;  // axios 自动解析 JSON
}