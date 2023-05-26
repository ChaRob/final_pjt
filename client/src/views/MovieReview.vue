<template>
  <div id="MovieReview" style="overflow: hidden;">
    <b-overlay
      overlay
      no-center
      show
      variant="transparent"
      blur="10px"
      opacity="0.9"
    >
    <b-img
    :src="poster(movie.backdrop_path)"
    heigth="600" width="3000"
    ></b-img>
    <template #overlay>
      <b-container class="mt-4 border border-light p-4" id="review-content">
        <b-row>
          <b-col>
            <h2 class="my-2 p-4 text-white">'{{movie.title}}'의 리뷰글</h2>
          </b-col>
          <div style="position: relative; top: 30px; right: 20px;">
            <b-button variant="primary" :to="{name: 'detail', params: {'id':movie.id}}">뒤로가기</b-button>
          </div>
        </b-row>
        <div v-if="reviews.length === 0">
          <h1 class="my-4 text-white">리뷰가 없습니다</h1>
        </div>
        <div v-else style="max-height: 1500px; overflow: auto; overflow-x: hidden;">
          <div class="mb-4" v-for="(review, idx) in reviews" :key="idx">
            <b-row>
              <b-col cols="2" class="pl-5 ml-5">
                <router-link :to="{name: 'profile', params: {'user_id':review.user.id}}">
                  <b-img v-if="review.user.profile_image" rounded="circle" :src="userImg(review.user.profile_image)"
                  width="100" height="100"
                  ></b-img>
                  <b-img v-else fluid rounded="circle" src="../assets/NoProfileImg.png"
                  width="100" height="100"
                  ></b-img>
                </router-link>
              </b-col>
              <b-col cols="8" class="text-white border rounded p-3">
                <b-row>
                  <b-col>
                    <router-link :to="{name: 'reviewdetail', params: {'review': review, 'movie':movie}}" style="color: white;">
                    <p style="text-align: start; font-size: 35px;">{{review.title}}</p>
                    </router-link>
                  </b-col>
                  <b-col cols="2" style="text-align: end; align-self: center; font-size: 25px;">
                    <b-icon-heart-fill style="color: red;"></b-icon-heart-fill> {{review.like_users.length}}명
                  </b-col>
                </b-row>
                <b-row>
                  <b-col>
                    <p style="text-align: start;">{{review.user.username}}</p>
                  </b-col>
                  <b-col>
                    <p style="text-align: end;">★{{review.rating}}</p>
                  </b-col>
                </b-row>
              </b-col>
            </b-row>
          </div>
        </div>
      </b-container>
      <SidebarViewVue/>
      <div id="ReviewCreateBtn">
        <b-button pill size="lg" variant="dark" style="color: white;"
        :to="{name: 'reviewcreate', params: {'id':movie.id}}">
        리뷰 쓰기</b-button>
      </div>
    </template>
    </b-overlay>
  </div>
</template>

<script>
import axios from 'axios'
import SidebarViewVue from '../components/SidebarView.vue'
import {BIconHeartFill} from 'bootstrap-vue'

export default {
  name: "MovieReview",
  components: {
    SidebarViewVue,
    BIconHeartFill,
  },
  data() {
    return {
      movie : this.$store.state.movie,
      reviews: [],
    }
  },
  methods: {
    poster(path){
      return this.$store.getters.getPosterPath + (path? path : '')
    },
    userImg(path) {
      return "http://127.0.0.1:8000/accounts" + path
    },
  },
  created() {
    axios({
      method: "GET",
      url: "http://127.0.0.1:8000/movies/review/" + this.movie.id
    })
    .then(response => {
      this.reviews = response.data
    })
    .catch(error => console.error(error))
  },
}
</script>

<style scoped>
#review-content {
  width: 100%;
  background-color: rgba( 0, 0, 0, 0.5 );
  border-radius: 10px;
}

#ReviewCreateBtn {
  position: fixed;
  bottom: 25px;
  left: 47.5%;
}
</style>