<template>
    <section class="chat-box">
      <div class="chat-box-list-container" ref="chatbox">
        <ul class="chat-box-list">
          <li
            class="message"
            v-for="(message, idx) in messages"
            :key="idx"
            :class="message.author"
          >
            <p>
              <span>{{ message.text }}</span>
            </p>
          </li>
        </ul>
      </div>
      <div class="chat-inputs">
        <input
          type="text"
          v-model="message"
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage">Send</button>
      </div>
    </section>
  </template>

<script>

export default {
  name: 'ChatBox',
  props: {
    'modelName': String
  },
  created () {
    this.history = []
  },
  data: () => ({
    message: '',
    messages: [] // this is for rendering
  }),
  methods: {
    sendMessage () {
      const message = this.message

      const newQuestion = { text: message, author: 'client' }

      this.messages.push(newQuestion)
      this.message = ''

      const url = `/api/chat/1/${this.modelName}`

      this.$axios.post(url, {
        'question': message,
        'history': this.history
      }).then(res => {
        const newAnswer = { text: res.data.answers[0], author: 'server' }

        this.messages.push(newAnswer)
        this.history.push(newQuestion, newAnswer)

        this.$emit('contextReceived', res.data.context)
        this.$nextTick(() => {
          this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
        })
      })
    }
  }
}
</script>

<style scoped>

.chat-box, .chat-box-list {
  display: flex;
  flex-direction: column;
  list-style-type: none;
}

 .chat-box-list-container {
  overflow: scroll;
  margin-bottom: 1px;
}

.chat-box-list {
  padding-left: 10px;
  padding-right: 10px;
}
 .chat-box-list span {
  padding: 8px;
  color: white;
  border-radius: 4px;
}
 .chat-box-list .server span {
  background: #9c0;
}
 .chat-box-list .server p {
  float: right;
}
 .chat-box-list .client span {
  background: #0070c8;
}
 .chat-box-list .client p {
  float: left;
}
 .chat-box {
  margin: 10px;
  border: 1px solid #999;
  width: 50vw;
  height: 50vh;
  border-radius: 4px;
  margin-left: auto;
  margin-right: auto;
  align-items: space-between;
  justify-content: space-between;
}
 .chat-inputs {
  display: flex;
}
.chat-inputs input {
  line-height: 3;
  width: 100%;
  border: 1px solid #999;
  border-left: none;
  border-bottom: none;
  border-right: none;
  border-bottom-left-radius: 4px;
  padding-left: 15px;
}
.chat-inputs button {
  width: 145px;
  color: white;
  background: #0070c8;
  border-color: #999;
  border-bottom: none;
  border-right: none;
  border-bottom-right-radius: 3px;
}

</style>
