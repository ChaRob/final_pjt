<template>
  <div id="RecommendView" class="">
    <b-img src="../assets/reguys.jpg" style="position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); z-index: -1; width: 100%;">
    </b-img>
    <b-container v-if="option===0" id="option-1" class="py-4" style="font-size: 40px; min-height: 800px; display: flex; align-items: center; justify-content: center;">
      <b-row style="position: absolute; top: 150px; color: white;"><h1>원하는 옵션을 선택하세요</h1></b-row>
      <b-row style="align-items: center; width: inherit; justify-content: space-around;">
        <b-col cols="5" class="border border-white rounded-pill text-white" style="height: 350px; cursor: pointer; background-color: rgba(0, 0, 0, 0.5);" @click="optionSelect(0)">
          <div style="position: relative; top: 1rem;">
            <b-img src="../assets/fortheater.png" height="250"></b-img>
            <p>영화관</p>
          </div>
        </b-col>
        <b-col cols="5" class="border border-white rounded-pill text-white" style="height: 350px; cursor: pointer; background-color: rgba(0, 0, 0, 0.5);" @click="optionSelect(1)">
          <div style="position: relative; top: 1rem;">
            <b-img src="../assets/cartoon_bedroom_elements.png" height="250"></b-img>
            <p>집</p>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <b-container v-if="option===1" id="option-2" class="py-4" style="font-size: 40px; min-height: 800px;">
      <div class="mt-4 pt-4 text-white">
        <div v-if="selectOption[0]==='집'">
          <h1>파티인원을 선택해주세요.</h1>
          <b-row v-if="user.followings === 0" style="justify-content: center;">
            <p class="p-4">파티 인원이 없습니다...</p>
          </b-row>
          <b-row v-else>
            <b-col style="font-size: 25px;">
              <b-form @submit.prevent="homeSelect">
                <b-form-group label="파티인원">
                  <b-form-checkbox-group
                  v-model="partySelectPeople"
                  :options="user.followings"
                  class=""
                  size="lg"
                  value-field="id"
                  text-field="username"
                  ></b-form-checkbox-group>
                </b-form-group>
                <b-button type="submit">선택 완료</b-button>
              </b-form>
            </b-col>
          </b-row>
        </div>
      </div>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "RecommendView",
  data() {
    return {
      user: null,
      option: 0,
      fullOption: [
        '영화관','집',
        '두번째선택'
      ],
      selectOption: [],
      partySelectPeople: [],
    }
  },
  methods: {
    optionSelect(idx) {
      const optionDOM = document.querySelector(`#option-${this.option+1}`)
      optionDOM.id = 'fade-out'
      this.selectOption.push(this.fullOption[idx])
      this.nextOption(idx)
    },
    nextOption(idx) {
      setTimeout(() => {
        if(idx===0) {
          this.$router.push({name: "RecommedResultTheater"})
        }
        this.option+=1
      }, 1500)
    },
    homeSelect() {
      const token = this.$store.state.User.token
      let input_url = ''
      if(this.partySelectPeople.length === 0) {
        input_url = "http://127.0.0.1:8000/recommendation/alone/"
      }
      else {
        input_url = "http://127.0.0.1:8000/recommendation/"
        for (const member of this.partySelectPeople) {
          input_url+=`-${member}`
        }
        input_url+="/"
      }
      axios({
      method: "GET",
      url: input_url,
      headers: {
        Authorization : `Token ${token}`
      }
    })
    .then(response => {
      this.$store.dispatch('setRecommendData', response.data)
      this.$router.push({name: "recommendresult"})
    })
    .catch(error => console.error(error))
    }
  },
  created() {
    const token = this.$store.state.User.token
    axios({
      method: "GET",
      url: "http://127.0.0.1:8000/accounts/userinfo/" + this.$store.state.User.user.user_id + "/",
      headers: {
        Authorization : `Token ${token}`
      }
    })
    .then(response => {
      this.user = response.data
    })
    .catch(error => console.error(error))
  }
}
</script>

<style scoped>
#RecommendView {
  min-height: 873px;
}

#fade-out {
  animation: fadeout 1.5s;
  -moz-animation: fadeout 2s; /* Firefox */
  -webkit-animation: fadeout 2s; /* Safari and Chrome */
  -o-animation: fadeout 2s; /* Opera */
  animation-fill-mode: forwards;
}

@keyframes fadeout {
    from {
        opacity: 1;
    }
    to {
        opacity: 0;
    }
}
</style>