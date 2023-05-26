<template>
  <div id="SidebarView">
    <div class="h2 mb-0" id="top-page-btn">
      <a href="#NavbarView">
        <b-icon-arrow-up>
        </b-icon-arrow-up>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "SidebarView",
  methods: {
  },
}
</script>

<style>
#top-page-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  cursor: pointer;
  border: 1px solid black;
  border-radius: 5px;
  background-color: rgba(255, 255, 255, 0.534);
}
</style>