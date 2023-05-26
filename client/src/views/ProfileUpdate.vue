<template>
  <div id="ProfileUpdate">
    <b-container class="py-4">
      <b-row id="update-board" class="justify-content-center">
        <b-col>
          <h1 class="mt-4">{{user.username}} 프로필 수정</h1>
          <b-form @submit.prevent="updateUserData">
            <b-form-group
              id="input-group-1"
              label="Email address"
              label-for="input-email"
              description="필수는 아닙니다."
              style="text-align: start;"
            >
              <b-form-input
                id="input-email"
                v-model="user.email"
                type="email"
                placeholder="Enter email"
              ></b-form-input>
            </b-form-group>
            <b-form-group
              id="input-group-2"
              label="자기소개글"
              label-for="input-intro"
              description="필수는 아닙니다."
              style="text-align: start;"
            >
              <b-form-input
                id="input-intro"
                v-model="user.intro"
                type="text"
                placeholder="Enter text"
              ></b-form-input>
            </b-form-group>
            <b-row>
              <b-col class="mt-3 mr-auto">
                <b-form-group label="<프로필 이미지 선택>">
                  <b-form-file accept=".jpg, .png, .gif" v-model="user.profile_image" plain></b-form-file>
                </b-form-group>
              </b-col>
            </b-row>
            <div style="text-align: start;">
              <b-button @click="user.profile_image = null" class="mr-2">Reset file</b-button>
            </div>
            <div class="mt-3">
              <p style="text-align: start;">Selected file: {{ user.profile_image ? user.profile_image.name : '' }}</p>
            </div>
            <b-button variant="success" type="submit">제출</b-button>
          </b-form>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "ProfileUpdate",
  data() {
    return {
      user: this.$route.params.user,
    }
  },
  methods: {
    updateUserData() {
      const token = this.$store.state.User.token
      axios({
        method: "PUT",
        url: "http://127.0.0.1:8000/accounts/update/",
        headers: {
          Authorization : `Token ${token}`,
          'Content-Type': 'multipart/form-data',
        },
        data: {
          'intro' : this.user.intro,
          'email' : this.user.email,
          'profile_image' : this.user.profile_image
        }
      })
      .then(() => {
        this.$router.push({name: 'profile', params: {'id': this.user.id}})
      })
      .catch(error => console.error(error))
    }
  },
  created() {
  },
}
</script>

<style scoped>
#ProfileUpdate {
  background-image: url('../assets/theaterImg.png');
  background-size: cover;
}

#update-board {
  border-radius: 25px;
  width: 600px;
  height: 800px;
  margin-right: auto;
  margin-left: auto;
  background-color: white;
}
</style>