<template>
  <div id="MovieDetailView" style="overflow-x: hidden">
    <b-overlay
      overlay
      no-center
      show
      variant="transparent"
      blur="10px"
      opacity="0.9"
    >
    <b-img
    v-if="movie.backdrop_path"
    :src="poster(movie.backdrop_path)"
    heigth="600" width="3100"
    ></b-img>
    <b-img
    v-else
    src="http://localhost:8080/img/no-image-icon-23492.ba6d4281.png"
    heigth="600" width="1800"
    >
    </b-img>
    <template #overlay>
      <b-spinner v-if="!movie" label="Spinning" style="position: absolute; left: 50%"></b-spinner>
      <b-container class="mt-4 border border-light" id="movie-content">
        <b-row no-gutters class="overflow-hidden text-white p-5">
          <b-col class="p-3">
            <b-img
            v-if="movie.poster_path"
            :src="poster(movie.poster_path)"
            heigth="600" width="400"
            style="border-radius: 5px;"
            ></b-img>
            <b-img
            v-else
            src="http://localhost:8080/img/no-image-icon-23492.ba6d4281.png"
            heigth="600" width="400"
            style="border-radius: 5px;"
            ></b-img>
          </b-col>
          <b-col class="p-3">
            <b-row>
              <b-col class="mb-2 pl-2" style="font-size: 40px;">
                {{titleText()}}
              </b-col>
            </b-row>
            <b-row class="justify-content-start">
              <b-col cols="3">
                ● {{movie.release_date}}
              </b-col>
              <b-col>
                ● {{getGenreList()}}
              </b-col>
            </b-row>
            <b-row class="mb-2">
              <b-col cols="3">
                ● {{movie.runtime}}분
              </b-col>
              <b-col>
                ● 평점 : {{movie.vote_average}}
              </b-col>
            </b-row>
            <b-row class="my-4">
              <b-col>
                <a :href="googlePlayPath(movie.title)" style="color: white;">
                <b-img
                src="@/assets/png-transparent-google-play-icon-logo-favicon.png"
                width="60" height="60"></b-img>
                영화 구매하기
                </a>
              </b-col>
              <b-col>
                <router-link :to="{name: 'review'}" style="color: white;">
                <b-img src="@/assets/review.png" width="60" height="60">  
                </b-img>
                리뷰 보기
                </router-link>
              </b-col>
            </b-row>
            <b-row>
              <b-col class="mb-4 text-warning" style="font-size: 19px;">
                {{movie.tagline}}
              </b-col>
            </b-row>
            <b-row>
              <b-col style="overflow: auto; overflow-x: hidden; max-height: 380px">{{ movie.overview }}</b-col>
            </b-row>
          </b-col>
        </b-row>
      </b-container>
      <b-container class="mt-4 p-3 border border-light text-white" id="movie-content">
        <b-tabs content-class="mt-3" v-model="tabIndex" fill>
          <b-tab title="배우" :title-link-class="linkClass(0)" active>
            <b-row id="actors">
              <b-col class="p-4" cols="3" v-for="(actor, idx) in movie.cast" :key="idx">
                <b-img v-if="actor.profile_path" :src="profilePath(actor.profile_path)"  width="236" height="300"></b-img>
                <b-img v-else src="../assets/NoProfileImg.png"  width="236" height="300"></b-img>
                <p class="text-center my-1" style="font-size: 24px;">{{actor.name}}</p>
                <p class="text-center my-1" style="font-size: 20px;">{{actor.character}}</p>
                <p class="text-center my-1" style="font-size: 15px;">{{actor.department}}</p>
              </b-col>
            </b-row>
          </b-tab>
          
          <b-tab title="트레일러" :title-link-class="linkClass(1)" class="mb-4 pb-5">
            <b-img v-if="$store.state.movie.video.length === 0" src="@/assets/no-image-icon-23492.png"
            rounded fluid center
            class="mx-3 ml-4"></b-img>
            <p v-if="$store.state.movie.video.length === 0" class="text-center">No Trailer</p>
            <div v-else>
              <b-embed
                type="iframe"
                aspect="16by9"
                :src="videoPath(currentPage-1)"
                allwofullscreen
              >
              </b-embed>
              <b-pagination
              v-model="currentPage"
              :total-rows="$store.state.movie.video.length"
              per-page="1"
              align="center"
              first-number
              last-number
              class="mt-4"
              ></b-pagination>
            </div>
          </b-tab>
          
          <b-tab title="배급사" :title-link-class="linkClass(2)">
            <b-row style="overflow: auto; max-height: 800px;">
              <b-col cols="4" v-for="(companie, idx) in movie.production_companies" :key="idx"
              style="display: flex; justify-content: center;flex-wrap: wrap; align-items: flex-end;"
              >
                <b-img v-if="companie.logo_path"
                :src="logoPath(companie.logo_path)"
                rounded thumbnail center
                class="mx-3 ml-4 bg-light"></b-img>
                <b-img v-else src="@/assets/no-image-icon-23492.png"
                rounded fluid center
                class="mx-3 ml-4"></b-img>
                <p class="text-center" style="font-size: 32px">{{companie.name}}</p>
              </b-col>
            </b-row>
          </b-tab>
          
          <b-tab title="추천" :title-link-class="linkClass(3)" style="overflow: auto; overflow-x: hidden; max-height: 800px;">
            <div class="text-center">
              <b-dropdown id="dropdown-1" text="영화 보기" class="m-md-2">
                <b-dropdown-item @click="recommendPage(0)">추천 영화</b-dropdown-item>
                <b-dropdown-item @click="recommendPage(1)">비슷한 영화</b-dropdown-item>
              </b-dropdown>
            </div>
            <b-row v-show="movie_recommed_page===0">
              <b-col>
                <p class="text-center text-warning" style="font-size: 30px">추천 영화</p>
              </b-col>
            </b-row>
            <b-row v-show="movie_recommed_page===1">
              <b-col>
                <p class="text-center text-warning" style="font-size: 30px">비슷한 영화</p>
              </b-col>
            </b-row>
            <b-row v-show="movie_recommed_page===0">
              <b-col cols="4" v-for="(recommend_movie, idx) in movie.recommendation" :key="idx"
              style="display: flex; justify-content: center;flex-wrap: wrap; align-items: center; flex-direction: column;">
                <a href="#NavbarView">
                <b-img :src="poster(recommend_movie.poster_path)"
                rounded center thumbnail width="150" height="200" @click="requestMovieData(recommend_movie.id)" style="cursor: pointer;"
                ></b-img>
                </a>
                <p class="text-center">{{recommend_movie.title}}</p>
              </b-col>
            </b-row>
            <b-row v-show="movie_recommed_page===1">
              <b-col cols="4" v-for="(similar_movie, idx) in movie.similar" :key="idx"
              style="display: flex; justify-content: center; flex-wrap: wrap; align-items: center; flex-direction: column;">
                <a href="#NavbarView">
                <b-img :src="poster(similar_movie.poster_path)"
                rounded center thumbnail width="150" height="200" @click="requestMovieData(similar_movie.id)" style="cursor: pointer;"
                ></b-img>
                </a>
                <p class="text-center">{{similar_movie.title}}</p>
              </b-col>
            </b-row>
          </b-tab>
        </b-tabs>
      </b-container>
    </template>
    </b-overlay>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "MovieDetailView",
  components: {
  },
  data() {
    return {
      id: this.$route.params.id,
      movie: {},
      tabIndex: 0,
      currentPage: 1,
      movie_recommed_page: 0,
    }
  },
  computed: {
    getScrollHeight() {
      return document.documentElement.scrollHeight
    }
  },
  methods: {
    requestMovieData(id) {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/movies/detail/" + id + "/",
      })
      .then(response => {
        this.movie = response.data
        this.$store.dispatch('Detail_Movie', this.movie)
      })
      .catch(error => console.error(error))
    },
    poster(path){
      return this.$store.getters.getPosterPath + path
    },
    titleText() {
      return this.movie.title + ' (' + this.movie.release_date?.slice(0,4) + ')'
    },
    getGenreList() {
      let textline = ''
      const GenreList = this.movie.genres || []
      for(const genre of GenreList){
        textline += genre.name + " "
      }
      return textline
    },
    linkClass(idx) {
      if (this.tabIndex === idx) {
        return ['bg-white', 'text-info']
      } else {
        return ['bg-transparent', 'text-warning']
      }
    },
    profilePath(path) {
      return "https://www.themoviedb.org/t/p/w300_and_h450_bestv2" + path
    },
    videoPath(idx){
      return 'https://www.youtube.com/embed/' + this.movie.video[idx].key
    },
    logoPath(path){
      return 'https://image.tmdb.org/t/p/original/' + path
    },
    googlePlayPath(path) {
      return `https://play.google.com/store/search?q=${path}&c=movies&hl=ko`
    },
    recommendPage(page) {
      this.movie_recommed_page = page
    }
  },
  created() {
    if(this.$route.params.id) {
      this.id = this.$route.params.id
      localStorage.setItem('id', this.id)
    }
    const id = localStorage.getItem('id')
    this.requestMovieData(id)
  }
}
</script>

<style scoped>
#MovieDetailView {
  text-align: left;
  box-shadow: 0px 0px 10px black;
}

#movie-content {
  width: 100%;
  background-color: rgba( 0, 0, 0, 0.5 );
  border-radius: 10px;
}

#actors {
  max-height: 800px;
  overflow: auto;
}

.customPagination > li {
  color: red;
}

.customPagination > li.active,
.customPagination > li:hover
{
  color: white;
  background-color: green!important;
}
</style>