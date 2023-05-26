<template>
  <div id="NavbarView">
    <b-navbar type="dark" variant="dark">
      <b-navbar-brand tag="h1" class="pl-5">
        BMYL
      </b-navbar-brand>
      
      <b-navbar-nav>
        <b-nav-item :to="{name: 'home'}">Home</b-nav-item>
        <b-nav-item :to="{name: 'movies'}">Movies</b-nav-item>
        <b-nav-item :to="{name: 'recommend'}">Recommend</b-nav-item>
        <b-nav-item-dropdown text="User">
          <b-dropdown-item v-if="!getLoginState" :to="{name: 'signup'}">SignUp</b-dropdown-item>
          <b-dropdown-item v-if="!getLoginState" :to="{name: 'login'}">Login</b-dropdown-item>
          <b-dropdown-item v-if="getLoginState" @click="logout()">Logout</b-dropdown-item>
          <b-dropdown-item v-if="getLoginState" :to="{name: 'profile', params: {'user_id' : $store.state.User.user.user_id}}">Profile</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>

      <b-navbar-nav class="mr-auto ml-2" v-if="$store.state.User.user" style="color: rgba(255, 255, 255, 0.5); font-size: 18px; font-weight: bold;">
        Welcome, {{$store.state.User.user.username}}
      </b-navbar-nav>

      <b-nav-form class="ml-auto" @submit.prevent="searchMovie">
        <b-form-input class="mr-2" v-model="SearchMovieName" placeholder="Search" @keyup.enter="searchMovie"></b-form-input>
        <b-button type="submit">Search</b-button>
      </b-nav-form>
    </b-navbar>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "NavbarView",
  data() {
    return {
      SearchMovieName: ''
    }
  },
  computed: {
    getLoginState() {
      return this.$store.getters.getLoginState
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
    },
    searchMovie() {
      const keyword = this.SearchMovieName
      axios({
        method: "GET",
        url: `http://127.0.0.1:8000/movies/search/${keyword}/`,
      })
      .then(response => {
        this.$store.dispatch('setSearchData', response.data.search_results)
        this.$router.push({name: "search", params: {'search_movies': response.data.search_results}})
        // this.SearchMovieName = ''
      })
      .catch(error => {
        console.error(error)
        // this.SearchMovieName = ''
      })
    }
  },
}
</script>

<style>

</style>