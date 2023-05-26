<template>
  <div id="ReviewCreate">
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
    heigth="600" width="1800"
    ></b-img>
    <template #overlay>
      <b-container class="mt-4 border border-light pl-3 py-4 pr-5 text-white" id="CreateBoard">
        <h1 class="p-4 ml-5">'{{movie.title}}'에 리뷰쓰기</h1>
        <b-form @submit.prevent="createReview()">
          <b-form-group required>
            <b-row class="justify-content-center align-items-center">
              <b-col sm="2" style="padding-left: 50px; padding-top: 5px;">
                <label for="type-text">제목 : </label>
              </b-col>
              <b-col sm="10">
                <b-form-input id="type-text" v-model="review.title"></b-form-input>
              </b-col>
            </b-row>
          </b-form-group>
          <b-form-group>
            <b-row class="justify-content-center align-items-center mt-4">
              <b-col sm="2" style="padding-left: 50px; padding-top: 5px;">
                <label for="rating-10">평점 : {{review.rating}}점</label>
              </b-col>
              <b-col sm="10">
                <b-form-rating id="rating-10" v-model="review.rating" stars="10"></b-form-rating>
              </b-col>
            </b-row>
          </b-form-group>
          <b-form-group required>
            <b-row class="justify-content-center align-items-center mt-4">
              <b-col sm="2" style="padding-left: 50px; padding-top: 5px;">
                <label for="type-text">내용 : </label>
              </b-col>
              <b-col sm="10" style="height: 100px">
                <b-form-textarea id="type-text" rows="3" max-rows="3" v-model="review.content"></b-form-textarea>
              </b-col>
            </b-row>
          </b-form-group>
          <b-row class="pr-3" style="justify-content: flex-end;">
            <b-button type="submit" variant="primary">등록</b-button>
          </b-row>
        </b-form>
      </b-container>
    </template>
    </b-overlay>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "ReviewCreate",
  data() {
    return {
      movie: this.$store.state.movie,
      review: {
        title: '',
        content: '',
        rating: 0
      },
    }
  },
  methods: {
    createReview() {
      const inputReview = this.review
      const token = this.$store.state.User.token
      const id = this.movie.id

      if(inputReview.title === '') {
        alert('제목이 없습니다.')
      }
      else if(inputReview.rating === 0){
        alert('평점이 0점입니다.')
      }
      else if(inputReview.content === '') {
        alert('내용이 없습니다.')
      }
      else{
        axios({
          method: "POST",
          url: "http://127.0.0.1:8000/movies/review/" + id + "/create/",
          headers: {
            Authorization: `Token ${token}`
          },
          data: {
            'title': inputReview.title,
            'content': inputReview.content,
            'rating': inputReview.rating,
            'movie_id': this.movie.id,
            'user': this.$store.state.User.user.user_id,
            'like_users': []
          }
        })
        .then(() => {
          this.$router.push({name:"review", params: {'id':this.movie.id}})
        })
        .catch(error => console.error(error))

        this.review = { title:'', content: '', rating: null}
      }
    },
    poster(path){
      return this.$store.getters.getPosterPath + (path? path : '')
    },
  }
}
</script>

<style scoped>
#CreateBoard {
  border-radius: 15px;
  background-color: rgba(44, 44, 44, 0.473);
}
</style>