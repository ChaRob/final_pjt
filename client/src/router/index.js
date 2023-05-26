import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MovieListView from '../views/MovieListView.vue'
import MovieDetailView from '../views/MovieDetailView.vue'
import RecommendView from '../views/RecommendView.vue'
import SignUpView from '../views/SignUpView.vue'
import LoginView from '../views/LoginView.vue'
import ProfileView from '../views/ProfileView.vue'
import ProfileUpdate from '../views/ProfileUpdate.vue'
import MovieReview from '../views/MovieReview.vue'
import MovieReviewDetail from '../views/MovieReviewDetail.vue'
import ReviewCreate from '../views/ReviewCreate.vue'
import ReviewUpdate from '../views/ReviewUpdate.vue'
import SearchView from '../views/SearchView.vue'
import RecommendResult from '../views/RecommendResult.vue'
import RecommedResultTheater from '../views/RecommedResultTheater.vue'

import store from '../store/index'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/movies',
    name: 'movies',
    component: MovieListView
  },
  {
    path: '/movie/detail',
    name: 'detail',
    component: MovieDetailView
  },
  {
    path: '/recommend',
    name: 'recommend',
    component: RecommendView,
    beforeEnter(to, from, next) {
      if(store.state.User.token){
        next()
      }
      else{
        alert('로그인이 필요합니다.')
        router.push({name:"login"})
      }
    }
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView
  },
  {
    path: '/profile/update',
    name: 'ProfileUpdate',
    component: ProfileUpdate
  },
  {
    path: '/review/:id',
    name: 'review',
    component: MovieReview
  },
  {
    path: '/review/:id/create',
    name: 'reviewcreate',
    component: ReviewCreate,
    beforeEnter(to, from, next) {
      if(store.state.User.token){
        next()
      }
      else{
        alert('로그인이 필요합니다.')
        router.push({name:"login"})
      }
    }
  },
  {
    path: '/review/update',
    name: 'updatereview',
    component: ReviewUpdate
  },
  {
    path: '/review/detail',
    name: 'reviewdetail',
    component: MovieReviewDetail
  },
  {
    path: '/search',
    name: 'search',
    component: SearchView
  },
  {
    path: '/recommendresult',
    name: 'recommendresult',
    component: RecommendResult
  },
  {
    path: '/recommendtheater',
    name: 'RecommedResultTheater',
    component: RecommedResultTheater
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

const originalPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
	return originalPush.call(this, location).catch(err => {
		if (err.name !== 'NavigationDuplicated') throw err;
	});
};

export default router

router.beforeEach((to, from, next) => {
  if(!(
    (to.name === "movies" && from.name === "detail") ||
    (to.name === "detail" && from.name === "movies")
    )) {
      store.dispatch('updatePage', {'page':1, 'filter':0})
    }
  next()
})