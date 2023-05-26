import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import User from './modules/User'

// import axios from 'axios'
// import router from '../router'

Vue.use(Vuex)

/* eslint-disable no-new */
const store = new Vuex.Store({
  plugins: [createPersistedState()],
  modules: {
    User
  },
  state: {
    poster_url_front: "https://www.themoviedb.org/t/p/original",
    topRatePage: 1,
    filter: 0,
    movie: {},
    profileID: null,
    search_movies: [],
    recommend_movie: [],
    genres: [
      {'id':12,'name':'모험'},
      {'id':14,'name':'판타지'},
      {'id':16,'name':'애니메이션'},
      {'id':18,'name':'드라마'},
      {'id':27,'name':'공포'},
      {'id':28,'name':'액션'},
      {'id':35,'name':'코미디'},
      {'id':36,'name':'역사'},
      {'id':37,'name':'서부'},
      {'id':53,'name':'스릴러'},
      {'id':80,'name':'범죄'},
      {'id':99,'name':'다큐멘터리'},
      {'id':878,'name':'SF'},
      {'id':9648,'name':'미스터리'},
      {'id':10402,'name':'음악'},
      {'id':10749,'name':'로맨스'},
      {'id':10751,'name':'가족'},
      {'id':10752,'name':'전쟁'},
      {'id':10770,'name':'TV 영화'},
    ],
  },
  getters: {
    getPosterPath(state) {
      return state.poster_url_front
    },
  },
  mutations: {
    UPDATE_PAGE(state, data) {
      state.topRatePage = data.page
      state.filter = data.filter
    },
    DETAIL_MOVIE(state, movie) {
      state.movie = movie
    },
    SET_PROFILE_ID(state, data) {
      state.profileID = data
    },
    SET_SEARCH_DATA(state, movies){
      state.search_movies = movies
    },
    SET_RECOMMEND_DATA(state, movies){
      state.recommend_movie = movies
    }
  },
  actions: {
    updatePage(context, data) {
      context.commit('UPDATE_PAGE', data)
    },
    Detail_Movie(context, movie) {
      context.commit('DETAIL_MOVIE', movie)
    },
    setProfileID(context, data) {
      context.commit('SET_PROFILE_ID', data)
    },
    setSearchData(context, movies) {
      context.commit('SET_SEARCH_DATA', movies)
    },
    setRecommendData(context, movies) {
      context.commit('SET_RECOMMEND_DATA', movies)
    }
  },
})

export default store
