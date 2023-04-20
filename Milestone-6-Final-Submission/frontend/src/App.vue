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

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
@-webkit-keyframes rotate {
  from {
    -webkit-transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(360deg);
  }
}
.load {
  width: 40px;
  height: 40px;
  margin: 30px auto 0;
  border: solid 3px #2a623d;
  border-radius: 50%;
  border-right-color: transparent;
  border-bottom-color: transparent;
  -webkit-transition: all 0.5s ease-in;
  -webkit-animation-name: rotate;
  -webkit-animation-duration: 1s;
  -webkit-animation-iteration-count: infinite;
  -webkit-animation-timing-function: linear;
  transition: all 0.5s ease-in;
  animation-name: rotate;
  animation-duration: 1s;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}




</style>
