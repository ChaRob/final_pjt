<template>
  <div class="RecommedResultTheater" style="padding-top: 75px;">
    <b-container>
      <h1 class="pt-4" style="color: white;">Box Office</h1>
      <b-carousel
        id="carousel-1"
        fade
        controls
        img-width="1024"
        img-height="768"
        style="box-shadow: 0px 0px 20px black; border: 5px solid white; border-radius: 15px;"
      >
        <b-carousel-slide v-for="(nowMovie, idx) in nowMovies" :key="idx"
        :img-src="poster(nowMovie.movie.backdrop_path)">
        <router-link :to="{name: 'detail', params: {'id': nowMovie.movie.id}}" style="text-decoration-line: none;">
          <div id="carousel-text">
            <b-row class="align-items-center justify-content-start px-4 py-2"><h2>{{nowMovie.movie.title}}</h2></b-row>
            <b-row class="align-items-center justify-content-start px-4" style="text-align: start; color: #ffc800;">{{nowMovie.movie.tagline}}</b-row>
            <b-row class="align-items-center justify-content-start px-4">순위 : {{nowMovie.rank}}위
               <span class="ml-1" v-if="nowMovie.rank_inten !== '0'" :style="{'color': isRank(nowMovie.rank_inten)}">({{nowMovie.rank_inten}})</span>
            </b-row>
            <b-row class="align-items-center justify-content-start px-4">개봉일 : {{nowMovie.open_dt}}</b-row>
            <b-row class="align-items-center justify-content-start px-4">총 관람객 수 : {{nowMovie.audiacc}}
              <span class="ml-1"> +{{nowMovie.audicnt}} (어제 관람객 수)</span>
            </b-row>
          </div>
        </router-link>
        </b-carousel-slide>
      </b-carousel>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'RecommedResultTheater',
  data() {
    return {
      nowMovies: [],
    }
  },
  components: {
  },
  methods: {
    poster(path){
      return this.$store.getters.getPosterPath + path
    },
    isRank(rank) {
      if(rank.includes('-')) {
        return 'red'
      }
      if(rank.includes('+')){
        return 'blue'
      }
      return 'white'
    }
  },
  created() {
    axios({
      method: "GET",
      url: "http://127.0.0.1:8000/movies/boxoffice/",
    })
    .then(response => {
      this.nowMovies = response.data
    })
    .catch(error => console.error(error))
  },
}
</script>
<style scoped>
.RecommedResultTheater {
  background-image: url('@/assets/home.png');
  background-color: rgb(0, 0, 0);
  background-repeat: no-repeat;
  background-size: cover;
  min-height: 100vh;
}

#carousel-text {
  height: 200px;
  color: white;
  z-index: 1;
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 35px;
  border: 1px solid white;
}
</style>