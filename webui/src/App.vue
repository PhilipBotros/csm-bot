<template>
  <div id="app">

    <!-- Navbar-->
<nav class="navbar navbar-expand-lg navbar-light bg-primary" data-bs-theme="dark">
  <div class="container-fluid justify-content-between">
    <!-- Left elements -->
    <div class="d-flex">
      <!-- Brand -->
      <a class="navbar-brand me-2 mb-1 d-flex align-items-center" href="#">
        <img
        src="./assets/logo-glass.svg"
        height="80"
        alt="glass"
        loading="lazy"/>
      </a>
    </div>
    <!-- Left elements -->

    <!-- Center elements -->
    <ul class="navbar-nav flex-row d-none d-md-flex">
      <li class="nav-item me-auto active">
        <a class="nav-link" href="#">
          New Tree
        </a>
      </li>
      <li class="nav-item me-auto active">
        <a class="nav-link" href="#">
          Most Popular
        </a>
      </li>
    </ul>
    <!-- Center elements -->

    <!-- Right elements -->
      <nav class="navbar navbar-expand-lg navbar-light bg-primary">
        <div class="container-fluid justify-content-between">
          <div class="d-flex">
            <a class="nav-link" href="#">
              <span><i class="bi-person"></i></span>
            </a>
          </div>
        </div>
      </nav>
    <!-- Right elements -->
  </div>
</nav>

    <!-- <img src="./assets/logo.png"> -->
    <section class="p-5">
    <router-view/>
    </section>

    <!-- Footer -->
<footer class="text-center text-lg-start bg-primary text-muted" data-bs-theme="dark">
  <div class="text-center p-4">
    I have {{ contextSize }} messages in my current context
  </div>
</footer>
<!-- Footer -->

  </div>
</template>

<script>
export default {
  name: 'App',

  data () {
    return {
      contextSize: 0
    }
  },
  methods: {
    getContextSize () {
      const path = `/api/context_size`
      this.$axios.get(path).then(response => {
        this.contextSize = response.data.contextSize
      }).catch(error => {
        console.log(error)
      })
    }
  },
  created () {
    this.getContextSize()
  }
}
</script>
