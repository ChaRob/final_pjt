<template>
  <div id="SearchView">
    <b-container class="py-4">
      <h1>검색 결과</h1>
      <div v-if="$store.state.search_movies.length > 0">
      <b-row>
        <b-col>
          <b-pagination
            v-model="page"
            :total-rows="$store.state.search_movies.length"
            per-page="18"
            align="center"
            pills
          ></b-pagination>
        </b-col>
      </b-row>
      <b-row>
        <b-col sm="auto" md="auto" lg="auto" v-for="(movie,idx) in $store.state.search_movies.slice((page-1)*18,page*18)" :key="idx">
          <MovieListItem
          :movie="movie"
          />
        </b-col>
      </b-row>
      </div>
      <div v-else class="mt-4">
        <h2>검색 결과가 없습니다.</h2>
      </div>
    </b-container>
  </div>
</template>

<script>
import MovieListItem from '@/components/MovieListItem.vue'

export default {
  name: "SearchView",
  data() {
    return {
      page: 1,
    }
  },
  components: {
    MovieListItem
  },
  methods:{
    
  },
}
</script>
<style scoped>
#SearchView {
  background-color: rgba(0, 0, 0, 0.2);
  min-height: 100vh;
}
</style>