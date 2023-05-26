<template>
  <div id="LoginView">
    <b-container id="form-input">
      <b-form @submit.prevent="logIn()" id="loginform">
        <b-form-group id="ID-input" label="ID" label-for="ID">
          <b-form-input
            id="ID"
            v-model="ID"
            placeholder="Enter ID"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group id="Password-input" label="Your Password" label-for="Password">
          <b-form-input
            id="Password"
            v-model="Password"
            type="password"
            placeholder="Enter Password"
            required
          ></b-form-input>

        </b-form-group>
        <div style="text-align: right;">
          <b-button id="loginBtn" type="submit" variant="success" class="mr-2 mt-4">Login</b-button>
        </div>
      </b-form>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "LoginView",
  data() {
    return {
      ID: '',
      Password: '',
    }
  },
  methods: {
    logIn() {
      const userdata = {
        'ID' : this.ID,
        'Password': this.Password
      }

      this.$store.dispatch('logIn', userdata)
    },
  },
}
</script>

<style scoped>
#LoginView {
  text-align: left;
  padding: 30px;
  font-size: 20pt;
  background-color: rgba(165, 17, 17, 0.911);
  color: white;
}

#form-input {
  background-image: url('../assets/popcorn.png'),url('../assets/loginpage.png');
  background-size: cover;
}

#loginBtn {
  text-align: center;
}

#loginform {
  height: 86.5vh;
  padding: 200px;
}
</style>