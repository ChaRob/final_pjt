<template>
  <div id="RecommendResult">
    <b-container class="py-4">
      <h1>추천 영화</h1>
      <div v-if="$store.state.recommend_movie.length > 0">
      <b-row>
        <b-col sm="auto" md="auto" lg="auto" v-for="(movie,idx) in $store.state.recommend_movie" :key="idx">
          <MovieListItem
          :movie="movie"
          />
        </b-col>
      </b-row>
      </div>
      <div v-else class="mt-4">
        <b-img src="../assets/reguysad.jpg">

        </b-img>
        <h2>추천 결과가 없습니다.</h2>
      </div>
    </b-container>
  </div>
</template>

<script>
import MovieListItem from '@/components/MovieListItem.vue'

export default {
  name: "RecommendResult",
  components: {
    MovieListItem
  },
  methods:{
    
  },
}
</script>
<style scoped>
#MovieListView {
  background-color: rgba(0, 0, 0, 0.2);
}
</style>