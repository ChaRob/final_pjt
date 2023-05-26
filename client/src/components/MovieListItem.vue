<template>
  <b-card id="MovieListItem">
    <b-card-img
    v-if="movie.poster_path"
    :src="poster(movie.poster_path)"
    height="400"
    class="cardimghover"
    @click.prevent="toDetail()"
    >
    </b-card-img>
    <div
    v-else
    >
    <b-card-img
    src="http://localhost:8080/img/no-image-icon-23492.ba6d4281.png"
    height="400"
    class="cardimghover"
    @click.prevent="toDetail()"
    >
    </b-card-img>
    {{movie.title}}
    </div>
    
  </b-card>
</template>

<script>
export default {
  name: "MovieListItem",
  props: {
    movie: Object
  },
  computed: {
    
  },
  methods: {
    poster(path){
      return this.$store.getters.getPosterPath + path
    },
    toDetail() {
      this.$router.push(
          {
            name: 'detail',
            params: {
              id: this.movie.id
            }
          }
        )
    },
  },
}
</script>

<style scoped>
#MovieListItem {
  width: 350px;
  height: 450px;
  margin-top: 20px;
}

.cardimghover {
  transition: all 0.5s;
  cursor: pointer;
}

.card-body {
  transition: all 0.5s;
  transition-delay: 0.3;
  box-shadow: 0px 0px 7px gray;
}

.card-body:hover {
  padding: 0px;
}

.cardimghover:hover {
  width: 345px;
  height: 450px;
}
</style>