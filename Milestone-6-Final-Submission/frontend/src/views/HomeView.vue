<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <div class="header">
      <input type="search" name="search" id="search" v-model="search" placeholder="Search...">
      <div class="recom">
        <ul>

        </ul>
      </div>

    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import { ref, watch } from 'vue';

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  },
  setup(){
    const search = ref('')
    const search_results = ref([])
    const terms = ref(0)
    watch(search, async (new_term) => {

      // console.log(new_term)
      const len = new_term.split(' ').length
      if (len > (terms.value + 1)){
        const resp = await fetch('http://localhost:5000/ticket/get-similar', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: new_term
        })
      })

      const data = await resp.json()
      search_results.value = data
      console.log(data)
      terms.value = len
      }

      else{
        console.log('word not complete yet')
      }
      
      

    }) 

    return {
      search
    }
  }
}
</script>


<style scoped>

.header{
  height: 50vh;
  width: 96%;
  display: flex;
  justify-content: center;

}

.header input{
  width: 75%;
  height: 60px;
  border-radius: 10px;
  border: 1px #333 solid;
  padding: 10px;
  font-size: 20px;
  position: relative;
}

</style>
