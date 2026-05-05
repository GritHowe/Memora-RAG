<template>
  <div class="app">
    <h1>AI 助手</h1>
    <ChatBox />
  </div>
</template>

<script setup>
import ChatBox from './components/ChatBox.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}
</style>