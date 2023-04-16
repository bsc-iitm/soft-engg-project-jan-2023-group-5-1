<template>
  <!-- <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav> -->
  <!-- <TopNav></TopNav> -->
  <SideNav></SideNav>
  <TopNav></TopNav>
  <div class="main"><router-view/></div>
</template>

<script>
import SideNav from './components/SideNav.vue';
import TopNav from './components/TopNav.vue';
  export default {
    components: {
      SideNav,
      TopNav
    }
  }

</script>

<style>
/* *{
  outline: limegreen 1px solid;
} */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0;
  padding: 0;

}

.main{
  margin-top: 100px;
  margin-left: 80px;
}




</style>
