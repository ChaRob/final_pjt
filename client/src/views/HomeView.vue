<template>
  <div class="HomeView" style="">
    <b-carousel
      id="carousel-1"
      fade
      :interval="3000"
      no-hover-pause
      img-width="1024"
      img-height="768"
      style="box-shadow: 0px 0px 20px black; width: 100%; opacity: 0.6;"
      class="m-0"
    >
      <b-carousel-slide v-for="(randomMovie, idx) in randomMovies" :key="idx"
      :img-src="poster(randomMovie.backdrop_path)">
      </b-carousel-slide>
    </b-carousel>
    <div id="mainPage">
      <b-img src="../assets/mysteryBox.png" height="300"></b-img>
      <b-form class="mx-4" @submit.prevent="searchMovie">
        <b-form-input class="mr-2" v-model="searchQuery" placeholder="Search" @keyup.enter="searchMovie"></b-form-input>
        <b-button type="submit">Search</b-button>
      </b-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'HomeView',
  data() {
    return {
      randomMovies: [],
      searchQuery: '',
    }
  },
  components: {
  },
  methods: {
    poster(path){
      return this.$store.getters.getPosterPath + path
    },
    searchMovie() {
      const keyword = this.searchQuery
      axios({
        method: "GET",
        url: `http://127.0.0.1:8000/movies/search/${keyword}/`,
      })
      .then(response => {
        this.$store.dispatch('setSearchData', response.data.search_results)
        this.$router.push({name: "search", params: {'search_movies': response.data.search_results}})
      })
      .catch(error => {
        console.error(error)
      })
    },
  },
  mounted() {
    axios({
      method: "GET",
      url: "http://127.0.0.1:8000/movies/home/",
    })
    .then(response => {
      this.randomMovies = response.data
    })
    .catch(error => console.error(error))
  },
}
</script>
<style scoped>
.HomeView {
  background-color: rgb(0, 0, 0);
  background-repeat: no-repeat;
  background-size: cover;
  min-height: 100vh;
}

#mainPage {
  min-width: 500px;
  min-height: 450px;
  position: absolute;
  top: 20rem;
  left: 50%;
  transform: translate(-50%,0);
  font-size: 50px;
  color: white;
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid white;
  border-radius: 35px;
}
</style>