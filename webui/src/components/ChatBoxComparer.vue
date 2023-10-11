<script>
export default {
  name: 'ChatBoxComparer',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      randomDatapoints: []
    }
  },
  methods: {
    updateChatbotContext (context) {
      this.randomDatapoints = context
    }
  }
}
</script>

<template>
  <div class="container">
    <div class="chat-boxes">
      <div>
        <h1>with context</h1>
        <ChatBox modelName="context" @contextReceived="updateChatbotContext"/>
      </div>
      <div>
        <h1>without context</h1>
        <ChatBox modelName="nocontext" />
      </div>
    </div>

    <div class="chatbot-context">
      <h1>Dataset</h1>
      <ul>
        <li v-for="(string, idx) in randomDatapoints" :key="idx">
          {{ string }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
}

.chat-boxes {
  flex: 1;
  margin-right: 20px;  /* Adjust as needed */
}

.chatbot-context {
  width: 40%;  /* Adjust width as needed */
  border: 1px solid #999;
  padding: 10px;
  border-radius: 4px;
}

.chatbot-context ul {
  padding: 0;
}

.chatbot-context li {
  margin-bottom: 1.5rem; /* adjust this value as needed */
}

</style>
