<template>
  <div id="ProfileView" class="pt-4">
    <b-container id="ProfileCard">
      <b-row style="height: 450px;">
        <b-col cols="4" class="p-5">
          <div id="User-img" style="border: 2px solid black; box-shadow: 0px 0px 5px white">
            <b-img v-if="user.profile_image" :src="userImg(user.profile_image)" width="281" height="352"></b-img>
            <b-img v-else src="../assets/NoProfileImg.png" width="281" height="352"></b-img>
          </div>
        </b-col>
        <b-col id="User-Profile" class="mx-4 py-4">
          <h1>{{user.username}}님의 프로필</h1>
          <b-button v-if="user.id === $store.state.User.user.user_id" variant="info" style="position: absolute; right: 15px; top: 25px;" @click="profileUpdate">프로필수정</b-button>
          <div class="mt-4">
            <b-col class="pl-0">
              팔로워 : {{userFollowerNum()}} / 팔로잉 : {{userFollowingNum()}}
            </b-col>
            <b-col v-if="($store.state.User.user !== null) && (user.id !== $store.state.User.user.user_id)" style="text-align: end;">
              <b-button variant="danger" v-if="userFollowers.includes($store.state.User.user.user_id)" @click="followUser(false)">팔로우취소</b-button>
              <b-button variant="warning" v-else @click="followUser(true)">팔로우하기</b-button>
            </b-col>
          </div>
          <div class="mt-3">
            <p v-if="user.intro" style="font-size: 20px;">자기소개 : {{user.intro}}</p>
            <p v-else style="font-size: 20px;">자기소개가 없습니다.</p>
          </div>
        </b-col>
      </b-row>
      <b-row class="pl-5 pr-4 py-4">
        <b-col style="background-color: rgba(0, 0, 0, 0);">
          <b-row class="pb-4 text-white">
            <h1>{{user.username}}님이 본 영화</h1>
          </b-row>
          <b-row>
            <b-col v-for="(review, idx) in user.review_set.slice((currentPage-1)*4,(currentPage)*4)" :key="idx"
            cols="3" class="py-4 rounded text-white" style="display: flex; flex-wrap: wrap; flex-direction: column; align-items: center; border: 2px solid white;">
              <b-img :src="poster(review.movie.poster_path)" width="220" height="280" style="cursor: pointer;" @click="moveReview(review, review.id)"></b-img>
              <b-row>
                <b-col>
                  <p class="m-0">{{review.movie.title}}</p>
                </b-col>
              </b-row>
              <b-row>
                <b-col>
                  <p>★{{review.rating}}</p>
                </b-col>
              </b-row>
            </b-col>
          </b-row>
          <b-pagination
            v-model="currentPage"
            :total-rows="user.review_set.length"
            per-page="4"
            first-number
            last-number
            pills
            align="center"
            class="mt-4"
          ></b-pagination>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "ProfileView",
  data() {
    return {
      id: null,
      user: null,
      currentPage: 1,
      userFollowers: [],
    }
  },
  methods: {
    userImg(path) {
      return "http://127.0.0.1:8000/accounts" + path
    },
    poster(path){
      return this.$store.getters.getPosterPath + (path? path : '')
    },
    userFollowerNum() {
      return this.userFollowers? this.userFollowers.length : 0
    },
    userFollowingNum() {
      return this.user.followings? this.user.followings.length : 0
    },
    followUser(Method) {
      const token = this.$store.state.User.token
      axios({
        method: "POST",
        url: "http://127.0.0.1:8000/accounts/follow/" + this.user.id + "/",
          headers: {
            Authorization : `Token ${token}`
          }
      })
      .then(() => {
        if(Method) {
          this.userFollowers.push(this.$store.state.User.user.user_id)
        }
        else {
          this.userFollowers.splice(this.userFollowers.indexOf(this.$store.state.User.user.user_id), 1)
        }
      })
      .catch(error => console.error(error))
    },
    moveReview(review, id) {
      this.$router.push({name: "reviewdetail", params: {'id': id, 'review': review, 'movie': review.movie}})
    },
    profileUpdate() {
      this.$router.push({name: "ProfileUpdate", params: {'user': this.user}})
    }
  },
  created() {
    this.id = this.$route.params.user_id
    if(this.id === undefined){
      this.id = this.$store.state.profileID
    }
    axios({
      method: "GET",
      url: "http://127.0.0.1:8000/accounts/userinfo/" + this.id + "/",
    })
    .then(response => {
      this.user = response.data
      this.$store.dispatch('setProfileID', this.id)
      for (const user of this.user.followers) {
        this.userFollowers.push(user.id)
      }
    })
    .catch(error => console.error(error))
  },
}
</script>

<style scoped>
#ProfileView {
  background-image: url('../assets/starry-night-sky.jpg');
  background-size: cover;
  min-height: 130vh;
}

#ProfileCard {
  border: 1px solid black;
  border-radius: 15px;
  box-shadow: 0px 0px 40px white;
  background-color: rgba(71, 68, 61, 0.473);
  text-align: start;
}

#User-img {
  border: 1px solid black;
  height: 100%;
  background-color: rgb(211, 211, 211);
  display: flex;
  justify-content: center;
  align-items: center;
}

#User-Profile {
  border: 1px solid black;
  background-color: rgb(211, 211, 211);
  margin-top: 45px;
  margin-bottom: 45px;
}
</style>