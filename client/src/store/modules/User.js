// import store from ".."
import axios from 'axios'
import router from '../../router'

const User = {
  state: {
    token: null,
    user: {
      username: '',
      email: '',
      user_id: null,
    }
  },
  getters: {
    getLoginState(state) {
      return state.token? true : false
    },
  },
  mutations: {
    SAVE_TOKEN(state, data) {
      state.token = data.key
      this.dispatch('setUserData')
    },
    LOG_OUT(state) {
      state.token = null
      state.user = null
      router.push({name: 'home'})
    },
    SET_USER_DATA(state, data) {
      const input_user = {
        username: data.username,
        email: data.email,
        user_id: data.pk,
      }
      state.user = input_user
    },
  },
  actions: {
    signUp(context, userdata) {
      const username = userdata.ID
      const password1 = userdata.Password
      const password2 = userdata.PasswordConfirm
      // const Email = userdata.Email

      axios({
        method: "POST",
        url: "http://127.0.0.1:8000/accounts/signup/",
        data: {
          username, password1, password2
        }
      })
      .then(response => {
        context.commit('SAVE_TOKEN', response.data)
      })
      .catch(error => console.error(error))
    },
    logIn(context, userdata) {
      const username = userdata.ID
      const password = userdata.Password
      
      axios({
        method: "POST",
        url: "http://127.0.0.1:8000/accounts/login/",
        data: {
          username, password
        }
      })
      .then(response => {
        context.commit('SAVE_TOKEN', response.data)
      })
      .catch(error => console.error(error))
    },
    logout(context) {
      context.commit('LOG_OUT')
    },
    setUserData(context) {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/accounts/user/",
        headers: {
          Authorization: `Token ${context.state.token}`
        }
      })
      .then(response => {
        context.commit('SET_USER_DATA', response.data)
        router.push({name: 'home'})
      })
      .catch(error => console.error(error))
    },
  }
}

export default User