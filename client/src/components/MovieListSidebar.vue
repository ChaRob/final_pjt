<template>
  <div id="MovieListSidebar">
    <div id="left-side" class="">
      <b-container class="py-4 px-3">
        <b-row>
          <b-col style="display: flex; justify-content: space-around; align-items: center;">
            <b-button @click="selectBtn(0)" :variant="select(0)" style="font-size: 20px" href="#NavbarView">인기순</b-button>
            <b-button @click="selectBtn(1)" :variant="select(1)" style="font-size: 20px" href="#NavbarView">평점순</b-button>
            <b-dropdown id="dropdown-dropup" dropup text="장르" :variant="select(2)" class="m-2" style="font-size: 20px">
              <b-dropdown-item v-for="(genre, idx) in $store.state.genres" :key="idx" @click="selectBtn(2+idx)" :variant="select(2+idx)" href="#NavbarView">{{genre.name}}</b-dropdown-item>
            </b-dropdown>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>

<script>
export default {
  name: "MovieListSidebar",
  data() {
    return {
      select_idx: this.$store.state.filter,
    }
  },
  methods: {
    select(idx) {
      if (this.select_idx === idx){
        return 'primary'
      }
      else{
        return ''
      }
    },
    selectBtn(idx) {
      this.select_idx = idx
      this.$emit('page-idx', idx)
    }
  },
}
</script>

<style>
#left-side {
  border: 1px solid white;
  border-radius: 25px;
  position: fixed;
  height: 10%;
  width: 40rem;
  bottom: 10px;
  left: 2%;
  background-color: rgb(240, 248, 250);
}
</style>