<template>
  <div id="SignUpView">
    <b-container class="text-white" style="margin-top: 25px;">
      <b-form @submit.prevent="signUp" id="signupform">
        <b-form-group id="ID-input" label="Your ID" label-for="ID">
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

        <b-form-group id="Password-Confirm-input" label="Password Confirm" label-for="Password-Confirm">
          <b-form-input
            id="Password-Confirm"
            v-model="Password_Confirm"
            type="password"
            placeholder="Enter Password Again"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group id="Address-input" label="Email address" label-for="Address" description="If necessary, it's not required.">
          <b-form-input
            id="Address"
            v-model="Email"
            type="email"
            placeholder="Enter email"
          ></b-form-input>
        </b-form-group>

        <div id="signBtn">
          <b-button type="submit" variant="primary" class="mr-2">Submit</b-button>
          <b-button type="reset" variant="danger outline-black">Reset</b-button>
        </div>
      </b-form>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "SignUpView",
  data() {
    return {
      ID: '',
      Password: '',
      Password_Confirm: '',
      Email: '',
    }
  },
  methods: {
    signUp() {
      const userdata = {
        'ID': this.ID,
        'Password': this.Password,
        'PasswordConfirm': this.Password_Confirm,
        'Email': this.Email
      }
      this.$root.$store.dispatch('signUp', userdata)

      this.ID = ''
      this.Password = ''
      this.Password_Confirm = ''
      this.Email = ''
    }
  },
}
</script>

<style scoped>
#SignUpView {
  text-align: left;
  padding: 30px;
  font-size: 20pt;
  background-image: url('../assets/theaterImg.png');
  background-size: cover;
}

#signBtn {
  text-align: right;
}

#signupform {
  height: 86.5vh;
  padding: 100px;
}
</style>