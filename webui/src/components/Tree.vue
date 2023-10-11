
<template>
  <section>
    <div class="container d-flex flex-column">
      <div v-for="node in this.sessionTree.flatten()" :key="node.identifier" class="d-inline-flex">
        <div v-for="n in node.level" :key="n" class="col-2"></div>
        <ChatMsg :answer="node.answer" :identifier="node.identifier" @sendMessage="sendMessageFromTreeLeaf" :loading="node.loading" class="col-5"/>
      </div>
    </div>
  </section>
</template>

<script>

class InteractionNode {
  constructor (answer, level, identifier, parentIdentifier) {
    this.answer = answer
    this.level = level
    this.identifier = identifier
    this.parentIdentifier = parentIdentifier

    this.loading = false
    this.question = ''
    this.children = []
  }

  addChild (answer, identifier) {
    const child = new InteractionNode(answer, this.level + 1, identifier, this.identifier)
    this.children.push(child)
    return child
  }

  flatten () {
    let res = []

    res.push(this)

    this.children.forEach(child => {
      res.push(...child.flatten())
    })
    return res
  }
};

class SessionTree {
  constructor () {
    this.nextIdentifier = 0
    this.root = new InteractionNode('Ask me stuff', 0, this.nextIdentifier++, -1)
    this.map = new Map() // identifier -> node... ok this is a bit silly
    this.map.set(this.root.identifier, this.root)
  }

  getHistory (leafIdentifer) {
    let messages = []
    for (let identifier = leafIdentifer; identifier !== -1;) {
      let node = this.map.get(identifier)
      messages.unshift({
        author: 'client',
        text: node.question
      })
      messages.unshift({
        author: 'server',
        text: node.answer
      })
      identifier = node.parentIdentifier
    }
    return messages
  }

  flatten () {
    return this.root.flatten()
  }

  getNode (identifier) {
    return this.map.get(identifier)
  }

  gotAnswer (nodeIdentifier, answer) {
    console.log('got answer ' + answer + ' for node ' + nodeIdentifier)
    const node = this.map.get(nodeIdentifier)
    let child = node.addChild(answer, this.nextIdentifier++)
    this.map.set(child.identifier, child)
  }
}

export default {
  name: 'Tree',
  data () {
    this.sessionTree = new SessionTree()

    /** mock
    this.sessionTree.gotAnswer(0, 'Answer A')
    this.sessionTree.gotAnswer(0, 'Answer B')
    this.sessionTree.gotAnswer(0, 'Answer C')
    this.sessionTree.gotAnswer(1, 'Answer D')
    this.sessionTree.gotAnswer(1, 'Answer E')
    this.sessionTree.gotAnswer(1, 'Answer F')
    this.sessionTree.gotAnswer(2, 'Answer G')
    */

    return {
      sessionTree: this.sessionTree,
      messageCounter: this.messageCounter
    }
  },
  methods: {
    sendMessageFromTreeLeaf (nodeIdentifier, message) {
      const url = '/api/chat/1/tree'
      const nodeEmitter = this.sessionTree.getNode(nodeIdentifier)

      console.log('Sending message ' + message + ' to ' + url)

      nodeEmitter.loading = true
      nodeEmitter.question = message

      this.$axios.post(url, {
        'question': message,
        'history': this.sessionTree.getHistory(nodeIdentifier)
      }).then(res => {
        res.data.answers.forEach(answer => {
          this.sessionTree.gotAnswer(nodeIdentifier, answer)
        })
        nodeEmitter.loading = false
      })
    }
  }
}
</script>
