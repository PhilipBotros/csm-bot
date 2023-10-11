
<template>
    <div class="card">
  <div class="card-body">
    <p class="card-text">{{ answer }}</p>
  </div>
  <div class="card-footer text-muted d-inline-flex">
    <div class="col-10">
        <input class="form-control form-control-sm"
          type="text"
          v-model="message"
          @keyup.enter="sendMessage"
          :disabled="loading"
        />
    </div>
    <div class="col">
      <button class="btn btn-primary btn-sm" @click="sendMessage" :disabled="loading">
        <div v-if="loading">
          <div class="spinner-border" role="status">
          </div>
      </div>
      <div v-else>
        Reply
      </div>
      </button>
    </div>

  </div>
</div>
</template>

<script>
export default {
  name: 'ChatMsg',

  props: {
    'answer': {
      type: String,
      default: 'How can I help you?'
    },
    'identifier': {
      type: Number,
      default: 1
    },
    'loading': {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      message: ''
    }
  },

  methods: {
    sendMessage () {
      if (this.message.length === 0) {
        return
      }

      this.$emit('sendMessage', this.identifier, this.message)
    }
  }
}
</script>
