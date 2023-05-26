<template>
  <div id="app">
    <NavbarView/>
    <SidebarView/>
    <router-view/>
  </div>
</template>
<script>
import NavbarView from '@/components/NavbarView.vue'
import SidebarView from '@/components/SidebarView.vue'

export default {
  name: "App",
  components: {
    NavbarView,
    SidebarView
  }
}
</script>

<style lang="scss">
@import "~@/assets/scss/vendors/bootstrap-vue/index";
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

a.router-link-exact-active {
  color: #42b983;
}

* {
  scroll-behavior: smooth;
}
</style>