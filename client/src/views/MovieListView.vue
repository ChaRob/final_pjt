<template>
  <div id="MovieListView">
    <div></div>
    <b-container class="py-4">
      <h1>영화 목록</h1>
      <b-row>
        <b-col></b-col>
        <b-col>
          <b-pagination
            v-model="page"
            :total-rows="totalnum"
            per-page="12"
            align="center"
            pills
          ></b-pagination>
        </b-col>
        <b-col>
          <b-row>
            <b-col>
              <b-input v-model="input_page" @keyup.enter="inputPage" placeholder="페이지 입력"></b-input>
            </b-col>
            <b-col cols="3">
              <b-button @click="inputPage">이동</b-button>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
      <b-row>
        <b-col sm="auto" md="auto" lg="auto" v-for="(movie,idx) in movies" :key=idx>
          <MovieListItem
          :movie="movie"
          />
        </b-col>
      </b-row>
    </b-container>
    <MovieListSidebar
    @page-idx="pageGetFilter"
    />
  </div>
</template>

<script>
import MovieListItem from '@/components/MovieListItem.vue'
import MovieListSidebar from '@/components/MovieListSidebar.vue'
import axios from 'axios'

export default {
  name: "MovieListView",
  data() {
    return {
      movies: [],
      page: this.$store.state.topRatePage,
      input_page: null,
      urls: [
        'http://127.0.0.1:8000/movies/popular/',
        'http://127.0.0.1:8000/movies/top_rated/',
      ],
      filter_page: this.$store.state.filter,
      totalnum: 0,
    }
  },
  components: {
    MovieListItem,
    MovieListSidebar
  },
  methods:{
    LoadMovie(page) {
      axios({
        method: "GET",
        url: this.urls[this.filter_page] + page + "/",
      })
      .then(response => {
        this.movies = response.data.data
        this.totalnum = response.data.totalnum
      })
      .catch(error => console.error(error))
    },
    inputPage() {
      this.$store.dispatch('updatePage', this.input_page)
      this.LoadMovie(this.$store.state.topRatePage)
      this.page = this.input_page
      this.input_page = ''
    },
    pageGetFilter(filter){
      this.filter_page = filter
      this.page = 1
      const payload = {
        filter : this.filter_page,
        page : this.page
      }
      this.$store.dispatch('updatePage', payload)
      this.LoadMovie(this.page)
    }
  },
  watch: {
    page() {
      const payload = {
        filter : this.filter_page,
        page : this.page
      }
      this.$store.dispatch('updatePage', payload)
      this.LoadMovie(this.$store.state.topRatePage)
    }
  },
  created() {
    this.LoadMovie(this.$store.state.topRatePage)
    for (const id_value of this.$store.state.genres) {
      this.urls.push(`http://127.0.0.1:8000/movies/genre/${id_value.id}/`)
    }
  },
}
</script>
<style scoped>
#MovieListView {
  background-color: rgba(0, 0, 0, 0.2);
  min-height: 873px;
}
</style>