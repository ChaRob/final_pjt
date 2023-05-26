<template>
  <div id="MovieReviewDetail" style="overflow-x: hidden">
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
                <p style="text-align: start; font-size: 35px;">{{review.title}}</p>
              </b-col>
              <b-col cols="1" style="text-align: end; align-self: center; color: red; font-size: 25px;">
                <b-icon-heart-fill v-if="review.like_users.includes(userid)" @click="reviewLike(false)"></b-icon-heart-fill>
                <b-icon-heart v-else @click="reviewLike(true)"></b-icon-heart>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <p style="text-align: start;">작성자 - {{review.user.username}}</p>
              </b-col>
              <b-col>
                <p style="text-align: end;">★{{review.rating}}</p>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <p style="text-align: start;">{{review.content}}</p>
              </b-col>
            </b-row>
            <b-row style="align-items: center;">
              <b-col cols="6" style="display: flex;">
                작성시간 : {{review.created_at.slice(0,10)}} {{review.created_at.slice(11,19)}}
              </b-col>
            </b-row>
            <b-row>
              <b-col cols="6" style="display: flex;">
                수정시간 : {{review.updated_at.slice(0,10)}} {{review.updated_at.slice(11,19)}}
              </b-col>
            </b-row>
            <b-row>
              <b-col style="display: flex; justify-content: flex-end;">
                <div v-if="review.user.id === userid" style="text-align: end;">
                  <b-button variant="warning" @click="updateReview">수정</b-button>
                  <b-button variant="danger" @click="deleteReview">삭제</b-button>
                </div>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <div class="text-white">
          <b-row>
            <b-col cols="1" class="px-5 mx-5"></b-col>
            <b-col cols="8" class="mt-4 p-2 border" style="text-align: left; margin-left: 42px;">
              <b-form v-if="$store.state.User.token" @submit.prevent="createComment">
                <b-form-group id="Content-Input" label="댓글" label-for="Content" style="font-size: 30px;">
                  <b-form-input
                    id="Content"
                    v-model="content"
                    placeholder="내용을 입력하세요"
                    required
                  ></b-form-input>
                </b-form-group>

                <div style="text-align: right;">
                  <b-button id="submitBtn" type="submit" variant="success" class="mr-2 mt-2">제출</b-button>
                </div>
              </b-form>
              <div v-else class="text-white p-4" style="font-size: 20px">
                <p>댓글을 작성하려면 로그인하세요.</p>
                <router-link :to="{name: 'login'}" style="color: white;">로그인하러가기</router-link>
              </div>
            </b-col>
          </b-row>
        </div>
        <div style="overflow: auto; overflow-x: hidden;">
          <b-row :id="commentid(comment.id)" class="text-white mt-4 p-4" v-for="(comment, idx) in comments" :key="idx">
            <b-col cols="2" class="ml-4 pl-4">
              <!-- 이미지 넣을 것. -->
              <b-row class="px-3 mt-2" style="justify-content: end; align-items: center;">
                <router-link :to="{name: 'profile', params: {'user_id':comment.user.id}}">
                <b-img v-if="comment.user.profile_image" :src="userImg(comment.user.profile_image)" width="50" height="50" rounded="circle"></b-img>
                <b-img v-else src="../assets/NoProfileImg.png" width="50" height="50" rounded="circle"></b-img>
                </router-link>
              </b-row>
            </b-col>
            <b-col cols="9">
                <!-- 작성된 댓글 내용 -->
              <b-row style="justify-content: flex-start;" class="border border-1 rounded p-2 pt-3">
                <b-col>
                  <p style="align-self: center; font-size: 20px; text-align: start;">{{comment.content}} - {{comment.user.username}}</p>
                </b-col>
                <b-col cols="3">
                  <div v-if="comment.user.id === userid" style="text-align: end;">
                    <b-button variant="warning" @click="updateModalOpen(idx)">수정</b-button>
                    <b-button variant="danger" @click="deleteComment(comment.id)">삭제</b-button>
                  </div>
                </b-col>
              </b-row>
            </b-col>
          </b-row>
        </div>
      </b-container>
      <b-modal ref="comment_update" hide-footer title="댓글 수정">
        <b-form @submit.prevent="updateComment">
          <b-form-input v-model="update_content">
          </b-form-input>
          <b-button class="mt-3" variant="warning" type="submit">수정</b-button>
          <b-button class="mt-3 mx-2" @click="closeModal">닫기</b-button>
        </b-form>
      </b-modal>
      <SidebarViewVue/>
    </template>
    </b-overlay>
  </div>
</template>

<script>
import axios from "axios"
import {BIconHeart, BIconHeartFill} from 'bootstrap-vue'
import SidebarViewVue from '../components/SidebarView.vue'

export default {
  name: "MovieReviewDetail",
  components: {
    BIconHeart,
    BIconHeartFill,
    SidebarViewVue,
  },
  data() {
    return {
      movie: null,
      review: null,
      content: null,
      comments: [],
      userid: null,
      update_content: null,
      update_id: null,
    }
  },
  methods: {
    poster(path){
      return this.$store.getters.getPosterPath + (path? path : '')
    },
    loadComment() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/movies/comment/" + this.review.id + "/"
      })
      .then(response => {
        this.comments = response.data
      })
      .catch(error => console.error(error))
    },
    createComment() {
      const token = this.$store.state.User.token
      axios({
        method: "POST",
        url: "http://127.0.0.1:8000/movies/comment/" + this.review.id + "/create/",
        headers: {
          Authorization : `Token ${token}`
        },
        data: {
          'content' : this.content,
          'review': this.review.id,
          'user': this.userid,
        }
      })
      .then(response => {
        this.comments.push(response.data)
        this.content = ''
      })
      .catch(error => console.error(error))
    },
    deleteComment(idx) {
      const token = this.$store.state.User.token
      const D_comment = document.querySelector(`#comment-${idx}`)
      axios({
        method: "DELETE",
        url: "http://127.0.0.1:8000/movies/comment/update/" + idx,
        headers: {
          Authorization : `Token ${token}`
        }
      })
      .then(() => {
        D_comment.remove()
      })
      .catch(error => console.error(error))
    },
    updateModalOpen(idx) {
      this.update_content = this.comments[idx].content
      this.update_id = this.comments[idx].id
      this.$refs['comment_update'].show()
    },
    closeModal() {
      this.$refs['comment_update'].hide()
    },
    updateComment() {
      const token = this.$store.state.User.token
      axios({
        method: "PUT",
        url: "http://127.0.0.1:8000/movies/comment/update/" + this.update_id + "/",
        headers: {
          Authorization : `Token ${token}`
        },
        data: {
          'content' : this.update_content,
          'review': this.review.id,
          'user': this.userid,
        }
      })
      .then(() => {
        for (const comment of this.comments) {
          if(comment.id === this.update_id) {
            comment.content = this.update_content
            break
          }
        }
      })
      .catch(error => console.error(error))
      this.closeModal()
    },
    deleteReview(){
      const token = this.$store.state.User.token
      axios({
        method: "DELETE",
        url: "http://127.0.0.1:8000/movies/review/detail/" + this.review.id,
        headers: {
          Authorization : `Token ${token}`
        }
      })
      .then(() => {
        this.$router.go(-1)
      })
      .catch(error => console.error(error))
    },
    commentid(idx) {
      return "comment-"+idx
    },
    updateReview(){
      this.$router.push({name: "updatereview", params: {'review' : this.review}})
    },
    reviewLike(Method) {
      const token = this.$store.state.User.token
      if(token === null){
        this.$router.push({name: "login"})
      }
      else{
        // method가 true면 좋아요 추가, false면 좋아요 취소
        axios({
          method: "POST",
          url: "http://127.0.0.1:8000/movies/review/detail/" + this.review.id + "/like/",
          headers: {
            Authorization : `Token ${token}`
          }
        })
        .then(() => {
          if(Method){
            this.review.like_users.push(this.userid)
          }
          else{
            this.review.like_users.splice(this.review.like_users.indexOf(this.userid), 1)
          }
        })
        .catch(error => console.error(error)) 
      }
    },
    userImg(path) {
      return "http://127.0.0.1:8000/accounts" + path
    },
  },
  mounted (){
    this.movie = this.$route.params.movie
    this.review = this.$route.params.review
    this.userid = this.$store.state.User.user.user_id? this.$store.state.User.user.user_id : -1
    this.loadComment()
  }
}
</script>

<style scoped>
#review-content {
  width: 100%;
  background-color: rgba( 0, 0, 0, 0.5 );
  border-radius: 10px;
}
</style>